import os

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request
import requests
import json
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
    print(movies)
    return render_template('index.html', movies = movies)

@app.route('/cart')
def cart():
    """Show Cart with cart contents""" 
    return render_template('cart.html')
    pass