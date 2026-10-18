import os
import streamlit as st # type: ignore
from openai import OpenAI, OpenAIError # type: ignore


# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="💬",
    layout="centered"
)

st.title("💬 AI Chatbot")
st.caption("A simple chatbot built with Streamlit and OpenAI")


# -------------------------------
# Load API key securely
# -------------------------------
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error(
        "OpenAI API key not found. "
        "Add it to .streamlit/secrets.toml."
    )
    st.stop()


client = OpenAI(api_key=api_key)

# Change the model here if needed.
MODEL = "gpt-6-luna"


# -------------------------------
# Initialize chat history
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------------------
# Display previous messages
# -------------------------------
for chat in st.session_state.messages:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])


# -------------------------------
# Get new user message
# -------------------------------
prompt = st.chat_input("Write your message here...")

if prompt:
    # Display the user's message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare conversation history for the API
    conversation = st.session_state.messages + [
        {"role": "user", "content": prompt}
    ]

    # Generate the assistant's response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.responses.create(
                    model=MODEL,
                    input=conversation,
                    max_output_tokens=1024
                )

                answer = response.output_text.strip()

                if not answer:
                    answer = "Sorry, I couldn't generate a text response."

            except OpenAIError as error:
                st.error(
                    "The API request failed. Check your API key, "
                    "API billing/quota, model access, and internet connection."
                )

                with st.expander("Error details"):
                    st.code(str(error))

            else:
                st.markdown(answer)

                # Save both messages only after a successful response
                st.session_state.messages.append(
                    {"role": "user", "content": prompt}
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )