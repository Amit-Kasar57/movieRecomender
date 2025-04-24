import pickle
import pandas as pd
import streamlit as st

# --- Page Config ---
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

# --- Session State for Login ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Login Page ---
if not st.session_state.logged_in:
    st.markdown("<div class='title'>🔐 Login to Continue</div>", unsafe_allow_html=True)
    with st.form("login_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
        with col2:
            last_name = st.text_input("Last Name")

        mobile = st.text_input("Mobile Number")
        password = st.text_input("Password", type="password")

        login_btn = st.form_submit_button("Login")

        if login_btn:
            if all([first_name, last_name, mobile, password]):
                st.success(f"Welcome, {first_name} 👋")
                st.session_state.logged_in = True
            else:
                st.warning("Please fill in all fields to login.")

# --- Main App ---
if st.session_state.logged_in:
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
    st.write("Pick a movie you like and get 5 similar recommendations!")

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
