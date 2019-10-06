import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
import requests
import json
from pymongo import MongoClient

load_dotenv()

#Client
client = MongoClient()
#Database associated with Client
db = client.MovieDB
#Collections associated with Database
cart_list = db.cart_list
wish_list = db.wish_list
current_index = db.current_index
current_index.drop()

app = Flask(__name__)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

#Show initial search page with attributions and big search bar
@app.route('/', methods=['GET', 'POST'])
def index():
    """Show Search Bar and Attributions"""

    #Page has just refreshed
    if request.method == 'GET':
        query = 'test'
    else:
        query = request.form.get('search')
    
    print(f"CURRENT COUNT 1 : {current_index.count()}")

    query_string = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US',
        'query': query,
        'include_adult': 'False'
    }

    r = requests.get("https://api.themoviedb.org/3/search/multi?", query_string)
    movies = json.loads(r.content)["results"]

    #Drop the collection if new post request
    if request.method == 'POST':
        current_index.drop()

    #Thanks to Mr. Ben Lafferty and Zurich Okoren for helping me understand lambda and filter better
    filtered_list = list(filter(lambda x: (x.get("title") or x.get("original_title" or x.get("original_name"))) and x.get("poster_path"), movies))

    #Add current index of movies to a collection
    current_index.insert_many(filtered_list)

    print(f"CURRENT COUNT 2 : {current_index.count()}")


    #Display all movies in current_index
    movies = [movie for movie in current_index.find()]

    return render_template('index.html', movies = movies)

#Route a single movie with description and images
@app.route('/movie/<movie_id>', methods=['POST'])
def movie_details(movie_id):
    """Show a single movies details"""
    
    return render_template('movie_details.html')
#Show shopping cart
@app.route('/cart')
def cart_index():
    """Show Cart with all cart contents""" 
    return render_template('cart.html')