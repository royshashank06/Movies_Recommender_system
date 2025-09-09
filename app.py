import streamlit as st
import pandas as pd
import pickle

import streamlit as st
import pandas as pd
import pickle


import streamlit as st
import pandas as pd
import pickle
import requests



st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# -----------------------------
# Custom CSS for styling
# -----------------------------
st.markdown("""
<style>
/* Page font */
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

/* App title */
.app-title {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 16px;
}

/* Card for movie details */
.movie-card {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 12px;
    text-align: center;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
}

/* Poster image */
.poster-img {
    border-radius: 10px;
    width: 100%;
    height: auto;
}

/* Movie name under poster */
.movie-name {
    font-size: 14px;
    font-weight: 600;
    margin-top: 6px;
}

/* Tags/overview box */
.movie-tags {
    font-size: 12px;
    color: #555555;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load DataFrame and similarity matrix
# -----------------------------
movies_list = pickle.load(open('movie_list.pkl', 'rb'))   # DataFrame
similarity = pickle.load(open('similarity.pkl', 'rb'))    # Similarity matrix

# Ensure DataFrame is valid
if not isinstance(movies_list, pd.DataFrame):
    movies_list = pd.DataFrame(movies_list)

movies_list['title'] = movies_list['title'].astype(str)

# Extract movie titles for selectbox
titles = movies_list['title'].values

# -----------------------------
# Function to fetch poster from TMDb
# -----------------------------
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=490695e5678b03943fc39f0bd4b16b3a&language=en-US"
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path', None)
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"

# -----------------------------
# Recommendation function
# -----------------------------
def recommend(movie):
    recommended_movies = []
    recommended_movies_poster = []

    index = movies_list[movies_list['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),
                       reverse=True, key=lambda x: x[1])

    for i in distances[1:6]:
        movie_id = movies_list.iloc[i[0]]['movie_id']   # fetch TMDb id
        recommended_movies.append(movies_list.iloc[i[0]]['title'])
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster

# -----------------------------
# App UI
# -----------------------------
st.markdown('<div class="app-title">🎬 Movies Recommender System</div>', unsafe_allow_html=True)

selected_movie = st.selectbox("Choose a movie:", titles)

if st.button("Recommend"):
    st.write("You selected:", selected_movie)

    # Movie details if available
    if 'tags' in movies_list.columns:
        movie_row = movies_list[movies_list['title'] == selected_movie].iloc[0]
        st.markdown('<div class="movie-tags">' + movie_row.get('tags', 'No additional details.') + '</div>', unsafe_allow_html=True)

    # Get recommendations
    names, posters = recommend(selected_movie)

    st.subheader("Recommended Movies")

    # Display recommended movies with posters in cards
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
            st.image(posters[idx], use_column_width=True, output_format="auto")
            st.markdown(f'<div class="movie-name">{names[idx]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)