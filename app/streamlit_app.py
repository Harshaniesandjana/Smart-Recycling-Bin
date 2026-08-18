import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import time
import qrcode
from io import BytesIO

# Load model
model = YOLO("runs/classify/train-7/weights/best.pt")

# Mapping categories to bins
CATEGORY_TO_BIN = {
    "battery": "HAZARDOUS_BIN",
    "biological": "ORGANIC_BIN",
    "cardboard": "PAPER_BIN",
    "clothes": "TEXTILE_BIN",
    "glass": "GLASS_BIN",
    "metal": "METAL_BIN",
    "paper": "PAPER_BIN",
    "plastic": "PLASTIC_BIN",
    "shoes": "TEXTILE_BIN",
    "trash": "GENERAL_WASTE_BIN"
}

BIN_COLORS = {
    "HAZARDOUS_BIN": "#ff4d4d",
    "ORGANIC_BIN": "#2ecc71",
    "PAPER_BIN": "#3498db",
    "TEXTILE_BIN": "#9b59b6",
    "GLASS_BIN": "#1abc9c",
    "METAL_BIN": "#e67e22",
    "PLASTIC_BIN": "#f1c40f",
    "GENERAL_WASTE_BIN": "#7f8c8d",
    "UNKNOWN": "#000000"
}

# ---------------------------
# BADGE SYSTEM
# ---------------------------
def get_badge(points):
    if points >= 1000:
        return "🔱 Diamond Recycler"
    elif points >= 500:
        return "💎 Platinum Recycler"
    elif points >= 250:
        return "🥇 Gold Recycler"
    elif points >= 100:
        return "🥈 Silver Recycler"
    else:
        return "🥉 Bronze Recycler"

# ---------------------------
# QR LOGIN SYSTEM
# ---------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "points" not in st.session_state:
    st.session_state.points = 0

def generate_qr(user_id):
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(user_id)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf)
    buf.seek(0)
    return buf

# ---------------------------
# UI DESIGN (mobile-friendly)
# ---------------------------

st.set_page_config(page_title="Smart Recycling Bin", layout="centered")

st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fc;
    }
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #2ecc71;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #555;
        margin-bottom: 30px;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>♻️ Smart Recycling Bin</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Recycle & verdien punten!</div>", unsafe_allow_html=True)

# ---------------------------
# LOGIN SECTION
# ---------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🔐 QR Login")

user_id_input = st.text_input("Voer jouw QR‑code in:")

if st.button("Login"):
    if user_id_input.strip() != "":
        st.session_state.user = user_id_input
        st.success(f"Ingelogd als: {user_id_input}")
    else:
        st.error("QR‑code ongeldig.")

if st.session_state.user:
    st.info(f"Welkom terug, {st.session_state.user}!")
else:
    st.warning("Je bent nog niet ingelogd.")
st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.user:
    st.stop()

# ---------------------------
# POINTS + BADGE CARD
# ---------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🏆 Jouw punten")
st.progress(min(st.session_state.points / 1000, 1.0))
st.write(f"**Totaal punten:** {st.session_state.points}")
st.write(f"**Badge:** {get_badge(st.session_state.points)}")
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# MODE SELECTOR
# ---------------------------
mode = st.radio("Kies modus:", ["📸 Live camera", "📤 Upload afbeelding"])

frame_placeholder = st.empty()
label_placeholder = st.empty()
bin_placeholder = st.empty()
points_placeholder = st.empty()

# ---------------------------
# CLASSIFICATION FUNCTIONS
# ---------------------------
def classify_frame(frame):
    results = model(frame)[0]
    label_index = results.probs.top1
    confidence = float(results.probs.top1conf)
    label = model.names[label_index]
    return label, confidence

def decide_bin(label):
    return CATEGORY_TO_BIN.get(label.lower(), "UNKNOWN")

def add_points():
    st.session_state.points += 10

# ---------------------------
# LIVE CAMERA MODE
# ---------------------------
if mode == "📸 Live camera":
    run_stream = st.checkbox("Start live camera stream")

    if run_stream:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("Camera niet gevonden.")
        else:
            while True:
                ret, frame = cap.read()
                if not ret:
                    st.error("Kon geen frame lezen.")
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_placeholder.image(frame_rgb, caption="Live camera")

                label, conf = classify_frame(frame_rgb)
                assigned_bin = decide_bin(label)

                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown(f"<h3>🔍 Herkenning: <b>{label}</b> ({conf:.2f})</h3>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown(
                    f"<h3 style='color:{BIN_COLORS[assigned_bin]};'>🗑️ Afvalbak: {assigned_bin}</h3>",
                    unsafe_allow_html=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

                add_points()
                points_placeholder.success(f"+10 punten! Totaal: {st.session_state.points}")

                time.sleep(1)

            cap.release()

# ---------------------------
# UPLOAD MODE
# ---------------------------
elif mode == "📤 Upload afbeelding":
    uploaded_file = st.file_uploader("Upload een afbeelding", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame_placeholder.image(frame_rgb, caption="Geüploade afbeelding")

        label, conf = classify_frame(frame_rgb)
        assigned_bin = decide_bin(label)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>🔍 Herkenning: <b>{label}</b> ({conf:.2f})</h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(
            f"<h3 style='color:{BIN_COLORS[assigned_bin]};'>🗑️ Afvalbak: {assigned_bin}</h3>",
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

        add_points()
        points_placeholder.success(f"+10 punten! Totaal: {st.session_state.points}")
