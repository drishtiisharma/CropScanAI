import requests
from io import BytesIO
from tensorflow.keras.models import load_model

from flask import Flask, render_template, request, jsonify, url_for, redirect, session
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import os
from flask_babel import Babel
import gdown   # 🔹 for downloading model from Google Drive

# ---------------------- FLASK SETUP ----------------------

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.config['SECRET_KEY'] = 'a-very-secret-key-for-sessions'
app.config['LANGUAGES'] = {'en': 'English', 'hi': 'हिन्दी'}

# ---------------------- LANGUAGE SETUP ----------------------

def get_locale():
    return session.get('language', 'en')

babel = Babel(app, locale_selector=get_locale)

@app.route('/language/<language>')
def set_language(language=None):
    session['language'] = language
    return redirect(request.referrer)

# ---------------------- MODEL SETUP ----------------------
'''
MODEL_PATH = "pearl_millet_ergot_model.h5"
# 🔹 Replace this with your actual Google Drive file ID
DRIVE_FILE_ID = "1ROzdGKtSsI-IRjElc8fxVDe0BBpSx_6m"

def ensure_model():
    """Downloads the model if not already available locally."""
    if not os.path.exists(MODEL_PATH):
        print("⏬ Model not found locally. Downloading from Google Drive...")
        url = f"https://drive.google.com/uc?id={DRIVE_FILE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False)
        print("✅ Model downloaded successfully!")

# Ensure model is available before starting
ensure_model()

# Load the trained Keras model
print("📦 Loading model...")
model = load_model(MODEL_PATH)
print("✅ Model loaded successfully!")
'''
MODEL_URL = "https://huggingface.co/drishtiisharma/pearl_millet_ergot_model/raw/main/pearl_millet_ergot_model.h5"

def load_remote_model():
    """Downloads and loads the model from Hugging Face directly into memory."""
    print("📥 Downloading model from Hugging Face...")
    response = requests.get(MODEL_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to download model: {response.status_code}")
    with open("model_temp.h5", "wb") as f:
        f.write(response.content)
    print("📦 Loading model into memory...")
    model = load_model("model_temp.h5")
    print("✅ Model loaded successfully!")
    return model

model = load_remote_model()


# ---------------------- IMAGE PROCESSING ----------------------

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# ---------------------- ROUTES ----------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about_ergot")
def about_ergot():
    return render_template("about_ergot.html")

@app.route("/identify")
def identify():
    return render_template("identify.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/official_insights")
def official_insights():
    return render_template("official_insights.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/results_healthy")
def results_healthy():
    return render_template(
        "results_healthy.html",
        result=session.get('result'),
        confidence=session.get('confidence'),
        filename=session.get('filename')
    )

@app.route("/ergot_detected")
def ergot_detected():
    return render_template(
        "ergot_detected.html",
        result=session.get('result'),
        confidence=session.get('confidence'),
        filename=session.get('filename')
    )

# ---------------------- PREDICTION LOGIC ----------------------

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]
    upload_dir = os.path.join(app.static_folder, "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    file.save(file_path)

    img = preprocess_image(file_path)
    pred = model.predict(img)[0][0]

    session['filename'] = file.filename
    session['confidence'] = round(float(pred) * 100, 2)

    if pred > 0.5:
        session['result'] = 'Healthy'
        return redirect(url_for('results_healthy'))
    else:
        session['result'] = 'Diseased: Ergot'
        return redirect(url_for('ergot_detected'))

# ---------------------- RUN APP ----------------------

if __name__ == "__main__":
    app.run(debug=True)
