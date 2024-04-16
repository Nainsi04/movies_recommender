'''import pickle
import streamlit as st
import requests

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

similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    num_columns = 5
    col_list = st.columns(num_columns)

    for i in range(min(num_columns, len(recommended_movie_names))):
        with col_list[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])

'''

# if st.button('Show Recommendation'):
#     recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
#     col1, col2, col3, col4, col5 = st.beta_columns(5)
#     with col1:
#         st.text(recommended_movie_names[0])
#         st.image(recommended_movie_posters[0])
#     with col2:
#         st.text(recommended_movie_names[1])
#         st.image(recommended_movie_posters[1])
#
#     with col3:
#         st.text(recommended_movie_names[2])
#         st.image(recommended_movie_posters[2])
#     with col4:
#         st.text(recommended_movie_names[3])
#         st.image(recommended_movie_posters[3])
#     with col5:
#         st.text(recommended_movie_names[4])
#         st.image(recommended_movie_posters[4])
#

import os
import pickle
import streamlit as st
import requests

# Get the absolute path of the directory where this script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define absolute paths to the pickled files
movies_file = os.path.join(script_directory, 'movies.pkl')
similarity_file = os.path.join(script_directory, 'similarity.pkl')

print("Script Directory:", script_directory)
print("Movies File Path:", movies_file)
print("Similarity File Path:", similarity_file)

# Function to fetch movie poster using TMDb API
def fetch_poster(movie_id):
    # Replace 'YOUR_API_KEY' with your actual TMDb API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY&language=en-US"
    data = requests.get(url)
    if data.status_code == 200:
        data = data.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
    return None

# Function to recommend movies based on selected movie
def recommend(movie):
    try:
        movies_data = pickle.load(open(movies_file, 'rb'))
        similarity_data = pickle.load(open(similarity_file, 'rb'))
    except FileNotFoundError:
        st.error("Error: Pickled data files not found. Please make sure the files exist.")
        return [], []

    index = movies_data[movies_data['title'] == movie].index[0]
    distances = sorted(enumerate(similarity_data[index]), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies_data.iloc[i[0]].movie_id
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movie_posters.append(poster_url)
            recommended_movie_names.append(movies_data.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')

movie_list = []
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    num_columns = 5
    col_list = st.columns(num_columns)

    for i in range(min(num_columns, len(recommended_movie_names))):
        with col_list[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
