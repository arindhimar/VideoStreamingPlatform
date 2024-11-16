from flask import Blueprint, request, jsonify, send_from_directory, Response
import os
import uuid
import subprocess
from models.episode import EpisodeModel
from concurrent.futures import ThreadPoolExecutor
import shutil
import urllib.parse

# Blueprint setup for episode-related routes
episode_blueprint = Blueprint('episode', __name__)
episode_model = EpisodeModel()  # Instance to interact with the Episode model
executor = ThreadPoolExecutor(max_workers=5)  # To handle video processing tasks concurrently

# Directory where uploaded video files will be stored
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def is_video_file(filename):
    """
    Checks if the uploaded file is a valid video file based on its extension.
    Returns True if it's a valid video, False otherwise.
    """
    return filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))

def process_video_task(video_path, output_path, anime_id, title, episode_number):
    """
    Processes the uploaded video file to generate HLS (HTTP Live Streaming) compatible segments.
    
    Args:
    video_path (str): Path to the uploaded video file.
    output_path (str): Directory where the output HLS segments will be stored.
    anime_id (int): ID of the anime the episode belongs to.
    title (str): Title of the episode.
    episode_number (int): Episode number for the anime.

    This function runs the ffmpeg command to encode the video, generate HLS playlists, 
    and store the segments. It updates the episode's status in the database upon completion.
    """
    # Define the HLS output path with unique audio variant
    hls_path = os.path.join(output_path, "index_%v.m3u8")

    # ffmpeg command to process video, map video/audio streams, encode, and generate HLS segments
    ffmpeg_command = [
        "ffmpeg", "-i", video_path,

        # Map video and audio streams
        "-map", "0:v:0", "-map", "0:a:0", "-map", "0:v:0", "-map", "0:a:1",

        # Force 8-bit encoding (to resolve 10-bit encode issues)
        "-pix_fmt", "yuv420p",

        # Video encoding settings
        "-codec:v", "h264_nvenc", "-preset", "slow", "-b:v", "1000k", "-s", "1280x720",

        # Audio encoding settings
        "-codec:a", "aac", "-b:a", "128k",
        
        # Handle corrupted frames
        "-err_detect", "ignore_err", "-fflags", "+genpts",
        
        # HLS settings
        "-hls_time", "10", "-hls_playlist_type", "vod",
        "-hls_segment_filename", os.path.join(output_path, "segment%03d_%v.ts"),
        "-hls_flags", "independent_segments",
        
        # Master playlist
        "-master_pl_name", "index.m3u8",
        "-var_stream_map", "v:0,a:0 v:1,a:1",
        
        # Start segment numbering at 0
        "-start_number", "0",
        
        hls_path
    ]


    try:
        # Run ffmpeg command to process the video
        subprocess.run(ffmpeg_command, check=True)
        ts_url_prefix = f"/stream/{anime_id}/{episode_number}/segment"
        
        # Update the episode status to 'ready' in the database
        episode_model.update_episode_status(anime_id, episode_number, 'ready', os.path.join(output_path, "index.m3u8"), ts_url_prefix)
        return True
    except subprocess.CalledProcessError as e:
        # In case of error, print the error and clean up
        print(f"Error in FFmpeg process: {e}")
        cleanup_after_failure(video_path, output_path, anime_id,episode_number)
        return False

def cleanup_after_failure(video_path, output_path, anime_id,episode_number):
    """
    Cleans up the uploaded video file, output files, and database entry if the video processing fails.

    Args:
    video_path (str): Path to the uploaded video file.
    output_path (str): Path to the output directory containing HLS segments.
    episode_number (int): Episode number for the anime.

    This function ensures that no unnecessary files remain in case of failure.
    """
    if os.path.exists(video_path):
        os.remove(video_path)  # Remove the uploaded video
    if os.path.exists(output_path):
        shutil.rmtree(output_path)  # Remove the output directory
    episode_model.delete_episode(anime_id,episode_number)  # Delete the episode from the database

# Route to fetch all episodes for a specific anime
@episode_blueprint.route('anime/<int:anime_id>', methods=['GET'])
def get_episodes_by_anime(anime_id):
    """
    Retrieves all episodes of an anime by its ID from the database.
    
    Args:
    anime_id (int): The ID of the anime.

    Returns:
    A JSON response containing a list of episodes for the given anime.
    """
    episodes = episode_model.fetch_episodes_by_anime_id(anime_id)
    return jsonify(episodes)

# Route to fetch the latest 5 episodes globally
@episode_blueprint.route('/latest', methods=['GET'])
def get_latest_episodes():
    """
    Retrieves the 5 latest episodes globally from the database.

    Returns:
    A JSON response containing the list of the latest 5 episodes.
    """
    try:
        # Fetch the latest 5 episodes from the database using the appropriate model method
        latest_episodes = episode_model.fetch_latest_episodes(limit=5)
        return jsonify(latest_episodes)
    except Exception as e:
        # Return an error message if something goes wrong
        return jsonify({"error": str(e)}), 500


# Route to fetch details for a specific episode
@episode_blueprint.route('/anime/<int:anime_id>/<int:episode_number>', methods=['GET'])
def get_episode_details(anime_id, episode_number):
    """
    Retrieves details of a specific episode of an anime by anime ID and episode number.
    
    Args:
    anime_id (int): The ID of the anime.
    episode_number (int): The specific episode number.

    Returns:
    A JSON response containing details for the specified episode, including the anime synopsis.
    """
    episode_details = episode_model.fetch_episode_details(anime_id, episode_number)
    if episode_details:
        return jsonify(episode_details), 200
    else:
        return jsonify({"error": "Episode not found"}), 404


# Route to handle video file upload
@episode_blueprint.route('/upload', methods=['POST'])
def upload_video():
    """
    Handles the upload of a video file, processes it, and stores it in the database.
    
    Validates the file, creates a new episode entry in the database, and then
    processes the video in the background.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if not is_video_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    # Get additional episode details from the form
    anime_id = request.form.get('anime_id')
    title = request.form.get('title')
    episode_number = request.form.get('episode_number')

    episode_id = str(uuid.uuid4())  # Generate a unique ID for the episode
    output_path = os.path.join(UPLOAD_FOLDER, episode_id)
    video_path = os.path.join(output_path, file.filename)
    os.makedirs(output_path, exist_ok=True)
    file.save(video_path)  # Save the uploaded video file

    try:
        # Create an entry in the database with status 'processing'
        episode_model.create_episode(anime_id, title, episode_number, "", "processing")

        # Submit the video processing task for background execution
        executor.submit(process_video_task, video_path, output_path, anime_id, title, episode_number)

        return jsonify({"message": "Video upload successful, processing in background"})
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "Failed to upload video, please try again."}), 500

# Route to stream the video with specific language/variant
@episode_blueprint.route('/stream/<int:anime_id>/<int:episode_number>/<int:variant>', methods=['GET'])
def stream_video(anime_id, episode_number, variant):
    """
    Streams a specific variant of the video (audio/language track) based on the requested variant.
    
    Args:
    anime_id (int): The ID of the anime.
    episode_number (int): The episode number.
    variant (int): The variant number (audio track or resolution).

    Returns:
    A Response containing the requested m3u8 file.
    """
    variant_filename = f'index_{variant}.m3u8'
    
    # Fetch episode details from the database
    episode = episode_model.get_episode(anime_id, episode_number)
    if not episode or episode['status'] != 'ready':
        return jsonify({"error": "Episode not found or not ready"}), 404

    # Get the path to the m3u8 file for the chosen variant
    m3u8_file_path = episode['m3u8_url']
    m3u8_dir = os.path.dirname(m3u8_file_path)
    
    # Serve the specific variant playlist
    try:
        with open(os.path.join(m3u8_dir, variant_filename), 'r') as file:
            m3u8_content = file.read()

        # Modify the m3u8 content to ensure correct segment paths
        return Response(m3u8_content, content_type='application/vnd.apple.mpegurl')

    except FileNotFoundError:
        return jsonify({"error": "Variant playlist not found"}), 404

# Route to stream video segments
@episode_blueprint.route('/stream/<int:anime_id>/<int:episode_number>/segment<path:filename>', methods=['GET'])
def stream_segment(anime_id, episode_number, filename):
    """
    Streams a specific video segment file.
    
    Args:
    anime_id (int): The ID of the anime.
    episode_number (int): The episode number.
    filename (str): The segment filename.

    Returns:
    The video segment file if found, else an error message.
    """
    # Decode the filename to handle spaces and other encoded characters
    filename = urllib.parse.unquote(filename)
    # print(f"Decoded filename: {filename}")  # Debug print to see the raw decoded filename
    
    # Prepend 'segment' to the filename to ensure it matches the naming format used for segments
    filename = 'segment' + filename  # Ensure correct segment filename formatting
    # print(f"Final filename after prepending 'segment': {filename}")  # Debug print

    # Fetch the episode details from the database to verify if it's available and ready
    # print("Fetching episode data...")
    episode = episode_model.get_episode(anime_id, episode_number)
    
    # Check if the episode exists and its status is 'ready' before proceeding
    if not episode or episode['status'] != 'ready':
        return jsonify({"error": "Episode not found or not ready"}), 404
    # print(f"Episode found: {episode}")

    # Decode the URL path for the segment directory, which stores the segment files
    segment_dir = urllib.parse.unquote(os.path.dirname(episode['m3u8_url']))
    # print(f"Decoded segment directory path: {segment_dir}")  # Debug print for segment directory path

    # Ensure no URL encoding issues by replacing spaces with '%20' (standard URL encoding)
    segment_dir = segment_dir.replace(' ', ' ')  # Ensure no encoding issues here
    filename = filename.replace(' ', ' ')  # Ensure no encoding issues for filename
    # print(f"Resolved segment directory: {segment_dir}")  # Debug print for final segment directory path
    # print(f"Resolved filename: {filename}")  # Debug print for final segment filename

    # Construct the full path to the video segment using the segment directory and filename
    file_path = os.path.join(segment_dir, filename)
    # print(f"Checking if file exists at: {file_path}")  # Debug print for the complete path check
    
    # If the segment file does not exist, log an error and return a 404
    if not os.path.exists(file_path):
        # print(f"File does not exist at path: {file_path}")  # Debug print if file is not found
        return jsonify({"error": "File not found"}), 404

    # If the file exists, log the serving path and send the file to the client
    # print(f"Serving segment from: {file_path}")  # Debug print for the file being served
    
    # Send the file from the segment directory with an option to download as an attachment
    return send_from_directory(segment_dir, filename, as_attachment=True), 200