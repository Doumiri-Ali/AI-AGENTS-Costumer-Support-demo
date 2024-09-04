import streamlit as st
from datetime import datetime
import os
from crud import (
    load_data,
    confirm_booking,
    booking_canceling,
    booking_update,
    show_my_pending_booked_cars,
    show_my_confirmed_booked_cars,
    show_my_booking_history
)

# Constants
BOOKINGS_FILE_PATH = 'Rental-Car-Business-Demo/data/bookings.csv'
CARS_FILE_PATH = 'Rental-Car-Business-Demo/data/cars.csv'

# Retrieve the path to the temporary file from the environment variable
user_id_file_path = os.getenv('USER_ID_FILE')

def load_user_id(file_path):
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return int(f.read().strip())
    else:
        st.error("User ID file not found.")
        st.stop()

user_id = load_user_id(user_id_file_path)
print(user_id)
# Load data
cars_df = load_data(CARS_FILE_PATH)

# Select box to choose the view
view_option = st.selectbox(
    "Select View",
    options=["Pending Bookings", "Confirmed Bookings", "Booking History"]
)

if view_option == "Pending Bookings":
    st.markdown("## Pending Bookings")
    pending_bookings = show_my_pending_booked_cars(user_id)
    #pending_bookings = pending_bookings[pending_bookings['booking_status'] == 1]
    #print("pending_bookings : ", pending_bookings.empty)

    if not pending_bookings.empty:
        for booking in pending_bookings.itertuples():
            car = cars_df[cars_df['car_id'] == booking.car_id].iloc[0]
            st.image(car['image_path'], width=300)
            st.markdown(f"**Car:** {car['name']} ({car.car_type})")
            st.markdown(f"**Start Date:** {booking.start_date}")
            st.markdown(f"**End Date:** {booking.end_date}")
            st.markdown(f"**Total Price:** ${booking.total_price}")

            # Confirm button
            if st.button(f"Confirm Booking {booking.booking_id}", key=f"confirm_{booking.booking_id}"):
                try:
                    confirm_booking(booking.booking_id)
                    st.success(f"Booking {booking.booking_id} confirmed!")
                    st.rerun()  # Refresh page
                except ValueError as e:
                    st.error(str(e))

            # Cancel button
            if st.button(f"Cancel Booking {booking.booking_id}", key=f"cancel_{booking.booking_id}"):
                try:
                    booking_canceling(booking.booking_id)
                    st.success(f"Booking {booking.booking_id} cancelled!")
                    st.rerun()  # Refresh page
                except ValueError as e:
                    st.error(str(e))

            # Update button
            with st.form(key=f"update_{booking.booking_id}"):
                new_start_date = st.date_input("New Start Date", datetime.strptime(booking.start_date, '%d/%m/%Y'))
                new_end_date = st.date_input("New End Date", datetime.strptime(booking.end_date, '%d/%m/%Y'))
                submit_button = st.form_submit_button("Update Booking")
                if submit_button:
                    if new_start_date > new_end_date:
                        st.error("End date must be after start date.")
                    else:
                        try:
                            booking_update(booking.booking_id, new_start_date.strftime('%d/%m/%Y'), new_end_date.strftime('%d/%m/%Y'))
                            st.success(f"Booking {booking.booking_id} updated!")
                            st.rerun()  # Refresh page
                        except ValueError as e:
                            st.error(str(e))
    else:
        st.markdown("You have no pending bookings.")

elif view_option == "Confirmed Bookings":
    st.markdown("## Confirmed Bookings")
    confirmed_bookings = show_my_confirmed_booked_cars(user_id)
    #confirmed_bookings = confirmed_bookings[confirmed_bookings['booking_status'] == 2]

    if not confirmed_bookings.empty:
        for booking in confirmed_bookings.itertuples():
            car = cars_df[cars_df['car_id'] == booking.car_id].iloc[0]
            st.image(car['image_path'], width=300)
            st.markdown(f"**Car:** {car['name']} ({car.car_type})")
            st.markdown(f"**Start Date:** {booking.start_date}")
            st.markdown(f"**End Date:** {booking.end_date}")
            st.markdown(f"**Total Price:** ${booking.total_price}")

            # Cancel button
            if st.button(f"Cancel Booking {booking.booking_id}", key=f"cancel_{booking.booking_id}"):
                try:
                    booking_canceling(booking.booking_id)
                    st.success(f"Booking {booking.booking_id} cancelled!")
                    st.rerun()  # Refresh page
                except ValueError as e:
                    st.error(str(e))

            # Update button
            with st.form(key=f"update_{booking.booking_id}"):
                new_start_date = st.date_input("New Start Date", datetime.strptime(booking.start_date, '%d/%m/%Y'))
                new_end_date = st.date_input("New End Date", datetime.strptime(booking.end_date, '%d/%m/%Y'))
                submit_button = st.form_submit_button("Update Booking")
                if submit_button:
                    if new_start_date > new_end_date:
                        st.error("End date must be after start date.")
                    else:
                        try:
                            booking_update(booking.booking_id, new_start_date.strftime('%d/%m/%Y'), new_end_date.strftime('%d/%m/%Y'))
                            st.success(f"Booking {booking.booking_id} updated!")
                            st.rerun()  # Refresh page
                        except ValueError as e:
                            st.error(str(e))
    else:
        st.markdown("No confirmed bookings found.")

elif view_option == "Booking History":
    st.markdown("## Booking History")
    booking_history = show_my_booking_history(user_id)

    if not booking_history.empty:
        for booking in booking_history.itertuples():
            car = cars_df[cars_df['car_id'] == booking.car_id].iloc[0]
            st.image(car['image_path'],width=300)
            st.markdown(f"**Car:** {car['name']} ({car.car_type})")
            print("car.name", car['name'])
            st.markdown(f"**Start Date:** {booking.start_date}")
            st.markdown(f"**End Date:** {booking.end_date}")
            st.markdown(f"**Total Price:** ${booking.total_price}")
            st.markdown(f"**Status:** {'Confirmed' if booking.booking_status == 2 else 'Cancelled'}")
            st.markdown("-------------------------------")
    else:
        st.markdown("No booking history found.")
