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

This project showcases an AI-powered customer support agent integrated into a car rental service demo. The agent is designed to handle various tasks related to car rentals, including searching for available cars, booking rentals, checking availability, and managing user information. The agent leverages LLaMA 3 models, providing powerful language understanding and generation capabilities, while interacting with the backend system through a Streamlit interface.

## Features

- **AI Customer Support**: The AI agent assists users with booking cars, checking availability, and managing reservations.
- **Zero-Shot Learning**: The agent uses a zero-shot learning approach, allowing it to handle diverse queries without specific training on the tasks.
- **Groq API Integration**: The AI agent is powered by Groq API, enabling efficient processing of user queries and interactions.
- **Streamlit Demo**: A fully functional Streamlit demo where the AI agent interacts with the car rental system in real-time.

### Core Functionalities:
- Car Search and Booking
- Availability Check
- Booking Management (Update, Cancel, Confirm)
- User Information Management
- Policy Lookup and Compliance

## Installation

To run this project locally, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/car-rental-ai-support.git
    cd car-rental-ai-support
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
    streamlit run app.py
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

- `conf.py`: Contains environment variables and file paths for cars, bookings, and user data.
- `conf2.py`: Manages policy rules and vector store retrieval for policy compliance and document similarity checks.

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

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
