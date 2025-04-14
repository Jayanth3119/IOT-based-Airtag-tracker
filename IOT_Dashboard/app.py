from flask import Flask, render_template, jsonify, request
import time
import json
import os
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')

# Store the last received data
last_data = {
    "device_id": "ESP-Tracker-01",
    "latitude": 12.870693,
    "longitude": 80.221922,
    "accuracy": 10.0,
    "speed": 0.0,
    "battery": 80,
    "signal": 75,
    "timestamp": time.time()
}

# Placeholder for history (would be a database in production)
location_history = []
MAX_HISTORY_SIZE = 50  # Limit number of history entries

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return render_template('index.html')

@app.route('/find-vehicle')
def find_vehicle_page():
    """Serve the Find My Vehicle page"""
    return render_template('find_vehicle.html')

@app.route('/air-tag')
def airtag_tracker():
    """Serve the Find My Vehicle page"""
    return render_template('airtag.html')

@app.route('/api/tracker-data', methods=['GET'])
def get_tracker_data():
    """API endpoint to get the latest tracker data"""
    global last_data
    return jsonify(last_data)

@app.route('/api/update', methods=['POST'])
def update_tracker():
    """API endpoint for the ESP8266 to send location updates"""
    global last_data, location_history
    
    if request.method == 'POST':
        try:
            # Handle both JSON and form data
            if request.is_json:
                data = request.get_json()
            else:
                # For devices that might send URL-encoded form data
                data = {
                    'device_id': request.form.get('device_id'),
                    'latitude': float(request.form.get('lat', 0)),
                    'longitude': float(request.form.get('lng', 0)),
                    'battery': int(request.form.get('bat', 0)),
                    'signal': int(request.form.get('sig', 0))
                }
                
                # Optional fields
                if 'acc' in request.form:
                    data['accuracy'] = float(request.form.get('acc'))
                if 'spd' in request.form:
                    data['speed'] = float(request.form.get('spd'))
            
            # Update required fields
            last_data["device_id"] = data.get('device_id', last_data["device_id"])
            last_data["latitude"] = data.get('latitude', last_data["latitude"])
            last_data["longitude"] = data.get('longitude', last_data["longitude"])
            last_data["battery"] = data.get('battery', last_data["battery"])
            last_data["signal"] = data.get('signal', last_data["signal"])
            last_data["timestamp"] = time.time()
            
            # Update optional fields if provided
            if 'accuracy' in data:
                last_data["accuracy"] = data['accuracy']
            if 'speed' in data:
                last_data["speed"] = data['speed']
            
            # Add to history
            history_entry = {
                "latitude": last_data["latitude"],
                "longitude": last_data["longitude"],
                "timestamp": last_data["timestamp"]
            }
            location_history.insert(0, history_entry)
            
            # Limit history size
            if len(location_history) > MAX_HISTORY_SIZE:
                location_history = location_history[:MAX_HISTORY_SIZE]
            
            # Save history to file (In production, use a proper database)
            save_history()
            
            return jsonify({"status": "success", "message": "Location updated"})
            
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
    
    return jsonify({"status": "error", "message": "Invalid request"}), 400

@app.route('/api/history', methods=['GET'])
def get_history():
    """API endpoint to get location history"""
    limit = request.args.get('limit', default=10, type=int)
    return jsonify(location_history[:limit])

def save_history():
    """Save history to a file (would be a database in production)"""
    try:
        with open('location_history.json', 'w') as f:
            json.dump(location_history, f)
    except Exception as e:
        print(f"Error saving history: {e}")

def load_history():
    """Load history from a file at startup"""
    global location_history
    try:
        if os.path.exists('location_history.json'):
            with open('location_history.json', 'r') as f:
                location_history = json.load(f)
    except Exception as e:
        print(f"Error loading history: {e}")

# For demo purposes, add a simulation endpoint
@app.route('/simulate', methods=['GET'])
def simulate():
    """Simple page to simulate device updates for testing"""
    return render_template('simulate.html')

if __name__ == '__main__':
    # Load history at startup
    load_history()
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)