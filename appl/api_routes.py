from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, Blueprint, session
from datetime import datetime, timedelta
from flask_mail import Mail
from appl.db_models import db, User, WasteCollection, RecyclingEffort, Locations, WasteType, WasteCollectionSchedule, Notification
from appl.notifications import send_notification
from werkzeug.exceptions import BadRequestKeyError

app = Flask(__name__)
mail = Mail(app)
api = Blueprint('api', __name__)

def flash_message(message, category):
    flash(message, category)

def register_routes(app):
    # Web App Routes
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/dashboard')
    def dashboard():
        if 'username' in session:
            return render_template('dashboard.html')
        else:
            flash_message('You need to log in first.', 'error')
            return redirect(url_for('login'))

    @app.route('/tracker', methods=['GET', 'POST'])
    def tracker():
        if 'username' not in session:
            flash_message('You need to log in first.', 'error')
            return redirect(url_for('login'))

        username = session['username']

        if request.method == 'POST':
            waste_name = request.form['waste_type']
            amount = request.form['amount']

            new_recycling_effort = RecyclingEffort(username=username, waste_name=waste_name, amount=amount, date=datetime.utcnow())
            db.session.add(new_recycling_effort)
            db.session.commit()
            flash_message('Thank you for recycling! You are making the world cleaner.', 'success')
            return redirect(url_for('tracker'))

        records = RecyclingEffort.query.filter_by(username=username).order_by(RecyclingEffort.date.desc()).all()
        last_month_total = db.session.query(db.func.sum(RecyclingEffort.amount)).filter(
            db.func.strftime('%Y-%m', RecyclingEffort.date) == (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m'),
            RecyclingEffort.username == username
        ).scalar() or 0

        show_congrats = last_month_total > 0

        total_recycled = db.session.query(db.func.sum(RecyclingEffort.amount)).filter_by(username=username).scalar() or 0
        monthly_average = total_recycled / max(1, db.session.query(db.func.count(db.distinct(db.func.strftime('%Y-%m', RecyclingEffort.date)))).filter_by(username=username).scalar())

        current_month_total = db.session.query(db.func.sum(RecyclingEffort.amount)).filter(
            db.func.strftime('%Y-%m', RecyclingEffort.date) == datetime.utcnow().strftime('%Y-%m'),
            RecyclingEffort.username == username
        ).scalar() or 0

        # Data for the chart
        chart_labels = [record.date.strftime('%Y-%m-%d') for record in records]
        chart_data = [record.amount for record in records]

        return render_template('tracker_dashboard.html', records=records, last_month_total=last_month_total, show_congrats=show_congrats,
                            total_recycled=total_recycled, monthly_average=monthly_average, current_month_total=current_month_total,
                            chart_labels=chart_labels, chart_data=chart_data)


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            if not username or not password:
                flash_message('Username and password are required.', 'error')
                return redirect(url_for('login'))

            try:
                user = User.query.filter_by(username=username).first()

                if user and user.password == password:
                    session['username'] = user.username
                    flash_message('Login successful!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash_message('Invalid Username or password.', 'error')
                    return redirect(url_for('login'))

            except Exception as e:
                flash_message(f"An error occurred: {str(e)}", 'error')
                return redirect(url_for('login'))

        return render_template('index.html')

    @app.route('/logout')
    def logout():
        session.pop('username', None)
        flash_message('You have been logged out.', 'info')
        return redirect(url_for('login'))

    @app.route('/create_user', methods=['POST', 'GET'])
    def create_user():
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role')
            
            # Check if the role is valid
            valid_roles = ['household', 'admin', 'service']
            if role not in valid_roles:
                flash_message('Invalid role selected.', 'error')
                return redirect(url_for('create_user'))

            # Check for existing username and email
            if User.query.filter_by(username=username).first():
                flash_message('Username already exists.', 'error')
                return redirect(url_for('create_user'))
            if User.query.filter_by(email=email).first():
                flash_message('Email already exists.', 'error')
                return redirect(url_for('create_user'))

            # Validate form inputs
            if len(email) < 4:
                flash_message('Email must be greater than 3 characters.', 'error')
            elif len(username) < 2:
                flash_message('Username must be greater than 1 character.', 'error')
            elif len(password) < 7:
                flash_message('Password must be at least 7 characters.', 'error')
            else:
                # Create new user

                new_user = User(email=email, password=password, username=username, role=role) 
                
                db.session.add(new_user)
                db.session.commit()
                flash_message('User created successfully.', 'success')
                flash_message('Please login to continue', 'info')
                return redirect(url_for('login'))
                
        
        return render_template('index.html')

    @app.route('/schedule', methods=['GET', 'POST'])
    def schedule_collection():
        if request.method == 'POST':
            try:
                username = request.form.get('username')
                location = request.form.get('location')
                collection_date = datetime.strptime(request.form.get('collection_date'), '%Y-%m-%d')
                waste_type = request.form.get('waste_type')

                if not username or not location or not collection_date or not waste_type or location == 'none':
                    flash('All fields are required!', 'danger')
                    return redirect(url_for('schedule_collection'))

                new_schedule = WasteCollectionSchedule(
                    username=username,
                    location=location,
                    collection_date=collection_date,
                    waste_type=waste_type,
                    status='scheduled'
                )
                db.session.add(new_schedule)
                db.session.commit()
                send_notification(username, 'Collection scheduled successfully!', 'confirmation')
                flash('Collection scheduled successfully!', 'success')
                return redirect(url_for('schedule_collection'))
            
            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'danger')
                return redirect(url_for('schedule_collection'))
        today = datetime.today().strftime('%Y-%m-%d')
        return render_template('schedule.html', today=today)

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
                send_notification(schedule.username, 'Collection updated successfully!', 'update')
                flash_message('Schedule updated successfully!', 'success')
            else:
                flash_message('Schedule not found.', 'error')
            return redirect(url_for('update_schedule'))
        return render_template('update_schedule.html')

    @app.route('/notifications', methods=['GET'])
    def view_notifications():
        username = session.get('username')
        if not username:
            flash_message('You need to log in first.', 'error')
            return redirect(url_for('login'))
        notifications = Notification.query.filter_by(username=username).order_by(Notification.date.desc()).all()
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
        new_user = User(username=username, email=email, password=password, role=role)
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Failed to create user', 'error': str(e)}), 500

    @api.route('/users/<int:username>', methods=['GET'])
    def api_get_user(username):
        user = User.query.get(username)
        if user:
            return jsonify(user.__dict__), 200
        else:
            return jsonify({'message': 'User not found'}), 404

    @api.route('/users', methods=['GET'])
    def api_get_all_users():
        users = User.query.all()
        return jsonify([user.__dict__ for user in users]), 200

    @api.route('/users/<int:username>', methods=['PUT'])
    def api_update_user(username):
        if not request.is_json:
            return jsonify({'message': 'Unsupported Media Type'}), 415
        data = request.json
        user = User.query.get(username)
        if user:
            user.username = data.get('username', user.username)
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

    @api.route('/users/<int:username>', methods=['DELETE'])
    def api_delete_user(username):
        user = User.query.get(username)
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
            username=data['username'],
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
