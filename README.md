# 🏆 Sports Personality Classifier

A machine learning application that classifies sports personalities from uploaded images. The application uses computer vision and machine learning to identify faces and classify them into different sports personalities.

## 🎯 Supported Players

1. **Lionel Messi** ⚽ (Football)
2. **Maria Sharapova** 🎾 (Tennis)
3. **Roger Federer** 🎾 (Tennis)
4. **Serena Williams** 🎾 (Tennis)
5. **Virat Kohli** 🏏 (Cricket)

## 🛠️ Technologies Used

### Backend
- **Python** - Core programming language
- **Flask** - Web framework for API
- **OpenCV** - Computer vision and image processing
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning model
- **Joblib** - Model serialization

### Frontend
- **Streamlit** - Modern web interface
- **Plotly** - Interactive visualizations
- **Pillow** - Image processing

### Machine Learning
- **Haar Cascades** - Face and eye detection
- **Wavelet Transform** - Feature extraction
- **Supervised Learning** - Classification model

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Extract model files:**
   ```bash
   unzip server.zip
   unzip haarcascades.zip
   ```

4. **Run the application:**
   ```bash
   python run_app.py
   ```

5. **Open your browser and go to:**
   ```
   http://127.0.0.1:8501
   ```

## 📁 Project Structure

```
├── streamlit_app.py          # Streamlit frontend
├── run_app.py               # Startup script
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── server/                 # Backend files
│   ├── server.py          # Flask API server
│   ├── util.py            # Core ML functions
│   ├── wavelet.py         # Wavelet transform
│   ├── artifact/          # Model files
│   └── haarcascades/      # Face detection models
├── UI/                    # Old HTML frontend (deprecated)
└── saved_model.pkl        # Trained ML model
```

## 🔧 Manual Setup

If you prefer to run components separately:

### Backend (Flask API)
```bash
cd server
python server.py
```
Backend will run on: http://127.0.0.1:5000

### Frontend (Streamlit)
```bash
streamlit run streamlit_app.py
```
Frontend will run on: http://127.0.0.1:8501

## 🎨 Features

### Modern UI
- **Responsive Design** - Works on desktop and mobile
- **Interactive Upload** - Drag and drop image upload
- **Real-time Processing** - Live image analysis
- **Visual Results** - Beautiful result cards with confidence scores

### Advanced Analytics
- **Confidence Scores** - See prediction confidence for each player
- **Probability Charts** - Interactive bar charts showing all probabilities
- **Error Handling** - Clear error messages and guidance

### Technical Features
- **Face Detection** - Automatically detects faces in images
- **Eye Detection** - Ensures quality by detecting eyes
- **Wavelet Features** - Advanced feature extraction
- **Machine Learning** - Trained model for accurate classification

## 🔍 How It Works

1. **Image Upload** - User uploads an image through the Streamlit interface
2. **Face Detection** - OpenCV detects faces using Haar Cascades
3. **Eye Detection** - Ensures the face has visible eyes for better accuracy
4. **Feature Extraction** - Wavelet transform extracts features from the image
5. **Classification** - Machine learning model predicts the sports personality
6. **Results Display** - Shows the result with confidence scores and visualizations

## 🐛 Troubleshooting

### Common Issues

**"Cannot connect to server"**
- Make sure the Flask backend is running on port 5000
- Check if the server directory contains all required files

**"No faces detected"**
- Upload an image with a clear, well-lit face
- Ensure the face is not too small or blurry
- Try a different image with better lighting

**"Missing dependencies"**
- Run: `pip install -r requirements.txt`
- Make sure you're using Python 3.7+

**"Model files not found"**
- Extract all zip files: `server.zip` and `haarcascades.zip`
- Ensure the directory structure matches the project layout

## 📊 Model Performance

The model uses:
- **Wavelet Transform** for feature extraction
- **Supervised Learning** with scikit-learn
- **Face and Eye Detection** for quality control
- **32x32 pixel** image processing

## 🤝 Contributing

Feel free to:
- Add more sports personalities
- Improve the UI/UX
- Enhance the machine learning model
- Add new features

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ using Streamlit, Flask, and Machine Learning**
