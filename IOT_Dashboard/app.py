from flask import Flask, render_template, jsonify, request
import time
import json
import os

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
    """Serve the AirTag-like tracker page"""
    return render_template('airtag.html')

@app.route('/api/tracker-data', methods=['GET'])
def get_tracker_data():
    """API endpoint to get the latest tracker data"""
    return jsonify(last_data)

@app.route('/api/update', methods=['POST'])
def update_tracker():
    """API endpoint for receiving location updates"""
    global last_data, location_history

    try:
        if request.is_json:
            data = request.get_json()
        else:
            # Accepting form data for compatibility
            data = {
                'device_id': request.form.get('device_id'),
                'latitude': float(request.form.get('lat', last_data["latitude"])),
                'longitude': float(request.form.get('lng', last_data["longitude"])),
                'battery': int(request.form.get('bat', last_data["battery"])),
                'signal': int(request.form.get('sig', last_data["signal"]))
            }
            if 'acc' in request.form:
                data['accuracy'] = float(request.form.get('acc'))
            if 'spd' in request.form:
                data['speed'] = float(request.form.get('spd'))

        # Update required fields safely
        last_data["device_id"] = data.get('device_id', last_data["device_id"])
        last_data["latitude"] = float(data.get('latitude', last_data["latitude"]))
        last_data["longitude"] = float(data.get('longitude', last_data["longitude"]))
        last_data["battery"] = int(data.get('battery', last_data["battery"]))
        last_data["signal"] = int(data.get('signal', last_data["signal"]))
        last_data["timestamp"] = time.time()

        # Update optional fields if provided
        if 'accuracy' in data:
            last_data["accuracy"] = float(data['accuracy'])
        if 'speed' in data:
            last_data["speed"] = float(data['speed'])

        # Add to history
        history_entry = {
            "latitude": last_data["latitude"],
            "longitude": last_data["longitude"],
            "timestamp": last_data["timestamp"]
        }
        location_history.insert(0, history_entry)

        # Limit history size
        location_history = location_history[:MAX_HISTORY_SIZE]

        # Save history to file
        save_history()
        return jsonify({"status": "success", "message": "Location updated"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/history', methods=['GET'])
def get_history():
    """API endpoint to get location history"""
    limit = request.args.get('limit', default=10, type=int)
    return jsonify(location_history[:limit])

def save_history():
    """Save history to a file"""
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

@app.route('/simulate', methods=['GET'])
def simulate():
    """Simple page to simulate device updates for testing"""
    return render_template('simulate.html')

if __name__ == '__main__':
    load_history()
    app.run(host='0.0.0.0', port=5000, debug=True)
