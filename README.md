# CropScanAI 🌾

## AI-Powered Ergot Detection System for Pearl Millet

CropScanAI is a web application that detects **Ergot disease in pearl millet grains** using Computer Vision and Deep Learning.

Ergot is a fungal disease caused by *Claviceps fusiformis* that can significantly reduce crop yield, affect grain quality, and pose health risks to humans and animals if contaminated grains are consumed.

Traditional disease detection often relies on manual inspection, which can be time-consuming, inconsistent, and difficult to perform at scale. CropScanAI provides a faster and more accessible solution by combining a **Convolutional Neural Network (CNN)** with a **Flask-based web application**.

Users can upload an image of pearl millet grains, and the system analyzes the image to determine whether the sample is healthy or infected. The project aims to assist farmers, researchers, and agricultural professionals in identifying Ergot infections early, reducing crop losses and improving agricultural decision-making.


## 📌 Problem Statement

Ergot disease is one of the most damaging fungal infections affecting pearl millet. Farmers often identify the disease only after visible symptoms become severe, leading to reduced crop quality and yield losses.

CropScanAI aims to:

- Reduce dependence on manual inspection
- Detect infection quickly and accurately
- Assist farmers in making timely decisions
- Improve accessibility through a web-based platform
- Promote technology-driven agriculture

## ✨ Features

- Upload pearl millet grain images for analysis
- AI-powered disease detection using CNN
- Real-time prediction through a Flask web application
- Confidence score for predictions
- Treatment recommendations for infected samples
- Downloadable PDF reports
- English and Hindi language support
- Farmer-friendly user interface
- Accessible through desktop and mobile web browsers
- Responsive user interface for multiple screen sizes
  
## 🧠 How It Works

1. User uploads an image of pearl millet grains.
2. The image is preprocessed using OpenCV.
3. The trained CNN model extracts visual features.
4. The model predicts whether the sample is:
   - Healthy
   - Ergot Infected
5. Results are displayed along with confidence scores and recommendations.

### 🚀 Live Demo [![Open CropScanAI](https://img.shields.io/badge/Live-Demo-success)](https://drishtiisharma-cropscanai.hf.space/)

## 📊 Model Performance

The CNN model was trained using TensorFlow and Keras on a dataset containing healthy and Ergot-infected pearl millet grain images.

| Metric | Value |
|----------|----------|
| Training Accuracy | 92% |
| Validation Accuracy | 90% |
| Epochs | 10 |

The model demonstrated strong performance and good generalization on unseen data.

## 🛠️ Technology Stack

### Machine Learning
- TensorFlow
- Keras
- OpenCV
- NumPy

### Backend
- Flask
- Flask-Babel

### Frontend
- HTML
- CSS
- JavaScript
- Font Awesome

### Development Tools
- Python
- Git
- VS Code


## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/CropScanAI.git
cd CropScanAI
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install tensorflow flask flask-babel opencv-python matplotlib gdown
```

### Train the Model

```bash
python train.py
```

### Run the Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## 🌍 Supported Languages

- English
- Hindi

The application uses Flask-Babel to provide multilingual support and improve accessibility for farmers.
