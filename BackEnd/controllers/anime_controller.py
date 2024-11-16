from flask import request, jsonify, Blueprint
from models.anime import AnimeModel
import requests
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Create a blueprint for anime-related routes
anime_blueprint = Blueprint('anime', __name__)
anime_model = AnimeModel()  # Create an instance of AnimeModel

# Get the ImgBB API key from environment variables
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

def upload_image_to_imgbb(image_file, name):
    """
    Uploads an image to ImgBB and returns the image URL.
    
    Args:
    image_file: The image file to upload.
    name: The name to use for the uploaded file.
    
    Returns:
    str: The URL of the uploaded image on ImgBB.
    
    Raises:
    Exception: If the upload fails.
    """
    url = f"https://api.imgbb.com/1/upload?key={IMGBB_API_KEY}"
    files = {'image': (name, image_file.read())}  # Rename the file before upload
    response = requests.post(url, files=files)
    response_data = response.json()
    if response_data['success']:
        return response_data['data']['url']
    else:
        raise Exception("Image upload to ImgBB failed.")

@anime_blueprint.route('/', methods=['GET'])
def get_all_anime():
    """
    Retrieve all anime records from the database.
    
    Returns:
    JSON: A list of all anime with relevant details (ID, title, synopsis, etc.)
    """
    rows = anime_model.fetch_all_anime()  # Fetch all anime from the database
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
        for row in rows  # Process each row of the result and convert it into a dictionary
    ]
    return jsonify(animes)

@anime_blueprint.route('/<int:anime_id>', methods=['GET'])
def get_anime(anime_id):
    """
    Retrieve a specific anime record by ID.
    
    Args:
    anime_id: The ID of the anime to retrieve.
    
    Returns:
    JSON: The details of the specific anime or an error message if not found.
    """
    anime = anime_model.fetch_anime_by_id(anime_id)
    if anime is None:
        return jsonify({'error': 'Anime not found'}), 404
    return jsonify(anime)

@anime_blueprint.route('/', methods=['POST'])
def create_anime():
    """
    Create a new anime record with optional thumbnail and banner uploads.
    
    Returns:
    JSON: A success message or error details.
    """
    data = request.form  # Get form data from the request
    title = data.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    synopsis = data.get('synopsis')
    release_date = data.get('release_date')
    status = data.get('status', 'ongoing')  # Default status is "ongoing"

    # Initialize URLs for thumbnail and banner
    thumbnail_url = None
    banner_url = None

    try:
        # If a thumbnail is provided, upload it to ImgBB and get the URL
        if 'thumbnail' in request.files:
            thumbnail_file = request.files['thumbnail']
            thumbnail_url = upload_image_to_imgbb(thumbnail_file, f"{title}_thumbnail")
        
        # If a banner is provided, upload it to ImgBB and get the URL
        if 'banner' in request.files:
            banner_file = request.files['banner']
            banner_url = upload_image_to_imgbb(banner_file, f"{title}_banner")
    except Exception as e:
        # Handle any error during image upload
        return jsonify({'error': str(e)}), 500

    # Create a new anime record in the database
    anime_model.create_anime(title, synopsis, release_date, status, thumbnail_url, banner_url)
    return jsonify({'message': 'Anime created successfully'}), 201

@anime_blueprint.route('/<int:anime_id>', methods=['PUT'])
def update_anime(anime_id):
    """
    Update an existing anime record.
    
    Args:
    anime_id: The ID of the anime to update.
    
    Returns:
    JSON: A success message or error details.
    """
    # Fetch the existing anime record
    anime = anime_model.fetch_anime_by_id(anime_id)
    if anime is None:
        return jsonify({'error': 'Anime not found'}), 404

    data = request.get_json() or request.form  # Get JSON or form data from the request
    title = data.get('title')
    synopsis = data.get('synopsis')
    release_date = data.get('release_date')
    status = data.get('status')
    thumbnail_url = data.get('thumbnail_url')
    banner_url = data.get('banner_url')

    # Update the anime record in the database
    anime_model.update_anime(anime_id, title, synopsis, release_date, status, thumbnail_url, banner_url)
    return jsonify({'message': 'Anime updated successfully'})

@anime_blueprint.route('/<int:anime_id>', methods=['DELETE'])
def delete_anime(anime_id):
    """
    Delete an anime record by ID.
    
    Args:
    anime_id: The ID of the anime to delete.
    
    Returns:
    JSON: A success message or error details.
    """
    # Fetch the anime record to ensure it exists
    anime = anime_model.fetch_anime_by_id(anime_id)
    if anime is None:
        return jsonify({'error': 'Anime not found'}), 404

    # Delete the anime record from the database
    anime_model.delete_anime(anime_id)
    return jsonify({'message': 'Anime deleted successfully'}), 200
