from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, Blueprint, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from app.db_models import db, User, WasteCollection, RecyclingEffort, Locations, WasteType, WasteCollectionSchedule, Notification, Credentials

app = Flask(__name__)
mail = Mail(app)
api = Blueprint('api', __name__)

def register_routes(app):
    # Web App Routes
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/dashboard')
    def dashboard():
        if 'user_id' in session:
            return render_template('dashboard.html')
        else:
            flash('You need to log in first.', 'error')
            return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            id = request.form.get('id')
            password = request.form.get('password')
            try:
                user = Credentials.query.filter_by(id=id).first()
                if user and check_password_hash(user.password, password):
                    session['user_id'] = user.id
                    session['username'] = user.username
                    flash('Login successful!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid email or password.', 'error')
                if not id or not password:
                    flash('ID and password are required.', 'error')
                return redirect(url_for('login'))
            except Exception as e:
                flash(f"An error occurred: {str(e)}", 'error')
                return redirect(url_for('login'))
        return render_template('index.html')

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        session.pop('username', None)
        return redirect(url_for('login'))

    @app.route('/create_user', methods=['POST', 'GET'])
    def create_user():
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role')
            user = User.query.filter_by(username=username).first()
            if user:
                flash('Username already exists.', 'error')
                return redirect(url_for('create_user'))
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_password, role=role)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash(f'User created successfully. User ID: {new_user.id}', 'success')
                flash('Please login to continue', 'info')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash('Failed to create user', 'error')
                return redirect(url_for('create_user'))
        return render_template('index.html')

    @app.route('/schedule', methods=['GET', 'POST'])
    def schedule_collection():
        if request.method == 'POST':
            user_id = request.form['user_id']
            collection_date = datetime.strptime(request.form['collection_date'], '%Y-%m-%dT%H:%M')
            waste_type = request.form['waste_type']
            new_schedule = WasteCollectionSchedule(user_id=user_id, collection_date=collection_date, waste_type=waste_type, status='scheduled')
            db.session.add(new_schedule)
            db.session.commit()
            send_notification(user_id, 'Collection scheduled successfully!', 'confirmation')
            return redirect(url_for('schedule_collection'))
        return render_template('schedule.html')

    @app.route('/update_schedule', methods=['GET', 'POST'])
    def update_schedule():
        if request.method == 'POST':
            data = request.form
            schedule_id = data.get('schedule_id')
            collection_date = datetime.strptime(data.get('collection_date'), '%Y-%m-%d')
            waste_type = data.get('waste_type')
            schedule = WasteCollectionSchedule.query.get(schedule_id)
            if schedule:
                schedule.collection_date = collection_date
                schedule.waste_type = waste_type
                db.session.commit()
                send_notification(schedule.user_id, 'Collection updated successfully!', 'update')
                flash('Schedule updated successfully!', 'success')
            else:
                flash('Schedule not found.', 'error')
            return redirect(url_for('update_schedule'))
        return render_template('update_schedule.html')

    @app.route('/notifications', methods=['GET'])
    def view_notifications():
        user_id = session.get('user_id')
        if not user_id:
            flash('You need to log in first.', 'error')
            return redirect(url_for('login'))
        notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.date.desc()).all()
        return render_template('notifications.html', notifications=notifications)

    # API Routes
    @api.route('/users', methods=['POST'])
    def api_create_user():
        if not request.is_json:
            return jsonify({'message': 'Unsupported Media Type'}), 415
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({'message': 'Username already exists.'}), 409
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Failed to create user', 'error': str(e)}), 500

    @api.route('/users/<int:user_id>', methods=['GET'])
    def api_get_user(user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify(user.__dict__), 200
        else:
            return jsonify({'message': 'User not found'}), 404

    @api.route('/users', methods=['GET'])
    def api_get_all_users():
        users = User.query.all()
        return jsonify([user.__dict__ for user in users]), 200

    @api.route('/users/<int:user_id>', methods=['PUT'])
    def api_update_user(user_id):
        if not request.is_json:
            return jsonify({'message': 'Unsupported Media Type'}), 415
        data = request.json
        user = User.query.get(user_id)
        if user:
            user.username = data.get('username', user.username)
            user.role = data.get('role', user.role)
            user.email = data.get('email', user.email)
            user.password = generate_password_hash(data.get('password')) if data.get('password') else user.password
            try:
                db.session.commit()
                return jsonify({'message': 'User updated successfully'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'message': 'Failed to update user', 'error': str(e)}), 500
        else:
            return jsonify({'message': 'User not found'}), 404

    @api.route('/users/<int:user_id>', methods=['DELETE'])
    def api_delete_user(user_id):
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

    @api.route('/wastecollection', methods=['POST'])
    def api_create_waste_collection():
        if not request.is_json:
            return jsonify({'message': 'Unsupported Media Type'}), 415
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

    @api.route('/wastecollection', methods=['GET'])
    def api_get_all_collections():
        w_collections = WasteCollection.query.all()
        return jsonify([w_collection.__dict__ for w_collection in w_collections]), 200

    @api.route('/wastecollection/<int:id>', methods=['GET'])
    def api_get_collection(id):
        w_collection = WasteCollection.query.get(id)
        if w_collection:
            return jsonify(w_collection.__dict__), 200
        else:
            return jsonify({'message': 'Collection not found'}), 404

    @api.route('/wastecollection/<int:id>', methods=['PUT'])
    def api_update_collection(id):
        if not request.is_json:
            return jsonify({'message': 'Unsupported Media Type'}), 415
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

    @api.route('/wastecollection/<int:id>', methods=['DELETE'])
    def api_delete_collection(id):
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

    # Register the blueprint
    app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    register_routes(app)
    app.run(debug=True)
