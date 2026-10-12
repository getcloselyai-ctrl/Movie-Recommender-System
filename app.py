import pickle
import streamlit as st
import requests
import lzma

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
/* Dark cinematic background */
.stApp {
    background: linear-gradient(135deg, #0b0b12, #171528, #0b0b12);
    color: #ffffff;
}


.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


h1 {
    text-align: center;
    font-size: 42px !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    padding: 25px 10px;
    border-radius: 18px;
    background: linear-gradient(90deg, #241b42, #39245c, #211b3b);
    border: 1px solid #49366b;
    box-shadow: 0 8px 30px rgba(120, 70, 220, 0.15);
    margin-bottom: 30px;
}


.stSelectbox label {
    color: #d8ccff !important;
    font-size: 17px !important;
    font-weight: 600 !important;
}


.stSelectbox div[data-baseweb="select"] > div {
    background-color: #1c1a2b;
    border: 1px solid #554477;
    border-radius: 12px;
    color: white;
}


.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(90deg, #8b5cf6, #6d4aff);
    color: white;
    font-size: 16px;
    font-weight: 700;
    transition: 0.25s ease;
}


.stButton > button:hover {
    background: linear-gradient(90deg, #a78bfa, #8b5cf6);
    color: white;
    border: none;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.3);
}

.stText {
    color: #f0eaff;
    font-size: 15px;
    font-weight: 600;
    text-align: center;
    min-height: 45px;
    padding-top: 12px;
}


[data-testid="stImage"] img {
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    transition: transform 0.25s ease;
}


[data-testid="stImage"] img:hover {
    transform: scale(1.04);
}


[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(lzma.open('similarity.pkl.xz','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])






