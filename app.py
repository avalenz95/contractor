from flask import Flask, render_template, request
import requests
import json
app = Flask(__name__)

#Show initial search page with attributions and big search bar
@app.route('/', methods=['GET'])
def index():
    """Show Search Bar and Attributions"""
    #query = request.form.get('search')

    query_string = {
        'api_key': 'c19ff401506998a56c82406befe55455',
        'language': 'en-US',
        'query': 'test',
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