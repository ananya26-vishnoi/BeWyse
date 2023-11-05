import firebase_admin
from firebase_admin import credentials

# Path to your Firebase service account key JSON file
FIREBASE_SERVICE_ACCOUNT_KEY = 'account/firebase.json'

# Initialize Firebase Admin SDK
cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_KEY)
firebase_admin.initialize_app(cred)