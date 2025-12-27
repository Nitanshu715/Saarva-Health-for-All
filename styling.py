import streamlit as st

def load_custom_css():
    st.markdown("""
        <style>
        input[type="text"], textarea {
            border: 2px solid #4CAF50; 
            border-radius: 6px;
            padding: 6px;
            font-size: 13px;
            transition: all 0.2s ease;
            min-height: 25px;
            max-height: 70px;
            overflow-y: auto;
        }
        input[type="text"]:focus, textarea:focus {
            max-height: 120px;
            box-shadow: 0 0 6px #4CAF50;
            font-size: 14px;
        }
        div.stSelectbox div[role="listbox"] {
            border: 2px solid #4CAF50;
            border-radius: 6px;
        }
        div.stButton > button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 6px;
            padding: 8px 16px;
            transition: background-color 0.2s ease;
            margin-top: 8px;
        }
        div.stButton > button:hover {
            background-color: #45a049;
        }
        .streamlit-expanderHeader {
            font-size: 18px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
