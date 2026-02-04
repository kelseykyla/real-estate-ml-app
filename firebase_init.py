# # # Changes made below -- version two
# import firebase_admin
# from firebase_admin import credentials
# import streamlit as st
# import json
# import logging

# def initialize_firebase():
#     """Initialize Firebase from Streamlit secrets."""
#     try:
#         if not firebase_admin._apps:  # Only initialize once
#             firebase_config = st.secrets["firebase"]

#             # Convert Streamlit Secrets (TomlDict) -> Python dict
#             cred_dict = dict(firebase_config)

#             # Ensure private key newlines are correctly formatted
#             cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")

#             # Debug log (optional, remove in production)
#             logging.info(f"Initializing Firebase for project: {cred_dict['project_id']}")

#             # Initialize directly from dict (not file path!)
#             cred = credentials.Certificate(cred_dict)
#             firebase_admin.initialize_app(cred)

#             logging.info("✅ Firebase initialized successfully.")
#         else:
#             logging.info("ℹ️ Firebase already initialized.")
#     except Exception as e:
#         logging.error(f"❌ Firebase initialization failed: {e}")
#         raise

import os
import firebase_admin
from firebase_admin import credentials
import logging
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

def initialize_firebase():
    try:
        key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

        if not key_path:
            raise ValueError("Firebase credentials path not found in environment variables.")

        cred = credentials.Certificate(key_path)

        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
            logging.info("Firebase successfully initialized.")
        else:
            logging.info("Firebase is already initialized.")
    
    except Exception as e:
        logging.error(f"Error initializing Firebase: {e}")
        raise
