from dotenv import load_dotenv
import os

load_dotenv()  

ALLOWED_EXTENSIONS = {"apk", "zip", "ipa", "appx"}
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "./uploads/")
API_URL = os.getenv("API_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "")
