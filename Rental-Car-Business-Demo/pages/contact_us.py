import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Constants
CONTACT_FILE_PATH = 'Rental-Car-Business-Demo/data/contacts.csv'


# Function to save contact messages to CSV
def save_contact_message(name, email, subject, message):
    # Create a new DataFrame for the contact message
    contact_df = pd.DataFrame({
        'timestamp': [datetime.now().strftime('%d-%m-%Y %H:%M:%S')],
        'name': [name],
        'email': [email],
        'subject': [subject],
        'message': [message]
    })

    # Check if the contact CSV file exists
    if os.path.exists(CONTACT_FILE_PATH):
        # Append to the existing file
        contact_df.to_csv(CONTACT_FILE_PATH, mode='a', header=False, index=False)
    else:
        # Create a new file
        contact_df.to_csv(CONTACT_FILE_PATH, mode='w', header=True, index=False)


# Page Title
st.title("Contact Us")

# Contact Form
with st.form(key='contact_form'):
    st.markdown("Please fill out the form below to get in touch with us.")

    name = st.text_input("Name")
    email = st.text_input("Email")
    subject = st.text_input("Subject")
    message = st.text_area("Message")

    submit_button = st.form_submit_button("Send Message")

    if submit_button:
        if not name or not email or not subject or not message:
            st.error("All fields are required.")
        else:
            try:
                save_contact_message(name, email, subject, message)
                st.success("Your message has been sent successfully!")
            except Exception as e:
                st.error(f"An error occurred while sending your message: {e}")
