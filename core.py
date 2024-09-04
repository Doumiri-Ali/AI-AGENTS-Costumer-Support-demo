from conf import *
from datetime import date, datetime, timedelta
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
from dateutil.parser import parse, ParserError
from typing import Optional, Tuple, Dict, List, Any
import pandas as pd
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import tools_condition
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from fuzzywuzzy import process, fuzz

def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame()


def save_data(df, file_path):
    df.to_csv(file_path, index=False)


cars_df = load_data(CARS_FILE_PATH)
bookings_df = load_data(BOOKINGS_FILE_PATH)
users_df = load_data(USERS_FILE_PATH)

min_price = cars_df['price'].min()
max_price = cars_df['price'].max()
unique_car_types = cars_df['car_type'].unique()

with open('Rental-Car-Business-Demo/data/user_id.conf', 'r') as file:
    user_id = int(file.read().strip())
user_info = users_df[users_df['user_id'] == int(user_id)]




@tool
def lookup_policy(query: str) -> str:
    """Consult the company policies to check whether certain options are permitted.
    Use this before making any flight changes performing other 'write' events."""
    docs = retriever.query(query, k=2)
    return "\n\n".join([doc["page_content"] for doc in docs])


@tool
def calculator(operation: str, num1: float, num2: float) -> dict:
    """

    This tool performs basic arithmetic calculations to help with price calculations and other numerical tasks related to car rentals.

    **Purpose:**
    The `calculator` function is designed to assist you in performing simple arithmetic operations. This can be particularly useful for calculating rental costs, applying discounts, or determining total charges based on various factors.

    **Arguments:**
    - `operation` (str): Specifies the type of arithmetic operation you want to perform. The valid options are:
        - 'add': To add two numbers (e.g., calculating the total rental cost by adding base price and additional fees).
        - 'subtract': To subtract one number from another (e.g., calculating the amount remaining after a discount).
        - 'multiply': To multiply two numbers (e.g., calculating the total cost by multiplying the daily rental rate by the number of rental days).
        - 'divide': To divide one number by another (e.g., calculating the average daily cost by dividing the total cost by the number of days).
    - `num1` (float): The first number involved in the calculation. This could represent an amount such as a rental rate or discount value.
    - `num2` (float): The second number involved in the calculation. This could represent another amount or quantity, such as the number of days for a rental or additional charges.

    **Returns:**
    - A dictionary containing either:
        - `'result'`: The result of the calculation, formatted as a float or integer, depending on the operation.
        - `'error'`: A message indicating any issues with the operation or input values (e.g., invalid operation type or division by zero).

    **Examples:**
    - **Adding Rental Charges:**
      ```python
      calculator('add', 50.0, 20.0)
      # Returns: {'result': 70.0}
      ```
      Adds the base rental fee and an additional fee to get the total rental cost.

    - **Calculating Discounted Price:**
      ```python
      calculator('subtract', 200.0, 30.0)
      # Returns: {'result': 170.0}
      ```
      Subtracts a discount amount from the original price to get the discounted price.

    - **Total Rental Cost Calculation:**
      ```python
      calculator('multiply', 30.0, 7)
      # Returns: {'result': 210.0}
      ```
      Multiplies the daily rental rate by the number of rental days to calculate the total rental cost.

    - **Average Daily Cost Calculation:**
      ```python
      calculator('divide', 210.0, 7)
      # Returns: {'result': 30.0}
      ```
      Divides the total rental cost by the number of days to find the average daily cost.

    **Error Handling:**
    - If you attempt an invalid operation or divide by zero, the function will return an error message to help you understand what went wrong.

    Use this tool to streamline your calculations and ensure accurate pricing for car rentals and related services.

    """

    # Ensure the operation is valid
    valid_operations = ['add', 'subtract', 'multiply', 'divide']
    if operation not in valid_operations:
        return {"error": f"Invalid operation '{operation}'. Valid operations are {', '.join(valid_operations)}."}

    # Perform the calculation based on the operation
    try:
        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 == 0:
                return {"error": "Division by zero is not allowed."}
            result = num1 / num2
        return {"result": result}

    except Exception as e:
        return {"error": str(e)}



@tool
def dates_calculator(operation: str, start_date: str, end_date: Optional[str] = None, days: Optional[int] = None) -> Dict[str, any]:
    """
    This tool performs date calculations to help manage rental periods and other date-related tasks.

    **Purpose:**
    The `dates_calculator` function assists with various date calculations, such as finding the duration between two dates, calculating a future or past date from a given start date, or determining the number of days between two dates. This is useful for managing rental periods, determining booking durations, or setting deadlines.

    **Arguments:**
    - `operation` (str): Specifies the type of date calculation to perform. The valid options are:
        - 'duration': Calculate the number of days between the start date and today.
        - 'add_days': Calculate a future date by adding a specified number of days to the start date.
        - 'subtract_days': Calculate a past date by subtracting a specified number of days from the start date.
        - 'days_between': Calculate the number of days between two given dates.
    - `start_date` (str): The initial date in `dd/mm/YYYY` format. This is the reference date for the calculation.
    - `end_date` (str, optional): The end date in `dd/mm/YYYY` format. This argument is required for the 'days_between' operation.
    - `days` (int, optional): The number of days to add or subtract from the start date. This argument is required for 'add_days' and 'subtract_days' operations.

    **Returns:**
    - A dictionary containing either:
        - `'result'`: The result of the date calculation. For 'duration' and 'days_between', it returns the number of days. For 'add_days' and 'subtract_days', it returns the calculated date in `dd/mm/YYYY` format.
        - `'error'`: A message indicating any issues with the operation or input values (e.g., invalid operation type or missing arguments).

    **Examples:**
    - **Calculating Duration Between Dates:**
      ```python
      dates_calculator('duration', '01/01/2024')
      # Returns: {'result': 45}
      ```
      Calculates the number of days from January 1, 2024, to today.

    - **Finding a Future Date:**
      ```python
      dates_calculator('add_days', '01/01/2024', days=30)
      # Returns: {'result': '31/01/2024'}
      ```
      Calculates the date 30 days after January 1, 2024.

    - **Finding a Past Date:**
      ```python
      dates_calculator('subtract_days', '01/01/2024', days=30)
      # Returns: {'result': '02/12/2023'}
      ```
      Calculates the date 30 days before January 1, 2024.

    - **Calculating Days Between Two Dates:**
      ```python
      dates_calculator('days_between', '01/01/2024', '15/02/2024')
      # Returns: {'result': 45}
      ```
      Calculates the number of days between January 1, 2024, and February 15, 2024.

    **Error Handling:**
    - If you attempt an invalid operation or provide an incorrect date format, the function will return an error message to help you understand what went wrong.
    - If the 'add_days' or 'subtract_days' operation is selected but no days argument is provided, it will also return an error message.
    - If the 'days_between' operation is selected but no end_date argument is provided, it will return an error message.

    Use this tool to efficiently handle date calculations related to rental periods, booking durations, or any other date-related needs.
    """

    try:
        # Parse the start date
        start_date = datetime.strptime(start_date, '%d/%m/%Y')

        if operation == 'duration':
            # Calculate the duration between the start date and today
            today = datetime.now()
            duration = (today - start_date).days
            return {"result": duration}

        elif operation == 'add_days':
            if days is None:
                return {"error": "The 'days' argument is required for 'add_days' operation."}
            # Calculate the future date
            future_date = start_date + timedelta(days=days)
            return {"result": future_date.strftime('%d/%m/%Y')}

        elif operation == 'subtract_days':
            if days is None:
                return {"error": "The 'days' argument is required for 'subtract_days' operation."}
            # Calculate the past date
            past_date = start_date - timedelta(days=days)
            return {"result": past_date.strftime('%d/%m/%Y')}

        elif operation == 'days_between':
            if end_date is None:
                return {"error": "The 'end_date' argument is required for 'days_between' operation."}
            # Parse the end date
            end_date = datetime.strptime(end_date, '%d/%m/%Y')
            # Calculate the number of days between the two dates
            days_between = (end_date - start_date).days
            return {"result": days_between}

        else:
            return {
                "error": f"Invalid operation '{operation}'. Valid operations are 'duration', 'add_days', 'subtract_days', and 'days_between'."}

    except ValueError as ve:
        return {"error": f"Date format error: {ve}"}
    except Exception as e:
        return {"error": str(e)}


@tool
def is_car_available(car_id: int, start_date: str, end_date: str) -> str:
    """
    Check if a specific car is available during the given rental period.

    Args:
        car_id (int): ID of the car (user_id) to check. you can retreive it by searching for the car using car_search()
        start_date (str): The start date for the rental period in any date format. use this date format dd/mm/YYYY
        end_date (str): The end date for the rental period in any date format. use this date format dd/mm/YYYY

    Returns:
        str: A message indicating whether the car is available or not, or an error message if dates are invalid.
    """
    bookings_df = load_data(BOOKINGS_FILE_PATH)

    def parse_date(date_str: str) -> Optional[datetime]:
        try:
            return parse(date_str, fuzzy=True)
        except (ParserError, ValueError, OverflowError):
            return None

    parsed_start_date = parse_date(start_date)
    parsed_end_date = parse_date(end_date)

    if (parsed_start_date is None) or (parsed_end_date is None):
        return "Error: Invalid date format. Please provide dates in a recognizable format."

    #if parsed_start_date > parsed_end_date:
        #return "Error: Start date must be before end date."

    try:
        car_bookings = bookings_df[(bookings_df['car_id'] == car_id) & (bookings_df['booking_status'] == 2)]
        for booking in car_bookings.itertuples():
            booking_start_date = parse_date(booking.start_date)
            booking_end_date = parse_date(booking.end_date)
            if booking_start_date and booking_end_date:
                if booking_start_date <= parsed_end_date and booking_end_date >= parsed_start_date:
                    return f"The car with ID {car_id} is not available for the specified dates."
        return f"The car with ID {car_id} is available for the specified dates."
    except Exception as e:
        return f"An error occurred while checking availability: {str(e)}"


def is_car_available2(car_id: int, start_date: date, end_date: date) -> bool:
    bookings_df = load_data(BOOKINGS_FILE_PATH)

    car_bookings = bookings_df[(bookings_df['car_id'] == car_id) & (bookings_df['booking_status'] == 2)]
    for booking in car_bookings.itertuples():
        booking_start_date = parse(booking.start_date)
        booking_end_date = parse(booking.end_date)


        if start_date <= booking_end_date and end_date >= booking_start_date:
            return False
    return True



@tool
def car_search(car_name: str = None,
               car_type: str = None,
               price_range: tuple = None,
               start_date: str = None,
               end_date: str = None) -> dict:
    """
    Search for available cars based on specified criteria.

    Args:
        car_name (str): Name of the car to search for.
        car_type (str): Type of car to search for.
        price_range (tuple): A tuple of floats containing the minimum and maximum price (min_price, max_price).
        start_date (str): The start date for the rental period in dd/mm/YYYY date format.
        end_date (str): The end date for the rental period in dd/mm/YYYY date format.

    Returns:
        dict: A dictionary containing available cars that match the search criteria.
    """
    cars_df = load_data(CARS_FILE_PATH)
    cars = cars_df



    # Parse dates if provided
    if start_date:
        start_date = parse(start_date)
    if end_date:
        end_date = parse(end_date)

    # Fuzzy matching for car name
    if car_name:
        car_names = cars_df['name'].unique()
        best_match = process.extractOne(car_name, car_names, scorer=fuzz.token_set_ratio)
        if best_match and best_match[1] >= 70:  # 70% similarity threshold
            car_name = best_match[0]
        cars = cars[cars['name'] == car_name]
        if cars.empty:
            car_types = cars_df['car_type'].unique()
            best_match = process.extractOne(car_name, car_types, scorer=fuzz.token_set_ratio)
            if best_match and best_match[1] >= 80:  # 70% similarity threshold
                car_type = best_match[0]
            cars = cars[cars['car_type'] == car_type]



    # Fuzzy matching for car type
    if car_type:
        car_types = cars_df['car_type'].unique()
        best_match = process.extractOne(car_type, car_types, scorer=fuzz.token_set_ratio)
        if best_match and best_match[1] >= 70:  # 70% similarity threshold
            car_type = best_match[0]
        cars = cars[cars['car_type'] == car_type]




    # Apply price range filter
    if price_range:
        cars = cars[(cars['price'] >= price_range[0]) & (cars['price'] <= price_range[1])]

    # Apply date availability filter
    if start_date and end_date:
        cars = cars[cars['car_id'].apply(lambda car_id: is_car_available2(car_id, start_date, end_date))]

    # Convert DataFrame to list of dictionaries
    result = {'available_cars': cars.to_dict(orient='records')}

    return result

#car_search.__doc__ %= (unique_car_types, min_price, max_price)

# Now you can apply the @tool decorator if needed
#car_search = tool(car_search)

@tool
def car_booking(car_id: int, start_date: str, end_date: str) -> dict:
    """
    Add a new car booking to the pending booked list , and not the confirmed booked list.
    then the user need to confirm the booking manually.

    Args:
        car_id (int): ID of the car being booked (car_id).
        start_date (str): Start date of the rental period in dd/mm/YYYY date format.
        end_date (str): End date of the rental period in dd/mm/YYYY date format.

    Returns:
        dict : Return a dictionarie with booking info if succeful or error.
    """


    bookings_df = load_data(BOOKINGS_FILE_PATH)
    cars_df = load_data(CARS_FILE_PATH)

    # Parse the start and end dates with flexible format handling
    start_date = parse(start_date)
    end_date = parse(end_date)

    if is_car_available2(car_id, start_date, end_date):

        days = (end_date - start_date).days
        car_price = cars_df.loc[cars_df['car_id'] == car_id, 'price'].values[0]
        total_price = abs(days * car_price)

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

        return new_booking
    else:
        return {"error": "Car is not available for the specified dates."}



def is_booking_available(booking_id: int) -> bool:
    bookings_df = load_data(BOOKINGS_FILE_PATH)

    # Check if the booking_id exists and is not canceled (status != 0)
    if booking_id in bookings_df['booking_id'].values:
        booking_status = bookings_df.loc[bookings_df['booking_id'] == booking_id, 'booking_status'].values[0]
        return booking_status != 0

    return False


@tool
def booking_canceling(booking_id: int) -> dict:
    """
    Cancel a booking by changing its status to 'Cancelled'.

    Args:
        booking_id (int): ID of the booking to be cancelled (booking_id).

    Returns:
        dict: A dictionary indicating success or error. If successful, it includes the updated booking information.
    """
    try:
        # Check if the booking is available (i.e., not already canceled)
        if not is_booking_available(booking_id):
            return {"error": f"Booking ID {booking_id} is not available or has already been canceled."}

        bookings_df = load_data(BOOKINGS_FILE_PATH)

        # Cancel the booking by setting its status to 0 (Cancelled)
        bookings_df.loc[bookings_df['booking_id'] == booking_id, 'booking_status'] = 0
        save_data(bookings_df, BOOKINGS_FILE_PATH)

        # Retrieve the updated booking and return it
        updated_booking = bookings_df[bookings_df['booking_id'] == booking_id].to_dict(orient='records')[0]
        return {"success": True, "data": updated_booking}

    except Exception as e:
        # Handle any unexpected errors
        return {"error": str(e)}

@tool
def booking_update(booking_id: int, new_start_date: str, new_end_date: str) -> dict:
    """
    Update an existing booking with new start and end dates.

    Args:
        booking_id (int): ID of the booking to be updated (booking_id).
        new_start_date (str): New start date of the rental period in dd/mm/YYYY date format.
        new_end_date (str): New end date of the rental period in dd/mm/YYYY date format.

    Returns:
        dict: A dictionary indicating success or error. If successful, it includes the updated booking information.
    """
    try:
        # Check if the booking is available (i.e., not canceled)
        if not is_booking_available(booking_id):
            return {"error": f"Booking ID {booking_id} is not available or has already been canceled."}

        # Load bookings and cars data
        bookings_df = load_data(BOOKINGS_FILE_PATH)
        cars_df = load_data(CARS_FILE_PATH)

        # Retrieve the booking and car information
        booking = bookings_df[bookings_df['booking_id'] == booking_id].iloc[0]
        car_id = booking['car_id']

        # Parse the new start and end dates
        try:
            new_start_date = datetime.strptime(new_start_date, '%d/%m/%Y')
            new_end_date = datetime.strptime(new_end_date, '%d/%m/%Y')
        except ValueError:
            return {"error": "Invalid date format. Please use dd/mm/YYYY."}

        # Check if the new end date is after the new start date
        if new_end_date <= new_start_date:
            return {"error": "End date must be after the start date."}

        # Check if the car is available for the new dates
        if not is_car_available2(car_id, new_start_date, new_end_date):
            return {"error": "The car is not available for the new dates specified."}

        # Get the price for the car
        car_info = cars_df[cars_df['car_id'] == car_id]
        if car_info.empty:
            return {"error": "Car ID not found."}
        price_per_day = car_info.iloc[0]['price']

        # Calculate the new total price
        duration = (new_end_date - new_start_date).days
        if duration < 0:
            return {"error": "End date must be after start date."}
        total_price = duration * int(price_per_day)

        # Update the booking with the new dates and total price
        bookings_df.loc[bookings_df['booking_id'] == booking_id, 'start_date'] = new_start_date.strftime('%d/%m/%Y')
        bookings_df.loc[bookings_df['booking_id'] == booking_id, 'end_date'] = new_end_date.strftime('%d/%m/%Y')
        bookings_df.loc[bookings_df['booking_id'] == booking_id, 'total_price'] = total_price

        # Save the updated bookings data
        save_data(bookings_df, BOOKINGS_FILE_PATH)

        # Retrieve the updated booking and return it
        updated_booking = bookings_df[bookings_df['booking_id'] == booking_id].to_dict(orient='records')[0]
        return {"success": True, "data": updated_booking}

    except Exception as e:
        # Handle any unexpected errors
        return {"error": str(e)}



@tool
def show_my_pending_booked_cars() -> dict:
    """
    Retrieve all pending bookings for a specific user.


    Returns:
        dict: dictionary of cars that are currently booked by the user with pending status.
    """
    global  user_id
    bookings_df = load_data(BOOKINGS_FILE_PATH)
    cars_df = load_data(CARS_FILE_PATH)

    user_bookings = bookings_df[(bookings_df['user_id'] == user_id) & (bookings_df['booking_status'] == 1)]
    booked_cars = pd.merge(user_bookings, cars_df, on='car_id')
    return booked_cars.to_dict(orient='records')


@tool
def confirm_pending_bookings() -> str:
    """
    Confirming the pending reservervations for the user.


    Returns:
        str : A policy message about confirming pending bookings.
    """
    return "the pending bookings cannot be confirmed , the user need to confirm the booking manually at the reservations page"

@tool
def show_my_confirmed_booked_cars() -> dict:
    """
    Retrieve all confirmed bookings for the user.


    Returns:
        dict: dictionary of cars that are currently booked by the user with confirmed status.
    """

    bookings_df = load_data(BOOKINGS_FILE_PATH)
    cars_df = load_data(CARS_FILE_PATH)

    user_bookings = bookings_df[(bookings_df['user_id'] == user_id) & (bookings_df['booking_status'] == 2)]
    booked_cars = pd.merge(user_bookings, cars_df, on='car_id')
    return booked_cars.to_dict(orient='records')


@tool
def show_my_booking_history() -> dict:
    """
    Retrieve the complete bookings history for the user.

    Returns:
        dict: dictionnairy of the last 5  bookings (past and present) by the user, excluding pending bookings. for more than 5 user need to check the bookings history manually
    """
    bookings_df = load_data(BOOKINGS_FILE_PATH)
    cars_df = load_data(CARS_FILE_PATH)

    user_history = bookings_df[(bookings_df['user_id'] == user_id) & (bookings_df['booking_status'] != 1)]
    # Merge with car data to get detailed information
    booking_history = pd.merge(user_history, cars_df, on='car_id')
    last_five_bookings = booking_history.tail(5)

    return last_five_bookings.to_dict(orient='records')


@tool
def show_personal_info() -> dict:
    """
    Retrieve all personal information for the user.

    Returns:
        dict: dictionary containing personal information of the  user.
    """
    global user_id
    return users_df[users_df['user_id'] == user_id].to_dict(orient='records')


@tool
def show_car_info(car_id: int) -> dict:
    """
    Retrieve information about a specific car based on its car_id , i you dont have the car_id you can use the search_car to get the cars ids

    Args:
        car_id (int): ID of the car (car_id) whose information is to be retrieved.

    Returns:
        dict: dictionary containing details of the specified car.
    """
    return cars_df[cars_df['car_id'] == car_id].to_dict(orient='records')


@tool
def show_cars() -> dict:
    """
    Retrieve information about all cars available in the system.

    Returns:
        dict: dictionary containing details of all cars.
    """
    global cars_df
    return cars_df.to_dict(orient='records')


def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


def create_tool_node_with_fallback(tools: list) -> dict:
    """
    Create a ToolNode with error handling fallback for a list of tools.

    This function creates a ToolNode from the given list of tools and adds
    an error handling fallback. If a tool execution fails, it will catch
    the error and return a message asking to fix the mistake.

    Args:
        tools (list): A list of tool objects to be used in the ToolNode.

    Returns:
        dict: A ToolNode object with error handling fallback.

    The returned ToolNode will:
    1. Attempt to execute the appropriate tool based on the input.
    2. If an error occurs, it will use the handle_tool_error function to
       generate an error message.
    3. The error message will be returned as a ToolMessage.

    Note: This function relies on the ToolNode class from langgraph.prebuilt
    and the RunnableLambda class from langchain_core.runnables.
    """

    return ToolNode(tools).with_fallbacks([RunnableLambda(handle_tool_error)], exception_key="error")


def _print_event(event: dict, _printed: set, max_length=1500):
    current_state = event.get("dialog_state")
    if current_state:
        print("Currently in: ", current_state[-1])
    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            print(msg_repr)
            _printed.add(message.id)


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]



def update_tool_messages(message):
    updated_messages = []

    #for message in tool_messages:
    content = str(message.content)


    # Initialize a list to store the extracted IDs
    extracted_info = []


    # Extract standalone booking_id
    booking_ids = re.findall(r'booking_id.*?(\d+)', content)
    if booking_ids :
        extracted_info.extend([{'booking_id': int(bid)} for bid in booking_ids])

    # Extract standalone car_id
    car_ids = re.findall(r'car_id.*?(\d+)', content)
    if car_ids:
        extracted_info.extend([{'car_id': int(cid)} for cid in car_ids])

    # Convert the extracted information to JSON string
    if extracted_info:
        content = json.dumps(extracted_info)

    # Update the message with the filtered content
    message.content = content
        #updated_messages.append(updated_message)

    return message

def clean_state(state):
    cleaned_messages = []
    middle_steps = []
    users = 0
    bots = 0

    for message in state.get("messages"):
        # Identify user input
        if isinstance(message, HumanMessage):
            user_input = message
            cleaned_messages.append(user_input)
            users += 1

        # Identify bot response
        elif isinstance(message, AIMessage):
            if message.content and message.response_metadata:
                # Before appending the bot's response, ensure any middle_steps are added
                cleaned_messages.append(message)
                bots += 1

                # After appending, if users == bots, update and append middle_steps
                if users == bots:
                    # Update ToolMessages in middle_steps if necessary

                    for index, step in enumerate(cleaned_messages):
                        if isinstance(step, ToolMessage):
                            if ('booking_id' in str(step.content)) or ('car_id' in str(step.content)):
                                print("************************** found it******")
                                print("step : ", step)
                                print("update_tool_messages(step) : ", update_tool_messages(step))
                                cleaned_messages[index] = update_tool_messages(step)
                        # Replace the middle_steps with their updated versions
                    cleaned_messages = [msg for msg in cleaned_messages if msg not in middle_steps]
                    middle_steps = []
            else:
                cleaned_messages.append(message)
                middle_steps.append(message)

        # Identify tool-related messages (middle steps)
        elif isinstance(message, ToolMessage):
            if ('booking_id' in str(message.content)) or ('car_id' in str(message.content)):
            #middle_steps.append(message)
                cleaned_messages.append(message)
            else:
                middle_steps.append(message)
                cleaned_messages.append(message)
            # Appending immediately, but will be updated later

    return {'messages': cleaned_messages}




class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            configuration = config.get("configurable", {})
            passenger_id = configuration.get("user_info", None)
            state = {**state, "user_info": passenger_id}
            state = clean_state(state)

            if len(state.get("messages")) >= 2:
                if state.get("messages")[-2].response_metadata:
                    tokens = state.get("messages")[-2].response_metadata['token_usage']['total_tokens']
                    if tokens < 6500 and tokens > 5000 :
                        state["messages"] = state.get("messages")[-4:]
                    elif tokens > 6500:
                        state["messages"] = state.get("messages")[-3:]
            else:
                state["messages"] = state.get("messages")

            result = self.runnable.invoke(state)

            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response and remove the empty result from the history.
            if not result.tool_calls and (
                    not result.content
                    or isinstance(result.content, list)
                    and not result.content[0].get("text")
            ):
                # Re-prompt for a real output
                state["messages"].append(("user", "Respond with a real output."))
            else:
                # After receiving a real output, remove the "Respond with a real output." from history
                state["messages"] = [
                    message for message in state["messages"]
                    if message != ("user", "Respond with a real output.")
                ]
                break

        return {"messages": result}




primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a dedicated and resourceful customer support assistant for a rental car company. "
            "Your primary objective is to assist users efficiently and accurately by leveraging the tools at your disposal. "
            "When conducting searches, apply a systematic approach: start with precise queries and gradually expand your search parameters if initial results are insufficient. "
            "Always strive to provide the most relevant information to the user, even if it requires multiple attempts. "
            "If you encounter difficulties, broaden your search scope or consider alternative phrasing to ensure comprehensive assistance. "
            "In your responses, clearly communicate any actions you are taking, and ensure the user feels supported and understood. Use Markdown for formatting your responses for clarity and readability."
           
            "\n\n### Key Capabilities:\n"
            "- Search for cars based on various criteria such as name, type, and price range, including availability within a specified date range.\n"
            "- Book a car for a specified period. The booking will initially be pending confirmation. ** you cant confirm penfing bookings , the user need to it manually**\n"
            "- Retrieve company policies related to bookings, cancellations, and other services.\n"
            "- Check if a specific car is available for the desired dates.\n"
            "- Cancel an existing booking by updating its status to 'Cancelled'.\n"
            "- Update an existing booking with new start and end dates, ensuring the car is available for the new dates.\n"
            "- Display a list of cars that the user has booked but not yet confirmed.\n"
            "- Display a list of cars that the user has confirmed bookings for.\n"
            "- Show the user’s up to 5 last bookings history (for more than 5 , the user need to check the history manually).\n"
            "- Display the user’s personal information stored in the system.\n"
            "- Provide detailed information about a specific car.\n"
            "- List all available cars in the inventory.\n"
            "\n\n### Key Considerations:\n"
            "- Persist in your search efforts, expanding your approach when needed.\n"
            "- Reference previous interactions to maintain continuity and relevance.\n"
            "- Prioritize clarity and helpfulness in every response, and be detailed in your response.\n"
            "- Use Markdown formatting to make your responses clear and structured.\n"
            "- handle all dates with in dd/mm/YYYY format"
            

            "\n\nCurrent user:\n\n{user_info}\n"
            "\nCurrent time (%d/%m/%Y): {time}.",
        ),
        ("placeholder", "{messages}"),
    ]
).partial(user_info=user_info, time=datetime.now().strftime('%d/%m/%Y'))

part_1_tools = [
    car_booking,
    lookup_policy,
    is_car_available,
    booking_canceling,
    confirm_pending_bookings,
    booking_update,
    calculator,
    dates_calculator,
    show_my_pending_booked_cars,
    show_my_confirmed_booked_cars,
    show_my_booking_history,
    show_personal_info,
    show_car_info,
    show_cars,
    car_search,
]
part_1_assistant_runnable = primary_assistant_prompt | llm.bind_tools(part_1_tools)

builder = StateGraph(State)

# Define nodes: these do the work
builder.add_node("assistant", Assistant(part_1_assistant_runnable))
builder.add_node("tools", create_tool_node_with_fallback(part_1_tools))
# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

# The checkpointer lets the graph persist its state
# this is a complete memory for the entire graph.
memory = MemorySaver()
part_1_graph = builder.compile(checkpointer=memory)


