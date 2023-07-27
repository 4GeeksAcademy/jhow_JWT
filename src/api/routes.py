"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint, Response
from src.api.models import db, User, Product, Order
from src.api.utils import generate_sitemap, APIException
from src.api.utils import save_new_product, update_product_by_id
from src.api.utils import check_is_admin_by_user_id
import bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from src import app

api = Blueprint('api', __name__)



# La clave secreta para firmar los tokens JWT
api.secret_key = 'Our_Unique_Proyect'

# Función para generar un token JWT
def generate_token(user_id):
    # payload = {'user_id': user_id}
    token = create_access_token(identity=user_id)
    return token

# Ruta para el registro de usuarios (signup)
@api.route('/signup', methods=['POST'])
def signup():
    data = request.json

    # Verificar si el usuario ya existe por su dirección de correo electrónico
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'El usuario ya existe. Intente con otro correo electrónico.'}), 409
    
    # Verificar si se proporcionó la contraseña en el payload
    if 'password' not in data or not data['password']:
        return jsonify({'message': 'El campo de contraseña es obligatorio.'}), 400


    # Encriptar la contraseña antes de guardarla en la base de datos
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    # Crear un nuevo usuario
    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=hashed_password.decode('utf-8'),  # Decodificar el hash para almacenarlo como cadena
        address=data['address'],
        location=data['location'],
        payment_method=data['payment_method'],
    )

    # Agregar el usuario a la base de datos
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuario creado exitosamente.'}), 201

# Ruta para el inicio de sesión de usuarios (login)
@api.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        # Generar un token JWT y devolverlo en la respuesta
        token = generate_token(user.id)
        return jsonify({'message': 'Inicio de sesión exitoso.', 'token': token}), 200
    else:
        return jsonify({'message': 'Credenciales inválidas. Por favor, intenta de nuevo.'}), 401

# Ruta para cerrar sesión (logout)
@api.route('/logout')
def logout():
    # Para cerrar sesión con JWT, simplemente se omite el token en el cliente.
    return jsonify({'message': 'Cierre de sesión exitoso.'}), 200



@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

# Rutas para Product
@api.route('/products', methods=['GET'])
def all_products():
    products = Product.query.all()
    return jsonify([p.serialize() for p in products]), 200

@api.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = Product.query.get(id)
    if product is None:
        raise APIException(message='Product not found', status_code=404)
    return jsonify(product.serialize()), 200

@api.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    request_body = request.get_json()
    current_user_id = get_jwt_identity()
    check_is_admin_by_user_id(current_user_id) 
    product = save_new_product(request_body)
    return jsonify(product.serialize()), 200

@api.route('/products/clothing', methods=['GET'])
def get_clothing_products():
    products = Product.query.filter_by(category_id=1)
    return jsonify([p.serialize() for p in products]), 200

@api.route('/products/accessories', methods=['GET'])
def get_accessories_accesories():
    products = Product.query.filter_by(category_id=2)
    return jsonify([p.serialize() for p in products]), 200

@api.route('/products/shoes', methods=['GET'])
def get_accessories_shoes():
    products = Product.query.filter_by(category_id=3)
    return jsonify([p.serialize() for p in products]), 200

@api.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    request_body = request.get_json()
    current_user_id = get_jwt_identity()
    check_is_admin_by_user_id(current_user_id) 
    updated_character = update_product_by_id(product_id, request_body)
    return jsonify(updated_character.serialize()), 200

@api.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    current_user_id = get_jwt_identity()
    check_is_admin_by_user_id(current_user_id) 
    product = Product.query.get(product_id)
    if product is None:
        raise APIException(message='Product not found', status_code=404)
    db.session.delete(product)
    db.session.commit()
    return Response(status=204)
# End rutas para products