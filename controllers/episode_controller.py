from flask import request, jsonify, Blueprint
from models.episode import EpisodeModel

episode_blueprint = Blueprint('episode', __name__)
episode_model = EpisodeModel()

@episode_blueprint.route('/episodes', methods=['POST'])
def create_episode():
    data = request.get_json()
    anime_id = data.get('anime_id')
    title = data.get('title')
    episode_number = data.get('episode_number')
    video_url = data.get('video_url')
    
    if not all([anime_id, title, episode_number, video_url]):
        return jsonify({'error': 'Missing required fields'}), 400

    episode_model.create_episode(anime_id, title, episode_number, video_url)
    return jsonify({'message': 'Episode created successfully'}), 201
