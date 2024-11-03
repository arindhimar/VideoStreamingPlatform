from flask import Blueprint, jsonify
import os

env_bp = Blueprint('env', __name__)

@env_bp.route('/api/config/imgbb', methods=['GET'])
def get_imgbb_key():
    imgbb_api_key = os.getenv("IMGBB_API_KEY")
    return jsonify({"imgbb_api_key": imgbb_api_key})

@env_bp.route('/api/config/anime_quote', methods=['GET'])
def get_anime_quote_key():
    anime_quote_key = os.getenv("ANIME_QUOTE_KEY")
    return jsonify({"anime_quote_key": anime_quote_key})
