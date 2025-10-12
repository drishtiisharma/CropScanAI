from flask import Flask, render_template, request, jsonify, url_for, redirect, session
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import os
from flask_babel import Babel

# creates the flask app instance and tells where the html and static files are
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# adding configurations to the flask app 
app.config['SECRET_KEY'] = 'a-very-secret-key-for-sessions' # flask uses this to secure sessions so the data stored between requests is safe 
app.config['LANGUAGES'] = {'en': 'English', 'hi': 'हिन्दी'} # which languages are supported


# defines your language selection function normally
def get_locale():
    # Get the language from the session, default language is English
    return session.get('language', 'en')

# tells flask-babel to use get_locale function every time it needs to decide what language to display.
babel = Babel(app, locale_selector=get_locale)
# --- END OF CORRECTION ---

# this route handles the actual language switch
# saves user's choice in session and redirects to the requested page
@app.route('/language/<language>')
def set_language(language=None):
    session['language'] = language
    return redirect(request.referrer)


# loads the trained keras model
MODEL_PATH = "pearl_millet_ergot_model.h5"
model = load_model(MODEL_PATH)

# image processing
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    return img


# routes for different pages
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

# prediction route
# is the heart of the app
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

# -------------------- RUN APP --------------------

if __name__ == "__main__":
    app.run(debug=True)