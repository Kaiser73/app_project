from operator import contains
import streamlit as st 
import pandas as pd
import numpy as np
from PIL import Image

top = Image.open(r"web.png")
sec = Image.open(r"rec.png")

audio_file = open(r'ES_Moonbase - Anthony Earls.mp3','rb')
audio_byte = audio_file.read()
st.audio(audio_byte, format='audio/ogg')


col1, col2, col3 = st.columns(3)
with col1:
    st.write('')
with col2:
    st.image(top)
with col3:
    st.write('')



st.header('Welcome to the biggest Platform of Movies and TV Shows in the World') 
st.header('We hope you gonna enjoy the Experience')

st.subheader('All Time Greatest Movies')
st.image(sec)

col1, col2, col3 = st.columns(3)
with col1:
    st.write('')
with col2:
    st.subheader('Movie Recommondations')
with col3:
    st.write('')


movies = pd.read_csv(r'movies.csv')
ratings = pd.read_csv(r'ratings.csv')


name = st.text_input('Please write your Name :')


my_sld_val= st.slider(f'How many Movies do you need {name}',0,20)


ranking = pd.DataFrame(ratings.groupby('movieId')['rating'].mean())
ranking['views']=pd.DataFrame(ratings.groupby('movieId')['userId'].count())
ranking = pd.merge(ranking,movies,how='left',on= 'movieId')
ranking['Year'] = ranking.title.str[-6:]
ranking['Year'] = ranking.Year.str.strip('()')
ranking = ranking[['title','views','rating','genres','Year']]
ranking = ranking.rename(columns={'title':'Titles',
'views':'Total Reviews',
'rating':'Rating',
'genres':'Genre',
'Year':'Release Year'})
ranking = ranking.loc[ranking['Total Reviews']>30]
top_rec = ranking.sort_values("Rating", ascending=False).head(my_sld_val)
top_rec.set_index('Titles', inplace=True)


st.subheader('Recommended by Ratings')
st.table(top_rec)



Genre_all = ranking.Genre
Genre_all = list(Genre_all.str.split('|'))
list_genre= ['']
for i in Genre_all:
    for j in i:
        list_genre.append(j)


genre_df = pd.DataFrame(list_genre).drop_duplicates()
Genres = list(genre_df[0])

genre = st.selectbox(f'What Movie Genre do want to watch {name}?', options=Genres)

def gen_rec(genre,my_sld_val):
    for i in ranking.Genre:
        if genre in i:
            top_genre = ranking.loc[ranking.Genre.str.contains(i),
            ['Titles','Total Reviews','Rating','Release Year']].nlargest(my_sld_val,'Total Reviews').sort_values('Rating', ascending=False)
            top_genre.set_index('Titles', inplace=True)
    return top_genre

st.subheader('Recommended by Genre')
st.table(gen_rec(genre,my_sld_val))

col1, col2, col3 = st.columns(3)
with col1:
    st.write('')
with col2:
    st.subheader(f'Have Fun {name} !!')
with col3:
    st.write('')

video_file = open(r"mj1.mp4",'rb')
video_byte = video_file.read()

col1, col2, col3 = st.columns(3)
with col1:
    st.write('')
with col2:
    st.video(video_byte)
with col3:
    st.write('')
