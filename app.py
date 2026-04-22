from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import fetch_user, save_user
from face_auth import get_face_encoding, verify_face
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "une_cle_tres_secrete_123"

@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html', email=session['user'])
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        face_data = request.form.get('face_data')

        if fetch_user(email):
            flash("Cet email est déjà utilisé.")
            return redirect(url_for('register'))

        encoding = None
        if face_data:
            encoding = get_face_encoding(face_data)

        user_data = {
            'email': email,
            'password_hash': generate_password_hash(password),
            'face_encoding': encoding,
            'created_at': datetime.now().isoformat()
        }
        save_user(user_data)

        flash("Inscription réussie ! Connectez-vous.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = fetch_user(email)
        if user and check_password_hash(user['password_hash'], password):
            session['user'] = email
            return redirect(url_for('index'))

        flash("Email ou mot de passe incorrect.")
    return render_template('login.html')

@app.route('/login/face', methods=['POST'])
def login_face():
    data = request.json
    email = data.get('email')
    face_image = data.get('face_image')

    user = fetch_user(email)
    if not user or 'face_encoding' not in user:
        return jsonify({"success": False, "message": "Utilisateur ou empreinte faciale inconnue"}), 404

    is_valid = verify_face(user['face_encoding'], face_image)

    if is_valid:
        session['user'] = email
        return jsonify({"success": True})

    return jsonify({"success": False, "message": "Visage non reconnu"}), 401

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
