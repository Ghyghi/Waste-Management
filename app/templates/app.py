from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_db_connection
import MySQLdb

app = Flask(__name__, template_folder='app/templates')
app.secret_key = 'your_secret_key'

def get_db_connection():
    return MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="",  # Replace with your MySQL password
        db="Smart_Waste",
        cursorclass=MySQLdb.cursors.DictCursor
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        db = None
        cursor = None
        try:
            db = get_db_connection()
            cursor = db.cursor()

            cursor.execute("SELECT id FROM users WHERE email = %s OR username = %s", (email, username))
            user = cursor.fetchone()

            if user:
                flash('Username or email already exists.', 'error')
                return redirect(url_for('register'))
            else:
                cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
                db.commit()
                flash('Registration successful!', 'success')
                return redirect(url_for('login'))

        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'error')
            return redirect(url_for('register'))

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = None
        cursor = None
        try:
            db = get_db_connection()
            cursor = db.cursor()

            cursor.execute("SELECT id, username, password FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password.', 'error')

        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'error')
            return redirect(url_for('login'))

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return f"Welcome, {session['username']}!"
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
