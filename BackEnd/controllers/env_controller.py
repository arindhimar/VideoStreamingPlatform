from flask import Blueprint, jsonify
import os

# Create a new Blueprint for the environment-related routes
env_bp = Blueprint('env', __name__)

@env_bp.route('/api/config/imgbb', methods=['GET'])
def get_imgbb_key():
    """
    Retrieve the ImgBB API key from environment variables.
    
    This route returns the ImgBB API key in a JSON response.
    
    Returns:
    JSON: Contains the ImgBB API key.
    """
    # Fetch the ImgBB API key from environment variables
    imgbb_api_key = os.getenv("IMGBB_API_KEY")
    # Return the key as a JSON response
    return jsonify({"imgbb_api_key": imgbb_api_key})

@env_bp.route('/api/config/anime_quote', methods=['GET'])
def get_anime_quote_key():
    """
    Retrieve the Anime Quote API key from environment variables.
    
    This route returns the Anime Quote API key in a JSON response.
    
    Returns:
    JSON: Contains the Anime Quote API key.
    """
    # Fetch the Anime Quote API key from environment variables
    anime_quote_key = os.getenv("ANIME_QUOTE_KEY")
    # Return the key as a JSON response
    return jsonify({"anime_quote_key": anime_quote_key})
