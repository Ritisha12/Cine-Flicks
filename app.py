#Imports
import streamlit as st
import pandas as pd
import requests
import pickle

# Load the processed data and similarity matrix
with open('movie_data.pkl','rb') as file:
    movies, cosine_sim = pickle.load(file)

#Generate reccomended movies based on users choice
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0] #extracting movie 
    sim_scores = list(enumerate(cosine_sim[idx]))  #get a similarity score
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    sim_scores = sim_scores[1:11] #get top 10 similiar movies 
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]

#Show reccomended movie posters
def fetch_poster(movie_id):
    api_key = '7b995d3c6fd91a2284b4ad8cb390c7b8'  
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
    return full_path

#Styling for background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://img.freepik.com/premium-vector/cinema-wallpaper-social-media-message-background-copy-space-text_95169-1425.jpg?semt=ais_hybrid");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: white; /* Ensures text remains visible on a busy background */
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>Cine Flicks 🎬</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #FFFFFF;'>Explore Movies You’ll Love </h3>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: #FFFFFF;'>Discover recommendations based on your favourite movies. Select a movie and let us do the rest  </h5>", unsafe_allow_html=True)

selected_movie = st.selectbox("Choose a movie:",movies['title'].values)

#Changing Button Color
st.markdown(
    """
    <style>
    .stButton button {
        background-color: #353839; /* Grey button background */
        color: white; /* Text color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

#Display Reccomended movies
if st.button('Recommend:'):
  reccommendations = get_recommendations(selected_movie)
  st.write('Top 10 Recommended Movies:')

  #create 2x5 grid layout
  for i in range(0,10,5): #loop over rows, 2 rows with 5 movies each
    cols=st.columns(5) #5 columns for each row
    for col,j in zip(cols,range(i,i+5)):
      if j<len(reccommendations):
        movie_title=reccommendations.iloc[j]['title']
        movie_id = reccommendations.iloc[j]['movie_id']
        poster_url = fetch_poster(movie_id)
        with col:
          st.image(poster_url,width =130)
          st.write(movie_title)