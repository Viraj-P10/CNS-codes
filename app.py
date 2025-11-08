from flask import Flask, render_template, request
import bcrypt

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# In-memory storage (use database in production)
users = {}

def hash_password(password):
    """Hash a password using bcrypt with salt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def verify_password(password, hashed):
    """Verify a password against a bcrypt hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    message_type = None
    hash_info = None
    encryption_technique = "bcrypt"

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        action = request.form.get('action')

        # Validation: Check for empty fields
        if not username or not password:
            message = "Please fill in all fields!"
            message_type = "error"

        elif action == 'register':
            # Registration
            if username in users:
                message = "Username already exists! Please choose another."
                message_type = "error"
            else:
                # Hash password and store
                hashed_password = hash_password(password)
                users[username] = hashed_password
                message = f"Registration successful for '{username}'! You can now login."
                message_type = "success"
                # Show hash for educational purposes
                hash_info = {
                    'plain_password': password,
                    'hashed_password': hashed_password.decode('utf-8'),
                    'userid': username,
                    'process': 'Encryption/Hashing'
                }

        elif action == 'login':
            # Login
            if username not in users:
                message = "Username not found! Please register first."
                message_type = "error"
            else:
                stored_hash = users[username]
                if verify_password(password, stored_hash):
                    message = f"Login successful! Welcome, '{username}'!"
                    message_type = "success"
                    hash_info = {
                        'plain_password': password,
                        'hashed_password': stored_hash.decode('utf-8'),
                        'userid': username,
                        'process': 'Decryption/Verification'
                    }
                else:
                    message = "Invalid password! Please try again."
                    message_type = "error"

    return render_template('index.html', message=message, message_type=message_type,
                            hash_info=hash_info, encryption_technique=encryption_technique)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)