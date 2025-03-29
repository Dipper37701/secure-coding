# backend/routes/product.py
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from werkzeug.utils import secure_filename
from models import db, Product, User
from utils.upload import save_file

product_bp = Blueprint('product', __name__)

@product_bp.route('/', methods=['GET'])
def get_products():
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Query active products
    products = Product.query.filter_by(is_active=True).order_by(
        Product.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'products': [product.to_dict() for product in products.items],
        'total': products.total,
        'pages': products.pages,
        'current_page': products.page
    }), 200

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': '상품을 찾을 수 없습니다.'}), 404
    
    if not product.is_active:
        return jsonify({'error': '이 상품은 더 이상 활성 상태가 아닙니다.'}), 403
    
    return jsonify({'product': product.to_dict()}), 200

@product_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or not user.is_active:
        return jsonify({'error': '권한이 없습니다.'}), 403
    
    # Check if form data
    if request.content_type and 'multipart/form-data' in request.content_type:
        data = request.form
        image = request.files.get('image')
        image_path = save_file(image) if image else None
    else:
        data = request.get_json()
        image_path = None
    
    # Validate input
    if not data or not data.get('name') or not data.get('price'):
        return jsonify({'error': '상품명과 가격은 필수입니다.'}), 400
    
    try:
        price = float(data['price'])
    except ValueError:
        return jsonify({'error': '가격은 숫자여야 합니다.'}), 400
    
    # Create product
    product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=price,
        seller_id=user_id,
        image_path=image_path
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify({
        'message': '상품이 등록되었습니다.',
        'product': product.to_dict()
    }), 201

@product_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    user_id = get_jwt_identity()
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': '상품을 찾을 수 없습니다.'}), 404
    
    if product.seller_id != user_id:
        return jsonify({'error': '이 상품을 수정할 권한이 없습니다.'}), 403
    
    # Check if form data
    if request.content_type and 'multipart/form-data' in request.content_type:
        data = request.form
        image = request.files.get('image')
        
        if image:
            # Remove old image if exists
            if product.image_path:
                old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], product.image_path.lstrip('/uploads/'))
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            image_path = save_file(image)
            if image_path:
                product.image_path = image_path
    else:
        data = request.get_json()
    
    # Update fields if provided
    if data.get('name'):
        product.name = data['name']
    
    if data.get('description') is not None:
        product.description = data['description']
    
    if data.get('price'):
        try:
            product.price = float(data['price'])
        except ValueError:
            return jsonify({'error': '가격은 숫자여야 합니다.'}), 400
    
    db.session.commit()
    
    return jsonify({
        'message': '상품이 업데이트되었습니다.',
        'product': product.to_dict()
    }), 200

@product_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    user_id = get_jwt_identity()
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': '상품을 찾을 수 없습니다.'}), 404
    
    if product.seller_id != user_id:
        return jsonify({'error': '이 상품을 삭제할 권한이 없습니다.'}), 403
    
    product.is_active = False
    db.session.commit()
    
    return jsonify({'message': '상품이 삭제되었습니다.'}), 200

@product_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user_products():
    user_id = get_jwt_identity()
    
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Query user's products
    products = Product.query.filter_by(seller_id=user_id).order_by(
        Product.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'products': [product.to_dict() for product in products.items],
        'total': products.total,
        'pages': products.pages,
        'current_page': products.page
    }), 200