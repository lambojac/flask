from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)



# Create
@app.route('/item', methods=['POST'])
def create_item():
    try:
        data = request.get_json()
        if 'name' not in data or 'description' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        new_item = Item(name=data['name'], description=data['description'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Item created successfully'}), 201
    except Exception as e:
        logging.error(f'Error creating item: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500

# Read (all items)
@app.route('/items', methods=['GET'])
def get_items():
    try:
        items = Item.query.all()
        return jsonify([{'id': item.id, 'name': item.name, 'description': item.description} for item in items])
    except Exception as e:
        logging.error(f'Error retrieving items: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500

# Read (single item)
@app.route('/item/<int:id>', methods=['GET'])
def get_item(id):
    try:
        item = Item.query.get(id)
        if item is None:
            return jsonify({'error': 'Item not found'}), 404
        return jsonify({'id': item.id, 'name': item.name, 'description': item.description})
    except Exception as e:
        logging.error(f'Error retrieving item: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500

# Update
@app.route('/item/<int:id>', methods=['PUT'])
def update_item(id):
    try:
        data = request.get_json()
        item = Item.query.get(id)
        if item is None:
            return jsonify({'error': 'Item not found'}), 404
        if 'name' in data:
            item.name = data['name']
        if 'description' in data:
            item.description = data['description']
        db.session.commit()
        return jsonify({'message': 'Item updated successfully'})
    except Exception as e:
        logging.error(f'Error updating item: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500

# Delete
@app.route('/item/<int:id>', methods=['DELETE'])
def delete_item(id):
    try:
        item = Item.query.get(id)
        if item is None:
            return jsonify({'error': 'Item not found'}), 404
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})
    except Exception as e:
        logging.error(f'Error deleting item: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
