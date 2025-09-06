# 🔐 Streamlit Login & Signup App

A simple yet **beautiful & modern authentication system** built with [Streamlit](https://streamlit.io/).  
This project allows users to **sign up, log in, and access a stylish interactive dashboard**—all using a secure **file-based JSON database** with salted SHA-256 password hashing.  

---

## ✨ Features

- 📝 **Signup & Login**
  - Stores credentials securely in `users.json`
  - Passwords are salted + hashed with SHA-256

- 🎨 **Modern Dashboard**
  - Gradient welcome card with hover animations
  - Metric cards that bounce on hover
  - Interactive line chart (Altair)
  - Action buttons with loaders & success messages
  - Stylish gradient logout button

- ⚡ **Lightweight**
  - No heavy DB required (runs with JSON file)
  - Runs locally with just Streamlit & a few libraries

---

## 📂 Project Structure
├── LoginSignup.py # Main app
├── users.json # Local DB (auto-created)
├── requirements.txt # Dependencies


---

## 🚀 Getting Started

### 1️⃣ Clone the repo
```bash
git clone https://github.com/your-username/streamlit-login-signup.git
cd streamlit-login-signup
```
### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Run the app
```bash
streamlit run LoginSignup.py
```
App will start at: http://localhost:8501

### 📦 Requirements
streamlit
altair
numpy
pandas
add more as you'd want......

### 🔒 Security Notes
- Passwords are never stored in plain text
- Each password is salted + hashed before saving
- For production, consider upgrading to PostgreSQL/MySQL backend

### 🤝 Contributing
Pull requests are welcome!
For major changes, please open an issue first to discuss what you’d like to change.

### 📜 License
MIT
