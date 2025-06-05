# 🏬 BizHunt – Pincode-Based Local Business Finder

**BizHunt** is a full-stack Django web application that helps users discover local businesses by pincode. It supports user and business registration, smart search powered by NLP, reviews, AI-driven recommendations, and a personalized experience for both consumers and business owners.


## 🚀 Features

- 🔍 **Pincode-Based Smart Search**  
  Find businesses near you using a pincode and get intelligent suggestions.

- 🧠 **AI-Powered Ranking**  
  Machine learning ranks businesses based on relevance and user engagement.

- 👤 **User & Business Registration**  
  Different roles for consumers and local business owners with secure authentication.

- ⭐ **Review & Rating System**  
  Logged-in users can rate and review local businesses.

- 📊 **Admin Dashboard**  
  View business listings, user engagement, and search trends.

- 🔐 **OAuth Login Integration**  
  Login securely via Google (keys stored using `.env` for security).


## 🧱 Tech Stack

| Layer       | Technology                       |
|-------------|----------------------------------|
| Backend     | Django, Django REST Framework    |
| Frontend    | HTML, CSS, JavaScript (Bootstrap)|
| Database    | SQLite (Dev), PostgreSQL (Prod)  |
| AI/NLP      | scikit-learn, spaCy              |
| Auth        | OAuth2 (Google) + Django AllAuth |
| Deployment  | Render / Heroku (optional)       |


## 📂 Project Structure

BizHunt/
├── BizHunt/ # Django project settings
├── business/ # Business listings app
├── reviews/ # Review & rating app
├── users/ # Authentication & profiles
├── templates/ # HTML templates
├── static/ # CSS, JS, static files
├── media/ # Uploaded logos/images
├── db.sqlite3 # Local DB (ignored in production)
├── .env # Environment variables (not tracked)
├── .gitignore # Git ignore config
└── requirements.txt # Python dependencies


## 📦 Setup Instructions

**i)Clone the Repo**

git clone https://github.com/SurabhiSupriya/BizHunt.git
cd BizHunt

**ii) Create Virtual Environment** 
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

**iii)Install Dependencies**

pip install -r requirements.txt

**iv)Add Environment Variables**
Create a .env file in the root directory:

GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret

**v)Run the Migrations**
python manage.py makemigrations
python manage.py migrate

**vi)Run the Server**

python manage.py runserver
Visit http://localhost:8000 in your browser.

💡 Future Enhancements
Business claim & verification flow

Advanced recommendation engine with collaborative filtering

Progressive Web App (PWA) support for mobile users

Analytics dashboard for business owners

**👩‍💻 Author**
Supriya Surabhi

![Screenshot 2025-06-05 134656](https://github.com/user-attachments/assets/604bc804-4e9b-4eb1-8192-6bac3c7899d7)
