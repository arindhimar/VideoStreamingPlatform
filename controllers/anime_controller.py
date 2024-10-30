from flask import request, jsonify, Blueprint
from models.anime import AnimeModel

anime_blueprint = Blueprint('anime', __name__)
anime_model = AnimeModel()

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
    """Create a new anime record."""
    data = request.get_json() or request.form
    if 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    synopsis = data.get('synopsis')
    release_date = data.get('release_date')
    status = data.get('status', 'ongoing')
    thumbnail_url = data.get('thumbnail_url')
    banner_url = data.get('banner_url')

    anime_model.create_anime(data['title'], synopsis, release_date, status, thumbnail_url, banner_url)
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
