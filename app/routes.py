from flask import request, jsonify, current_app as app
from app.models import db, User, WasteCollection, RecyclingEffort, Locations

def register_routes(app):
    # API Routes for User

    @app.route('/api/users', methods=['POST'])
    def create_user():
        data = request.json
        new_user = User(username=data['username'],
                        role=data['role'],
                        email=data['email'],
                        password=data['password'])
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Failed to create user', 'error': str(e)}), 500

    @app.route('/api/users', methods=['GET'])
    def get_all_users():
        users = User.query.all()
        return jsonify([user.__dict__ for user in users]), 200

    @app.route('/api/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify(user.__dict__), 200
        else:
            return jsonify({'message': 'User not found'}), 404

    
    @app.route('/api/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        data = request.json
        user = User.query.get(user_id)
        if user:
            user.username = data.get('username', user.username)
            user.role = data.get('role', user.role)
            user.email = data.get('email', user.email)
            user.password = data.get('password', user.password)
            
            try:
                db.session.commit()
                return jsonify({'message': 'User updated successfully'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'message': 'Failed to update user', 'error': str(e)}), 500
        else:
            return jsonify({'message': 'User not found'}), 404

    @app.route('/api/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            try:
                db.session.delete(user)
                db.session.commit()
                return jsonify({'message': 'User deleted successfully'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'message': 'Failed to delete user', 'error': str(e)}), 500
        else:
            return jsonify({'message': 'User not found'}), 404


    # API Routes for Waste Collection

    @app.route('/api/wastecollection', methods=['POST'])
    def create_waste_collection():
        data = request.json
        new_collection = WasteCollection(
            user_id=data['user_id'],
            date=data['date'],
            status=data['status'],
            waste_type=data['waste_type'],
            location=data['location']
        )
        
        try:
            db.session.add(new_collection)
            db.session.commit()
            return jsonify({'message': 'Waste collection created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Failed to create waste collection', 'error': str(e)}), 500

    @app.route('/api/wastecollection', methods=['GET'])
    def get_all_collections():
        w_collections = WasteCollection.query.all()
        return jsonify([w_collection.__dict__ for w_collection in w_collections]), 200

    @app.route('/api/wastecollection/<int:id>', methods=['GET'])
    def get_collection(id):
        w_collection = WasteCollection.query.get(id)
        if w_collection:
            return jsonify(w_collection.__dict__), 200
        else:
            return jsonify({'message': 'Collection not found'}), 404

    @app.route('/api/wastecollection/<int:id>', methods=['PUT'])
    def update_collection(id):
        data = request.json
        w_collection = WasteCollection.query.get(id)
        if w_collection:
            w_collection.date = data.get('date', w_collection.date)
            w_collection.status = data.get('status', w_collection.status)
            w_collection.waste_type = data.get('waste_type', w_collection.waste_type)
            w_collection.location = data.get('location', w_collection.location)
            
            try:
                db.session.commit()
                return jsonify({'message': 'Collection updated successfully'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'message': 'Failed to update collection', 'error': str(e)}), 500
        else:
            return jsonify({'message': 'Collection not found'}), 404

    @app.route('/api/wastecollection/<int:id>', methods=['DELETE'])
    def delete_collection(id):
        w_collection = WasteCollection.query.get(id)
        if w_collection:
            try:
                db.session.delete(w_collection)
                db.session.commit()
                return jsonify({'message': 'Collection deleted successfully'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'message': 'Failed to delete collection', 'error': str(e)}), 500
        else:
            return jsonify({'message': 'Collection not found'}), 404
        
    # API Routes for Recycling Effort

    @app.route('/api/recyclingeffort', methods=['POST'])
    def create_recycling_effort():
        data = request.json
        new_effort = RecyclingEffort(
            user_id=data['user_id'],
            date=data['date'],
            waste_type=data['waste_type']
        )
        
        try:
            db.session.add(new_effort)
            db.session.commit()
            return jsonify({'message': 'Recycling effort created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Failed to create recycling effort', 'error': str(e)}), 500

    @app.route('/api/recyclingeffort', methods=['GET'])
    def get_all_recycling_efforts():
        efforts = RecyclingEffort.query.all()
        return jsonify([effort.__dict__ for effort in efforts]), 200

    @app.route('/api/recyclingeffort/<int:id>', methods=['GET'])
    def get_recycling_effort(id):
        effort = RecyclingEffort.query.get(id)
        if effort:
            return jsonify(effort.__dict__), 200
        else:
            return jsonify({'message': 'Recycling effort not found'}), 404

    @app.route('/api/recyclingeffort/<int:id>', methods=['PUT'])
    def update_recycling_effort(id):
        data = request.json
        effort = RecyclingEffort.query.get(id)
        if effort:
            effort.date = data.get('date', effort.date)
            effort.waste_type = data.get('waste_type', effort.waste_type)

            try:
                db.session.commit()
                return jsonify({'message': 'Recycling effort updated successfully'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'message': 'Failed to update recycling effort', 'error': str(e)}), 500
        else:
            return jsonify({'message': 'Recycling effort not found'}), 404

    @app.route('/api/recyclingeffort/<int:id>', methods=['DELETE'])
    def delete_recycling_effort(id):
        effort = RecyclingEffort.query.get(id)
        if effort:
            try:
                db.session.delete(effort)
                db.session.commit()
                return jsonify({'message': 'Recycling effort deleted successfully'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'message': 'Failed to delete recycling effort', 'error': str(e)}), 500
        else:
            return jsonify({'message': 'Recycling effort not found'}), 404

    # API Routes for Locations

    @app.route('/api/locations', methods=['POST'])
    def create_location():
        data = request.json
        new_location = Locations(
            locations=data['locations']
        )
        
        try:
            db.session.add(new_location)
            db.session.commit()
            return jsonify({'message': 'Location created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Failed to create location', 'error': str(e)}), 500

    @app.route('/api/locations', methods=['GET'])
    def get_all_locations():
        locations = Locations.query.all()
        return jsonify([location.__dict__ for location in locations]), 200

    @app.route('/api/locations/<int:id>', methods=['GET'])
    def get_location(id):
        location = Locations.query.get(id)
        if location:
            return jsonify(location.__dict__), 200
        else:
            return jsonify({'message': 'Location not found'}), 404

    @app.route('/api/locations/<int:id>', methods=['PUT'])
    def update_location(id):
        data = request.json
        location = Locations.query.get(id)
        if location:
            location.locations = data.get('locations', location.locations)

            try:
                db.session.commit()
                return jsonify({'message': 'Location updated successfully'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'message': 'Failed to update location', 'error': str(e)}), 500
        else:
            return jsonify({'message': 'Location not found'}), 404

    @app.route('/api/locations/<int:id>', methods=['DELETE'])
    def delete_location(id):
        location = Locations.query.get(id)
        if location:
            try:
                db.session.delete(location)
                db.session.commit()
                return jsonify({'message': 'Location deleted successfully'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'message': 'Failed to delete location', 'error': str(e)}), 500
        else:
            return jsonify({'message': 'Location not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
