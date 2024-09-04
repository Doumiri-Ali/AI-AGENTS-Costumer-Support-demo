import pandas as pd
import os

# Sample data for cars.csv
cars_data = {
    'car_id': list(range(0, 20)),
    'name': [
        'Toyota Camry', 'Honda Civic', 'Ford Mustang', 'Chevrolet Malibu',
        'BMW X5', 'Audi Q7', 'Mercedes-Benz E-Class', 'Lexus RX 350',
        'Porsche 911', 'Chevrolet Corvette', 'Jaguar F-Type', 'Mazda MX-5 Miata',
        'Volkswagen Jetta', 'Hyundai Sonata', 'Nissan Altima', 'Kia Optima',
        'Ford Explorer', 'Toyota Highlander', 'Honda Pilot', 'Jeep Grand Cherokee'
    ],
    'car_type': [
        'Sedan', 'Sedan', 'Sports', 'Sedan', 'SUV', 'SUV', 'Luxury', 'SUV',
        'Luxury', 'Luxury', 'Luxury', 'Convertible', 'Sedan', 'Sedan', 'Sedan', 'Sedan',
        'SUV', 'SUV', 'SUV', 'SUV'
    ],
    'price': [
        45, 50, 70, 55, 80, 85, 95, 90, 120, 130, 140, 75, 50, 55, 60, 65,
        85, 90, 95, 100
    ],
    'year': [
        2021, 2020, 2022, 2021, 2022, 2021, 2023, 2023, 2022, 2021, 2022, 2020,
        2021, 2022, 2021, 2023, 2022, 2021, 2023, 2021
    ],
    'fuel_type': [
        'Gasoline', 'Gasoline', 'Gasoline', 'Gasoline', 'Gasoline', 'Diesel', 'Gasoline', 'Hybrid',
        'Gasoline', 'Gasoline', 'Gasoline', 'Gasoline', 'Gasoline', 'Gasoline', 'Gasoline', 'Gasoline',
        'Gasoline', 'Gasoline', 'Gasoline', 'Diesel'
    ],
    'transmission': [
        'Automatic', 'Automatic', 'Manual', 'Automatic', 'Automatic', 'Automatic', 'Automatic', 'Automatic',
        'Manual', 'Automatic', 'Automatic', 'Manual', 'Automatic', 'Automatic', 'Automatic', 'Automatic',
        'Automatic', 'Automatic', 'Automatic', 'Automatic'
    ],
    'mileage': [
        15000, 20000, 10000, 12000, 18000, 16000, 5000, 8000, 6000, 7000, 4000, 12000,
        20000, 18000, 17000, 15000, 22000, 21000, 19000, 20000
    ],
    'image_path': [
        'Rental-Car-Business-Demo/assets/images/toyota_camry.png',
        'Rental-Car-Business-Demo/assets/images/honda_civic.png',
        'Rental-Car-Business-Demo/assets/images/ford_mustang.png',
        'Rental-Car-Business-Demo/assets/images/chevrolet_malibu.png',
        'Rental-Car-Business-Demo/assets/images/bmw_x5.png',
        'Rental-Car-Business-Demo/assets/images/audi_q7.png',
        'Rental-Car-Business-Demo/assets/images/mercedes_benz_e_class.png',
        'Rental-Car-Business-Demo/assets/images/lexus_rx_350.png',
        'Rental-Car-Business-Demo/assets/images/porsche_911.png',
        'Rental-Car-Business-Demo/assets/images/chevrolet_corvette.png',
        'Rental-Car-Business-Demo/assets/images/jaguar_f_type.png',
        'Rental-Car-Business-Demo/assets/images/mazda_mx5_miata.png',
        'Rental-Car-Business-Demo/assets/images/volkswagen_jetta.png',
        'Rental-Car-Business-Demo/assets/images/hyundai_sonata.png',
        'Rental-Car-Business-Demo/assets/images/nissan_altima.png',
        'Rental-Car-Business-Demo/assets/images/kia_optima.png',
        'Rental-Car-Business-Demo/assets/images/ford_explorer.png',
        'Rental-Car-Business-Demo/assets/images/toyota_highlander.png',
        'Rental-Car-Business-Demo/assets/images/honda_pilot.png',
        'Rental-Car-Business-Demo/assets/images/jeep_grand_cherokee.png'
    ]
}


# Sample data for bookings.csv
bookings_data = {
    'booking_id': [0, 1],
    'car_id': [0, 2],
    'user_id': [101, 102],
    'start_date': ['01/08/2024', '15/08/2024'],
    'end_date': ['07/08/2024', '20/08/2024'],
    'total_price': [315, 420],
    'booking_status': [0,0]
}

# Sample data for users.csv
users_data = {
    'user_id': [101, 102],
    'name': ['John Doe', 'Jane Smith'],
    'email': ['john@example.com', 'jane@example.com'],
    'phone': ['555-1234', '555-5678'],
    'address': ['123 Elm St', '456 Oak St']
}

# Sample data for reviews.csv


# Create DataFrames
cars_df = pd.DataFrame(cars_data)
bookings_df = pd.DataFrame(bookings_data)
users_df = pd.DataFrame(users_data)


# Define file paths
file_paths = {
    'cars': 'Rental-Car-Business-Demo/data/cars.csv',
    'bookings': 'Rental-Car-Business-Demo/data/bookings.csv',
    'users': 'Rental-Car-Business-Demo/data/users.csv',
}

# Check if the directory exists, if not create it
os.makedirs(os.path.dirname(file_paths['cars']), exist_ok=True)

# Save DataFrames to CSV if they do not exist
if not os.path.exists(file_paths['cars']):
    cars_df.to_csv(file_paths['cars'], index=False)
    print(f"CSV file {file_paths['cars']} created successfully!")

if not os.path.exists(file_paths['bookings']):
    bookings_df.to_csv(file_paths['bookings'], index=False)
    print(f"CSV file {file_paths['bookings']} created successfully!")

if not os.path.exists(file_paths['users']):
    users_df.to_csv(file_paths['users'], index=False)
    print(f"CSV file {file_paths['users']} created successfully!")


print("CSV file creation check complete!")