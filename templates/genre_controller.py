from flask import request, jsonify, Blueprint
from models.genre import GenreModel

genre_blueprint = Blueprint('genre', __name__)
genre_model = GenreModel()

@genre_blueprint.route('/', methods=['GET'])
def get_all_genres():
    """Retrieve all genres."""
    genres = genre_model.fetch_all_genres()
    return jsonify(genres), 200

@genre_blueprint.route('/genres/<int:genre_id>', methods=['GET'])
def get_genre(genre_id):
    """Retrieve a specific genre by ID."""
    genre = genre_model.fetch_genre_by_id(genre_id)
    if genre is None:
        return jsonify({'error': 'Genre not found'}), 404
    return jsonify(genre), 200

@genre_blueprint.route('/', methods=['POST'])
def create_genre():
    """Create a new genre."""
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Genre name is required'}), 400

    try:
        genre_model.create_genre(name)
        return jsonify({'message': 'Genre created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500



