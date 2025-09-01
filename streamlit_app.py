import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- APP TITLE AND CONFIGURATION ---
st.set_page_config(page_title="Behavior Reflections Log", layout="wide")
st.title("Behavior Reflections Log")

# --- DATA STORAGE SETUP ---
# Define the name of the CSV file where data will be stored.
CSV_FILE = 'behavior_log.csv'

# Define the columns for the DataFrame.
COLUMNS = [
    "Student Name",
    "Homeroom Teacher",
    "Location of Incident",
    "Date",
    "Number of Reflections",
    "Action Taken",
    "Notes"
]

# --- FUNCTIONS ---
def load_data():
    """Load existing data from the CSV file, or create a new DataFrame if the file doesn't exist."""
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=COLUMNS)

def save_data(df):
    """Save the DataFrame to the CSV file."""
    df.to_csv(CSV_FILE, index=False)

# --- FORM FOR DATA ENTRY ---
st.header("Log a New Incident")

# Create a form for user input.
with st.form("behavior_log_form", clear_on_submit=True):
    # Create columns for a cleaner layout.
    col1, col2 = st.columns(2)

    with col1:
        student_name = st.text_input("Student Name")
        location = st.text_input("Location of Incident")
        num_reflections = st.number_input("Number of Reflections", min_value=0, step=1)

    with col2:
        homeroom_teacher = st.text_input("Homeroom Teacher")
        incident_date = st.date_input("Date of Incident", value=datetime.today())
        action_taken = st.text_input("Action Taken")

    notes = st.text_area("Notes")

    # Create a submit button for the form.
    submitted = st.form_submit_button("Submit Reflection")

# --- DATA PROCESSING AND STORAGE ---
# When the form is submitted, add the new data to the CSV.
if submitted:
    # Load the existing data.
    df = load_data()

    # Create a new entry as a DataFrame.
    new_entry = pd.DataFrame([{
        "Student Name": student_name,
        "Homeroom Teacher": homeroom_teacher,
        "Location of Incident": location,
        "Date": incident_date.strftime("%Y-%m-%d"),
        "Number of Reflections": num_reflections,
        "Action Taken": action_taken,
        "Notes": notes
    }])

    # Concatenate the new entry with the existing data.
    df = pd.concat([df, new_entry], ignore_index=True)

    # Save the updated data.
    save_data(df)

    # Display a success message.
    st.success("Reflection logged successfully!")

# --- DISPLAY EXISTING DATA ---
st.header("Previously Logged Reflections")

# Load and display the data from the CSV file.
log_df = load_data()
if not log_df.empty:
    st.dataframe(log_df, use_container_width=True)
else:
    st.info("No reflections have been logged yet.")