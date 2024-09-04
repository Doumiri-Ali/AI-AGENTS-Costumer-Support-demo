# Car Rental AI Customer Support

This repository contains a car rental AI customer support system, built using LangGraph AI agents (Zero-Shot Agent) over LLaMA 3 with Groq API integration. The AI agent is applied to a Streamlit demo, where it interacts with the car rental system to provide a seamless customer experience.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [API Integration](#api-integration)
- [State Management and Error Handling](#state-management-and-error-handling)
- [License](#license)

## Project Overview

This project showcases an AI-powered customer support agent integrated into a car rental service demo. The agent is designed to handle various tasks related to car rentals, including searching for available cars, booking rentals, checking availability, and managing user information. The agent leverages **LLaMA 3 70B** model, providing powerful language understanding and generation capabilities, while interacting with the backend system through a Streamlit interface.

## Features

- **AI Customer Support**: The AI agent assists users with booking cars, checking availability, managing reservations and more ...
- **Zero-Shot Agent**: The Zero-Shot Agent operates with the simplest working implementation, relying on tools provided and prompting it to use them effectively to assist users. 
- **Groq API Integration**: The AI agent is powered by Groq API, enabling efficient processing of user queries and interactions.
- **Streamlit Demo**: A fully functional Streamlit demo where the AI agent interacts with the car rental system in real-time.

### Core Functionalities:

- **Search for Cars**: Search for cars based on various criteria such as name, type, price range, and availability within a specified date range.
- **Book a Car**: Book a car for a specified period. Bookings are initially pending confirmation and need manual confirmation by the user.
- **Retrieve Company Policies**: Retrieve company policies related to bookings, cancellations, and other services.
- **Check Car Availability**: Verify if a specific car is available for the desired dates.
- **Cancel a Booking**: Cancel an existing booking by updating its status to 'Cancelled'.
- **Update a Booking**: Modify an existing booking with new start and end dates, ensuring availability for the new dates.
- **Show Pending Bookings**: Display a list of cars that the user has booked but not yet confirmed.
- **Show Confirmed Bookings**: Display a list of cars that the user has confirmed bookings for.
- **Show Booking History**: Display the user’s last 5 bookings history (more than 5 require manual checking).
- **Show Personal Information**: Display the user’s personal information stored in the system.
- **Get Car Information**: Provide detailed information about a specific car.
- **List All Cars**: List all available cars in the inventory.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/Doumiri-Ali/AI-AGENTS-Costumer-Support-demo.git
    cd AI-AGENTS-Costumer-Support-demo
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables:
   - `GROQ_API_KEY`: Your API key for Groq.
   - Optionally, set up other API keys if using alternative LLMs:
     - `ANTHROPIC_API_KEY`
     - `TAVILY_API_KEY`

4. Start the Streamlit application:

    ```bash
    streamlit run Rental-Car-Business-Demo/pages/login.py
    ```

## Usage

After starting the Streamlit application, you can interact with the AI-powered car rental system through the user-friendly interface. The AI agent can handle various tasks:

- **Search for Cars**: Find available cars based on name, type, price range, and rental period.
- **Book a Car**: Reserve a car for a specific rental period.
- **Manage Bookings**: Update, cancel, or confirm bookings.
- **Check Availability**: Verify if a car is available for a desired rental period.
- **User Information**: View and manage personal information and booking history.
- **Policy Lookup**: Consult company policies for rental terms and conditions.

## Configuration

The application uses configuration files to manage various aspects of the system:

- `conf.py`: Contains environment variables and file paths for cars, bookings, user data, manages policy rules and vector store retrieval for policy compliance and document similarity checks.

### Key Configuration Files
- `company_rules.md`: Contains business rules and policies in Markdown format.
- `vectors.json`: Stores document vectors for efficient querying and retrieval of policy rules.

## API Integration

The AI agent interacts with external APIs to generate embeddings and process user queries:

- **Groq API**: The primary API used for language model operations.
- **Hugging Face API**: Used for generating text embeddings for document similarity checks.

### Key API Endpoints
- **LLM Operations**: Handles text generation and query processing.
- **Embedding Generation**: Generates embeddings for documents and queries for policy lookup.

## State Management and Error Handling

The system employs robust state management and error handling mechanisms:

- **State Management**: Tracks user interactions, tool usage, and assistant responses.
- **Error Handling**: Captures and manages errors during tool execution, providing feedback to the user.

### Key Components
- **State Management**: Functions to clean and update message states.
- **Error Handling**: Functions to handle tool errors and provide fallback options.


## Presentation Video

Watch the 10-minute presentation video showcasing the car rental AI customer support system:

[Watch the Presentation Video](https://drive.google.com/file/d/1P8LLI2Q6xPwy7oYWgX2q9kElnZkvzTWB/view?usp=sharing)


### **In this video, you'll see the AI agent interacting with users, including tests with intentionally poor English to demonstrate its ability to handle and understand varied language proficiency. The video includes examples of the AI responding to queries despite non-standard or less accurate English inputs, highlighting its robustness and adaptability in real-world scenarios.**
