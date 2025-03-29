# backend/routes/report.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Report, User, Product
from config import Config

report_bp = Blueprint('report', __name__)

@report_bp.route('/user/<int:target_id>', methods=['POST'])
@jwt_required()
def report_user(target_id):
    reporter_id = get_jwt_identity()
    
    # Cannot report yourself
    if reporter_id == target_id:
        return jsonify({'error': '자신을 신고할 수 없습니다.'}), 400
    
    # Check if target exists
    target = User.query.get(target_id)
    if not target:
        return jsonify({'error': '사용자를 찾을 수 없습니다.'}), 404
    
    data = request.get_json()
    
    # Validate input
    if not data or not data.get('reason'):
        return jsonify({'error': '신고 사유는 필수입니다.'}), 400
    
    # Create report
    report = Report(
        reporter_id=reporter_id,
        target_id=target_id,
        reason=data['reason']
    )
    
    db.session.add(report)
    
    # Increment report count for target
    target.report_count += 1
    
    # Check if report threshold is reached
    if target.report_count >= Config.REPORT_THRESHOLD_USER:
        target.is_active = False
    
    db.session.commit()
    
    return jsonify({'message': '사용자가 신고되었습니다.'}), 201

@report_bp.route('/product/<int:product_id>', methods=['POST'])
@jwt_required()
def report_product(product_id):
    reporter_id = get_jwt_identity()
    
    # Check if product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': '상품을 찾을 수 없습니다.'}), 404
    
    # Cannot report your own product
    if product.seller_id == reporter_id:
        return jsonify({'error': '자신의 상품을 신고할 수 없습니다.'}), 400
    
    data = request.get_json()
    
    # Validate input
    if not data or not data.get('reason'):
        return jsonify({'error': '신고 사유는 필수입니다.'}), 400
    
    # Create report
    report = Report(
        reporter_id=reporter_id,
        product_id=product_id,
        reason=data['reason']
    )
    
    db.session.add(report)
    
    # Increment report count for product
    product.report_count += 1
    
    # Check if report threshold is reached
    if product.report_count >= Config.REPORT_THRESHOLD_PRODUCT:
        product.is_active = False
    
    db.session.commit()
    
    return jsonify({'message': '상품이 신고되었습니다.'}), 201
