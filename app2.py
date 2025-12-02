import streamlit as st
import pickle
import requests

# -----------------------------
# Chargement des données
# -----------------------------
movies = pickle.load(open("movies_list.pkl",'rb'))
similarity = pickle.load(open("similarity.pkl",'rb'))
movies_list = movies['title'].values

API_KEY = "8c5314238911203fd34e5fd129e04496"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    return recommend_movie, recommend_poster

# -----------------------------
# CSS et style
# -----------------------------
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://wallpaperaccess.com/full/1755935.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    h1 {
        color: #ff4b4b;
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
    h3 {
        text-align: center;
        color: #f5f5f5;
        font-family: 'Arial', sans-serif;
    }
    .stButton button {
        background-color: #ff4b4b;
        color: white;
        height: 3em;
        width: 100%;
        border-radius: 10px;
        font-size: 16px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Titre
# -----------------------------
st.markdown("<h1>🎬 Movies Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<h3>Discover movies you'll love!</h3>", unsafe_allow_html=True)
st.write("---")

# -----------------------------
# Sidebar
# -----------------------------
selected_movie = st.sidebar.selectbox("Select a movie", movies_list)
st.sidebar.markdown("### 🔎 Find your next movie!")

# -----------------------------
# Bouton et recommandations
# -----------------------------
if st.button('Show Recommendations'):
    movie_name, movie_poster = recommend(selected_movie)
   
    st.write("### Recommended Movies")
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            # Utilisation du nouveau paramètre use_container_width
            st.image(movie_poster[i], use_container_width=True)
            st.markdown(f"<h4 style='text-align: center; color: #fff;'>{movie_name[i]}</h4>", unsafe_allow_html=True)


