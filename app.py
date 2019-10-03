from flask import Flask, render_template, request

app = Flask(__name__)

#Show initial search page with attributions and big search bar
@app.route('/')
def index():
    """Show Search Bar and Attributions"""
    return render_template('index.html')

@app.route('/cart')
def cart():
    """Show Cart with cart contents"""
    pass