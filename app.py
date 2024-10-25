from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import subprocess

app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SPLIT_FOLDER'] = 'splits'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['SPLIT_FOLDER'], exist_ok=True)

def is_video_file(filename):
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv')
    return filename.lower().endswith(video_extensions)

def split_video(input_path, output_dir, segment_duration=10):
    output_pattern = os.path.join(output_dir, "part_%03d.mp4")
    ffmpeg_path = "C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin"  # Ensure 'ffmpeg' is in PATH; or provide the full path here
    
    try:
        subprocess.run(
            [
                ffmpeg_path,
                "-i", input_path,
                "-f", "segment",
                "-segment_time", str(segment_duration),
                "-reset_timestamps", "1",
                output_pattern
            ],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print("FFmpeg error:", e.stderr)  # Logs FFmpeg error output
        raise  # Reraise the exception to be handled by the calling function

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    if file.filename == '' or not is_video_file(file.filename):
        return jsonify({"error": "No selected video file or incorrect file type"}), 400
    
    # Save the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    # Define output folder for splits
    split_output_dir = os.path.join(app.config['SPLIT_FOLDER'], file.filename.split('.')[0])
    os.makedirs(split_output_dir, exist_ok=True)
    
    # Split the video with error handling
    try:
        split_video(file_path, split_output_dir)
    except Exception as e:
        print("Error in split_video function:", str(e))  # Logs error to the server console
        return jsonify({"error": f"Error splitting video: {str(e)}"}), 500

    # List of split video file paths
    split_files = [os.path.join(split_output_dir, f) for f in os.listdir(split_output_dir)]
    return jsonify({"success": True, "split_files": split_files})

if __name__ == "__main__":
    app.run(debug=True)
