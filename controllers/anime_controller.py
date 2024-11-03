from flask import request, jsonify, Blueprint
from models.anime import AnimeModel
import requests
from dotenv import load_dotenv
import os

load_dotenv()

anime_blueprint = Blueprint('anime', __name__)
anime_model = AnimeModel()

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

def upload_image_to_imgbb(image_file, name):
    """Uploads an image to ImgBB and returns the image URL."""
    url = f"https://api.imgbb.com/1/upload?key={IMGBB_API_KEY}"
    files = {'image': (name, image_file.read())}  # Renames the file before upload
    response = requests.post(url, files=files)
    response_data = response.json()
    if response_data['success']:
        return response_data['data']['url']
    else:
        raise Exception("Image upload to ImgBB failed.")

@anime_blueprint.route('/', methods=['GET'])
def get_all_anime():
    """Retrieve all anime records."""
    rows = anime_model.fetch_all_anime()
    animes = [
        {
            'anime_id': row['anime_id'],
            'title': row['title'],
            'synopsis': row['synopsis'],
            'release_date': row['release_date'],
            'status': row['status'],
            'thumbnail_url': row['thumbnail_url'],
            'banner_url': row['banner_url']
        }
        for row in rows
    ]
    return jsonify(animes)

@anime_blueprint.route('/<int:anime_id>', methods=['GET'])
def get_anime(anime_id):
    """Retrieve a specific anime record by ID."""
    anime = anime_model.fetch_anime_by_id(anime_id)
    if anime is None:
        return jsonify({'error': 'Anime not found'}), 404
    return jsonify(anime)

@anime_blueprint.route('/', methods=['POST'])
def create_anime():
    """Create a new anime record with optional thumbnail and banner uploads."""
    data = request.form
    title = data.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    synopsis = data.get('synopsis')
    release_date = data.get('release_date')
    status = data.get('status', 'ongoing')

    thumbnail_url = None
    banner_url = None

    try:
        if 'thumbnail' in request.files:
            thumbnail_file = request.files['thumbnail']
            thumbnail_url = upload_image_to_imgbb(thumbnail_file, f"{title}_thumbnail")
        
        if 'banner' in request.files:
            banner_file = request.files['banner']
            banner_url = upload_image_to_imgbb(banner_file, f"{title}_banner")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    anime_model.create_anime(title, synopsis, release_date, status, thumbnail_url, banner_url)
    return jsonify({'message': 'Anime created successfully'}), 201

@anime_blueprint.route('/<int:anime_id>', methods=['PUT'])
def update_anime(anime_id):
    """Update an existing anime record."""
    anime = anime_model.fetch_anime_by_id(anime_id)
    if anime is None:
        return jsonify({'error': 'Anime not found'}), 404

    data = request.get_json() or request.form
    title = data.get('title')
    synopsis = data.get('synopsis')
    release_date = data.get('release_date')
    status = data.get('status')
    thumbnail_url = data.get('thumbnail_url')
    banner_url = data.get('banner_url')

    anime_model.update_anime(anime_id, title, synopsis, release_date, status, thumbnail_url, banner_url)
    return jsonify({'message': 'Anime updated successfully'})

@anime_blueprint.route('/<int:anime_id>', methods=['DELETE'])
def delete_anime(anime_id):
    """Delete an anime record by ID."""
    anime = anime_model.fetch_anime_by_id(anime_id)
    if anime is None:
        return jsonify({'error': 'Anime not found'}), 404

    anime_model.delete_anime(anime_id)
    return jsonify({'message': 'Anime deleted successfully'}), 200