from flask import request, jsonify, Blueprint
from models.genre import GenreModel

# Create a Blueprint for the genre routes
genre_blueprint = Blueprint('genre', __name__)
# Initialize the GenreModel which handles database operations
genre_model = GenreModel()

@genre_blueprint.route('/', methods=['GET'])
def get_all_genres():
    """
    Retrieve all genres.
    
    This route fetches all genre records from the database and returns them in a JSON format.
    
    Returns:
    JSON: List of all genres.
    """
    # Fetch all genres from the database using the GenreModel
    genres = genre_model.fetch_all_genres()
    # Return the genres in JSON format with a 200 status code
    return jsonify(genres), 200

@genre_blueprint.route('/<int:genre_id>', methods=['GET'])
def get_genre(genre_id):
    """
    Retrieve a specific genre by ID.
    
    This route fetches a genre record by its ID from the database and returns it in a JSON format.
    
    Args:
    genre_id (int): The ID of the genre to fetch.
    
    Returns:
    JSON: The specific genre or an error message if not found.
    """
    # Fetch a specific genre by its ID
    genre = genre_model.fetch_genre_by_id(genre_id)
    if genre is None:
        # If the genre is not found, return an error with 404 status
        return jsonify({'error': 'Genre not found'}), 404
    # Return the genre in JSON format with a 200 status code
    return jsonify(genre), 200

@genre_blueprint.route('/', methods=['POST'])
def create_genre():
    """
    Create a new genre.
    
    This route creates a new genre record in the database using the provided genre name.
    
    Returns:
    JSON: A success message if the genre was created or an error message.
    """
    # Get the JSON data from the request body
    data = request.get_json()
    name = data.get('name')

    # Check if the genre name is provided
    if not name:
        # If not, return an error with 400 status
        return jsonify({'error': 'Genre name is required'}), 400

    try:
        # Attempt to create the genre in the database
        genre_model.create_genre(name)
        # Return a success message with a 201 status (Created)
        return jsonify({'message': 'Genre created successfully'}), 201
    except Exception as e:
        # If an error occurs, return an error message with a 500 status (Internal Server Error)
        return jsonify({'error': str(e)}), 500

@genre_blueprint.route('/<int:genre_id>', methods=['PUT'])
def update_genre(genre_id):
    """
    Update an existing genre.
    
    This route updates a genre's name based on the genre ID.
    
    Args:
    genre_id (int): The ID of the genre to update.
    
    Returns:
    JSON: A success message if the genre was updated, or an error message.
    """
    # Fetch the genre by its ID
    genre = genre_model.fetch_genre_by_id(genre_id)
    if genre is None:
        # If the genre is not found, return an error with 404 status
        return jsonify({'error': 'Genre not found'}), 404

    # Get the updated data from the request body
    data = request.get_json()
    name = data.get('name')
    
    # Check if the genre name is provided
    if not name:
        # If not, return an error with 400 status
        return jsonify({'error': 'Genre name is required'}), 400

    try:
        # Attempt to update the genre in the database
        genre_model.update_genre(genre_id, name)
        # Return a success message with a 200 status (OK)
        return jsonify({'message': 'Genre updated successfully'}), 200
    except Exception as e:
        # If an error occurs, return an error message with a 500 status (Internal Server Error)
        return jsonify({'error': str(e)}), 500

@genre_blueprint.route('/<int:genre_id>', methods=['DELETE'])
def delete_genre(genre_id):
    """
    Delete a genre by ID.
    
    This route deletes a genre record from the database by its ID.
    
    Args:
    genre_id (int): The ID of the genre to delete.
    
    Returns:
    JSON: A success message if the genre was deleted, or an error message.
    """
    # Fetch the genre by its ID
    genre = genre_model.fetch_genre_by_id(genre_id)
    if genre is None:
        # If the genre is not found, return an error with 404 status
        return jsonify({'error': 'Genre not found'}), 404

    try:
        # Attempt to delete the genre from the database
        genre_model.delete_genre(genre_id)
        # Return a success message with a 200 status (OK)
        return jsonify({'message': 'Genre deleted successfully'}), 200
    except Exception as e:
        # If an error occurs, return an error message with a 500 status (Internal Server Error)
        return jsonify({'error': str(e)}), 500
