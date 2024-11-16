from flask import Blueprint, request, jsonify, send_from_directory,Response
import os
import uuid
import subprocess
from models.episode import EpisodeModel
from concurrent.futures import ThreadPoolExecutor
import shutil
import urllib.parse


episode_blueprint = Blueprint('episode', __name__)
episode_model = EpisodeModel()
executor = ThreadPoolExecutor(max_workers=5)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def is_video_file(filename):
    return filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))

def process_video_task(video_path, output_path, anime_id, title, episode_number):
    # Define paths for the main HLS playlist and segment files
    video_hls_path = os.path.join(output_path, "video.m3u8")
    segment_path = os.path.join(output_path, "segment%03d.ts")
    
    # Define paths for audio playlists (Japanese and English)
    japanese_audio_path = os.path.join(output_path, "audio_jpn.m3u8")
    english_audio_path = os.path.join(output_path, "audio_eng.m3u8")
    
    # Initialize base ffmpeg command
    ffmpeg_command = [
        "ffmpeg", "-i", video_path,
        "-codec:v", "libx264", "-preset", "fast", "-crf", "23"
    ]
    
    # Parse for audio streams and apply mappings accordingly
    stream_info = subprocess.run(
        ["ffmpeg", "-i", video_path],
        stderr=subprocess.PIPE,
        text=True
    ).stderr

    # Check if dual audio is available
    if "Stream #0:1" in stream_info and "Stream #0:2" in stream_info:
        # Dual audio (Japanese and English)
        ffmpeg_command.extend([
            # Map video stream and first audio stream (Japanese)
            "-map", "0:v:0",
            "-map", "0:a:0",
            "-map", "0:a:1",
            
            # Video settings
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            
            # Japanese audio settings
            "-c:a:0", "aac", "-b:a:0", "128k", "-f", "hls",
            "-hls_segment_filename", segment_path,
            "-hls_time", "10", "-hls_playlist_type", "vod",
            "-metadata:s:a:0", "language=jpn", "-metadata:s:a:0", "title=Japanese",
            japanese_audio_path,

            # English audio settings
            "-c:a:1", "aac", "-b:a:1", "128k", "-f", "hls",
            "-hls_segment_filename", segment_path,
            "-metadata:s:a:1", "language=eng", "-metadata:s:a:1", "title=English",
            english_audio_path,
        ])
    
    # Add HLS output settings for video
    ffmpeg_command.extend([
        "-hls_time", "10",
        "-hls_playlist_type", "vod",
        "-hls_segment_filename", segment_path,
        video_hls_path
    ])
    
    try:
        # Run the FFmpeg command
        subprocess.run(ffmpeg_command, check=True)
        
        # Create the master playlist with #EXT-X-MEDIA tags for audio tracks
        master_playlist_content = (
            "#EXTM3U\n"
            "#EXT-X-VERSION:3\n"
            f"#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=640x360,CODECS=\"avc1.4d401f,mp4a.40.2\"\n"
            f"{video_hls_path}\n"
            f"#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID=\"audio\",NAME=\"Japanese\",AUTOSELECT=YES,DEFAULT=YES,URI=\"{japanese_audio_path}\"\n"
            f"#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID=\"audio\",NAME=\"English\",AUTOSELECT=NO,DEFAULT=NO,URI=\"{english_audio_path}\"\n"
        )
        
        # Write the master playlist file
        with open(os.path.join(output_path, "index.m3u8"), "w") as f:
            f.write(master_playlist_content)

        # Update episode status in the database
        ts_url_prefix = f"/stream/{anime_id}/{episode_number}/segment"
        episode_model.update_episode_status(anime_id, episode_number, 'ready', video_hls_path, ts_url_prefix)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error in FFmpeg process: {e}")
        cleanup_after_failure(video_path, output_path, episode_number)
        return False



# def process_video_task(video_path, output_path, anime_id, title, episode_number):
#     hls_path = os.path.join(output_path, "index.m3u8")
#     segment_path = os.path.join(output_path, "segment%03d.ts")
    
#     # Check for the number of audio streams
#     stream_info = subprocess.run(
#         ["ffmpeg", "-i", video_path],
#         stderr=subprocess.PIPE,
#         text=True
#     ).stderr
    
#     # Set the mapping and metadata based on available streams
#     ffmpeg_command = [
#         "ffmpeg", "-i", video_path,
#         "-codec:v", "libx264", "-preset", "fast", "-crf", "23"
#     ]
    
#     # Parse for audio streams and apply mappings accordingly
#     if "Stream #0:1" in stream_info and "Stream #0:2" in stream_info:
#         # Dual audio stream: Japanese and English
#         ffmpeg_command.extend([
#             "-map", "0:v:0",
#             "-map", "0:a:0",  # Japanese
#             "-map", "0:a:1",  # English
#             "-c:a", "aac", "-b:a", "128k",
#             "-metadata:s:a:0", "language=jpn",
#             "-metadata:s:a:0", "title=Japanese",
#             "-metadata:s:a:1", "language=eng",
#             "-metadata:s:a:1", "title=English"
#         ])
#     elif "Stream #0:1" in stream_info:
#         # Single audio stream
#         ffmpeg_command.extend([
#             "-map", "0:v:0",
#             "-map", "0:a:0",  # Default single audio
#             "-c:a", "aac", "-b:a", "128k",
#             "-metadata:s:a:0", "language=eng",
#             "-metadata:s:a:0", "title=English"
#         ])
    
#     # Add HLS output settings
#     ffmpeg_command.extend([
#         "-hls_time", "10",
#         "-hls_playlist_type", "vod",
#         "-hls_segment_filename", segment_path,
#         hls_path
#     ])
    
#     try:
#         # Run the FFmpeg command
#         subprocess.run(ffmpeg_command, check=True)
        
#         ts_url_prefix = f"/stream/{anime_id}/{episode_number}/segment"
        
#         # Update episode status in database
#         episode_model.update_episode_status(anime_id, episode_number, 'ready', hls_path, ts_url_prefix)
        
#         return True
#     except subprocess.CalledProcessError as e:
#         print(f"Error in FFmpeg process: {e}")
#         cleanup_after_failure(video_path, output_path, episode_number)
#         return False




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


# @episode_blueprint.route('/stream/<int:anime_id>/<int:episode_number>', methods=['GET'])
# def stream_video(anime_id, episode_number):
#     # Fetch the episode details from the database
#     episode = episode_model.get_episode(anime_id, episode_number)
    
#     # Check if the episode exists and is ready
#     if not episode or episode['status'] != 'ready':
#         return jsonify({"error": "Episode not found or not ready"}), 404

#     # Get the path to the .m3u8 playlist file
#     m3u8_file_path = episode['m3u8_url']
#     m3u8_dir = os.path.dirname(m3u8_file_path)
#     m3u8_filename = os.path.basename(m3u8_file_path)

#     # Serve the .m3u8 file from its directory
#     return send_from_directory(m3u8_dir, m3u8_filename)


@episode_blueprint.route('/stream/<int:anime_id>/<int:episode_number>', methods=['GET'])
def stream_video(anime_id, episode_number):
    # Fetch the episode details from the database
    episode = episode_model.get_episode(anime_id, episode_number)
    
    # Check if the episode exists and is ready
    if not episode or episode['status'] != 'ready':
        return jsonify({"error": "Episode not found or not ready"}), 404

    # Get the path to the .m3u8 playlist file
    m3u8_file_path = episode['m3u8_url']
    m3u8_dir = os.path.dirname(m3u8_file_path)
    m3u8_filename = os.path.basename(m3u8_file_path)

    # Serve the .m3u8 file from its directory
    # Modify the .m3u8 content to use the correct URL format for segment files
    with open(os.path.join(m3u8_dir, m3u8_filename), 'r') as file:
        m3u8_content = file.read()

    # Replace the segment URLs to include the episode_number
    m3u8_content = m3u8_content.replace("segment", f"{episode_number}/segment")
    # m3u8_content = m3u8_content.replace("playlist", f"{episode_number}/segment")

    # Return the modified .m3u8 file
    return Response(m3u8_content, content_type='application/vnd.apple.mpegurl')


@episode_blueprint.route('/stream/<int:anime_id>/<int:episode_number>/segment<path:filename>', methods=['GET'])
def stream_segment(anime_id, episode_number, filename):
    # Decode the filename to handle spaces and other encoded characters
    filename = urllib.parse.unquote(filename)
    print(f"Decoded filename: {filename}")
    
    filename = 'segment' + filename  # Ensure correct segment filename formatting

    # Fetch the episode details from the database
    print("Fetching episode data...")
    episode = episode_model.get_episode(anime_id, episode_number)
    
    # Check if the episode exists and is ready
    if not episode or episode['status'] != 'ready':
        return jsonify({"error": "Episode not found or not ready"}), 404

    # Decode the URL path for the segment directory
    segment_dir = urllib.parse.unquote(os.path.dirname(episode['m3u8_url']))
    print(f"Decoded segment directory path: {segment_dir}")

    # Replace spaces with '%20' for URL encoding
    segment_dir = segment_dir.replace(' ', ' ')  # Ensure no encoding issues here
    filename = filename.replace(' ', ' ')  # Ensure no encoding issues for filename

    # Log the resolved segment directory and filename for debugging
    print(f"Resolved segment directory: {segment_dir}")
    print(f"Resolved filename: {filename}")

    # Check if the file exists at the path
    file_path = os.path.join(segment_dir, filename)
    print(f"Checking if file exists at: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"File does not exist at path: {file_path}")
        return jsonify({"error": "File not found"}), 404

    # Log the segment directory for debugging
    print(f"Serving segment from: {file_path}")

    # Send the file from the segment directory
    return send_from_directory(segment_dir, filename, as_attachment=True), 200
