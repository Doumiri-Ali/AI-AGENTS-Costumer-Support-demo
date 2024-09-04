import streamlit as st
import pandas as pd
import os
import subprocess
import sys
import signal
import create_csv_files

USER_ID_FILE_PATH = 'Rental-Car-Business-Demo/data/user_id.conf'
# Define paths
users_csv_path = 'Rental-Car-Business-Demo/data/users.csv'

# Load user data
if os.path.exists(users_csv_path):
    users_df = pd.read_csv(users_csv_path)
else:
    # Create a DataFrame if users.csv does not exist
    users_df = pd.DataFrame(columns=['user_id', 'name', 'email', 'phone', 'address'])

# Set page configuration
st.set_page_config(page_title='Login/Registration', page_icon='🔑', layout='centered')

# Hide the sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state for page and user data
if 'page' not in st.session_state:
    st.session_state['page'] = 'Login'
if 'user' not in st.session_state:
    st.session_state['user'] = None

# Page navigation
if st.session_state['page'] == 'Login':
    st.title("Login or Register")

    # Login Section
    email = st.text_input("Email")

    # Buttons layout
    col1, col2 = st.columns([3, 1])

    with col1:
        login_button = st.button("Login")
    with col2:
        register_button = st.button("Register")

    if login_button:
        if email:
            user = users_df[users_df['email'] == email]
            if not user.empty:
                st.session_state['user'] = user.iloc[0].to_dict()  # Store user info in session state
                st.session_state['page'] = 'Redirect'  # Set page to redirect
                st.rerun()  # Force rerun to reflect changes
            else:
                st.error("Email not found. Please register.")
        else:
            st.error("Please enter an email.")

    if register_button:
        st.session_state['page'] = 'Register'

elif st.session_state['page'] == 'Register':
    st.title("Register")

    # Registration Form
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    address = st.text_input("Address")

    if st.button("Submit Registration"):
        if full_name and email and phone and address:
            # Determine new user ID
            if not users_df.empty:
                new_user_id = users_df['user_id'].max() + 1
            else:
                new_user_id = 101  # Starting ID

            # Append new user to DataFrame
            new_user = pd.DataFrame({
                'user_id': [new_user_id],
                'name': [full_name],
                'email': [email],
                'phone': [phone],
                'address': [address]
            })

            users_df = pd.concat([users_df, new_user], ignore_index=True)

            # Save updated DataFrame to CSV
            users_df.to_csv(users_csv_path, index=False)

            st.success("Registration successful! You can now log in.")
            st.session_state['page'] = 'Login'  # Go back to login page
        else:
            st.error("Please fill out all fields.")

elif st.session_state['page'] == 'Redirect':
    st.write("Redirecting to the main application...")

    # Save the user ID to a fixed file path
    with open(USER_ID_FILE_PATH, 'w') as file:
        file.write(str(st.session_state['user']['user_id']))

    # Set environment variable for the file path
    os.environ['USER_ID_FILE'] = USER_ID_FILE_PATH

    # Stop the current Streamlit process
    try:
        os.kill(os.getpid(), signal.SIGTERM)
    except Exception as e:
        st.error(f"Failed to stop Streamlit process: {e}")

    # Start the new Streamlit process
    try:
        subprocess.Popen([sys.executable, '-m', 'streamlit', 'run', 'Rental-Car-Business-Demo/pages/app.py'])
        st.write("Streamlit app started.")
    except Exception as e:
        st.error(f"Failed to start Streamlit app: {e}")

    # End the current Streamlit app
    st.stop()