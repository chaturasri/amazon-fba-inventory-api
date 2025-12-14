from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fba_inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    stock_fc1 = db.Column(db.Integer, default=0)  # Fulfillment Center 1
    stock_fc2 = db.Column(db.Integer, default=0)  # Fulfillment Center 2
    safety_stock = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {
            'id': self.id, 'name': self.name, 'sku': self.sku,
            'stock_fc1': self.stock_fc1, 'stock_fc2': self.stock_fc2,
            'total_stock': self.stock_fc1 + self.stock_fc2,
            'safety_stock': self.safety_stock
        }

# Routes
@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    total_stock = data.get('stock_fc1', 0) + data.get('stock_fc2', 0)
    if total_stock < data.get('safety_stock', 10):
        return jsonify({'error': 'Insufficient stock vs safety threshold'}), 400
    
    product = Product(
        name=data['name'], sku=data['sku'],
        stock_fc1=data.get('stock_fc1', 0),
        stock_fc2=data.get('stock_fc2', 0),
        safety_stock=data.get('safety_stock', 10)
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.as_dict()), 201

@app.route('/api/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([p.as_dict() for p in products])

@app.route('/api/inventory/low-stock', methods=['GET'])
def low_stock_alert():
    low_stock = Product.query.filter(
        Product.stock_fc1 + Product.stock_fc2 < Product.safety_stock
    ).all()
    return jsonify([p.as_dict() for p in low_stock])

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'FBA Inventory API'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
