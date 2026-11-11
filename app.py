import streamlit as st
import pickle
import requests
import io


movies = pickle.load(open("movies.pkl", "rb"))

# Load similarity.pkl from Hugging Face
url = "https://huggingface.co/datasets/Roshankac/movie-recommender-data/resolve/main/similarity.pkl"

response = requests.get(url)
similarity = pickle.load(io.BytesIO(response.content))


def fetch_poster(movie_name):

    url = f"http://www.omdbapi.com/?t={movie_name}&apikey=f4d45ae9"

    data = requests.get(url).json()

    if data.get("Response") == "False":
        return "https://via.placeholder.com/300x450?text=No+Poster"

    return data.get("Poster")


def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:

        movie_name = movies.iloc[i[0]].title

        recommended_movies.append(movie_name)

        poster = fetch_poster(movie_name)

        recommended_posters.append(poster)

    return recommended_movies, recommended_posters


movies_list = movies["title"].values


st.title("Movie Recommender System")


selected_movie_name = st.selectbox(
    "Select a Movie",
    movies_list
)


if st.button("Recommend"):

    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])

       
