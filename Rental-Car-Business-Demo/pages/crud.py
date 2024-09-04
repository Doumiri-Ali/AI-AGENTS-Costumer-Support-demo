# car_rental_crud.py

import pandas as pd
import os
from datetime import datetime

# File paths
CARS_FILE_PATH = 'Rental-Car-Business-Demo/data/cars.csv'
BOOKINGS_FILE_PATH = 'Rental-Car-Business-Demo/data/bookings.csv'
USERS_FILE_PATH = 'Rental-Car-Business-Demo/data/users.csv'


def load_data(file_path):
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the loaded data. Returns an empty DataFrame if the file does not exist.
    """
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame()


def save_data(df, file_path):
    """
    Save a pandas DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): DataFrame to be saved.
        file_path (str): Path to the CSV file where the DataFrame will be saved.
    """
    df.to_csv(file_path, index=False)


def car_search(car_type, price_range, start_date, end_date):
    """
    Search for available cars based on specified criteria.

    Args:
        car_type (str): Type of car to search for (e.g., 'SUV', 'Sedan').
        price_range (tuple): A tuple containing the minimum and maximum price (min_price, max_price).
        start_date (str): The start date for the rental period in 'dd/mm/yyyy' format.
        end_date (str): The end date for the rental period in 'dd/mm/yyyy' format.

    Returns:
        pd.DataFrame: DataFrame containing available cars that match the search criteria.
    """
    cars_df = load_data(CARS_FILE_PATH)
    bookings_df = load_data(BOOKINGS_FILE_PATH)

    start_date = datetime.strptime(start_date, '%d/%m/%Y')
    end_date = datetime.strptime(end_date, '%d/%m/%Y')

    def is_car_available(car_id, start_date, end_date):
        """
        Check if a specific car is available during the given rental period.

        Args:
            car_id (int): ID of the car to check.
            start_date (datetime): Start date of the rental period.
            end_date (datetime): End date of the rental period.

        Returns:
            bool: True if the car is available, False otherwise.
        """
        car_bookings = bookings_df[(bookings_df['car_id'] == car_id) & (bookings_df['booking_status'] == 2)]
        for booking in car_bookings.itertuples():
            booking_start_date = datetime.strptime(booking.start_date, '%d/%m/%Y')
            booking_end_date = datetime.strptime(booking.end_date, '%d/%m/%Y')
            if booking_start_date <= end_date and booking_end_date >= start_date:
                return False
        return True

    available_cars = cars_df[
        (cars_df['car_type'] == car_type) & (cars_df['price'] >= price_range[0]) & (cars_df['price'] <= price_range[1])]
    available_cars = available_cars[
        available_cars['car_id'].apply(lambda car_id: is_car_available(car_id, start_date, end_date))]
    return available_cars


def car_booking(user_id, car_id, start_date, end_date):
    """
    Add a new car booking to the system.

    Args:
        user_id (int): ID of the user making the booking.
        car_id (int): ID of the car being booked.
        start_date (str): Start date of the rental period in 'dd/mm/yyyy' format.
        end_date (str): End date of the rental period in 'dd/mm/yyyy' format.

    Returns:
        pd.DataFrame: Updated DataFrame of bookings including the new booking.
    """
    cars_df = load_data(CARS_FILE_PATH)
    bookings_df = load_data(BOOKINGS_FILE_PATH)

    start_date = datetime.strptime(start_date, '%d/%m/%Y')
    end_date = datetime.strptime(end_date, '%d/%m/%Y')

    days = (end_date - start_date).days + 1
    car_price = cars_df.loc[cars_df['car_id'] == car_id, 'price'].values[0]
    total_price = days * car_price

    new_booking_id = bookings_df['booking_id'].max() + 1 if not bookings_df.empty else 1
    new_booking = {
        'booking_id': new_booking_id,
        'car_id': car_id,
        'user_id': user_id,
        'start_date': start_date.strftime('%d/%m/%Y'),
        'end_date': end_date.strftime('%d/%m/%Y'),
        'total_price': total_price,
        'booking_status': 1  # Status 1 = Pending
    }

    new_booking_df = pd.DataFrame([new_booking])
    bookings_df = pd.concat([bookings_df, new_booking_df], ignore_index=True)
    save_data(bookings_df, BOOKINGS_FILE_PATH)

    return bookings_df


def confirm_booking(booking_id):
    """
    Confirm a pending booking by changing its status to 'Confirmed'.

    Args:
        booking_id (int): ID of the booking to be confirmed.

    Returns:
        pd.DataFrame: Updated DataFrame of bookings with the confirmed booking.

    Raises:
        ValueError: If the booking ID does not exist or is not in pending status.
    """
    bookings_df = load_data(BOOKINGS_FILE_PATH)

    if booking_id in bookings_df['booking_id'].values:
        if bookings_df.loc[bookings_df['booking_id'] == booking_id, 'booking_status'].values[0] == 1:
            bookings_df.loc[bookings_df['booking_id'] == booking_id, 'booking_status'] = 2  # Status 2 = Confirmed
            save_data(bookings_df, BOOKINGS_FILE_PATH)
            return bookings_df
        else:
            raise ValueError(f"Booking ID {booking_id} is not in pending status.")
    else:
        raise ValueError(f"Booking ID {booking_id} does not exist.")


def booking_canceling(booking_id):
    """
    Cancel a booking by changing its status to 'Cancelled'.

    Args:
        booking_id (int): ID of the booking to be cancelled.

    Returns:
        pd.DataFrame: Updated DataFrame of bookings with the cancelled booking.
    """
    bookings_df = load_data(BOOKINGS_FILE_PATH)
    bookings_df.loc[bookings_df['booking_id'] == booking_id, 'booking_status'] = 0  # Status 0 = Cancelled
    save_data(bookings_df, BOOKINGS_FILE_PATH)
    return bookings_df


def booking_update(booking_id, new_start_date, new_end_date):
    """
    Update an existing booking with new start and end dates.

    Args:
        booking_id (int): ID of the booking to be updated.
        new_start_date (str): New start date of the rental period in 'dd/mm/yyyy' format.
        new_end_date (str): New end date of the rental period in 'dd/mm/yyyy' format.

    Returns:
        pd.DataFrame: Updated DataFrame of bookings with the modified booking.
    """
    bookings_df = load_data(BOOKINGS_FILE_PATH)

    new_start_date = datetime.strptime(new_start_date, '%d/%m/%Y')
    new_end_date = datetime.strptime(new_end_date, '%d/%m/%Y')

    bookings_df.loc[bookings_df['booking_id'] == booking_id, 'start_date'] = new_start_date.strftime('%d/%m/%Y')
    bookings_df.loc[bookings_df['booking_id'] == booking_id, 'end_date'] = new_end_date.strftime('%d/%m/%Y')
    save_data(bookings_df, BOOKINGS_FILE_PATH)
    return bookings_df


def show_my_pending_booked_cars(user_id):
    """
    Retrieve all pending bookings for a specific user.

    Args:
        user_id (int): ID of the user whose pending bookings are to be retrieved.

    Returns:
        pd.DataFrame: DataFrame of cars that are currently booked by the user with pending status.
    """
    bookings_df = load_data(BOOKINGS_FILE_PATH)
    cars_df = load_data(CARS_FILE_PATH)

    user_bookings = bookings_df[(bookings_df['user_id'] == user_id) & (bookings_df['booking_status'] == 1)]
    booked_cars = pd.merge(user_bookings, cars_df, on='car_id')
    return booked_cars


def show_my_confirmed_booked_cars(user_id):
    """
    Retrieve all confirmed bookings for a specific user.

    Args:
        user_id (int): ID of the user whose confirmed bookings are to be retrieved.

    Returns:
        pd.DataFrame: DataFrame of cars that are currently booked by the user with confirmed status.
    """
    bookings_df = load_data(BOOKINGS_FILE_PATH)
    cars_df = load_data(CARS_FILE_PATH)

    user_bookings = bookings_df[(bookings_df['user_id'] == user_id) & (bookings_df['booking_status'] == 2)]
    booked_cars = pd.merge(user_bookings, cars_df, on='car_id')
    return booked_cars


def show_my_booking_history(user_id):
    """
    Retrieve the complete booking history for a specific user.

    Args:
        user_id (int): ID of the user whose booking history is to be retrieved.

    Returns:
        pd.DataFrame: DataFrame of all bookings (past and present) by the user, excluding pending bookings.
    """
    bookings_df = load_data(BOOKINGS_FILE_PATH)
    cars_df = load_data(CARS_FILE_PATH)

    user_history = bookings_df[(bookings_df['user_id'] == user_id) & (bookings_df['booking_status'] != 1)]
    booking_history = pd.merge(user_history, cars_df, on='car_id')
    return booking_history


def show_personal_info(user_id):
    """
    Retrieve personal information for a specific user.

    Args:
        user_id (int): ID of the user whose personal information is to be retrieved.

    Returns:
        pd.DataFrame: DataFrame containing personal information of the specified user.
    """
    users_df = load_data(USERS_FILE_PATH)
    return users_df[users_df['user_id'] == user_id]


def show_car_info(car_id):
    """
    Retrieve information about a specific car.

    Args:
        car_id (int): ID of the car whose information is to be retrieved.

    Returns:
        pd.DataFrame: DataFrame containing details of the specified car.
    """
    cars_df = load_data(CARS_FILE_PATH)
    return cars_df[cars_df['car_id'] == car_id]


def show_cars():
    """
    Retrieve information about all cars available in the system.

    Returns:
        pd.DataFrame: DataFrame containing details of all cars.
    """
    cars_df = load_data(CARS_FILE_PATH)
    return cars_df
