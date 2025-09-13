# 🏥 Saarva Health  
**Digital Healthcare for Kerala's Migrant Workforce**  

🔗 [Live Demo](https://saarva.streamlit.app/) | 💻 [GitHub Repository](https://github.com/Nitanshu715/Saarva-Health-for-All) | 📚 Documentation  

---

## 🌟 Overview  
**Saarva Health** is a digital healthcare platform built during **Smart India Hackathon 2024** to empower Kerala’s migrant workforce with **accessible, multilingual, and secure healthcare services**.  

It bridges the gap between patients, doctors, and hospitals by providing:  
- ✅ Centralized medical records (Electronic Health Records - EHR)  
- ✅ Doctor and hospital directories  
- ✅ Artificial Intelligence (AI) powered health analytics  
- ✅ Multilingual and user-friendly interface  

---

## 🎯 Problem Statement  
Kerala’s migrant workforce faces:  
- 🌐 **Language barriers** with healthcare providers  
- 📑 Lack of centralized medical records management  
- 🏥 Difficulty finding hospitals and specialists  
- ❌ Limited knowledge of local healthcare systems  

---

## 💡 Our Solution  
Saarva Health delivers a **one-stop healthcare ecosystem**:  
- **🔐 Digital Health Records**: Secure cloud-based storage and JSON (JavaScript Object Notation) backup  
- **🏥 Hospital Directory**: District-wise searchable hospital profiles  
- **👨‍⚕️ Doctor Network**: Browse and filter by specialization  
- **🤖 Artificial Intelligence Analytics**: Disease prediction and health trend insights  
- **👤 Personal Dashboard**: Track health goals and profile settings  

---

## 🚀 Features  

### 🔐 Authentication  
- Secure signup and login with **SHA-256 (Secure Hash Algorithm 256-bit) + salt hashing**  
- Profile picture support  
- Session management  

### 📊 Medical Records  
- Store consultations, laboratory tests, vaccinations, and surgeries  
- MongoDB (Mongo DataBase) cloud storage with JSON (JavaScript Object Notation) backup  
- Export and view in table or card formats  

### 🏥 Hospital Directory  
- Curated list of Kerala’s hospitals with details and images  
- Direct hospital links  

### 👨‍⚕️ Doctor Network  
- Search and filter doctors by specialization  
- Contact details and hospital affiliation  

### 🤖 Artificial Intelligence Analytics  
- **Random Forest Classifier** for disease risk prediction  
- Visualizations: disease distribution, age demographics, and trends  
- Interactive charts via Matplotlib and Seaborn  

### 👤 Profile  
- Manage personal information and health goals  
- Upload profile photo  
- Privacy-first data controls  

---

## 🛠️ Technology Stack  

**Frontend:** Streamlit, HTML (HyperText Markup Language), CSS (Cascading Style Sheets), JavaScript  
**Backend:** Python 3.8+, MongoDB (Mongo DataBase) Atlas, JSON (JavaScript Object Notation) for backup  
**Machine Learning and Analytics:** Scikit-learn, Pandas (Python Data Analysis Library), NumPy (Numerical Python), Matplotlib, Seaborn  
**Security:** Hashlib, Secrets (token generation), Base64 (encoding)  
**Extras:** Pillow (Python Imaging Library), PyMongo (Python MongoDB Integration)  

---

## 🎨 User Interface and Design  
- **Indian-inspired theme** (Saffron 🟧 + Purple 🟪)  
- Responsive design (desktop and mobile)  
- Accessibility-focused typography and navigation  

---

## 📦 Installation  

```bash
# Clone repository
git clone https://github.com/Nitanshu715/Saarva-Health-for-All.git
cd Saarva-Health-for-All

# Setup virtual environment
python -m venv saarva_env
source saarva_env/bin/activate   # Windows: saarva_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add MongoDB credentials in .env
MONGODB_URI=your_mongodb_connection_string

# Run application
streamlit run main.py
```

---

## 📈 Performance  
- ⚡ Load time: less than 3 seconds  
- 🗄️ Database response: less than 500 milliseconds  
- 🤖 Machine Learning accuracy: 85%+  
- 🔒 Encrypted storage and tokenized sessions  

---

## 🏆 Hackathon Recognition  
Built by **Team GenMinds** for **Smart India Hackathon 2024**  
Theme: *Digital Healthcare for Underserved Communities*  

👥 Team Roles:  
- **Garvit** – Team Leader, Artificial Intelligence and Machine Learning, Analytics  
- **Abhinav** – Backend Development and Security  
- **Vanshika and Vaani** – Data Analysis and Database Management  
- **Nitanshu** – Full-stack Development and Deployment  
- **Shagun** – User Interface/User Experience and Quality Assurance  

---

## 🚦 Roadmap  

### 🔄 Next Release (Version 2.0)  
- 📞 Telemedicine (video consultation)  
- 📱 Mobile Application (iOS and Android)  
- 🤖 Artificial Intelligence Chatbot for health queries  
- 🚑 SOS emergency features  

### 🎯 Long-term  
- Government integration with National Digital Health Mission (NDHM)  
- Expansion across India  
- Blockchain-secured health records  
- Internet of Things (IoT) device integration for live monitoring  

---

## 📚 Resources  
- [National Digital Health Mission (NDHM) Guidelines](https://ndhm.gov.in)  
- [Healthcare Dataset (Kaggle)](https://www.kaggle.com/datasets/prasad22/healthcare-dataset)  
- [Nature Article on Electronic Health Records](https://www.nature.com/articles/s41598-025-94339-w)  

---

## 📜 License  
Licensed under **MIT (Massachusetts Institute of Technology) License** © 2024 Team GenMinds  

---

## 📞 Contact  
📧 Email: genminds.sih2025@gmail.com  
🔗 [GitHub Repository](https://github.com/Nitanshu715/Saarva-Health-for-All) | [Live Demo](https://saarva.streamlit.app/)  

<div align="center">  
🚀 Built with ❤️ by **Team GenMinds** | Making Healthcare Accessible for All  
</div>
