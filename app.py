import csv
import os
import pickle
import pandas as pd
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

# --- Session State for Login ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- Page Config (must be at the very top) ---
st.set_page_config(page_title="Movie Recommender", layout="centered")

# --- Custom Style ---
st.markdown("""
    <style>
    body {
        background-color: #f9f9f9;
    }
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #1f77b4;
    }
    .movie {
        font-size: 20px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Login/Register Toggle ---
if not st.session_state.logged_in:
    auth_mode = st.radio("Choose Mode", ["Login", "Create Account"])

    if auth_mode == "Login":
        # --- Login Page ---
        st.markdown("<div class='title'>🔐 Login to Continue</div>", unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            users = load_users()  # Load users from the CSV
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome back, {username}!")
            else:
                st.error("Invalid username or password.")

    else:
        # --- Create Account Page ---
        st.markdown("<div class='title'>🆕 Create Account</div>", unsafe_allow_html=True)
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")

        if st.button("Create Account"):
            users = load_users()  # Load users from the CSV
            if new_username in users:
                st.warning("Username already exists. Try a different one.")
            else:
                save_user(new_username, new_password)  # Save new user to CSV
                st.success("Account created successfully! You can now log in.")
else:
    # --- Proceed if logged in ---
    # --- Load Data ---
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)

    # --- Recommend Function ---
    def recommend(movie):
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        return [movies.iloc[i[0]].title for i in movie_list]

    # --- UI Starts ---
    st.markdown("<div class='title'>🎥 Movie Recommender System</div>", unsafe_allow_html=True)
    st.write(f"Welcome, **{st.session_state.username}**! Pick a movie you like and get 5 similar recommendations.")

    # --- Movie Dropdown ---
    selected_movie = st.selectbox("Select a movie", movies['title'].values)

    # --- Recommend Button ---
    if st.button("✨ Recommend"):
        recommended = recommend(selected_movie)
        st.subheader("📽️ Recommended Movies & Trailers:")
        for movie in recommended:
            st.markdown(f"<div class='movie'>🎬 {movie}</div>", unsafe_allow_html=True)
            yt_link = f"https://www.youtube.com/results?search_query={movie.replace(' ', '+')}+trailer"
            st.markdown(f"[▶️ Watch Trailer on YouTube]({yt_link})", unsafe_allow_html=True)

    # --- Divider ---
    st.markdown("---")

    # --- Custom YouTube Search ---
    st.subheader("🔎 Want to search your favourite movie?")
    custom_movie = st.text_input("Enter movie name")
    if custom_movie:
        search_url = f"https://www.youtube.com/results?search_query={custom_movie.replace(' ', '+')}+trailer"
        st.markdown(f"[🔍 Search YouTube for Trailer]({search_url})", unsafe_allow_html=True)
