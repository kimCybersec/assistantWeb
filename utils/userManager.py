import hashlib
from flask import request
import os

def generateUserId():
    """Generate consistent anonymous user ID based on IP"""
    ip = request.remote_addr or '127.0.0.1'  
    salt = os.getenv("userId_SALT", "default_salt_value")
    return hashlib.sha256(f"{ip}{salt}".encode()).hexdigest()[:16]  