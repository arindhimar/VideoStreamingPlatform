from flask import Blueprint, request, jsonify, send_from_directory
import os
import uuid
import subprocess
from models.episode import EpisodeModel
from concurrent.futures import ThreadPoolExecutor
import shutil

episode_blueprint = Blueprint('episode', __name__)
episode_model = EpisodeModel()
executor = ThreadPoolExecutor(max_workers=5)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def is_video_file(filename):
    return filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))

def process_video_task(video_path, output_path, anime_id, title, episode_number):
    hls_path = os.path.join(output_path, "index.m3u8")
    ffmpeg_command = [
        "ffmpeg", "-i", video_path, "-codec:v", "libx264", "-codec:a", "aac",
        "-hls_time", "10", "-hls_playlist_type", "vod",
        "-hls_segment_filename", os.path.join(output_path, "segment%03d.ts"),
        "-start_number", "0", hls_path
    ]

    try:
        subprocess.run(ffmpeg_command, check=True)
        ts_url_prefix = f"/stream/{anime_id}/{episode_number}/segment"
        
        # Call update_episode_status with both anime_id and episode_number
        episode_model.update_episode_status(anime_id, episode_number, 'ready', hls_path, ts_url_prefix)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error in FFmpeg process: {e}")
        cleanup_after_failure(video_path, output_path, episode_number)
        return False


def cleanup_after_failure(video_path, output_path, episode_number):
    # Remove uploaded video file
    if os.path.exists(video_path):
        os.remove(video_path)

    # Remove output directory
    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    # Remove database entry
    episode_model.delete_episode(episode_number)
    
    
@episode_blueprint.route('anime/<int:anime_id>', methods=['GET'])
def get_episodes_by_anime(anime_id):
    """Retrieve all episodes for a specific anime by its ID."""
    episodes = episode_model.fetch_episodes_by_anime_id(anime_id)
    return jsonify(episodes)

@episode_blueprint.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if not is_video_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    anime_id = request.form.get('anime_id')
    title = request.form.get('title')
    episode_number = request.form.get('episode_number')

    episode_id = str(uuid.uuid4())
    output_path = os.path.join(UPLOAD_FOLDER, episode_id)
    video_path = os.path.join(output_path, file.filename)
    os.makedirs(output_path, exist_ok=True)
    file.save(video_path)

    try:
        # Create an entry with status 'processing' (single entry)
        episode_model.create_episode(anime_id, title, episode_number, "", "processing")

        # Process video in background and update status once ready
        executor.submit(process_video_task, video_path, output_path, anime_id, title, episode_number)

        return jsonify({"message": "Video upload successful, processing in background"})

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "Failed to upload video, please try again."}), 500
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if not is_video_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    # Fetch anime_id, title, and episode_number from the request
    anime_id = request.form.get('anime_id')  
    title = request.form.get('title')  
    episode_number = request.form.get('episode_number')  

    episode_id = str(uuid.uuid4())
    output_path = os.path.join(UPLOAD_FOLDER, episode_id)
    video_path = os.path.join(output_path, file.filename)
    os.makedirs(output_path, exist_ok=True)
    file.save(video_path)

    # Start a transaction for database operations
    try:
        # Create an entry in the database with initial status as 'processing'
        episode_model.create_episode(anime_id, title, episode_number, "", "")  # Initial status

        # Submit the video processing task
        executor.submit(process_video_task, video_path, output_path, anime_id, title, episode_number)

        video_url = f"/stream/{episode_id}/index.m3u8"
        return jsonify({"message": "Video upload successful, processing in background", "videoUrl": video_url})

    except Exception as e:
        # Handle rollback if there was an error before video processing
        print(f"Error occurred: {e}")
        return jsonify({"error": "Failed to upload video, please try again."}), 500

@episode_blueprint.route('/stream/<int:anime_id>/<int:episode_number>/index.m3u8')
def stream_video(anime_id, episode_number):
    # Fetch the episode details from the database
    episode = episode_model.get_episode(anime_id, episode_number)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    output_path = os.path.join(UPLOAD_FOLDER, str(episode['episode_id']))  # Adjust based on how you store episode_id
    return send_from_directory(output_path, 'index.m3u8')

@episode_blueprint.route('/stream/<int:anime_id>/<int:episode_number>/segment<path:filename>')
def stream_segment(anime_id, episode_number, filename):
    # Fetch the episode details from the database
    episode = episode_model.get_episode(anime_id, episode_number)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    output_path = os.path.join(UPLOAD_FOLDER, str(episode['episode_id']))  # Adjust based on how you store episode_id
    return send_from_directory(output_path, filename)
