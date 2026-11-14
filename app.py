
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

latest_location = {}
emergency_alerts = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/location", methods=["POST"])
def update_location():
    global latest_location

    data = request.get_json()

    if not data or "latitude" not in data or "longitude" not in data:
        return jsonify({"error": "Invalid location"}), 400

    latest_location = {
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    print("Location updated:", latest_location)
    return jsonify({"status": "Location updated"})

@app.route("/api/location", methods=["GET"])
def get_location():
    if not latest_location:
        return jsonify({"error": "No location available"}), 404

    return jsonify(latest_location)

@app.route("/api/sos", methods=["POST"])
def sos():
    alert = {
        "message": "SOS EMERGENCY!",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "location": latest_location.copy()
    }

    emergency_alerts.append(alert)
    print("\n!!! SOS EMERGENCY ALERT !!!")
    print(alert)

    return jsonify({
        "status": "SOS recorded",
        "alert": alert
    })

if __name__ == "__main__":
    app.run(debug=True)
