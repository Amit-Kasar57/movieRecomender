import pickle
import pandas as pd
import streamlit as st
import auth  # Importing the authentication script

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

# --- Proceed if logged in ---
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
