from flask import *
from waste.forms import *
from waste.models import *
from flask_login import login_required, current_user, login_user, logout_user
from waste import *
from sqlalchemy import or_, and_
from waste.mailapi import *

def flash_message(message, category):
    flash(message, category)

# APP routes
def register_routes(app):
    
    #Home Route
    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('index.html')
    
    #Register Route
    @app.route('/register', methods=['GET', 'POST'])
    @app.route('/register/', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()

        if form.validate_on_submit():

            firstname = form.firstname.data
            secondname = form.secondname.data
            username = form.username.data
            email = form.email.data
            role = form.role.data
            password = form.password.data

            #Check if the user exists
            existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

            if existing_user:
                flash_message('Username or email already in use. Try again', 'danger')
                return render_template('register.html', form=form)
            else:
                new_user= User(firstname=firstname, secondname=secondname, username=username, email=email, role=role, password=password, confirmed=False)
                db.session.add(new_user)
                db.session.commit()
                send_confirmation_email(new_user.email)
                flash_message('A confirmation email has been sent via email. Please confirm your email to log in.', 'success')
                return redirect(url_for('login'))
            
        return render_template('register.html', form=form)
    
    # Email Confirmation Route
    @app.route('/confirm/<token>')
    def confirm_email(token):
        try:
            email = confirm_token(token)
        except:
            flash_message('The confirmation link is invalid or has expired.', 'danger')
            return redirect(url_for('resend_confirmation'))

        user = User.query.filter_by(email=email).first_or_404()
        if user.confirmed:
            flash_message('Account already confirmed. Please log in.', 'success')
        else:
            user.confirmed = True
            db.session.commit()
            flash_message('You have confirmed your account. Thanks!', 'success')
        return redirect(url_for('login'))
    
    # Re-send Confirmation Route
    @app.route('/resend_confirmation', methods=['GET', 'POST'])
    def resend_confirmation():
        form = ResendConfirmationForm()
        if form.validate_on_submit():
            email = form.email.data
            user = User.query.filter_by(email=email).first()
            if user and not user.confirmed:
                send_confirmation_email(user.email)
                flash_message('A new confirmation email has been sent.', 'success')
            else:
                flash_message('Email not found or already confirmed.', 'danger')
        return render_template('resend_confirmation.html', form=form)

    #Login Route
    @app.route('/login', methods=['GET', 'POST'])
    @app.route('/login/', methods=['GET', 'POST'])
    def login():
        form = LoginForm()

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            role = form.role.data

            # Check if user credentials are correct
            user = User.query.filter_by(username=username, role=role).first()
            if user and user.password == password:
                if not user.confirmed:
                    flash_message('Please confirm your email address first.', 'warning')
                    return redirect(url_for('resend_confirmation'))
                else:
                    login_user(user)
                    flash_message('User logged in successfully!', 'success') 

                # Redirect based on user role
                if user.role == 'Household':
                    print("Redirecting to house_dashboard")
                    return redirect(url_for('house_dashboard'))
                elif user.role == 'Collector':
                    print("Redirecting to collector_dashboard")
                    return redirect(url_for('collector_dashboard'))
                else:
                    flash_message('Invalid role. Please try again.', 'danger')
                    return redirect(url_for('login'))
            else:
                flash_message('Invalid username, role, or password. Please try again.', 'danger')
                return render_template('login.html', form=form)
        return render_template('login.html', form=form)
    
    #Forgot Password Route
    @app.route('/forgot_password', methods=['GET', 'POST'])
    def forgot_password():
        form = ForgotPasswordForm()

        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user:
                user.password = password
                db.session.commit()
                flash_message('Password updated successfully.', 'success')
                return redirect(url_for('login'))
        return render_template('forgot.html', form=form)
    
    #Household Dashboard
    @app.route('/house/dashboard')
    @login_required
    def house_dashboard():
        return render_template('house/dashboard.html')

    #Collector Dashboard
    @app.route('/collector/dashboard')
    @login_required
    def collector_dashboard():
        return render_template('collector/dashboard.html')