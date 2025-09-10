import streamlit as st
import hashlib
import json
import os
import secrets
import pandas as pd
import base64
from PIL import Image
import io
from datetime import datetime, date

USERS_FILE = "users.json"
PATIENTS_FILE = "patients.json"
RECORDS_FILE = "records.json"
DOCTORS_FILE = "doctors.json"
PROFILE_PICS_DIR = "profile_pics"
BG_IMAGE_PATH = "bg.jpg"
# Create profile pics directory if it doesn't exist
if not os.path.exists(PROFILE_PICS_DIR):
    os.makedirs(PROFILE_PICS_DIR)

# ---------- Indian Theme/Background ----------
def set_indian_theme():
    # Initialize dark mode state
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    
    # Check for background image
    bg_css = ""
    if os.path.exists(BG_IMAGE_PATH):
        try:
            with open(BG_IMAGE_PATH, "rb") as f:
                bg_img = base64.b64encode(f.read()).decode()
            bg_css = f"""
            .stApp {{
                background-image: url("data:image/jpg;base64,{bg_img}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                background-position: center;
            }}
            """
        except Exception as e:
            st.warning(f"Could not load background image: {e}")

    # Dark/Light mode colors
    if st.session_state.dark_mode:
        main_bg = "rgba(30, 30, 30, 0.94)"
        card_bg = "rgba(40, 40, 40, 0.95)"
        text_color = "#FFFFFF"
        secondary_text = "#CCCCCC"
        input_bg = "rgba(50, 50, 50, 0.98)"
        border_color = "rgba(100, 100, 100, 0.5)"
    else:
        main_bg = "rgba(255, 253, 250, 0.94)"
        card_bg = "rgba(255,255,255,0.95)"
        text_color = "#333333"
        secondary_text = "#666666"
        input_bg = "rgba(255, 255, 255, 0.98)"
        border_color = "rgba(255,153,51,0.3)"

    # Comprehensive Indian theme styling
    st.markdown(
        f"""
        <style>
        {bg_css}
        
        /* Main container styling */
        .main, [data-testid="stAppViewContainer"] {{
            background: {main_bg} !important;
            backdrop-filter: blur(10px);
            color: {text_color} !important;
        }}
        
        /* Hide default header */
        [data-testid="stHeader"] {{
            background: transparent !important;
            height: 0px !important;
        }}
        
        /* Indian color palette variables */
        :root {{
            --saffron: #FF9933;
            --white: #FFFFFF;
            --green: #138808;
            --navy: #000080;
            --purple: #8B4789;
            --gold: #FFD700;
            --maroon: #8B0000;
        }}
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {{
            width: 280px !important;
            min-width: 280px !important;
            background: linear-gradient(180deg, rgba(255,153,51,0.95) 0%, rgba(138,71,137,0.95) 100%);
            border-right: 3px solid var(--gold);
            padding: 20px;
        }}
        
        section[data-testid="stSidebar"] > div {{
            padding: 0 !important;
        }}
        
        /* Sidebar buttons - make them work normally */
        section[data-testid="stSidebar"] .stButton > button {{
            background: rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            border: 2px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 12px !important;
            width: 100% !important;
            padding: 12px 20px !important;
            margin: 8px 0 !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            text-align: left !important;
            transition: all 0.3s ease !important;
        }}
        
        section[data-testid="stSidebar"] .stButton > button:hover {{
            background: rgba(255, 255, 255, 0.25) !important;
            border-color: var(--gold) !important;
            transform: translateX(5px) !important;
            box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4) !important;
        }}
        
        /* Active button styling */
        section[data-testid="stSidebar"] .stButton > button[aria-pressed="true"] {{
            background: rgba(255, 255, 255, 0.95) !important;
            color: var(--purple) !important;
            border-color: var(--gold) !important;
            box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4) !important;
        }}
        
        /* Card styling */
        .dashboard-card, .app-card {{
            background: {card_bg} !important;
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(139,71,137,0.12);
            padding: 1.5rem;
            margin-bottom: 20px;
            border: 1px solid {border_color};
            color: {text_color} !important;
        }}
        
        /* Form elements */
        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stSelectbox > div > div > select {{
            background: {input_bg} !important;
            border: 2px solid {border_color} !important;
            border-radius: 10px !important;
            color: {text_color} !important;
            font-size: 14px !important;
        }}
        
        .stTextInput > div > div > input:focus,
        .stTextArea textarea:focus {{
            border-color: var(--purple) !important;
            box-shadow: 0 0 0 2px rgba(139,71,137,0.1) !important;
        }}
        
        /* Main content buttons */
        .stButton > button:not(section[data-testid="stSidebar"] .stButton > button) {{
            background: linear-gradient(135deg, var(--saffron) 0%, var(--purple) 100%);
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.5rem 1.5rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(255,153,51,0.25) !important;
        }}
        
        .stButton > button:not(section[data-testid="stSidebar"] .stButton > button):hover {{
            background: linear-gradient(135deg, var(--purple) 0%, var(--saffron) 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(139,71,137,0.3) !important;
        }}
        
        /* Logo and title */
        .indian-logo {{
            font-family: 'Georgia', serif;
            font-weight: 700;
            font-size: 2.5rem;
            background: linear-gradient(90deg, var(--saffron) 0%, var(--green) 50%, var(--purple) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 10px;
        }}
        
        .indian-subtitle {{
            font-size: 1.1rem;
            color: var(--purple);
            text-align: center;
            margin-bottom: 30px;
            font-style: italic;
        }}
        
        /* Metrics */
        [data-testid="metric-container"] {{
            background: {card_bg} !important;
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }}
        
        [data-testid="metric-container"] [data-testid="metric-label"] {{
            color: var(--purple) !important;
            font-weight: 600 !important;
        }}
        
        [data-testid="metric-container"] [data-testid="metric-value"] {{
            color: var(--saffron) !important;
            font-weight: 700 !important;
        }}
        
        /* Doctor cards */
        .doctor-card {{
            background: {card_bg} !important;
            padding: 1.2rem;
            margin-bottom: 15px;
            border-radius: 12px;
            border-left: 4px solid var(--saffron);
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            color: {text_color} !important;
        }}
        
        .doctor-card:hover {{
            transform: translateX(5px);
            box-shadow: 0 6px 18px rgba(139,71,137,0.15);
        }}
        
        .doctor-name {{
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--purple);
            margin-bottom: 5px;
        }}
        
        .doctor-speciality {{
            font-size: 0.95rem;
            color: var(--saffron);
            font-weight: 600;
            margin-bottom: 8px;
        }}
        
        .doctor-info {{
            font-size: 0.9rem;
            color: {secondary_text};
            line-height: 1.5;
        }}
        
        /* Profile picture styling */
        .profile-pic {{
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 4px solid var(--gold);
            object-fit: cover;
            margin: 0 auto;
            display: block;
        }}
        
        /* Alerts and info boxes */
        .stAlert {{
            background: {card_bg} !important;
            border: 1px solid {border_color} !important;
            border-radius: 10px !important;
            color: {text_color} !important;
        }}
        
        /* DataFrames */
        .stDataFrame {{
            border: 1px solid {border_color} !important;
            border-radius: 10px !important;
        }}
        
        /* Text colors for dark mode */
        .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {{
            color: {text_color} !important;
        }}
        
        /* Radio buttons and checkboxes */
        .stRadio > div, .stCheckbox > div {{
            color: {text_color} !important;
        }}
        
        /* Select boxes */
        .stSelectbox > div > div > div {{
            color: {text_color} !important;
        }}
        
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
        /* Hide code blocks that might appear accidentally */
        .stCodeBlock {{
            display: none !important;
        }}
        
        /* Modal/Dialog styling */
        .modal-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }}
        
        .modal-content {{
            background: {card_bg};
            border-radius: 16px;
            padding: 2rem;
            max-width: 600px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
            border: 2px solid var(--gold);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
        }}
        
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------- Utils ----------
def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except (json.JSONDecodeError, IOError) as e:
            st.warning(f"Error loading {path}: {e}")
            return default
    return default

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error saving {path}: {e}")

def load_users():
    return load_json(USERS_FILE, {})

def save_users(data: dict):
    save_json(USERS_FILE, data)

def make_password_hash(password: str, salt: str = None) -> str:
    if salt is None:
        salt = secrets.token_hex(16)
    h = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}${h}"

def verify_password(password: str, stored: str) -> bool:
    try:
        salt, h = stored.split("$", 1)
        return hashlib.sha256((salt + password).encode("utf-8")).hexdigest() == h
    except Exception:
        return False

def save_profile_pic(username, uploaded_file):
    """Save uploaded profile picture"""
    if uploaded_file is not None:
        try:
            # Create filename
            file_extension = uploaded_file.name.split('.')[-1]
            filename = f"{username}_profile.{file_extension}"
            filepath = os.path.join(PROFILE_PICS_DIR, filename)
            
            # Save file
            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            return filepath
        except Exception as e:
            st.error(f"Error saving profile picture: {e}")
    return None

def get_profile_pic_path(username):
    """Get profile picture path for user"""
    for ext in ['jpg', 'jpeg', 'png', 'gif']:
        filepath = os.path.join(PROFILE_PICS_DIR, f"{username}_profile.{ext}")
        if os.path.exists(filepath):
            return filepath
    return None

# ---------- Initialize default data ----------
def initialize_default_data():
    # Initialize doctors data if file doesn't exist or is empty
    if not os.path.exists(DOCTORS_FILE):
        default_doctors = {
            "doctors": [
                {"name": "Dr. Rajiv Narang", "hospital": "AIIMS Delhi", "phone": "011-26594681", "speciality": "Cardiology"},
                {"name": "Prof. Anita Saxena", "hospital": "AIIMS Delhi", "phone": "011-26594681", "speciality": "Cardiology"},
                {"name": "Prof. Balram Bhargava", "hospital": "AIIMS Delhi", "phone": "011-26594681", "speciality": "Cardiology"},
                {"name": "Dr. S. Seth", "hospital": "AIIMS Delhi", "phone": "011-26594681", "speciality": "Cardiology"},
                {"name": "Dr. R. Juneja", "hospital": "AIIMS Delhi", "phone": "011-26594681", "speciality": "Cardiology"},
                {"name": "Dr. P. Venugopal", "hospital": "AIIMS Delhi", "phone": "011-26594681", "speciality": "Cardiothoracic Surgery"},
                {"name": "Dr. A. Sampath Kumar", "hospital": "AIIMS Delhi", "phone": "011-26594681", "speciality": "Cardiothoracic Surgery"},
                {"name": "Dr. Balram Airan", "hospital": "AIIMS Delhi", "phone": "011-26594681", "speciality": "Cardiothoracic Surgery"},
                {"name": "Dr. B. L. Chaudhary", "hospital": "Lok Nayak Hospital, Delhi", "phone": "011-23862000", "speciality": "General Medicine"},
                {"name": "Dr. Anurag Rohtagi", "hospital": "Lok Nayak Hospital, Delhi", "phone": "011-23862000", "speciality": "Medicine"},
                {"name": "Dr. Surender Deora", "hospital": "AIIMS Jodhpur", "phone": "0291-2740144", "speciality": "Cardiology"},
                {"name": "Dr. Rahul Choudhary", "hospital": "AIIMS Jodhpur", "phone": "0291-2740144", "speciality": "Emergency Medicine"},
                {"name": "Dr. Sanjeev Gupta", "hospital": "Apollo Hospital, Bhubaneswar", "phone": "08093060206", "speciality": "General Surgery"},
                {"name": "Dr. E. C. Vinay Kumar", "hospital": "Apollo Hospital, Bhubaneswar", "phone": "916746661066", "speciality": "General Surgery"},
                {"name": "Dr. Amit Kumar Tyagi", "hospital": "AIIMS Rishikesh", "phone": "020-26128000", "speciality": "ENT"},
            ]
        }
        save_json(DOCTORS_FILE, default_doctors)
    
    # Initialize sample records if file doesn't exist
    if not os.path.exists(RECORDS_FILE):
        default_records = {
            "records": [
                {"date": "2025-01-15", "type": "Consultation", "doctor": "Dr. Rajiv Narang", "diagnosis": "Hypertension", "prescription": "Amlodipine 5mg"},
                {"date": "2025-02-20", "type": "Lab Test", "test": "Complete Blood Count", "result": "Normal", "lab": "AIIMS Lab"},
                {"date": "2025-03-10", "type": "Vaccination", "vaccine": "COVID-19 Booster", "center": "AIIMS Delhi"},
            ]
        }
        save_json(RECORDS_FILE, default_records)

# ---------- Record Addition Functions ----------
def show_add_record_dialog():
    """Display the add new record dialog"""
    st.markdown("### ➕ Add New Medical Record")
    
    with st.form("add_record_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Basic Information
            st.markdown("#### 📋 Basic Information")
            record_date = st.date_input(
                "Date",
                value=date.today(),
                help="Date of the medical record"
            )
            
            record_type = st.selectbox(
                "Record Type",
                ["Consultation", "Lab Test", "Vaccination", "Surgery", "Emergency", "Follow-up", "Other"],
                help="Type of medical record"
            )
            
            patient_id = st.text_input(
                "Patient ID",
                value=st.session_state.get('current_user', ''),
                help="Patient identification number"
            )
            
        with col2:
            # Medical Details
            st.markdown("#### 🏥 Medical Details")
            doctor_name = st.text_input(
                "Doctor Name",
                placeholder="e.g., Dr. Rajiv Narang",
                help="Name of the attending doctor"
            )
            
            hospital = st.text_input(
                "Hospital/Clinic",
                placeholder="e.g., AIIMS Delhi",
                help="Name of the hospital or clinic"
            )
            
            diagnosis = st.text_input(
                "Diagnosis",
                placeholder="e.g., Hypertension, Diabetes",
                help="Medical diagnosis or condition"
            )
        
        # Additional fields based on record type
        if record_type == "Lab Test":
            st.markdown("#### 🧪 Lab Test Details")
            col3, col4 = st.columns(2)
            with col3:
                test_name = st.text_input(
                    "Test Name",
                    placeholder="e.g., Complete Blood Count"
                )
            with col4:
                test_result = st.text_input(
                    "Test Result",
                    placeholder="e.g., Normal, Abnormal"
                )
            lab_name = st.text_input(
                "Laboratory",
                placeholder="e.g., AIIMS Lab"
            )
            
        elif record_type == "Vaccination":
            st.markdown("#### 💉 Vaccination Details")
            col3, col4 = st.columns(2)
            with col3:
                vaccine_name = st.text_input(
                    "Vaccine Name",
                    placeholder="e.g., COVID-19 Booster"
                )
            with col4:
                vaccination_center = st.text_input(
                    "Vaccination Center",
                    placeholder="e.g., AIIMS Delhi"
                )
            batch_number = st.text_input(
                "Batch Number (Optional)",
                placeholder="Vaccine batch number"
            )
            
        elif record_type == "Surgery":
            st.markdown("#### ⚕️ Surgery Details")
            col3, col4 = st.columns(2)
            with col3:
                surgery_type = st.text_input(
                    "Surgery Type",
                    placeholder="e.g., Appendectomy"
                )
            with col4:
                surgeon = st.text_input(
                    "Surgeon",
                    placeholder="e.g., Dr. Smith"
                )
            surgery_notes = st.text_area(
                "Surgery Notes",
                placeholder="Additional notes about the surgery"
            )
        
        # Common fields for all record types
        st.markdown("#### 📝 Additional Information")
        col5, col6 = st.columns(2)
        
        with col5:
            prescription = st.text_area(
                "Prescription/Treatment",
                placeholder="Medications prescribed or treatment given",
                height=100
            )
            
        with col6:
            notes = st.text_area(
                "Additional Notes",
                placeholder="Any additional notes or observations",
                height=100
            )
        
        symptoms = st.text_input(
            "Symptoms",
            placeholder="e.g., fever, headache, cough",
            help="Symptoms experienced by the patient"
        )
        
        # Form submission buttons
        col7, col8, col9 = st.columns([1, 1, 1])
        
        with col8:
            submitted = st.form_submit_button(
                "💾 Save Record",
                use_container_width=True,
                type="primary"
            )
        
        with col9:
            cancel = st.form_submit_button(
                "❌ Cancel",
                use_container_width=True
            )
    
    # Handle form submission
    if submitted:
        # Validate required fields
        if not all([record_date, record_type, patient_id]):
            st.error("⚠️ Please fill in all required fields (Date, Record Type, Patient ID)")
            return
        
        # Create new record
        new_record = {
            "date": record_date.strftime("%Y-%m-%d"),
            "type": record_type,
            "patient_id": patient_id,
            "doctor": doctor_name,
            "hospital": hospital,
            "diagnosis": diagnosis,
            "prescription": prescription,
            "notes": notes,
            "symptoms": symptoms
        }
        
        # Add specific fields based on record type
        if record_type == "Lab Test":
            new_record.update({
                "test": test_name,
                "result": test_result,
                "lab": lab_name
            })
        elif record_type == "Vaccination":
            new_record.update({
                "vaccine": vaccine_name,
                "center": vaccination_center,
                "batch_number": batch_number
            })
        elif record_type == "Surgery":
            new_record.update({
                "surgery_type": surgery_type,
                "surgeon": surgeon,
                "surgery_notes": surgery_notes
            })
        
        # Save to records file
        records_db = load_json(RECORDS_FILE, {"records": []})
        records_db["records"].append(new_record)
        save_json(RECORDS_FILE, records_db)
        
        st.success("✅ Medical record added successfully!")
        st.session_state.show_add_record = False
        st.rerun()
    
    if cancel:
        st.session_state.show_add_record = False
        st.rerun()

# ---------- Sidebar Navigation ----------
def show_sidebar():
    # Initialize navigation state
    if "selected_nav" not in st.session_state:
        st.session_state.selected_nav = "Dashboard"
    
    # Sidebar title
    st.sidebar.markdown("### 🏥 Navigation")
    st.sidebar.markdown("---")
    
    # Navigation buttons - simple and functional
    if st.sidebar.button("🏠 Dashboard", use_container_width=True):
        st.session_state.selected_nav = "Dashboard"
        st.rerun()
    
    if st.sidebar.button("📋 Medical Records", use_container_width=True):
        st.session_state.selected_nav = "Records"
        st.rerun()
    
    if st.sidebar.button("👨‍⚕️ Doctors", use_container_width=True):
        st.session_state.selected_nav = "Doctors"
        st.rerun()
    
    if st.sidebar.button("👤 Profile", use_container_width=True):
        st.session_state.selected_nav = "Profile"
        st.rerun()
    
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        logout()

# ---------- Home/Auth ----------
def show_landing():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='indian-logo'>🏥 Saarva Health</div>", unsafe_allow_html=True)
        st.markdown("<div class='indian-subtitle'>Empowering India with Digital Healthcare</div>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            show_login()
        
        with tab2:
            show_signup()

def show_login():
    with st.form("login_form", clear_on_submit=False):
        st.markdown("### Welcome Back!")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("🔐 Login", use_container_width=True)
        with col2:
            st.form_submit_button("Forgot Password?", use_container_width=True)
    
    if submit:
        if not username or not password:
            st.error("⚠️ Please enter both username and password")
            return
        
        user_info = st.session_state.user_data.get(username)
        if user_info and verify_password(password, user_info.get("password", "")):
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success("✅ Login successful!")
            st.balloons()
            st.rerun()
        else:
            st.error("❌ Invalid credentials")

def show_signup():
    with st.form("signup_form", clear_on_submit=False):
        st.markdown("### Create Account")
        new_username = st.text_input("Choose Username", placeholder="Pick a unique username")
        new_password = st.text_input("Create Password", type="password", placeholder="Strong password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
        agree = st.checkbox("I agree to the Terms and Conditions")
        submit = st.form_submit_button("📝 Sign Up", use_container_width=True)
    
    if submit:
        if not all([new_username, new_password, confirm_password]):
            st.error("⚠️ All fields are required")
            return
        if not agree:
            st.error("⚠️ Please agree to the Terms and Conditions")
            return
        if new_username in st.session_state.user_data:
            st.error("❌ Username already exists")
            return
        if new_password != confirm_password:
            st.error("❌ Passwords don't match")
            return
        if len(new_password) < 6:
            st.error("⚠️ Password must be at least 6 characters")
            return
        
        st.session_state.user_data[new_username] = {"password": make_password_hash(new_password)}
        save_users(st.session_state.user_data)
        st.success("✅ Account created successfully! Please login.")

# ---------- Dashboard Pages ----------
def dashboard_home():
    st.markdown(
        f"""
        <div class="dashboard-card">
            <h1 style='color:#8B4789; margin-bottom: 10px;'>Welcome, {st.session_state.get('current_user', 'User')} 👋</h1>
            <p style='color:#FF9933; font-size: 1.1rem;'>Your personalized health dashboard</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Visits", "12", "↑ 2 this month")
    with col2:
        st.metric("Active Doctors", "15", "↑ 3 new")
    with col3:
        st.metric("Lab Reports", "8", "2 pending")
    with col4:
        st.metric("Health Score", "85%", "↑ 5%")
    
    st.markdown("---")
    
    # Disease Prediction Section
    st.markdown("### 🔬 AI Disease Prediction")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        symptoms = st.text_area(
            "Enter your symptoms",
            placeholder="e.g., fever, headache, cough, body ache",
            height=100
        )
    
    with col2:
        st.markdown("##### Quick Symptoms")
        if st.button("🤒 Fever"):
            symptoms = "fever"
        if st.button("🤕 Headache"):
            symptoms = "headache"
        if st.button("🤧 Cold & Cough"):
            symptoms = "cold, cough, sneezing"
    
    if st.button("🔍 Analyze Symptoms", use_container_width=True):
        if symptoms:
            with st.spinner("Analyzing symptoms..."):
                import time
                time.sleep(2)
            
            st.success("### Prediction Results")
            col1, col2 = st.columns(2)
            with col1:
                st.info("""
                **Possible Condition:** Viral Infection  
                **Confidence:** 78%  
                **Severity:** Mild to Moderate
                """)
            with col2:
                st.warning("""
                **Recommended Actions:**
                - Rest and hydration
                - Monitor temperature
                - Consult doctor if symptoms persist
                """)
            
            st.download_button(
                "📄 Download Full Report",
                "Detailed medical report content here...",
                file_name="medical_report.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("Please enter symptoms to get prediction")

def dashboard_records():
    st.markdown("<h1 style='color:#8B4789;'>📋 Medical Records</h1>", unsafe_allow_html=True)
    
    # Initialize the show_add_record state
    if "show_add_record" not in st.session_state:
        st.session_state.show_add_record = False
    
    # Show add record dialog if requested
    if st.session_state.show_add_record:
        show_add_record_dialog()
        return
    
    # Load records
    records_db = load_json(RECORDS_FILE, {"records": []})
    
    if records_db.get("records"):
        # Display options
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            view_type = st.radio("View as:", ["Cards", "Table"], horizontal=True)
        with col2:
            st.write("")  # Empty space
        with col3:
            if st.button("➕ Add New Record", use_container_width=True):
                st.session_state.show_add_record = True
                st.rerun()
        
        st.markdown("---")
        
        if view_type == "Table":
            df = pd.DataFrame(records_db["records"])
            st.dataframe(df, use_container_width=True, height=400)
        else:
            for record in records_db["records"]:
                record_display = ""
                for key, value in record.items():
                    if value:  # Only show non-empty values
                        record_display += f"**{key.title().replace('_', ' ')}:** {value}<br>"
                
                st.markdown(
                    f"""
                    <div class="dashboard-card">
                        <h4 style='color:#FF9933;'>{record.get('type', 'Record')} - {record.get('date', 'N/A')}</h4>
                        <p>{record_display}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("📭 No medical records found. Your medical history will appear here.")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("➕ Add Your First Record", use_container_width=True):
                st.session_state.show_add_record = True
                st.rerun()

def dashboard_contacts():
    st.markdown("<h1 style='color:#8B4789;'>👨‍⚕️ Doctor Directory</h1>", unsafe_allow_html=True)
    
    # Load doctors data
    doctors_db = load_json(DOCTORS_FILE, {})
    
    if doctors_db and "doctors" in doctors_db and doctors_db["doctors"]:
        # Search and filter
        col1, col2 = st.columns([2, 1])
        with col1:
            search = st.text_input("🔍 Search doctors", placeholder="Name, hospital, or speciality")
        with col2:
            specialities = list(set([d.get("speciality", "Unknown") for d in doctors_db["doctors"]]))
            filter_spec = st.selectbox("Filter by Speciality", ["All"] + specialities)
        
        # Filter doctors
        filtered_doctors = doctors_db["doctors"]
        if search:
            search_lower = search.lower()
            filtered_doctors = [
                d for d in filtered_doctors 
                if search_lower in d.get("name", "").lower() 
                or search_lower in d.get("hospital", "").lower()
                or search_lower in d.get("speciality", "").lower()
            ]
        
        if filter_spec != "All":
            filtered_doctors = [d for d in filtered_doctors if d.get("speciality") == filter_spec]
        
        # Display doctors
        st.markdown(f"**Found {len(filtered_doctors)} doctors**")
        
        for doc in filtered_doctors:
            st.markdown(
                f"""
                <div class="doctor-card">
                    <div class="doctor-name">{doc.get('name', 'Unknown')}</div>
                    <div class="doctor-speciality">🏥 {doc.get('speciality', 'General')}</div>
                    <div class="doctor-info">
                        <strong>Hospital:</strong> {doc.get('hospital', 'N/A')}<br>
                        <strong>Phone:</strong> 📞 {doc.get('phone', 'N/A')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.error("❌ No doctor information available. Please check if the doctors.json file exists and is properly formatted.")
        
        # Show sample format
        with st.expander("Expected JSON format for doctors.json"):
            st.code("""
{
  "doctors": [
    {
      "name": "Dr. Name",
      "hospital": "Hospital Name",
      "phone": "Phone Number",
      "speciality": "Speciality"
    }
  ]
}
            """)

def dashboard_profile():
    st.markdown("<h1 style='color:#8B4789;'>👤 My Profile</h1>", unsafe_allow_html=True)
    
    user = st.session_state.get("current_user", "Guest")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Profile picture section
        profile_pic_path = get_profile_pic_path(user)
        
        if profile_pic_path and os.path.exists(profile_pic_path):
            # Display existing profile picture
            try:
                with open(profile_pic_path, "rb") as f:
                    img_data = f.read()
                img_b64 = base64.b64encode(img_data).decode()
                st.markdown(
                    f"""
                    <div style='text-align: center; padding: 20px;'>
                        <img src="data:image/jpeg;base64,{img_b64}" class="profile-pic" />
                        <div style='margin-top: 10px; font-size: 1.1rem; color: #8B4789;'>{user}</div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            except Exception as e:
                # Fallback to default avatar
                st.markdown(
                    f"""
                    <div style='text-align: center; padding: 20px;'>
                        <div style='width: 120px; height: 120px; background: linear-gradient(135deg, #FF9933, #8B4789); 
                                    border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                                    margin: 0 auto; color: white; font-size: 48px; font-weight: bold;'>
                            {user[0].upper()}
                        </div>
                        <div style='margin-top: 10px; font-size: 1.1rem; color: #8B4789;'>{user}</div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        else:
            # Default avatar
            st.markdown(
                f"""
                <div style='text-align: center; padding: 20px;'>
                    <div style='width: 120px; height: 120px; background: linear-gradient(135deg, #FF9933, #8B4789); 
                                border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                                margin: 0 auto; color: white; font-size: 48px; font-weight: bold;'>
                        {user[0].upper()}
                    </div>
                    <div style='margin-top: 10px; font-size: 1.1rem; color: #8B4789;'>{user}</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        # Profile picture upload
        st.markdown("#### Update Profile Picture")
        uploaded_file = st.file_uploader(
            "Choose a profile picture", 
            type=['png', 'jpg', 'jpeg', 'gif'],
            help="Upload a new profile picture (PNG, JPG, JPEG, GIF)"
        )
        
        if uploaded_file is not None:
            if st.button("💾 Save Profile Picture"):
                saved_path = save_profile_pic(user, uploaded_file)
                if saved_path:
                    st.success("✅ Profile picture updated!")
                    st.rerun()
                else:
                    st.error("❌ Failed to save profile picture")
        
    with col2:
        st.markdown("#### Account Details")
        st.info(f"""
        **Username:** {user}  
        **Status:** Active  
        **Member Since:** 2025  
        **Role:** Patient  
        """)
        
        if st.button("🔒 Change Password"):
            st.info("Password change functionality coming soon!")

    st.markdown("---")
    st.markdown("#### App Preferences")
    st.checkbox("Enable Notifications", value=True)
    
    # Dark Mode Toggle
    dark_mode = st.checkbox("Dark Mode", value=st.session_state.get("dark_mode", False))
    if dark_mode != st.session_state.get("dark_mode", False):
        st.session_state.dark_mode = dark_mode
        st.rerun()
    
    st.text_area("Health Goals", placeholder="Describe your personal health goals...")

def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.selected_nav = "Dashboard"
    if "show_add_record" in st.session_state:
        del st.session_state.show_add_record
    st.success("👋 Logged out successfully!")
    st.rerun()

# ---------- Main App Logic ----------
def main():
    # Page configuration
    st.set_page_config(
        page_title="Saarva Health - Digital Healthcare",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Set theme
    set_indian_theme()

    # Initialize data files
    initialize_default_data()

    # Load users into session state
    if "user_data" not in st.session_state:
        st.session_state.user_data = load_users()

    # Check login status
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.current_user = None

    # Show home/login/signup page if not logged in
    if not st.session_state.logged_in:
        show_landing()
        return
    
    # Show sidebar navigation
    show_sidebar()
    
    # Dashboard: Select page
    nav = st.session_state.get("selected_nav", "Dashboard")
    if nav == "Dashboard":
        dashboard_home()
    elif nav == "Records":
        dashboard_records()
    elif nav == "Doctors":
        dashboard_contacts()
    elif nav == "Profile":
        dashboard_profile()
    elif nav == "Logout":
        logout()
    else:
        st.error("Unknown navigation option!")

if __name__ == "__main__":
    main()
