from flask import request, jsonify, Blueprint
from models.user import UserModel

user_blueprint = Blueprint('user', __name__)
user_model = UserModel()

@user_blueprint.route('/users', methods=['GET'])
def get_all_users():
    users = user_model.fetch_all_users()
    return jsonify(users)

@user_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_model.fetch_user_by_id(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

@user_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if 'username' not in data or 'password' not in data or 'email' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    user_model.create_user(data['username'], data['password'], data['email'])
    return jsonify({'message': 'User created successfully'}), 201
