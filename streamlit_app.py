import streamlit as st
import requests
import base64
import io
from PIL import Image
import json

# Page configuration
st.set_page_config(
    page_title="Sports Personality Classifier",
    page_icon="🏆",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .player-card {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .result-card {
        border: 3px solid #28a745;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .confidence-badge {
        background: #28a745;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">🏆 Sports Personality Classifier</h1>', unsafe_allow_html=True)
st.markdown("""
This application can classify sports personalities from uploaded images. 
Currently supports: **Lionel Messi**, **Maria Sharapova**, **Roger Federer**, **Serena Williams**, and **Virat Kohli**.
""")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    **How it works:**
    1. Upload an image containing a face
    2. The system detects faces and eyes
    3. Uses machine learning to classify the sports personality
    4. Shows results with confidence scores
    
    **Requirements:**
    - Clear face in the image
    - Good lighting
    - Face should be clearly visible
    """)
    
    st.header("🔧 Technical Details")
    st.markdown("""
    - **Backend:** Flask API with OpenCV
    - **Model:** Machine Learning with wavelet features
    - **Face Detection:** Haar Cascades
    - **Frontend:** Streamlit
    """)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Upload Image")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg'],
        help="Upload an image containing a sports personality's face"
    )
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Add classify button
        if st.button("🔍 Classify Image", type="primary"):
            with st.spinner("Analyzing image..."):
                try:
                    # Send request to Flask API
                    response = requests.post(
                        "http://127.0.0.1:5000/classify_image",
                        data={"image_data": f"data:image/jpeg;base64,{img_str}"},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        if result and len(result) > 0:
                            # Find the best match
                            best_match = max(result, key=lambda x: max(x['class_probability']))
                            confidence = max(best_match['class_probability'])
                            
                            # Display result
                            with col2:
                                st.header("🎯 Classification Result")
                                
                                # Player information
                                player_info = {
                                    "lionel_messi": {
                                        "name": "Lionel Messi",
                                        "sport": "Football",
                                        "emoji": "⚽"
                                    },
                                    "maria_sharapova": {
                                        "name": "Maria Sharapova", 
                                        "sport": "Tennis",
                                        "emoji": "🎾"
                                    },
                                    "roger_federer": {
                                        "name": "Roger Federer",
                                        "sport": "Tennis", 
                                        "emoji": "🎾"
                                    },
                                    "serena_williams": {
                                        "name": "Serena Williams",
                                        "sport": "Tennis",
                                        "emoji": "🎾"
                                    },
                                    "virat_kohli": {
                                        "name": "Virat Kohli",
                                        "sport": "Cricket",
                                        "emoji": "🏏"
                                    }
                                }
                                
                                player = player_info.get(best_match['class'])
                                if player:
                                    st.markdown(f"""
                                    <div class="result-card">
                                        <h2>{player['emoji']} {player['name']}</h2>
                                        <p><strong>Sport:</strong> {player['sport']}</p>
                                        <div class="confidence-badge">
                                            Confidence: {confidence:.1f}%
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # Show all probabilities
                                    st.subheader("📊 All Probabilities")
                                    prob_data = {
                                        "Lionel Messi": best_match['class_probability'][1],
                                        "Maria Sharapova": best_match['class_probability'][2], 
                                        "Roger Federer": best_match['class_probability'][3],
                                        "Serena Williams": best_match['class_probability'][4],
                                        "Virat Kohli": best_match['class_probability'][5]
                                    }
                                    
                                    # Create a bar chart
                                    import plotly.express as px
                                    fig = px.bar(
                                        x=list(prob_data.keys()),
                                        y=list(prob_data.values()),
                                        title="Classification Probabilities",
                                        labels={'x': 'Player', 'y': 'Probability (%)'},
                                        color=list(prob_data.values()),
                                        color_continuous_scale='RdYlGn'
                                    )
                                    fig.update_layout(showlegend=False)
                                    st.plotly_chart(fig, use_container_width=True)
                                    
                        else:
                            st.error("❌ No faces detected in the image. Please upload an image with a clear face.")
                            
                    else:
                        st.error(f"❌ Server error: {response.status_code}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to the server. Please make sure the Flask server is running on port 5000.")
                except requests.exceptions.Timeout:
                    st.error("❌ Request timed out. Please try again.")
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")

with col2:
    if not uploaded_file:
        st.header("👥 Supported Players")
        
        # Display player cards
        players = [
            {"name": "Lionel Messi", "sport": "Football", "emoji": "⚽"},
            {"name": "Maria Sharapova", "sport": "Tennis", "emoji": "🎾"},
            {"name": "Roger Federer", "sport": "Tennis", "emoji": "🎾"},
            {"name": "Serena Williams", "sport": "Tennis", "emoji": "🎾"},
            {"name": "Virat Kohli", "sport": "Cricket", "emoji": "🏏"}
        ]
        
        for player in players:
            st.markdown(f"""
            <div class="player-card">
                <h3>{player['emoji']} {player['name']}</h3>
                <p><strong>{player['sport']}</strong></p>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Built with ❤️ using Streamlit, Flask, and Machine Learning</p>
</div>
""", unsafe_allow_html=True)