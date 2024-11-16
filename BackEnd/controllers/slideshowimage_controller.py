from flask import request, jsonify, Blueprint
from models.slideshowimage import SlideshowImageModel
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create a Blueprint for slideshow-related routes
slideshow_blueprint = Blueprint('slideshow', __name__)
# Initialize the SlideshowImageModel which handles database operations
slideshow_image_model = SlideshowImageModel()

# Fetch the ImgBB API key from environment variables
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

def upload_image_to_imgbb(image_file):
    """
    Uploads an image to ImgBB and returns the image URL.
    
    Args:
    image_file: The image file to upload to ImgBB.
    
    Returns:
    str: The URL of the uploaded image.
    
    Raises:
    Exception: If the image upload to ImgBB fails.
    """
    url = f"https://api.imgbb.com/1/upload?key={IMGBB_API_KEY}"
    files = {'image': (image_file.filename, image_file.read())}
    response = requests.post(url, files=files)
    response_data = response.json()
    
    # Check if the upload was successful
    if response_data['success']:
        return response_data['data']['url']
    else:
        raise Exception("Image upload to ImgBB failed.")

# Route to retrieve all slideshow images
@slideshow_blueprint.route('/', methods=['GET'])
def get_all_images():
    """Retrieve all slideshow images."""
    images = slideshow_image_model.fetch_all_images()
    return jsonify({'images': images})

# Route to retrieve a specific slideshow image by its ID
@slideshow_blueprint.route('/<int:image_id>', methods=['GET'])
def get_image(image_id):
    """Retrieve a specific slideshow image by ID."""
    image = slideshow_image_model.fetch_image_by_id(image_id)
    if image is None:
        return jsonify({'error': 'Image not found'}), 404
    return jsonify(image)

# Route to upload images and store their metadata
@slideshow_blueprint.route('/upload', methods=['POST'])
def create_images():
    """
    Create multiple slideshow images with optional ImgBB upload and metadata.
    
    This route accepts multiple images, uploads them to ImgBB, and stores their URLs and metadata.
    
    Returns:
    JSON: A success message along with the URLs of the uploaded images.
    """
    responses = []
    try:
        if 'images' in request.files:
            for index, image_file in enumerate(request.files.getlist('images')):
                # Upload each image to ImgBB and get the URL
                image_url = upload_image_to_imgbb(image_file)
                # Store image data in the database with its URL
                slideshow_image_model.create_image(image_url)
                responses.append({'image_url': image_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Images created successfully', 'responses': responses}), 201

# Route to update the URL of an existing slideshow image
@slideshow_blueprint.route('/<int:image_id>', methods=['PUT'])
def update_image(image_id):
    """Update an existing slideshow image's URL."""
    image = slideshow_image_model.fetch_image_by_id(image_id)
    if image is None:
        return jsonify({'error': 'Image not found'}), 404

    # Get the updated image URL from the request data
    data = request.get_json() or request.form
    image_url = data.get('image_url')

    # Update the image URL in the database
    slideshow_image_model.update_image(image_id, image_url)
    return jsonify({'message': 'Image updated successfully'})

# Route to delete a slideshow image by its ID
@slideshow_blueprint.route('/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    """Delete a slideshow image by ID."""
    image = slideshow_image_model.fetch_image_by_id(image_id)
    if image is None:
        return jsonify({'error': 'Image not found'}), 404

    # Delete the image from the database
    slideshow_image_model.delete_image(image_id)
    return jsonify({'message': 'Image deleted successfully'}), 200
