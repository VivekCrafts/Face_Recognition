from flask import Flask, request, jsonify
from flask_cors import CORS
import util
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

@app.route('/classify_image', methods=['POST'])
def classify_image():
    try:
        if 'image_data' not in request.form:
            return jsonify({'error': 'No image data provided'}), 400
        
        image_data = request.form['image_data']
        
        if not image_data:
            return jsonify({'error': 'Empty image data'}), 400

        result = util.classify_image(image_data)
        
        if not result:
            return jsonify({'error': 'No faces detected in the image'}), 400
            
        response = jsonify(result)
        return response
        
    except Exception as e:
        logger.error(f"Error in classify_image: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == "__main__":
    print("Starting Python Flask Server For Sports Celebrity Image Classification")
    util.load_saved_artifacts()
    app.run(host='0.0.0.0', port=5000, debug=False)
