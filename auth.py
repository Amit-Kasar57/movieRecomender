import csv
import os
import streamlit as st

# --- Utility Functions ---
def load_users(file='users.csv'):
    if not os.path.exists(file):
        return {}
    with open(file, mode='r') as f:
        reader = csv.DictReader(f)
        return {row['username']: row['password'] for row in reader}

def save_user(username, password, file='users.csv'):
    file_exists = os.path.exists(file)
    with open(file, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['username', 'password'])  # Write header
        writer.writerow([username, password])

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- Login/Register Toggle ---
auth_mode = st.radio("Choose Mode", ["Login", "Create Account"])

if auth_mode == "Login":
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        users = load_users()
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome back, {username}!")
        else:
            st.error("Invalid username or password.")

else:
    st.subheader("🆕 Create Account")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Create Account"):
        users = load_users()
        if new_username in users:
            st.warning("Username already exists. Try a different one.")
        else:
            save_user(new_username, new_password)
            st.success("Account created successfully! You can now log in.")
