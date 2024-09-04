import streamlit as st
import pandas as pd
import os
import subprocess
import sys
import signal
from streamlit_option_menu import option_menu




# Set up the Streamlit app
st.set_page_config(page_title="Rental Car Service", page_icon="🚗")

# Define paths
users_csv_path = 'Rental-Car-Business-Demo/data/users.csv'

# Load user data
if os.path.exists(users_csv_path):
    users_df = pd.read_csv(users_csv_path)
else:
    users_df = pd.DataFrame(columns=['user_id', 'name', 'email', 'phone', 'address'])

# Retrieve the path to the temporary file from the environment variable
user_id_file_path = os.getenv('USER_ID_FILE')

# Default user info
user_name = "Guest"

if user_id_file_path and os.path.exists(user_id_file_path):
    with open(user_id_file_path, 'r') as file:
        user_id = file.read().strip()
    user_info = users_df[users_df['user_id'] == int(user_id)]
    if not user_info.empty:
        user_name = user_info.iloc[0]['name']

# Sidebar for navigation and user info
st.sidebar.header(f"Hello, {user_name}")

# Define pages
pages = {
    "Home": "Rental-Car-Business-Demo/pages/home.py",
    "Reservations": "Rental-Car-Business-Demo/pages/Reservations.py",
    "Customer Support": "Rental-Car-Business-Demo/pages/customer_support.py",
    "Contact Us": "Rental-Car-Business-Demo/pages/contact_us.py",
    "FAQ": "Rental-Car-Business-Demo/pages/FAQ.py"
}

# Display option menu for "Customer Support"
with st.sidebar:
    selected_option = option_menu(
        menu_title=None,
        options=["Home", "Reservations", "Customer Support", "Contact Us", "FAQ"],
        icons=["house", "calendar", "chat", "envelope", "question-circle"],
        default_index=list(pages.keys()).index("Home"),
        orientation="vertical",
        key="main_menu"
    )

# Floating chat button

# Logout button
if st.sidebar.button("Logout"):
    # Clear the user ID temp file
    if user_id_file_path and os.path.exists(user_id_file_path):
        try:
            os.remove(user_id_file_path)
            st.write("User ID file cleared.")
        except Exception as e:
            st.error(f"Failed to clear user ID file: {e}")

    # Stop the current Streamlit process
    try:
        os.kill(os.getpid(), signal.SIGTERM)
    except Exception as e:
        st.error(f"Failed to stop Streamlit process: {e}")

    # Start the new Streamlit process
    try:
        subprocess.Popen([sys.executable, '-m', 'streamlit', 'run', 'Rental-Car-Business-Demo/pages/login.py'])
        st.write("Streamlit app started.")
    except Exception as e:
        st.error(f"Failed to start Streamlit app: {e}")

    # End the current Streamlit app
    st.stop()

# Import and run the selected page
if selected_option:
    page = pages[selected_option]
    with open(page) as f:
        exec(f.read())


