import streamlit as st
import os
import pandas as pd
from datetime import datetime
from crud import car_search, car_booking

# Convert the car data to a DataFrame
cars_df = pd.read_csv("Rental-Car-Business-Demo/data/cars.csv")

# Extract unique car types for the selectbox
unique_car_types = cars_df['car_type'].unique()

# Get the minimum and maximum prices for the slider
min_price = cars_df['price'].min()
max_price = cars_df['price'].max()

# Initialize session state
if 'show_content' not in st.session_state:
    st.session_state.show_content = False

# Display Hero Section if content is not yet shown
if not st.session_state.show_content:
    st.markdown(
        """
        <style>
        .hero {
            background-image: url('https://source.unsplash.com/1600x900/?car'); 
            background-size: cover;
            padding: 100px 0;
            text-align: center;
            color: white;
        }
        .hero h1 {
            font-size: 3.5em;
            font-weight: bold;
        }
        .hero p {
            font-size: 1.5em;
            margin-bottom: 30px;
        }
        </style>
        <div class="hero">
            <h1>Welcome to Our Rental Car Service</h1>
            <p>Find the best cars at affordable prices</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Streamlit button that triggers the content display
    if st.button("Book Now", type='primary'):
        st.session_state.show_content = True
        st.rerun()  # Rerun to update the page

# Display the rest of the content if the button was clicked
if st.session_state.show_content:
    st.markdown("## Search for Your Car")

    # Retrieve the path to the temporary file from the environment variable
    user_id_file_path = os.getenv('USER_ID_FILE')
    if user_id_file_path and os.path.exists(user_id_file_path):
        with open(user_id_file_path, 'r') as f:
            user_id = int(f.read().strip())
    else:
        st.error("User ID not found.")
        st.stop()

    # Search Section
    car_type = st.selectbox("Select Car Type", options=unique_car_types)
    price_range = st.slider("Select Price Range", min_price, max_price, (min_price, max_price))

    start_date = st.date_input("Select Start Date", datetime.today())
    end_date = st.date_input("Select End Date", datetime.today())

    if start_date > end_date:
        st.error("End date must be after start date.")
        st.stop()

    # Search cars using the imported function
    available_cars = car_search(car_type, price_range, start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'))

    st.markdown("### Available Cars")

    # Display all available cars in a grid with images and features
    for i in range(0, len(available_cars), 3):
        cols = st.columns(3)
        for j, car in enumerate(available_cars.iloc[i:i+3].itertuples()):
            with cols[j]:
                # Extract the image path
                image_path = os.path.join('', car.image_path)
                if os.path.exists(image_path):
                    st.image(image_path, use_column_width=True)
                else:
                    st.image('Rental-Car-Business-Demo/assets/images/default_car.png', use_column_width=True)  # Use a default image if the specified one is not found
                st.markdown(f"**{car.name}**")
                st.markdown(f"Type: {car.car_type}")
                st.markdown(f"Price: ${car.price}/day")
                st.markdown(f"Year: {car.year}")
                st.markdown(f"Fuel: {car.fuel_type}")
                st.markdown(f"Transmission: {car.transmission}")
                st.markdown(f"Mileage: {car.mileage} miles")
                if st.button("Book Now", key=f"book_{car.car_id}"):
                    # Book the selected car using the imported function
                    car_booking(user_id, car.car_id, start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'))
                    st.success(f"Booking created successfully for Car ID {car.car_id}!")

    # Footer
    st.markdown(
        """
        <style>
        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 0.9em;
            color: gray;
        }
        </style>
        <div class="footer">
            <p>&copy; 2024 Rental Car Service. All rights reserved.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
