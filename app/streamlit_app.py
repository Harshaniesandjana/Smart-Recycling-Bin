import streamlit as st
import json
import os
import hashlib
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image

# ============================================================
# 1. DATABASE & LOGIN SYSTEM
# ============================================================

USERS_DB = "app/users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USERS_DB):
        return {}
    with open(USERS_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_DB, "w") as f:
        json.dump(users, f, indent=4)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Gebruiker bestaat al."
    users[username] = {
        "password": hash_password(password),
        "points": 0
    }
    save_users(users)
    return True, "Account succesvol aangemaakt!"

def login_user(username, password):
    users = load_users()
    if username not in users:
        return False, "Gebruiker bestaat niet."
    if users[username]["password"] != hash_password(password):
        return False, "Wachtwoord is onjuist."
    return True, users[username]

def update_points(username, points):
    users = load_users()
    users[username]["points"] = points
    save_users(users)

# ============================================================
# 2. LOGIN UI STYLING
# ============================================================

login_css = """
<style>
.login-container {
    max-width: 420px;
    margin: auto;
    margin-top: 60px;
    padding: 30px;
    background: #ffffff;
    border-radius: 14px;
    box-shadow: 0px 4px 18px rgba(0,0,0,0.12);
}
.login-title {
    text-align: center;
    font-size: 28px;
    font-weight: 700;
    color: #2ecc71;
    margin-bottom: 10px;
}
.login-subtitle {
    text-align: center;
    font-size: 15px;
    color: #555;
    margin-bottom: 25px;
}
input[type=text], input[type=password] {
    border-radius: 8px !important;
    padding: 10px !important;
    border: 1px solid #ccc !important;
}
.stButton>button {
    width: 100%;
    border-radius: 8px;
    background-color: #2ecc71;
    color: white;
    padding: 10px;
    font-size: 16px;
    border: none;
}
.stButton>button:hover {
    background-color: #27ae60;
}
</style>
"""
st.markdown(login_css, unsafe_allow_html=True)

# ============================================================
# 3. LOGIN LOGIC
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">Smart Recycling Bin</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">Log in of maak een nieuw account</div>', unsafe_allow_html=True)

    tab_login, tab_register = st.tabs(["🔐 Inloggen", "🆕 Registreren"])

    with tab_login:
        username = st.text_input("Gebruikersnaam")
        password = st.text_input("Wachtwoord", type="password")

        if st.button("Inloggen"):
            success, data = login_user(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.points = data["points"]
                st.success(f"Ingelogd als {username}")
            else:
                st.error(data)

    with tab_register:
        new_user = st.text_input("Nieuwe gebruikersnaam")
        new_pass = st.text_input("Nieuw wachtwoord", type="password")

        if st.button("Account aanmaken"):
            success, msg = register_user(new_user, new_pass)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ============================================================
# 4. YOLO MODEL LADEN
# ============================================================

model = YOLO("runs/classify/train-7/weights/best.pt")

LABELS = [
    "battery", "biological", "cardboard", "clothes", "glass",
    "metal", "paper", "plastic", "shoes", "trash"
]

BIN_COLORS = {
    "battery": "🔋",
    "biological": "🌱",
    "cardboard": "📦",
    "clothes": "👕",
    "glass": "🍾",
    "metal": "🔧",
    "paper": "📄",
    "plastic": "🧴",
    "shoes": "👟",
    "trash": "🗑️"
}

# ============================================================
# 5. BADGE SYSTEM
# ============================================================

def get_badge(points):
    if points >= 1000:
        return "💎 Diamond Recycler"
    elif points >= 500:
        return "🔱 Platinum Recycler"
    elif points >= 250:
        return "🥇 Gold Recycler"
    elif points >= 100:
        return "🥈 Silver Recycler"
    else:
        return "🥉 Bronze Recycler"

# ============================================================
# 6. APP INTERFACE
# ============================================================

st.title("♻️ Smart Recycling Bin – AI Afval Classificatie")

st.write(f"👤 Ingelogd als **{st.session_state.username}**")
st.write(f"⭐ Punten: **{st.session_state.points}**")
st.write(f"🏆 Badge: **{get_badge(st.session_state.points)}**")

mode = st.radio("Kies modus:", ["📸 Camera", "📤 Upload"])

# ============================================================
# 7. CAMERA MODE
# ============================================================

if mode == "📸 Camera":
    st.write("Live camera classificatie")

    camera = st.camera_input("Maak een foto")

    if camera:
        img = Image.open(camera)
        img_array = np.array(img)

        results = model(img_array)
        pred = results[0].probs.top1
        label = LABELS[pred]
        conf = float(results[0].probs.top1conf)

        st.success(f"Herkenning: **{label}** ({conf:.2f}) {BIN_COLORS[label]}")

        st.session_state.points += 10
        update_points(st.session_state.username, st.session_state.points)

# ============================================================
# 8. UPLOAD MODE
# ============================================================

if mode == "📤 Upload":
    uploaded = st.file_uploader("Upload een afbeelding", type=["jpg", "png"])

    if uploaded:
        img = Image.open(uploaded)
        st.image(img, caption="Geüpload beeld")

        img_array = np.array(img)
        results = model(img_array)
        pred = results[0].probs.top1
        label = LABELS[pred]
        conf = float(results[0].probs.top1conf)

        st.success(f"Herkenning: **{label}** ({conf:.2f}) {BIN_COLORS[label]}")

        st.session_state.points += 10
        update_points(st.session_state.username, st.session_state.points)
