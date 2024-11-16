import os
import uuid
import subprocess
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=5)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def is_video_file(filename):
    return filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))

def process_video_task(video_path, output_path):
    # FFmpeg command for HLS conversion
    hls_path = os.path.join(output_path, "index.m3u8")
    ffmpeg_command = [
        "ffmpeg", "-i", video_path, "-codec:v", "libx264", "-codec:a", "aac",
        "-hls_time", "10", "-hls_playlist_type", "vod",
        "-hls_segment_filename", os.path.join(output_path, "segment%03d.ts"),
        "-start_number", "0", hls_path
    ]
    try:
        subprocess.run(ffmpeg_command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error in FFmpeg process: {e}")
        return False

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if not is_video_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    # Prepare paths for the upload
    episode_id = str(uuid.uuid4())
    output_path = os.path.join(UPLOAD_FOLDER, episode_id)
    video_path = os.path.join(output_path, file.filename)
    os.makedirs(output_path, exist_ok=True)
    file.save(video_path)

    # Start the background task for video processing
    executor.submit(process_video_task, video_path, output_path)
    video_url = f"/stream/{episode_id}/index.m3u8"

    return jsonify({"message": "Video upload successful, processing in background", "videoUrl": video_url})

if __name__ == "__main__":
    app.run(debug=True)
