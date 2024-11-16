from flask import Flask, render_template, send_from_directory
from flask_cors import CORS  # Import CORS
import requests
from controllers.user_controller import user_blueprint
from controllers.genre_controller import genre_blueprint
from controllers.anime_controller import anime_blueprint
from controllers.episode_controller import episode_blueprint
from controllers.slideshowimage_controller import slideshow_blueprint
from controllers.env_controller import env_bp  
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register Blueprints
app.register_blueprint(anime_blueprint, url_prefix='/anime')
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(genre_blueprint, url_prefix='/genres')
app.register_blueprint(episode_blueprint, url_prefix='/episodes')
app.register_blueprint(slideshow_blueprint, url_prefix='/slideshow')
app.register_blueprint(env_bp, url_prefix='/env')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/stream')
def stream():
    return render_template('trystream.html')

@app.route('/fetch-news')
def fetch_news():
    url = "https://www.animenewsnetwork.com/all/rss.xml"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.content, 200, {'Content-Type': 'application/xml'}
    else:
        return {"error": "Failed to fetch news"}, response.status_code

if __name__ == "__main__":
    app.run(debug=True)
