from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, LoginManager, UserMixin
import secrets
import csv
from datetime import datetime
from sqlalchemy import func
from flask_mail import Mail, Message
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_phishing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Generate a random secret key

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@example.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your-email-password'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'  # Replace with your email

# Initialize database and mail
db = SQLAlchemy(app)
mail = Mail(app)

# Setup logging
logging.basicConfig(filename='submissions.log', level=logging.INFO)

# Define the database models
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    domain_type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # New role field

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define the routes
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    password = request.form['password']

    # Hash the password before storing
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Determine the domain type
    if email.endswith('@umassmemorial.org'):
        domain_type = 'trusted'
        feedback_message = (
            "Thank you for submitting your credentials. "
            "Your email is from a trusted domain, but remember to always double-check the sender’s email address for subtle changes or typos."
        )
    elif email.endswith('@gmail.com'):
        domain_type = 'free'
        feedback_message = (
            "It looks like you used a Gmail account. Be extra cautious with emails from free email providers like Gmail, Yahoo, or Hotmail. "
            "Phishers often use these to impersonate legitimate organizations."
        )
    else:
        domain_type = 'unknown'
        feedback_message = (
            "Caution: Your email is from an unfamiliar domain. "
            "Be very careful with such emails, especially if they ask for sensitive information or credentials."
        )

    # Save the email, hashed password, and domain type to the database
    new_submission = Submission(email=email, password=hashed_password, domain_type=domain_type)
    db.session.add(new_submission)
    db.session.commit()

    # Send an email alert to you
    send_email_alert(email)

    return render_template('feedback.html', message=feedback_message)

def send_email_alert(submitted_email):
    # Email configuration
    sender_email = "your_email@example.com"  # Replace with your email
    sender_password = "your_password"  # Replace with your email password
    recipient_email = "naesutton@gmail.com"  # Your email

    # Create the email
    subject = "New Submission Alert"
    body = f"A new submission has been made with the email: {submitted_email}."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Connect to the mail server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Using Gmail's SMTP server
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = 'user'  # Default role

        # Check if the user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "User already exists!"

        # Create a new user and save to the database
        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return "Invalid username or password!"
        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('app_login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    submissions_by_date = db.session.query(
        func.date(Submission.timestamp), func.count(Submission.id)
    ).group_by(func.date(Submission.timestamp)).all()

    dates = [str(date) for date, count in submissions_by_date]
    counts = [count for date, count in submissions_by_date]

    submissions = Submission.query.all()
    return render_template('dashboard.html', submissions=submissions, dates=dates, counts=counts)


@app.route('/export')
@login_required
def export_data():
    # Query all submissions from the database
    submissions = Submission.query.all()

    # Create a response object with CSV headers
    response = make_response()
    response.headers['Content-Disposition'] = 'attachment; filename=submissions.csv'
    response.headers['Content-Type'] = 'text/csv'

    # Use StringIO to write CSV data to the response
    import io
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write the header row
    writer.writerow(['ID', 'Email', 'Domain Type', 'Timestamp'])

    # Write the data rows
    for submission in submissions:
        writer.writerow([submission.id, submission.email, submission.domain_type, submission.timestamp])

    # Place the CSV data into the response
    response.data = output.getvalue()
    output.close()

    return response


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database and tables if they don't exist
    app.run(debug=True)
