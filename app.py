import streamlit as st
import json
import os
import requests

# File path for topics
TOPICS_FILE = "topics.json"
BACKEND_URL = "http://localhost:8000/query"

def load_topics():
    if os.path.exists(TOPICS_FILE):
        with open(TOPICS_FILE, "r") as f:
            data = json.load(f)
        return data.get("topics", [])
    else:
        return []

def save_topics(topics):
    with open(TOPICS_FILE, "w") as f:
        json.dump({"topics": topics}, f, indent=4)

def handle_query(selected_field, user_question):
    if user_question:
        payload = {
            "field": selected_field,
            "question": user_question
        }
        try:
            response = requests.post(BACKEND_URL, json=payload)
            # print(response.body)
            response.raise_for_status()
            answer = response.json().get("body", "No answer found.")
            st.write(f"**Answer:** {answer}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with the backend: {str(e)}")
    else:
        st.warning("Please ask a question.")

# Initialize session state variables if they don't exist
if 'submit_pressed' not in st.session_state:
    st.session_state.submit_pressed = False

# Load topics initially
topics = load_topics()

# Streamlit app layout
st.set_page_config(page_title="RAG Query Application", layout="wide")
st.title("RAG Query Application ❓❓")

# Dropdown for selecting a field
selected_field = st.selectbox("Select a field", topics)

# Text input for the user's query
user_question = st.text_input(
    f"Ask a question about {selected_field}",
    key="question_input",
    label_visibility="visible"
)

# Submit Query button
if st.button("Submit Query"):
    handle_query(selected_field, user_question)

# Section to add new fields
st.subheader("Add New Field")

new_field = st.text_input("Enter a new field name")

# Button to add the new field
if st.button("Add Field"):
    if new_field:
        topics = load_topics()
        if new_field not in topics:
            topics.append(new_field)
            save_topics(topics)
            st.success(f"Field '{new_field}' added successfully!")
            st.experimental_rerun()
        else:
            st.warning("Field already exists!")
    else:
        st.warning("Please enter a field name.")

# Display available topics
st.write("### Available Fields:")
st.write(topics)
