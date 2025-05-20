from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
from utils.matching import load_data, train_tfidf, get_answer
from utils.preprocessing import preprocess
import datetime
import re  # For regular expressions


app = Flask(__name__)
app.secret_key = '5acf9c10e72aea640a15e8b3b8b5988e80ab2034ee38c8ec2fb7abf9b542e912'  # Change this to a random secret key

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['medibot_db']
users_collection = db['users']
chats_collection = db['chats']  # New collection for chats

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_data):
        self.user_data = user_data
    
    def get_id(self):
        return str(self.user_data['_id'])

    @property
    def username(self):
        return self.user_data['username']

@login_manager.user_loader
def load_user(user_id):
    try:
        user_data = users_collection.find_one({'_id': ObjectId(user_id)})
        return User(user_data) if user_data else None
    except:
        return None

# Load data and preprocess
df = load_data(r'C:/Users/ACER/OneDrive/Desktop/mca/pro2/medical_chatbot/Data/train.csv')
df['Processed_Question'] = df['Question'].apply(preprocess)

# Train TF-IDF
vectorizer, tfidf_matrix = train_tfidf(df, 'Processed_Question')

# Routes
@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = users_collection.find_one({'username': username})

        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data)
            login_user(user)
            return redirect(url_for('chat'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        emailid = request.form['emailid']
        password = request.form['password']

        # Username validation: 3 to 8 characters, alphanumeric only
        if not re.match(r'^[a-zA-Z0-9]{3,8}$', username):
            flash('Username must be 3 to 8 characters long and contain only letters and numbers.', 'error')
            return redirect(url_for('signup'))

        # Email validation: basic email format check
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', emailid):
            flash('Invalid email address. Please enter a valid email.', 'error')
            return redirect(url_for('signup'))

        # Password validation: at least 8 characters, 1 uppercase, 1 lowercase, 1 digit, 1 special character
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            flash('Password must be at least 8 characters long and contain at least 1 uppercase letter, 1 lowercase letter, 1 digit, and 1 special character.', 'error')
            return redirect(url_for('signup'))

        # Check if username already exists
        if users_collection.find_one({'username': username}):
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('signup'))

        # Check if email already exists
        if users_collection.find_one({'emailid': emailid}):
            flash('Email already exists. Please use a different email.', 'error')
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Insert user data into the database
        user_data = {
            'username': username,
            'emailid': emailid,
            'password': hashed_password
        }
        users_collection.insert_one(user_data)

        flash('Accounst created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/chat')
@login_required
def chat():
    return render_template('index.html', username=current_user.username)

@app.route('/chat', methods=['POST'])
@login_required
def chat_api():
    user_query = request.json.get('message')
    answer = get_answer(user_query, vectorizer, tfidf_matrix, df)
    return jsonify({"response": answer})

# New chat endpoints
@app.route('/save-chat', methods=['POST'])
@login_required
def save_chat():
    try:
        data = request.json
        chat_data = {
            "user_id": current_user.get_id(),
            "messages": data['messages'],
            "timestamp": datetime.datetime.utcnow()
        }
        
        result = chats_collection.insert_one(chat_data)
        return jsonify({
            "status": "success",
            "chat_id": str(result.inserted_id)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-chats', methods=['GET'])
@login_required
def get_chats():
    try:
        chats = list(chats_collection.find(
            {"user_id": current_user.get_id()},
            {"_id": 0, "messages": 1, "timestamp": 1}
        ).sort("timestamp", -1))
        
        # Convert datetime to strings
        for chat in chats:
            chat['timestamp'] = chat['timestamp'].isoformat()
        return jsonify(chats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)