import numpy as np
import pandas as pd
# from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import bs4 as bs

import requests
from PIL import Image

import streamlit as st
my_api_key ="4ed2377b21fae18ab4132a5cef98a519"
st.set_page_config(layout ='wide')
page_bg_img = '''
<style>
body {
background-image: "image.jpg";
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

# load the nlp model and tfidf vectorizer from disk

# vectorizer = pickle.load(open('tranform.pkl','rb'))

def create_similarity():
    data = pd.read_csv('main_data.csv')
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    # creating a similarity score matrix
    similarity = cosine_similarity(count_matrix)
    return data,similarity

def rcmd(m):
    m = m.lower()
    try:
        data.head()
        similarity.shape
    except:
        data, similarity = create_similarity()
    if m not in data['movie_title'].unique():
        return('Sorry! try another movie name')
    else:
        i = data.loc[data['movie_title']==m].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
        lst = lst[1:11] # excluding first item since it is the requested movie itself
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['movie_title'][a])
        return l
# converting list of string to list (eg. "["abc","def"]" to ["abc","def"])

def convert_to_list(my_list):
    my_list = my_list.split('","')
    my_list[0] = my_list[0].replace('["','')
    my_list[-1] = my_list[-1].replace('"]','')
    return my_list

def get_suggestions():
    data = pd.read_csv('main_data.csv')
    return list(data['movie_title'].str.capitalize())



def printDetails(details):
    path = 'https://image.tmdb.org/t/p/original'+details['poster_path']
    # st.write(path)
    # image = Image.open(requests.get(path, stream=True).raw)
    # st.image(image,width=200)
    markdown = f"""


                  
                <img src="{path}" alt="{details['original_title']}" style="display: block; margin: 0 auto; width: 25%;" />
                  
                

                <div style=" color: #0DF1C5 ;font-weight:700;font-weight:700;font-size: 30px;text-align: center;">
                        Movies Name: {details['original_title']}
                </div>
                <div style=" color: #0DF1C5 ;font-weight:700;font-weight:700;font-size: 30px;text-align: center;">
                        Rating : {details['rating']}
                </div>
                <div style=" color: #0DF1C5 ;font-weight:700;font-weight:700;font-size: 30px;text-align: center;">
                       Release Date : {details['release_date']}

                </div>


                <div style=" color: #0DF1C5 ;font-weight:700;font-weight:700;font-size: 30px;text-align: center;">
                       Overview : 
                       <p style=" color: #FF9898">{details['overview']}</p>

                </div>

                <br>

                <div style=" color: #F1150D ;font-weight:700;font-weight:700;font-size: 50px;text-align: center;">
                            Cast

                </div>
               

    """

    st.markdown(markdown,unsafe_allow_html=True)
    poster,name = details['cast'][0],details['cast'][1] 

    # cast_id = details['cast'][2] 
    printImageCast(poster,name)  
    
def printImageCast(poster_path,name):

    # st.markdown("### About cast")
    idx =  0
    col = st.columns(4)
    for i in range(len(name)//2):
        path = 'https://image.tmdb.org/t/p/original'+poster_path[i]
        image = Image.open(requests.get(path, stream=True).raw)
        col[i].image(image,width=200, caption=name[i])

    col = st.columns(4)
    for i in range(len(name)//2,len(name)):
        # st.write(i)
        path = 'https://image.tmdb.org/t/p/original'+poster_path[i]
        image = Image.open(requests.get(path, stream=True).raw)

        # li = f"https://en.wikipedia.org/wiki/{name[i].replace(' ','_')}"
        # caption = st.markdown(f"[{name[i]}]({li})")
        # st.markdown(caption)
        
        col[idx].image(image,width=200, caption=name[i])
        idx +=1 
    



def get_movie_cast(movie_id):
    url = "https://api.themoviedb.org/3/movie/"+str(movie_id)+"/credits?api_key="+my_api_key
    cast_details = json.loads(requests.get(url).text)
    length = len(cast_details['cast'])
    if length >8:
        length = 8
    poster_path = []
    name = []
    cast_id = []
    for i in range(length):
        # st.write(cast_details['cast'][0])
        poster_path.append(cast_details['cast'][i]['profile_path'])
        name.append(cast_details['cast'][i]['name'])
        cast_id.append(cast_details['cast'][i]['id'])
    return [poster_path,name,cast_id]




def get_details_movie(title,w):
    
    url='https://api.themoviedb.org/3/search/movie?api_key='+my_api_key+'&query='+title

    details = json.loads(requests.get(url).text)
    # st.write(url)
    storeDetails = {}

    storeDetails['original_title'] = details['results'][0]['title']
    storeDetails['overview'] = details['results'][0]['overview']
    storeDetails['release_date'] = details['results'][0]['release_date']
    storeDetails['rating'] = details['results'][0]['vote_average']
    storeDetails['poster_path'] = details['results'][0]['poster_path']
    storeDetails['movie_id'] = details['results'][0]['id']

    if w == True:
        cast = get_movie_cast(storeDetails['movie_id'])
        storeDetails['cast'] = cast
    # st.write(f"{storeDetails}")
    return storeDetails

def displayMovieImage(poster_path,name):

    col = st.columns(5)
    for i in range(5):
        path = 'https://image.tmdb.org/t/p/original'+poster_path[i]
        image = Image.open(requests.get(path, stream=True).raw)
        col[i].image(image,width=200, caption=name[i])
    idx =0
    col = st.columns(5)
    for i in range(5,10):
        path = 'https://image.tmdb.org/t/p/original'+poster_path[i]
        image = Image.open(requests.get(path, stream=True).raw)
        col[idx].image(image,width=200, caption=name[i])
        idx +=1

    

def recommerder_movie_details(movie_list):

    # movie_list = []
    poster_path = []
    name = []
    i = 0
    for movie in movie_list:
        movie = movie.capitalize()
        detail = get_details_movie(movie,False)
        # st.write(detail)
    # for i in range(len(detail)):
        poster_path.append(detail['poster_path'])
        name.append(detail['original_title'])
        i +=1
    # st.write([poster_path,name])

    mark =  """
                <style>
                .green {
                    color: green;
                    font-weight:700;
                    font-size: 30px;
                    text-align: center;
                }
                </style>

                <div class="green">
                    Recommendation Movies
                    <br>
                </div>
            """
    st.markdown(mark,unsafe_allow_html=True)

    displayMovieImage(poster_path,name)






def main():
    st.header('Movie Recommender')
    suggestions = get_suggestions()
    movie_name = st.selectbox("Enter a movie name",suggestions)
    
    # st.write(suggestions)
    if st.button("Get Recommend"):
        
        # st.write(rc)
        movie_details = get_details_movie(movie_name,True)
        printDetails(movie_details)
        rc = rcmd(movie_name)

        recommerder_movie_details(rc)

if __name__ == '__main__':
    main()