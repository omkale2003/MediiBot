🚀 Project Overview  

This Medical Chatbot Web App allows users to:  
💬 Ask health-related questions  
🤖 Get intelligent responses using TF-IDF NLP  
💾 Save and view past conversations  
🔐 Secure login and signup system  

Built with Flask and MongoDB, this project simulates a lightweight intelligent assistant for basic medical FAQs.

✨ Features  

✔ User Authentication (Signup/Login)  
✔ Medical Question Answering (using TF-IDF)  
✔ MongoDB-based Chat History  
✔ Clean UI with Bootstrap  
✔ Flash Messaging & Session Handling  

🛠 Technologies Used  

| Layer        | Tools/Frameworks                  |
|--------------|----------------------------------|
| Backend      | Python (Flask), Flask-Login      |
| NLP Engine   | Scikit-learn, Pandas, NLTK       |
| Frontend     | HTML, CSS, Bootstrap             |
| Database     | MongoDB with PyMongo             |
| Data Source  | `train.csv` of Q&A medical pairs |


🔧 Installation Guide  

Prerequisites  

- Python 3.8+  
- MongoDB (local or MongoDB Atlas)  
- Pip  

Steps  

1. Clone the repository
git clone https://github.com/yourusername/medical-chatbot.git
cd medical-chatbot

2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
or
source venv/bin/activate  # Linux/Mac

3. Install required packages
pip install -r requirements.txt

4. Configure your MongoDB connection in app.py
Example:
client = MongoClient("mongodb://localhost:27017/")

5. Run the application
python app.py

Open your browser and go to:
👉 `http://localhost:5000`

📂 Project Structure

medical-chatbot/
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── index.html
│   └── history.html
├── app.py
├── train.csv
├── requirements.txt
└── README.md



⚙ Configuration

To secure secrets, use a `.env` file:

```env
SECRET_KEY=your_secret_key
MONGO_URI=mongodb://localhost:27017/medibot
```

> Update `app.py` to load environment variables if needed.


💻 Usage

1. Register or log in
2. Ask medical questions in the chatbot
3. Receive answers and view your chat history
4. Logout securely when done


🖼 Screenshots

*(Insert UI screenshots here if available)*


🗃 Database Schema

Users Collection

```json
{
  "_id": ObjectId,
  "username": "john123",
  "emailid": "john@example.com",
  "password": "hashed_password"
}
```

Chats Collection

```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "messages": [
    {"sender": "user", "message": "What is a fever?"},
    {"sender": "bot", "message": "Fever is a temporary increase in body temperature."}
  ],
  "timestamp": ISODate
}
```

🔮 Future Enhancements

🧠 Add Machine Learning/Deep Learning models
🎤 Voice input and output
🌐 Multilingual support
📲 Mobile responsive UI or app version
👩‍⚕️ Doctor appointment system integration

🧠 Helping users make informed health decisions – one chat at a time.
