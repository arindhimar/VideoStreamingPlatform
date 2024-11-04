from flask import request, jsonify, Blueprint
from models.slideshowimage import SlideshowImageModel
import requests
from dotenv import load_dotenv
import os

load_dotenv()

slideshow_blueprint = Blueprint('slideshow', __name__)
slideshow_image_model = SlideshowImageModel()

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

def upload_image_to_imgbb(image_file):
    """Uploads an image to ImgBB and returns the image URL."""
    url = f"https://api.imgbb.com/1/upload?key={IMGBB_API_KEY}"
    files = {'image': (image_file.filename, image_file.read())}
    response = requests.post(url, files=files)
    response_data = response.json()
    if response_data['success']:
        return response_data['data']['url']
    else:
        raise Exception("Image upload to ImgBB failed.")

@slideshow_blueprint.route('/', methods=['GET'])
def get_all_images():
    """Retrieve all slideshow images."""
    images = slideshow_image_model.fetch_all_images()
    return jsonify({'images': images}) 


@slideshow_blueprint.route('/<int:image_id>', methods=['GET'])
def get_image(image_id):
    """Retrieve a specific slideshow image by ID."""
    image = slideshow_image_model.fetch_image_by_id(image_id)
    if image is None:
        return jsonify({'error': 'Image not found'}), 404
    return jsonify(image)

@slideshow_blueprint.route('/upload', methods=['POST'])
def create_images():
    """Create multiple slideshow images with optional ImgBB upload and metadata."""
    responses = []
    try:
        if 'images' in request.files:
            for index, image_file in enumerate(request.files.getlist('images')):
                image_url = upload_image_to_imgbb(image_file)
                # Store image data in the database along with its metadata
                slideshow_image_model.create_image(image_url)
                responses.append({
                    'image_url': image_url,
                })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Images created successfully', 'responses': responses}), 201

@slideshow_blueprint.route('/<int:image_id>', methods=['PUT'])
def update_image(image_id):
    """Update an existing slideshow image's URL."""
    image = slideshow_image_model.fetch_image_by_id(image_id)
    if image is None:
        return jsonify({'error': 'Image not found'}), 404

    data = request.get_json() or request.form
    image_url = data.get('image_url')

    slideshow_image_model.update_image(image_id, image_url)
    return jsonify({'message': 'Image updated successfully'})

@slideshow_blueprint.route('/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    """Delete a slideshow image by ID."""
    image = slideshow_image_model.fetch_image_by_id(image_id)
    if image is None:
        return jsonify({'error': 'Image not found'}), 404

    slideshow_image_model.delete_image(image_id)
    return jsonify({'message': 'Image deleted successfully'}), 200
