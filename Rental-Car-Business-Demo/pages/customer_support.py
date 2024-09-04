import streamlit as st
import time
from assistant import chatloop  # Ensure the function is imported correctly

# Hide Streamlit's default header and footer
def hide_streamlit_header_footer():
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
        </style>
        """
    st.markdown(hide_st_style, unsafe_allow_html=True)

# Display existing messages
def display_existing_messages():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Add user message to session
def add_user_message_to_session(prompt):
    if prompt:
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

# Generate assistant response using the chatloop function
def generate_assistant_response(prompt):
    # Simulate a delay in the response generation
    response = chatloop(prompt)
    return response

# Streamlit app starts here
st.title("AI Customer Support")

hide_streamlit_header_footer()
display_existing_messages()

query = st.chat_input("Ask any question related to our service")

if query:
    add_user_message_to_session(query)

    # Show typing animation
    typing_animation = st.empty()
    typing_animation.markdown("""
        <style>
        .chat-bubble {
            background-color: #FCE9E9;  /* Light red background */
            padding: 12px 24px;  /* Smaller padding */
            border-radius: 16px;  /* Smaller border radius */
            border-bottom-left-radius: 2px;
            display: inline-block;
        }
        .typing {
            align-items: center;
            display: flex;
            height: 15px;  /* Adjusted height */
        }
        .typing .dot {
            animation: mercuryTypingAnimation 1.8s infinite ease-in-out;
            background-color: #F28D8D;  /* Light red color */
            border-radius: 50%;
            height: 5px;  /* Slightly smaller size */
            margin-right: 4px;
            width: 5px;  /* Slightly smaller size */
            display: inline-block;
        }
        .typing .dot:nth-child(1) {
            animation-delay: 200ms;
        }
        .typing .dot:nth-child(2) {
            animation-delay: 300ms;
        }
        .typing .dot:nth-child(3) {
            animation-delay: 400ms;
        }
        .typing .dot:last-child {
            margin-right: 0;
        }
        @keyframes mercuryTypingAnimation {
            0% {
                transform: translateY(0px);
                background-color: #F28D8D;
            }
            28% {
                transform: translateY(-5px);
                background-color: #F8B2B2;
            }
            44% {
                transform: translateY(0px);
                background-color: #FCE9E9;
            }
        }
        </style>
        <div class="chat-bubble">
            <div class="typing">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Measure the time taken to generate the response
    start_time = time.time()
    response = generate_assistant_response(query)
    end_time = time.time()

    # Clear typing animation if response is fast
    if end_time - start_time < 2:
        typing_animation.empty()

    # Show the response
    with st.chat_message("assistant"):
        st.session_state["messages"].append({"role": "assistant", "content": response})
        st.markdown(response)

    # Ensure typing animation is cleared if it was not cleared
    typing_animation.empty()
