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
import streamlit.components.v1 as components
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
import plotly.graph_objects as go
import pymongo

# MongoDB connection
try:
    client = pymongo.MongoClient("mongodb+srv://SAARVA:SAARVA_123@cluster0.tnivgkn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["saarva_health"]
    patients_new = db["patients_new"]
    records_collection = db["records"]  # Renamed to avoid conflict
    MONGODB_CONNECTED = True
except Exception as e:
    MONGODB_CONNECTED = False
    print(f"MongoDB connection failed: {e}")

def add_patient_to_db(name, age, gender):
    if MONGODB_CONNECTED:
        try:
            patient_doc = {"name": name, "age": age, "gender": gender}
            result = patients_new.insert_one(patient_doc)
            return str(result.inserted_id)
        except:
            return None
    return None

def get_all_patients_from_db():
    if MONGODB_CONNECTED:
        try:
            return list(patients_new.find({}, {"_id": 0}))
        except:
            return []
    return []

def add_record_to_db(record_data):
    if MONGODB_CONNECTED:
        try:
            records_collection.insert_one(record_data)
            return True
        except:
            return False
    return False

def get_all_records_from_db():
    if MONGODB_CONNECTED:
        try:
            return list(records_collection.find({}, {"_id": 0}))
        except:
            return []
    return []
# Configuration
USERS_FILE = "users.json"
PATIENTS_FILE = "patients.json"
RECORDS_FILE = "records.json"
DOCTORS_FILE = "doctors.json"
PROFILE_PICS_DIR = "profile_pics"
LOGO_PATH = "logo.png"
PHOTOS_DIR = "photos"

# Create directories if they don't exist
for directory in [PROFILE_PICS_DIR, PHOTOS_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

def set_indian_theme():
    """Set the Indian-themed styling for the application"""
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
        
    # Color scheme
    if st.session_state.dark_mode:
        main_bg = "#1e1e1e"
        card_bg = "#2d2d2d"
        text_color = "#FFFFFF"
        secondary_text = "#CCCCCC"
        input_bg = "#3d3d3d"
        border_color = "#555555"
        sidebar_bg = "linear-gradient(180deg, rgba(45,45,45,0.95) 0%, rgba(60,60,60,0.95) 100%)"
    else:
        main_bg = "#FFFDF8"
        card_bg = "#FFFFFF"
        text_color = "#333333"
        secondary_text = "#666666"
        input_bg = "#FFFFFF"
        border_color = "rgba(255,153,51,0.3)"
        sidebar_bg = "linear-gradient(180deg, rgba(255,153,51,0.95) 0%, rgba(138,71,137,0.95) 100%)"
    
    st.markdown(
        f"""
        <style>
        /* Hide default elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        [data-testid="stHeader"] {{background: transparent !important; height: 0px !important;}}
        
        /* Main container */
        .main .block-container {{
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            margin-top: 0rem !important;
            max-width: 100% !important;
        }}
        
        .stApp {{background: {main_bg} !important;}}
        .main {{padding: 0 !important;}}
        
        /* Color variables */
        :root {{
            --saffron: #FF9933;
            --purple: #8B4789;
            --gold: #FFD700;
            --green: #138808;
        }}
        
        /* Landing page logo */
        .logo-container.landing {{
            position: relative !important;
            top: 15% !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            width: 150px !important;
            height: 150px !important;
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255,255,255,0.95);
            border-radius: 50%;
            box-shadow: 0 8px 32px rgba(139,71,137,0.15);
        }}
        
        .logo-container.landing img {{
            width: 120px !important;
            height: 120px !important;
            border-radius: 50%;
        }}
        
        /* Dashboard logo */
        .logo-container:not(.landing) {{
            position: fixed !important;
            top: 10px !important;
            left: relative !important;
            width: 80px !important;
            height: 80px !important;
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255,255,255,0.95);
            border-radius: 50%;
            box-shadow: 0 4px 16px rgba(139,71,137,0.15);
            transition: left 0.3s ease;
        }}
        section[data-testid="stSidebar"][aria-expanded="false"] ~ div .logo-container:not(.landing) {{
    left: 10px !important;
}}
        .logo-container:not(.landing) img {{
            width: 60px !important;
            height: 60px !important;
            border-radius: 50%;
        }}
        
        /* Sidebar collapsed logo position */
        .css-1d391kg + div .logo-container:not(.landing) {{left: 10px !important;}}
        
        /* Landing page layout */
        .landing-page-wrapper {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 1vh;
            padding: 0;
            margin: 0;
        }}
        /* Remove sidebar artifacts */
.css-1d391kg {{
    background: transparent !important;
    box-shadow: none !important;
}}

/* Ensure main content fills properly */
.main .block-container {{
    background: {main_bg} !important;
}}

/* Remove any residual sidebar styling */
section[data-testid="stSidebar"]:not([aria-expanded="true"]) {{
    box-shadow: none !important;
    border: none !important;
}}
        .landing-subtitle {{
            font-size: 1.2rem;
            color: var(--saffron);
            text-align: center;
            margin: 20px 0;
            font-style: italic;
        }}
        
        /* Sidebar styling */
        /* Sidebar styling - remove all artifacts */
section[data-testid="stSidebar"] {{
    background: {sidebar_bg} !important;
    border-right: 3px solid var(--gold);
    box-shadow: none !important;
}}

/* Remove sidebar container artifacts */
.css-1d391kg {{
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
}}

/* Remove any residual styling when sidebar is collapsed */
.css-1d391kg:not([aria-expanded="true"]) {{
    background: {main_bg} !important;
    width: 0 !important;
}}
        
        section[data-testid="stSidebar"] h3 {{
            color: white !important;
            font-weight: 700 !important;
            text-align: center !important;
            margin-bottom: 10px !important;
            margin-top: 0 !important;
            font-size: 1.1rem !important;
        }}
        
        section[data-testid="stSidebar"] .stButton > button {{
            background: rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
            width: 100% !important;
            padding: 12px 16px !important;
            margin: 4px 0 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
        }}
        
        section[data-testid="stSidebar"] .stButton > button:hover {{
            background: rgba(255, 255, 255, 0.2) !important;
            border-color: var(--gold) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3) !important;
            color: var(--gold) !important;
        }}
        
        section[data-testid="stSidebar"] hr {{
            border: none !important;
            height: 1px !important;
            background: rgba(255, 255, 255, 0.2) !important;
            margin: 15px 0 !important;
        }}
        
        /* Overlapping banner */
        .dashboard-banner {{
            position: fixed !important;
            top: 0 !important;
            left: 280px !important;
            right: 0 !important;
            z-index: 999 !important;
            background: rgba(255,153,51,0.95) !important;
            backdrop-filter: blur(10px) !important;
            border-bottom: 2px solid var(--purple) !important;
            padding: 10px 0 !important;
            transition: left 0.3s ease !important;
        }}
        section[data-testid="stSidebar"][aria-expanded="false"] ~ div .dashboard-banner {{
    left: 0 !important;
}}
        .css-1d391kg ~ div .dashboard-banner {{left: 0 !important;}}
        
        /* Main content with banner spacing */
        .main-content-with-banner {{
            margin-top: 1px !important;
            padding-top: 1px !important;
        }}
        /* Override Streamlit main container spacing */
div.block-container {{
    padding-top: 0 !important;
    margin-top: 0 !important;
}}

/* Also force vertical blocks to remove spacing */
[data-testid="stVerticalBlock"] {{
    margin-top: 0 !important;
    padding-top: 0 !important;
}}
        /* Cards */
        .dashboard-card {{
            background: {card_bg} !important;
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(139,71,137,0.12);
            padding: 1.5rem;
            margin-bottom: 20px;
            border: 1px solid {border_color};
            color: {text_color} !important;
        }}
        
        .hospital-card {{
            background: {card_bg} !important;
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(139,71,137,0.12);
            overflow: hidden;
            margin-bottom: 20px;
            border: 1px solid {border_color};
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .hospital-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 32px rgba(139,71,137,0.2);
        }}
        
        .hospital-image {{
            width: 100%;
            height: 200px;
            object-fit: cover;
        }}
        
        .hospital-content {{
            padding: 1.5rem;
            color: {text_color} !important;
        }}
        
        .hospital-name {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--saffron);
            margin-bottom: 8px;
        }}
        
        .hospital-description {{
            font-size: 0.9rem;
            color: {secondary_text};
            line-height: 1.5;
            margin-bottom: 12px;
        }}
        
        .hospital-link {{
            color: var(--green);
            font-weight: 600;
            text-decoration: none;
        }}
        
        /* Profile pictures */
        .dashboard-profile-pic {{
            width: 250px;
            height: 250px;
            border-radius: 50%;
            border: 3px solid var(--gold);
            object-fit: cover;
            float: right;
            margin-right: 15px;
            margin-top: -50px;
        }}
        
        .dashboard-profile-default {{
            width: 250px;
            height: 250px;
            border-radius: 50%;
            background: linear-gradient(135deg, #FF9933, #8B4789);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 48px;
            font-weight: bold;
            float: right;
            margin-right: 15px;
            margin-top: -50px;
        }}
        
        /* Buttons */
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
        
        /* Forms */
        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stSelectbox > div > div > select {{
            background: {input_bg} !important;
            border: 2px solid {border_color} !important;
            border-radius: 10px !important;
            color: {text_color} !important;
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
        
        /* Text colors */
        .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {{
            color: {text_color} !important;
        }}
        
        /* Login/Signup tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0px !important;
            border: none !important;
            background: transparent !important;
            box-shadow: none !important;
            margin-bottom: 0px !important;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            height: auto !important;
            background: transparent !important;
            color: {text_color} !important;
            border: none !important;
            border-radius: 0px !important;
            box-shadow: none !important;
            padding: 0 16px !important;
            font-size: 1.02rem !important;
            font-weight: 600 !important;
            transition: color 0.2s;
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
            color: var(--purple) !important;
            background: transparent !important;
            text-decoration: underline;
        }}
        
        .stTabs [aria-selected="true"] {{
            color: var(--saffron) !important;
            background: transparent !important;
            border-bottom: 2.5px solid var(--saffron) !important;
            border-radius: 0 !important;
            box-shadow: none !important;
        }}
        
        /* Analytics specific styling */
        .analytics-card {{
            background: {card_bg} !important;
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(139,71,137,0.12);
            padding: 2rem;
            margin-bottom: 20px;
            border: 1px solid {border_color};
            color: {text_color} !important;
            position: relative;
            border-left: 4px solid var(--saffron);
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, var(--saffron) 0%, var(--purple) 100%) !important;
            color: white !important;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 6px 20px rgba(139,71,137,0.2);
            transition: transform 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
        }}
        
        .metric-value {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        
        .metric-label {{
            font-size: 1rem;
            opacity: 0.9;
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
        
        /* Profile page styling */
        .profile-header {{
            background: {card_bg};
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(139,71,137,0.12);
            margin-bottom: 2rem;
            border: 1px solid {border_color};
        }}
        
        .profile-pic-large {{
            width: 150px;
            height: 150px;
            border-radius: 50%;
            border: 4px solid var(--gold);
            object-fit: cover;
            margin: 0 auto 20px auto;
            display: block;
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        }}
        
        .profile-pic-default-large {{
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: linear-gradient(135deg, #FF9933, #8B4789);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 60px;
            font-weight: bold;
            margin: 0 auto 20px auto;
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        }}
        
        .profile-info-card {{
            background: {card_bg};
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 16px rgba(139,71,137,0.08);
            border: 1px solid {border_color};
            margin-bottom: 1.5rem;
        }}
        
        .info-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid {border_color};
        }}
        
        .info-item:last-child {{
            border-bottom: none;
        }}
        
        .info-label {{
            font-weight: 600;
            color: var(--purple);
            font-size: 0.95rem;
        }}
        
        .info-value {{
            color: {text_color};
            font-weight: 500;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------- Analytics Functions ----------
@st.cache_data
def load_analytics_data():
    """Load and preprocess the dataset for analytics"""
    try:
        # Try different possible paths for the dataset
        possible_paths = [
            "src/data/dataset_with_random_year.csv",
            "src/data/dataset_with_random_year.xlsx", 
            "data/dataset_with_random_year.csv",
            "data/dataset_with_random_year.xlsx",
            "dataset_with_random_year.csv",
            "dataset_with_random_year.xlsx"
        ]
        
        df = None
        for path in possible_paths:
            if os.path.exists(path):
                if path.endswith('.xlsx'):
                    df = pd.read_excel(path)
                else:
                    df = pd.read_csv(path)
                break
        
        if df is None:
            # Create sample data if file not found
            np.random.seed(42)
            sample_data = {
                'Medical_Condition': np.random.choice(['Diabetes', 'Hypertension', 'Asthma', 'Arthritis', 'Heart Disease'], 1000),
                'Age': np.random.randint(20, 80, 1000),
                'Admission_Year': np.random.randint(2020, 2025, 1000),
                'Area': np.random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata'], 1000)
            }
            df = pd.DataFrame(sample_data)
        
        # Clean column names
        df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
        
        # Drop rows with any missing values
        df.dropna(inplace=True)
        
        # Convert Admission_Year to integer
        if 'Admission_Year' in df.columns:
            df['Admission_Year'] = df['Admission_Year'].astype(int)
        
        return df
    
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def train_analytics_model(df):
    """Train the disease prediction model"""
    try:
        if df is None or df.empty:
            return None, None
        
        # Features for the model
        features = ['Admission_Year', 'Age'] if 'Admission_Year' in df.columns else ['Age']
        X = df[features].copy()
        y = df['Medical_Condition']
        
        # Encode the categorical target variable
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)
        
        # Train a Random Forest Classifier
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y_encoded)
        
        return model, le
    
    except Exception as e:
        st.error(f"Error training model: {e}")
        return None, None

def create_analytics_visualizations(df):
    """Create interactive visualizations using Plotly"""
    try:
        if df is None or df.empty:
            return None, None, None, None
        disease_counts = df['Medical_Condition'].value_counts().reset_index()
        disease_counts.columns = ['Medical_Condition', 'count']
        
        # Chart 1: Disease Distribution
        fig1 = px.bar(
            disease_counts,
            x='Medical_Condition', y='count',
            title='Disease Distribution',
            labels={'Medical_Condition': 'Medical Condition', 'count': 'Number of Cases'},
            color='Medical_Condition',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig1.update_layout(
            title_font_size=20,
            title_x=0.5,
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        # Chart 2: Age Distribution by Disease
        fig2 = px.histogram(
            df, x='Age', color='Medical_Condition',
            title='Age Distribution by Disease',
            nbins=20,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig2.update_layout(
            title_font_size=20,
            title_x=0.5,
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        # Chart 3: Disease Cases by Area (if Area column exists)
        fig3 = None
        if 'Area' in df.columns:
            area_disease = df.groupby(['Area', 'Medical_Condition']).size().reset_index(name='count')
        fig3 = px.bar(
        area_disease, x='Area', y='count', color='Medical_Condition',
        title='Disease Cases by Area',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
        fig3.update_layout(
        title_font_size=20,
        title_x=0.5,
        xaxis_title_font_size=14,
        yaxis_title_font_size=14,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

        # Chart 4: Yearly Trends (if Admission_Year column exists)
        fig4 = None
        if 'Admission_Year' in df.columns:
            yearly_data = df.groupby(['Admission_Year', 'Medical_Condition']).size().reset_index(name='count')
            fig4 = px.line(
                yearly_data, x='Admission_Year', y='count', color='Medical_Condition',
                title='Disease Trends Over Years',
                color_discrete_sequence=px.colors.qualitative.Dark24
            )
            fig4.update_layout(
                title_font_size=20,
                title_x=0.5,
                xaxis_title_font_size=14,
                yaxis_title_font_size=14,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
        
        return fig1, fig2, fig3, fig4
    
    except Exception as e:
        st.error(f"Error creating visualizations: {e}")
        return None, None, None, None

def load_json(path, default):
    """Load JSON file with error handling"""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return default
    return default

def save_json(path, data):
    """Save data to JSON file"""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error saving {path}: {e}")

def make_password_hash(password: str) -> str:
    """Create password hash with salt"""
    salt = secrets.token_hex(16)
    h = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}${h}"

def verify_password(password: str, stored: str) -> bool:
    """Verify password against stored hash"""
    try:
        salt, h = stored.split("$", 1)
        return hashlib.sha256((salt + password).encode("utf-8")).hexdigest() == h
    except:
        return False

def display_logo():
    """Display logo based on login state"""
    if os.path.exists(LOGO_PATH):
        try:
            with open(LOGO_PATH, "rb") as f:
                logo_data = f.read()
            logo_b64 = base64.b64encode(logo_data).decode()
            
            logo_class = "logo-container landing" if not st.session_state.get('logged_in', False) else "logo-container"
            
            st.markdown(
                f"""
                <div class="{logo_class}">
                    <img src="data:image/png;base64,{logo_b64}" />
                </div>
                """,
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Error loading logo: {e}")

def get_dashboard_profile_pic(username):
    """Get HTML for dashboard profile picture"""
    profile_pic_path = None
    for ext in ['jpg', 'jpeg', 'png', 'gif']:
        filepath = os.path.join(PROFILE_PICS_DIR, f"{username}_profile.{ext}")
        if os.path.exists(filepath):
            profile_pic_path = filepath
            break
    
    if profile_pic_path:
        try:
            with open(profile_pic_path, "rb") as f:
                img_data = f.read()
            img_b64 = base64.b64encode(img_data).decode()
            return f'<img src="data:image/jpeg;base64,{img_b64}" class="dashboard-profile-pic" />'
        except:
            pass
    
    return f'<div class="dashboard-profile-default">{username[0].upper()}</div>'

def get_hospitals_data():
    """Get hospital data for display"""
    return [
        {
            "location": "🏥 Thiruvananthapuram",
            "hospitals": [
                {
                    "name": "KIMSHEALTH Trivandrum",
                    "description": "A leading multi-specialty hospital offering advanced healthcare services.",
                    "image": "KIMSHEALTH_Trivandrum.jpeg",
                    "website": "https://www.kimshealth.org/"
                },
                {
                    "name": "Ananthapuri Hospitals & Research Institute",
                    "description": "Known for its comprehensive medical services and research initiatives.",
                    "image": "Ananthapuri_Hospitals_and_Research_Institute.jpg",
                    "website": "https://www.ananthapurihospitals.com/"
                }
            ]
        },
        {
            "location": "🏥 Kochi",
            "hospitals": [
                {
                    "name": "Aster Medcity",
                    "description": "A quaternary care facility with international accreditation and a wide range of specialties.",
                    "image": "Aster_Medcity.jpg",
                    "website": "https://www.asterhospitals.in/"
                },
                {
                    "name": "Rajagiri Hospital",
                    "description": "Offers top-notch care in oncology, orthopedics, and cardiac sciences.",
                    "image": "Rajagiri_Hospital.jpg",
                    "website": "https://www.rajagirihospital.com/"
                }
            ]
        },
        {
            "location": "🏥 Kozhikode",
            "hospitals": [
                {
                    "name": "Aster MIMS",
                    "description": "A multi-specialty hospital with expertise in cardiac sciences, oncology, and neuroscience.",
                    "image": "Aster_MIMS.jpeg",
                    "website": "https://www.asterhospitals.in/"
                },
                {
                    "name": "Starcare Hospital",
                    "description": "Known for its comprehensive diagnostic and treatment facilities across various specialties.",
                    "image": "Starcare_Hospital.avif",
                    "website": "https://www.starcarehospitals.com/"
                }
            ]
        },
        {
            "location": "🏥 Kollam",
            "hospitals": [
                {
                    "name": "KIMSHEALTH Kollam",
                    "description": "A top multi-specialty hospital offering specialized care with experienced doctors and nursing staff.",
                    "image": "KIMSHEALTH_Kollam.jpg",
                    "website": "https://www.kimshealth.org/kollam/"
                },
                {
                    "name": "Meditrina Hospital",
                    "description": "Provides advanced medical services with a focus on patient care and comfort.",
                    "image": "Meditrina_Hospital.jpg",
                    "website": "https://www.meditrinahospitals.com/"
                }
            ]
        },
        {
            "location": "🏥 Thrissur",
            "hospitals": [
                {
                    "name": "Atreya Hospital",
                    "description": "Renowned for its world-class healthcare services, especially in surgical specialties and neurosurgery.",
                    "image": "Atreya_Hospital.jpeg",
                    "website": "https://www.atreyahospital.co.in/"
                },
                {
                    "name": "Elite Mission Hospital",
                    "description": "Offers trusted medical services, advanced diagnostics, and 24/7 emergency support.",
                    "image": "Elite_Mission_Hospital.jpeg",
                    "website": "https://elitemissionhospital.com/"
                }
            ]
        },
        {
            "location": "🏥 Kannur",
            "hospitals": [
                {
                    "name": "Aster MIMS Kannur",
                    "description": "Provides comprehensive healthcare with international standards in cardiology, neurology, and oncology.",
                    "image": "Aster_MIMS_Kannur.jpeg",
                    "website": "https://www.asterhospitals.in/hospitals/aster-mims-kannur"
                },
                {
                    "name": "Koyili Hospital",
                    "description": "Known for its excellent medical expertise, nursing care, and quality diagnostic services.",
                    "image": "Koyili_Hospital.jpg",
                    "website": "https://koyilihospital.org/"
                }
            ]
        }
    ]

def show_dashboard_banner():
    """Display the typing animation banner"""
    st.markdown(
        '''
        <div class="dashboard-banner">
            <div style="text-align:center;">
                <span id="typing-text" style="font-size:18px; font-weight:700; color:white; font-family:'Poppins', sans-serif;"></span>
            </div>
        </div>
        <script>
        const texts = ["Being Healthy, Keeps Stay Happy", "Empowering Healthcare Access for Kerala's Migrant Workforce"];
        let count = 0, index = 0, currentText = '', letter = '';
        function type(){
            if(count === texts.length){ count = 0; }
            currentText = texts[count];
            letter = currentText.slice(0, ++index);
            document.getElementById("typing-text").textContent = letter;
            if(letter.length === currentText.length){
                count++;
                index = 0;
                setTimeout(type, 700);
            } else {
                setTimeout(type, 40);
            }
        }
        type();
        </script>
        ''',
        unsafe_allow_html=True
    )

def initialize_default_data():
    """Initialize default JSON data files"""
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
    
    if not os.path.exists(RECORDS_FILE):
        default_records = {
            "records": [
                {"date": "2025-01-15", "type": "Consultation", "doctor": "Dr. Rajiv Narang", "diagnosis": "Hypertension", "prescription": "Amlodipine 5mg"},
                {"date": "2025-02-20", "type": "Lab Test", "test": "Complete Blood Count", "result": "Normal", "lab": "AIIMS Lab"},
                {"date": "2025-03-10", "type": "Vaccination", "vaccine": "COVID-19 Booster", "center": "AIIMS Delhi"},
            ]
        }
        save_json(RECORDS_FILE, default_records)

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

def show_add_record_dialog():
    """Display the add new record dialog with comprehensive health fields"""
    st.markdown("### Add New Medical Record")
    
    with st.form("add_record_form", clear_on_submit=True):
        # Main layout with two columns like your brother's design
        col_personal, col_medical = st.columns([0.4, 0.6])
        
        with col_personal:
            st.markdown("#### Personal Information")
            
            # Basic patient info
            full_name = st.text_input("Full Name", placeholder="Enter patient name")
            mobile = st.text_input("Mobile Number", placeholder="Enter mobile")
            address = st.text_area("Address", max_chars=200, height=100, placeholder="Enter current address")
            
            col_age, col_gender = st.columns(2)
            with col_age:
                age = st.slider("Age", 0, 120, 25)
            with col_gender:
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            
            # Record metadata
            st.markdown("#### Record Details")
            record_date = st.date_input(
                "Date",
                value=date.today(),
                help="Date of the medical record"
            )
            
            record_type = st.selectbox(
                "Record Type",
                ["Consultation", "Lab Test", "Vaccination", "Surgery", "Emergency", "Follow-up", "Health Checkup", "Other"],
                help="Type of medical record"
            )
            
            patient_id = st.text_input(
                "Patient ID",
                value=st.session_state.get('current_user', ''),
                help="Patient identification number"
            )
            
        with col_medical:
            st.markdown("#### Health Information")
            
            # Physical measurements
            col_height, col_weight = st.columns(2)
            with col_height:
                height_cm = st.slider("Height (cm)", 30, 250, 170)
            with col_weight:
                weight_kg = st.slider("Weight (kg)", 1, 300, 70)
            
            # Vital signs
            col_bp, col_sugar = st.columns(2)
            with col_bp:
                blood_pressure = st.text_input("Blood Pressure", placeholder="e.g., 120/80 mmHg")
            with col_sugar:
                blood_sugar = st.text_input("Blood Sugar", placeholder="mg/dL")
            
            # Medical history fields
            allergies = st.text_area("Allergies", max_chars=100, height=70, placeholder="List any known allergies")
            existing_conditions = st.text_area("Existing Health Conditions", max_chars=200, height=100, placeholder="Current medical conditions")
            current_medications = st.text_area("Current Medications", max_chars=200, height=100, placeholder="Medications being taken")
            recent_symptoms = st.text_area("Recent Symptoms / Tests", max_chars=200, height=100, placeholder="Recent symptoms or test results")
        
        # Medical professional details
        st.markdown("#### Medical Professional Details")
        col_doc, col_hospital = st.columns(2)
        with col_doc:
            doctor_name = st.text_input(
                "Doctor Name",
                placeholder="e.g., Dr. Rajiv Narang",
                help="Name of the attending doctor"
            )
        with col_hospital:
            hospital = st.text_input(
                "Hospital/Clinic",
                placeholder="e.g., AIIMS Delhi",
                help="Name of the hospital or clinic"
            )
        
        # Diagnosis and treatment
        st.markdown("#### Diagnosis & Treatment")
        diagnosis = st.text_input(
            "Diagnosis",
            placeholder="e.g., Hypertension, Diabetes",
            help="Medical diagnosis or condition"
        )
        
        col_prescription, col_notes = st.columns(2)
        with col_prescription:
            prescription = st.text_area(
                "Prescription/Treatment",
                placeholder="Medications prescribed or treatment given",
                height=100
            )
        with col_notes:
            notes = st.text_area(
                "Additional Notes",
                placeholder="Any additional notes or observations",
                height=100
            )
        
        # Additional fields based on record type
        if record_type == "Lab Test":
            st.markdown("#### Lab Test Details")
            col3, col4 = st.columns(2)
            with col3:
                test_name = st.text_input(
                    "Test Name",
                    placeholder="e.g., Complete Blood Count"
                )
                lab_name = st.text_input(
                    "Laboratory",
                    placeholder="e.g., AIIMS Lab"
                )
            with col4:
                test_result = st.text_input(
                    "Test Result",
                    placeholder="e.g., Normal, Abnormal"
                )
                test_values = st.text_area(
                    "Test Values",
                    placeholder="Detailed test results",
                    height=70
                )
            
        elif record_type == "Vaccination":
            st.markdown("#### Vaccination Details")
            col3, col4 = st.columns(2)
            with col3:
                vaccine_name = st.text_input(
                    "Vaccine Name",
                    placeholder="e.g., COVID-19 Booster"
                )
                batch_number = st.text_input(
                    "Batch Number",
                    placeholder="Vaccine batch number"
                )
            with col4:
                vaccination_center = st.text_input(
                    "Vaccination Center",
                    placeholder="e.g., AIIMS Delhi"
                )
                next_dose = st.date_input(
                    "Next Dose Date (if applicable)",
                    value=None
                )
            
        elif record_type == "Surgery":
            st.markdown("#### Surgery Details")
            col3, col4 = st.columns(2)
            with col3:
                surgery_type = st.text_input(
                    "Surgery Type",
                    placeholder="e.g., Appendectomy"
                )
                surgeon = st.text_input(
                    "Surgeon",
                    placeholder="e.g., Dr. Smith"
                )
            with col4:
                surgery_duration = st.text_input(
                    "Duration",
                    placeholder="e.g., 2 hours"
                )
                anesthesia_type = st.text_input(
                    "Anesthesia Type",
                    placeholder="e.g., General"
                )
            surgery_notes = st.text_area(
                "Surgery Notes",
                placeholder="Detailed notes about the surgery",
                height=80
            )
        
        # Form submission buttons
        st.markdown("---")
        col7, col8, col9 = st.columns([1, 1, 1])
        
        with col8:
            submitted = st.form_submit_button(
                "Save Record",
                use_container_width=True,
                type="primary"
            )
        
        with col9:
            cancel = st.form_submit_button(
                "Cancel",
                use_container_width=True
            )
    
    # Handle form submission
    if submitted:
        # Validate required fields
        if not all([record_date, record_type, full_name]):
            st.error("Please fill in all required fields (Date, Record Type, Full Name)")
            return
        
        # Create comprehensive new record
        new_record = {
            "date": record_date.strftime("%Y-%m-%d"),
            "type": record_type,
            "patient_id": patient_id,
            "full_name": full_name,
            "age": age,
            "gender": gender,
            "mobile": mobile,
            "address": address,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "blood_pressure": blood_pressure,
            "blood_sugar": blood_sugar,
            "allergies": allergies,
            "existing_conditions": existing_conditions,
            "current_medications": current_medications,
            "recent_symptoms": recent_symptoms,
            "doctor": doctor_name,
            "hospital": hospital,
            "diagnosis": diagnosis,
            "prescription": prescription,
            "notes": notes
        }
        # Save to MongoDB first (if connected)
        if add_record_to_db(new_record):
            st.success("Medical record saved to database!")
        else:
            st.warning("Database unavailable, saving locally only")
    
        # Always save to JSON as backup
        records_db = load_json(RECORDS_FILE, {"records": []})
        records_db["records"].append(new_record)
        save_json(RECORDS_FILE, records_db)
    
        st.success("Medical record added successfully!")
        st.session_state.show_add_record = False
        st.rerun()
        # Add specific fields based on record type
        if record_type == "Lab Test":
            new_record.update({
                "test_name": test_name,
                "test_result": test_result,
                "lab_name": lab_name,
                "test_values": test_values if 'test_values' in locals() else ""
            })
        elif record_type == "Vaccination":
            new_record.update({
                "vaccine_name": vaccine_name,
                "vaccination_center": vaccination_center,
                "batch_number": batch_number,
                "next_dose": next_dose.strftime("%Y-%m-%d") if 'next_dose' in locals() and next_dose else ""
            })
        elif record_type == "Surgery":
            new_record.update({
                "surgery_type": surgery_type,
                "surgeon": surgeon,
                "surgery_duration": surgery_duration if 'surgery_duration' in locals() else "",
                "anesthesia_type": anesthesia_type if 'anesthesia_type' in locals() else "",
                "surgery_notes": surgery_notes if 'surgery_notes' in locals() else ""
            })
        
        # Save to records file
        records_db = load_json(RECORDS_FILE, {"records": []})
        records_db["records"].append(new_record)
        save_json(RECORDS_FILE, records_db)
        
        st.success("Comprehensive medical record added successfully!")
        st.balloons()  # Celebration effect
        st.session_state.show_add_record = False
        st.rerun()
    
    if cancel:
        st.session_state.show_add_record = False
        st.rerun()

def show_sidebar():
    """Display sidebar navigation"""
    if "selected_nav" not in st.session_state:
        st.session_state.selected_nav = "Dashboard"
    
    st.sidebar.markdown("### Navigation")
    st.sidebar.markdown("---")
    
    nav_items = ["Dashboard", "Medical Records", "Doctors", "Analytics", "Profile"]
    for item in nav_items:
        if st.sidebar.button(item, use_container_width=True):
            st.session_state.selected_nav = item
            st.rerun()
    
    st.sidebar.markdown("---")
    
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.selected_nav = "Dashboard"
        st.success("Logged out successfully!")
        st.rerun()

def show_landing():
    """Display landing page with login/signup"""
    st.markdown('<div class="landing-page-wrapper">', unsafe_allow_html=True)
    
    st.markdown(
        '<div style="text-align: center;"><div class="landing-subtitle">Empowering India with Digital Healthcare</div></div>',
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            show_login()
        
        with tab2:
            show_signup()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_login():
    """Display login form"""
    with st.form("login_form", clear_on_submit=False):
        st.markdown("### Welcome Back!")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Login", use_container_width=True)
        with col2:
            st.form_submit_button("Forgot Password?", use_container_width=True)
    
    if submit:
        if not username or not password:
            st.error("Please enter both username and password")
            return
        
        user_info = st.session_state.user_data.get(username)
        if user_info and verify_password(password, user_info.get("password", "")):
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success("Login successful!")
            st.balloons()
            st.rerun()
        else:
            st.error("Invalid credentials")

def show_signup():
    """Display signup form"""
    with st.form("signup_form", clear_on_submit=False):
        st.markdown("### Create Account")
        new_username = st.text_input("Choose Username", placeholder="Pick a unique username")
        new_password = st.text_input("Create Password", type="password", placeholder="Strong password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
        agree = st.checkbox("I agree to the Terms and Conditions")
        submit = st.form_submit_button("Sign Up", use_container_width=True)
    
    if submit:
        if not all([new_username, new_password, confirm_password]):
            st.error("All fields are required")
            return
        if not agree:
            st.error("Please agree to the Terms and Conditions")
            return
        if new_username in st.session_state.user_data:
            st.error("Username already exists")
            return
        if new_password != confirm_password:
            st.error("Passwords don't match")
            return
        if len(new_password) < 6:
            st.error("Password must be at least 6 characters")
            return
        
        st.session_state.user_data[new_username] = {"password": make_password_hash(new_password)}
        save_json(USERS_FILE, st.session_state.user_data)
        st.success("Account created successfully! Please login.")

def dashboard_home():
    """Main dashboard page with beautiful UI"""
    user = st.session_state.get('current_user', 'User')
    profile_pic_html = get_dashboard_profile_pic(user)
    
    st.markdown('<div class="main-content-with-banner">', unsafe_allow_html=True)
    
    # Welcome section
    st.markdown(
        f"""
        <div class="dashboard-card">
            {profile_pic_html}
            <h1 style='color:#8B4789; margin-bottom: 10px;'>Welcome, {user}</h1>
            <p style='color:#FF9933; font-size: 1.1rem;'>Your personalized health dashboard</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Visits", "12", "2 this month")
    with col2:
        st.metric("Active Doctors", "15", "3 new")
    with col3:
        st.metric("Lab Reports", "8", "2 pending")
    with col4:
        st.metric("Health Score", "85%", "5%")
    
    st.markdown("---")
    
    # Top Hospitals Section
    st.markdown("### Top Hospitals")
    
    hospitals_data = get_hospitals_data()
    
    for location_data in hospitals_data:
        st.markdown(f"#### {location_data['location']}")
        
        cols = st.columns(2)
        
        for idx, hospital in enumerate(location_data['hospitals']):
            with cols[idx % 2]:
                # Check if image exists
                image_path = os.path.join(PHOTOS_DIR, hospital['image'])
                if os.path.exists(image_path):
                    try:
                        with open(image_path, "rb") as f:
                            img_data = f.read()
                        img_b64 = base64.b64encode(img_data).decode()
                        img_html = f'<img src="data:image/jpeg;base64,{img_b64}" class="hospital-image" alt="{hospital["name"]}" />'
                    except:
                        img_html = '<div style="width:100%; height:200px; background: linear-gradient(135deg, #FF9933, #8B4789); display:flex; align-items:center; justify-content:center; color:white; font-size:24px; font-weight:bold;">🏥</div>'
                else:
                    img_html = '<div style="width:100%; height:200px; background: linear-gradient(135deg, #FF9933, #8B4789); display:flex; align-items:center; justify-content:center; color:white; font-size:24px; font-weight:bold;">🏥</div>'
                
                # Create hospital card
                st.markdown(
                    f"""
                    <a href="{hospital['website']}" target="_blank" style="text-decoration: none;">
                        <div class="hospital-card">
                            {img_html}
                            <div class="hospital-content">
                                <div class="hospital-name">{hospital['name']}</div>
                                <div class="hospital-description">{hospital['description']}</div>
                                <a href="{hospital['website']}" class="hospital-link" target="_blank">🔗 Website</a>
                            </div>
                        </div>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Contact Us Section
    st.markdown("### Contact Us")
    st.markdown(
        """
        <div style='text-align:center; background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.1); margin-bottom: 2rem;'>
            <h3 style='color:#8B4789; margin-bottom: 1.5rem;'>Get in Touch</h3>
            <div style='margin-bottom: 1rem;'>
                <strong style='color:#FF9933; font-size: 1.1rem;'>Phone:</strong> 
                <span style='font-size: 1.1rem;'>+91 98765 43210</span>
            </div>
            <div style='margin-bottom: 1rem;'>
                <strong style='color:#FF9933; font-size: 1.1rem;'>Email:</strong> 
                <span style='font-size: 1.1rem;'>SaarvaHealth@gmail.com</span>
            </div>
            <p style='color:#666; margin-top: 1rem; font-style: italic;'>
                We're here to help with your healthcare needs 24/7
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

def dashboard_records():
    """Medical records page"""
    st.markdown('<div class="main-content-with-banner">', unsafe_allow_html=True)
    
    st.markdown("<h1 style='color:#8B4789;'>Medical Records</h1>", unsafe_allow_html=True)
     # Load records from both MongoDB and JSON
    mongo_records = get_all_records_from_db()
    json_records = load_json(RECORDS_FILE, {"records": []}).get("records", [])
    
    # Combine and deduplicate records
    all_records = mongo_records + json_records
    # Remove duplicates based on date, type, and patient_id
    seen = set()
    unique_records = []
    for record in all_records:
        key = (record.get('date'), record.get('type'), record.get('patient_id'))
        if key not in seen:
            seen.add(key)
            unique_records.append(record)
    # Initialize the show_add_record state
    if "show_add_record" not in st.session_state:
        st.session_state.show_add_record = False
    
    # Show add record dialog if requested
    if st.session_state.show_add_record:
        show_add_record_dialog()
        st.markdown('</div>', unsafe_allow_html=True)
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
            if st.button("Add New Record", use_container_width=True):
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
        st.info("No medical records found. Your medical history will appear here.")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Add Your First Record", use_container_width=True):
                st.session_state.show_add_record = True
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def dashboard_doctors():
    """Doctor directory page"""
    st.markdown('<div class="main-content-with-banner">', unsafe_allow_html=True)
    
    st.markdown("<h1 style='color:#8B4789;'>Doctor Directory</h1>", unsafe_allow_html=True)
    
    # Load doctors data
    doctors_db = load_json(DOCTORS_FILE, {})
    
    if doctors_db and "doctors" in doctors_db and doctors_db["doctors"]:
        # Search and filter
        col1, col2 = st.columns([2, 1])
        with col1:
            search = st.text_input("Search doctors", placeholder="Name, hospital, or speciality")
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
                    <div class="doctor-speciality">{doc.get('speciality', 'General')}</div>
                    <div class="doctor-info">
                        <strong>Hospital:</strong> {doc.get('hospital', 'N/A')}<br>
                        <strong>Phone:</strong> {doc.get('phone', 'N/A')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.error("No doctor information available. Please check if the doctors.json file exists and is properly formatted.")
        
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
    
    st.markdown('</div>', unsafe_allow_html=True)

def dashboard_analytics():
    """Advanced Analytics Dashboard with Disease Prediction Model"""
    st.markdown('<div class="main-content-with-banner">', unsafe_allow_html=True)
    
    st.markdown("<h1 style='color:#8B4789; text-align:center;'>Healthcare Analytics Dashboard</h1>", unsafe_allow_html=True)
    
    # Load data and model
    with st.spinner("Loading analytics data..."):
        df = load_analytics_data()
        model, label_encoder = train_analytics_model(df)
    
    if df is None:
        st.error("Unable to load analytics data. Please check if the dataset file exists in the correct location.")
        st.info("Expected locations: src/data/dataset_with_random_year.csv or src/data/dataset_with_random_year.xlsx")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Analytics Overview Cards
    st.markdown("### Overview Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    total_cases = len(df)
    unique_diseases = df['Medical_Condition'].nunique()
    avg_age = df['Age'].mean()
    current_year = datetime.now().year
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{total_cases:,}</div>
                <div class="metric-label">Total Cases</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{unique_diseases}</div>
                <div class="metric-label">Disease Types</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{avg_age:.1f}</div>
                <div class="metric-label">Avg Patient Age</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col4:
        if 'Area' in df.columns:
            unique_areas = df['Area'].nunique()
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{unique_areas}</div>
                    <div class="metric-label">Coverage Areas</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{current_year}</div>
                    <div class="metric-label">Current Year</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
    
    st.markdown("---")
    
    # AI Disease Prediction Section
    st.markdown("### AI Disease Prediction Tool")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(
            """
            <div class="analytics-card">
                <h3 style='color:#8B4789; margin-bottom: 1rem;'>Predict Disease Risk</h3>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Prediction inputs
        pred_age = st.slider("Patient Age", 18, 100, 35, key="pred_age")
        
        if 'Admission_Year' in df.columns:
            min_year = int(df['Admission_Year'].min())
            max_year = int(df['Admission_Year'].max())
            pred_year = st.slider("Year", min_year, max_year, current_year, key="pred_year")
        else:
            pred_year = current_year
        
        if st.button("Predict Disease Risk", use_container_width=True, type="primary"):
            if model and label_encoder:
                # Make prediction
                if 'Admission_Year' in df.columns:
                    features = np.array([[pred_year, pred_age]])
                else:
                    features = np.array([[pred_age]])
                
                prediction = model.predict(features)[0]
                prediction_proba = model.predict_proba(features)[0]
                
                predicted_disease = label_encoder.inverse_transform([prediction])[0]
                confidence = max(prediction_proba) * 100
                
                st.session_state.prediction_result = {
                    'disease': predicted_disease,
                    'confidence': confidence,
                    'age': pred_age,
                    'year': pred_year
                }
    
    with col2:
        if 'prediction_result' in st.session_state:
            result = st.session_state.prediction_result
            
            st.markdown(
                f"""
                <div class="analytics-card" style="background: linear-gradient(135deg, #FF9933 0%, #8B4789 100%); color: white;">
                    <h3 style='color: white; margin-bottom: 1rem;'>Prediction Results</h3>
                    <div style='font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem;'>
                        {result['disease']}
                    </div>
                    <div style='font-size: 1.2rem; margin-bottom: 0.5rem;'>
                        Confidence: {result['confidence']:.1f}%
                    </div>
                    <div style='font-size: 1rem; opacity: 0.9;'>
                        Age: {result['age']} years | Year: {result['year']}
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Additional insights
            st.markdown("##### Risk Factors & Recommendations")
            if result['confidence'] > 70:
                st.success("High confidence prediction - Consider preventive measures")
            elif result['confidence'] > 50:
                st.warning("Moderate confidence - Monitor symptoms and consult healthcare provider")
            else:
                st.info("Low confidence - Multiple conditions possible, seek medical evaluation")
    
    st.markdown("---")
    
    # Data Visualizations
    st.markdown("### Data Visualizations & Insights")
    
    # Generate visualizations
    fig1, fig2, fig3, fig4 = create_analytics_visualizations(df)
    
    # Display charts in tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Disease Distribution", "Age Analysis", "Geographic Analysis", "Temporal Trends"])
    
    with tab1:
        if fig1:
            st.plotly_chart(fig1, use_container_width=True)
            
            # Insights
            most_common = df['Medical_Condition'].value_counts().iloc[0]
            most_common_disease = df['Medical_Condition'].value_counts().index[0]
            
            st.markdown(
                f"""
                <div class="analytics-card">
                    <h4 style='color:#8B4789;'>Key Insights</h4>
                    <ul>
                        <li><strong>Most Common Disease:</strong> {most_common_disease} ({most_common} cases)</li>
                        <li><strong>Disease Diversity:</strong> {unique_diseases} different conditions tracked</li>
                        <li><strong>Distribution:</strong> Shows prevalence patterns across conditions</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    with tab2:
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)
            
            # Age-related insights
            age_stats = df.groupby('Medical_Condition')['Age'].agg(['mean', 'min', 'max']).round(1)
            
            st.markdown(
                """
                <div class="analytics-card">
                    <h4 style='color:#8B4789;'>Age Distribution Analysis</h4>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.dataframe(age_stats, use_container_width=True)
    
    with tab3:
        if fig3 and 'Area' in df.columns:
            st.plotly_chart(fig3, use_container_width=True)
            
            # Geographic insights
            area_stats = df.groupby('Area').agg({
                'Medical_Condition': 'count',
                'Age': 'mean'
            }).round(1)
            area_stats.columns = ['Total Cases', 'Avg Age']
            
            st.markdown(
                """
                <div class="analytics-card">
                    <h4 style='color:#8B4789;'>Geographic Distribution</h4>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.dataframe(area_stats, use_container_width=True)
        else:
            st.info("Geographic data not available in the current dataset")
    
    with tab4:
        if fig4 and 'Admission_Year' in df.columns:
            st.plotly_chart(fig4, use_container_width=True)
            
            # Temporal insights
            yearly_stats = df.groupby('Admission_Year').agg({
                'Medical_Condition': 'count',
                'Age': 'mean'
            }).round(1)
            yearly_stats.columns = ['Total Cases', 'Avg Age']
            
            st.markdown(
                """
                <div class="analytics-card">
                    <h4 style='color:#8B4789;'>Temporal Trends</h4>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.dataframe(yearly_stats, use_container_width=True)
        else:
            st.info("Temporal data not available in the current dataset")
    
    st.markdown("---")
    
    # Advanced Analytics Section
    st.markdown("### Advanced Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div class="analytics-card">
                <h4 style='color:#8B4789;'>Model Performance</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if model:
            # Calculate and display model metrics
            from sklearn.model_selection import cross_val_score
            from sklearn.metrics import accuracy_score
            
            features = ['Admission_Year', 'Age'] if 'Admission_Year' in df.columns else ['Age']
            X = df[features]
            y = df['Medical_Condition']
            
            # Encode target
            y_encoded = label_encoder.transform(y)
            
            # Cross-validation scores
            cv_scores = cross_val_score(model, X, y_encoded, cv=5)
            
            st.metric("Model Accuracy", f"{cv_scores.mean():.1%}", f"±{cv_scores.std():.1%}")
            st.metric("Cross-Val Score", f"{cv_scores.mean():.3f}")
            st.metric("Training Samples", f"{len(df):,}")
    
    with col2:
        st.markdown(
            """
            <div class="analytics-card">
                <h4 style='color:#8B4789;'>Data Quality</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Data quality metrics
        total_records = len(df)
        complete_records = df.dropna().shape[0]
        completeness = (complete_records / total_records) * 100
        
        st.metric("Data Completeness", f"{completeness:.1f}%")
        st.metric("Complete Records", f"{complete_records:,}")
        st.metric("Data Coverage", f"{df.columns.size} fields")
    
    # Export functionality
    st.markdown("---")
    st.markdown("### Export Analytics Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Download Dataset", use_container_width=True):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"healthcare_analytics_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Generate Report", use_container_width=True):
            report_content = f"""
            Healthcare Analytics Report
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            
            Summary Statistics:
            - Total Cases: {total_cases:,}
            - Unique Diseases: {unique_diseases}
            - Average Patient Age: {avg_age:.1f} years
            - Data Completeness: {completeness:.1f}%
            
            Most Common Diseases:
            {df['Medical_Condition'].value_counts().head().to_string()}
            
            Age Distribution by Disease:
            st.markdown("### Age Analysis")
if age_stats is not None:
    st.text(age_stats.to_string())
else:
    st.warning("Age statistics unavailable.")

            """
            
            st.download_button(
                label="Download Report",
                data=report_content,
                file_name=f"analytics_report_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    with col3:
        if st.button("View Raw Data", use_container_width=True):
            with st.expander("Raw Dataset Preview", expanded=False):
                st.dataframe(df, use_container_width=True, height=400)
    
    st.markdown('</div>', unsafe_allow_html=True)

def dashboard_profile():
    """User profile page"""
    st.markdown('<div class="main-content-with-banner">', unsafe_allow_html=True)
    
    st.markdown("<h1 style='color:#8B4789; text-align: center; margin-bottom: 2rem;'>My Profile</h1>", unsafe_allow_html=True)
    
    user = st.session_state.get("current_user", "Guest")
    
    # Profile Header Section
    with st.container():
        profile_pic_path = get_profile_pic_path(user)
        
        if profile_pic_path and os.path.exists(profile_pic_path):
            try:
                with open(profile_pic_path, "rb") as f:
                    img_data = f.read()
                img_b64 = base64.b64encode(img_data).decode()
                profile_img = f'<img src="data:image/jpeg;base64,{img_b64}" class="profile-pic-large" />'
            except Exception:
                profile_img = f'''
                <div class="profile-pic-default-large">
                    {user[0].upper()}
                </div>
                '''
        else:
            profile_img = f'''
            <div class="profile-pic-default-large">
                {user[0].upper()}
            </div>
            '''
        
        st.markdown(
            f"""
            <div class="profile-header">
                {profile_img}
                <h2 style='text-align: center; color: #8B4789; margin: 0;'>{user}</h2>
                <p style='text-align: center; color: #FF9933; font-size: 1.1rem; margin: 10px 0 0 0;'>Official Account</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Main Profile Content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Account Information Card
        st.markdown(
            f"""
            <div class="profile-info-card">
                <h3 style='color: #8B4789; margin-bottom: 1rem; text-align: center;'>Account Information</h3>
                <div class="info-item">
                    <span class="info-label">Username</span>
                    <span class="info-value">{user}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Account Status</span>
                    <span class="info-value" style='color: #138808; font-weight: 600;'>Active</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Member Since</span>
                    <span class="info-value">January 2025</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Account Type</span>
                    <span class="info-value">Patient</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Last Login</span>
                    <span class="info-value">Today</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Security Card
        st.markdown(
            """
            <div class="profile-info-card">
                <h3 style='color: #8B4789; margin-bottom: 1rem; text-align: center;'>Security</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("Change Password", use_container_width=True):
            st.info("Password change functionality will be implemented soon!")
        
        if st.button("Two-Factor Authentication", use_container_width=True):
            st.info("Two-factor authentication setup coming soon!")
    
    with col2:
        # Profile Picture Management
        st.markdown(
            """
            <div class="profile-info-card">
                <h3 style='color: #8B4789; margin-bottom: 1rem; text-align: center;'>Profile Picture can be updated here</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        uploaded_file = st.file_uploader(
            "Upload new profile picture", 
            type=['png', 'jpg', 'jpeg', 'gif'],
            help="Choose a new profile picture (PNG, JPG, JPEG, GIF)"
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            if uploaded_file is not None:
                if st.button("Save Picture", use_container_width=True):
                    saved_path = save_profile_pic(user, uploaded_file)
                    if saved_path:
                        st.success("Profile picture updated!")
                        st.rerun()
                    else:
                        st.error("Failed to save profile picture")
        
        with col_b:
            if st.button("Remove Picture", use_container_width=True):
                # Remove profile picture logic
                for ext in ['jpg', 'jpeg', 'png', 'gif']:
                    filepath = os.path.join(PROFILE_PICS_DIR, f"{user}_profile.{ext}")
                    if os.path.exists(filepath):
                        os.remove(filepath)
                        st.success("Profile picture removed!")
                        st.rerun()
                        break
        
        # Preferences Card
        st.markdown(
            """
            <div class="profile-info-card">
                <h3 style='color: #8B4789; margin-bottom: 1rem; text-align: center;'>Preferences</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # App Preferences
        notifications = st.checkbox("Enable Notifications", value=True)
        
        # Dark Mode Toggle
        dark_mode = st.checkbox("Dark Mode", value=st.session_state.get("dark_mode", False))
        if dark_mode != st.session_state.get("dark_mode", False):
            st.session_state.dark_mode = dark_mode
            st.rerun()
        
        email_updates = st.checkbox("Email Updates", value=False)
        data_sharing = st.checkbox("Anonymous Data Sharing", value=False)
    
    # Health Goals Section
    st.markdown("---")
    st.markdown(
        """
        <div class="profile-info-card">
            <h3 style='color: #8B4789; margin-bottom: 1rem; text-align: center;'>Health Goals & Notes</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    with col1:
        health_goals = st.text_area(
            "Personal Health Goals",
            placeholder="Describe your health objectives, fitness goals, or medical targets...",
            height=100
        )
    
    with col2:
        medical_notes = st.text_area(
            "Important Medical Notes",
            placeholder="Any important medical information, allergies, or notes for healthcare providers...",
            height=100
        )
    
    # Save Preferences Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Save All Preferences", use_container_width=True, type="primary"):
            # Here you would save user preferences to a file or database
            st.success("Preferences saved successfully!")
            st.balloons()
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application function"""
    # Page configuration
    st.set_page_config(
        page_title="Saarva Health - Digital Healthcare",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Set theme
    set_indian_theme()
    
    # Display logo
    display_logo()
    
    # Initialize data files
    initialize_default_data()
    
    # Load users into session state
    if "user_data" not in st.session_state:
        st.session_state.user_data = load_json(USERS_FILE, {})
    
    # Initialize login state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.current_user = None
    
    # Show login page if not logged in
    if not st.session_state.logged_in:
        show_landing()
        return
    
    # Show banner and sidebar for logged-in users
    show_dashboard_banner()
    show_sidebar()
    
    # Route to appropriate page
    nav = st.session_state.get("selected_nav", "Dashboard")
    
    if nav == "Dashboard":
        show_dashboard_banner()  # This line must be here
        dashboard_home()
    elif nav == "Medical Records":
        dashboard_records()
    elif nav == "Doctors":
        dashboard_doctors()
    elif nav == "Analytics":
        dashboard_analytics()
    elif nav == "Profile":
        dashboard_profile()

if __name__ == "__main__":
    main()
