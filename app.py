from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import uuid
import subprocess

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads/'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def is_video_file(filename):
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv')
    return filename.lower().endswith(video_extensions)



#need to implement queue system in this (file must be uploaded first and then added to queue ,  admin can tract thrugh panel regarding file processing)
@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '' or not is_video_file(file.filename):
        return jsonify({"error": "No selected video file or incorrect file type"}), 400

    # Generate a unique lesson ID
    lesson_id = str(uuid.uuid4())
    filename_extension = file.filename.rsplit('.', 1)[1]  # Get file extension
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], lesson_id, f"main_{lesson_id}.{filename_extension}")

    # Create a unique folder for each upload based on UUID
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], lesson_id)
    hls_path = os.path.join(output_path, "index.m3u8")
    os.makedirs(output_path, exist_ok=True)

    # Save the uploaded video with the new filename
    file.save(video_path)

    # FFmpeg command to convert the video to HLS format
    ffmpeg_command = [
        "ffmpeg",
        "-i", video_path,
        "-codec:v", "libx264",
        "-codec:a", "aac",
        "-hls_time", "10",
        "-hls_playlist_type", "vod",
        "-hls_segment_filename", os.path.join(output_path, "segment%03d.ts"),
        "-start_number", "0",
        hls_path
    ]

    try:
        # Execute the FFmpeg command
        subprocess.run(ffmpeg_command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.stderr}")  # Log error output
        return jsonify({"error": "Error converting video to HLS format"}), 500

    # URL for accessing the video playlist
    video_url = f"/stream/{lesson_id}/index.m3u8"

    return jsonify({
        "message": "Video converted to HLS format",
        "videoUrl": video_url,
        "lessonId": lesson_id
    })

@app.route('/stream/<lesson_id>/<path:filename>')
def stream(lesson_id, filename):
    # Serve the .m3u8 and .ts files from the generated lesson folder
    directory = os.path.join(app.config['UPLOAD_FOLDER'], lesson_id)
    return send_from_directory(directory, filename)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
