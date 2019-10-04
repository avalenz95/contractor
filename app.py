import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import requests
import json

load_dotenv()

app = Flask(__name__)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
#Show initial search page with attributions and big search bar
@app.route('/', methods=['GET', 'POST'])
def index():
    """Show Search Bar and Attributions"""

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

    #Thanks to Mr. Ben Lafferty and Zurich Okoren for helping me understand lambda and filter better
    filtered_list = list(filter(lambda x: (x.get("title") or x.get("original_title" or x.get("original_name"))) and x.get("poster_path"), movies))

    #Check if movie has a title or a name remove it if it does not have either
    # movies_list = filter(lambda movie: (movie.get("title", False) or movie.get("original_name", False)) and movie.get("poster_path", False), movies)
    # movies_list = list(filter(lambda x: (x.get("title", False)) or (x.get("original_name", False)) and (x.get("poster_path", False)), movies))
    print(filtered_list)
        
    return render_template('index.html', movies = filtered_list)

#Show shopping cart
@app.route('/cart')
def cart():
    """Show Cart with cart contents""" 
    return render_template('cart.html')