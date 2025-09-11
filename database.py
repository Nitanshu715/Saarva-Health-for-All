# Database functions (MongoDB integration - commented out for now)

# from pymongo import MongoClient
# import streamlit as st

# mongo_uri = "mongodb+srv://username:password@cluster.mongodb.net/test?retryWrites=true&w=majority"
# client = MongoClient(mongo_uri)
# db = client["health_db"]
# collection = db["migrant_health_records"]

# def upload_to_mongodb(data):
#     try:
#         collection.insert_one(data)
#         return True
#     except Exception as e:
#         st.error(f"Failed to update MongoDB: {e}")
#         return False
