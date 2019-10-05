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

app = Flask(__name__)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
#Show initial search page with attributions and big search bar
@app.route('/', methods=['GET', 'POST'])
def index():
    """Show Search Bar and Attributions"""

    if request.method == 'GET':
        movie = request.form.get("details")
        return redirect(url_for('movie_details', movie_object=movie))



    if request.method == 'POST':
        query = request.form.get('search')
    else:
        query = 'test'


    query_string = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US',
        'query': query,
        'include_adult': 'False'
    }
    r = requests.get("https://api.themoviedb.org/3/search/multi?", query_string)
    movies = json.loads(r.content)["results"]

    #Check if movie has a title or a name remove it if it does not have either
    #Thanks to Mr. Ben Lafferty and Zurich Okoren for helping me understand lambda and filter better
    filtered_list = list(filter(lambda x: (x.get("title") or x.get("original_title" or x.get("original_name"))) and x.get("poster_path"), movies))

    #Check if movie has a title or a name remove it if it does not have either

    return render_template('index.html', movies = filtered_list)

#Route a single movie with description and images
@app.route('/movie/<movie_object>', methods=['GET'])
def movie_details(movie_object):
    """Show a single movies details"""

    return render_template('movie_details.html', movie=movie_object)

#Show shopping cart
@app.route('/cart')
def cart_index():
    """Show Cart with all cart contents""" 
    return render_template('cart.html')