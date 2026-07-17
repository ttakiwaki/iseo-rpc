from dotenv import load_dotenv
import os
import time
import threading
import requests
from flask import Flask, request
from flask_cors import CORS
from pypresence import Presence, ActivityType

# Grabs Discord Application Client ID from .env file
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")

# Initialize app with CORS (opens API requests from all origins)
app = Flask(__name__)
CORS(app)

# Connects to discord
rpc = Presence(CLIENT_ID)

try:
    rpc.connect()
    print("Connected to Discord")
except:
    print("Discord not found. make sure the desktop app is running")

# Helps avoid being rate limited by Discord
pending_timer = None
last_track = None

def make_timestamp(current_time, duration):
    now = time.time()
    start_time = now - current_time
    end_time = start_time + duration
    return int(start_time), int(end_time)

# Send data to Discord

def get_cover(payload):
    if not payload.get("albumMBID"):
        return None

    url = f"https://coverartarchive.org/release/{payload['albumMBID']}/front"
    response = requests.get(url, allow_redirects=True)
    if response.status_code == 200:
        return url
    return None
    

def to_discord(payload):
    global last_track

    if not payload.get("playing"):
        rpc.clear()
        last_track = None
        return


    key = (payload["title"], payload["artist"])
    if key == last_track:
        return
    
    last_track = key
    cover_url = get_cover(payload)

    if payload.get("playing"):
        start_time, end_time = make_timestamp(payload["currentTime"], payload["duration"])
        rpc.update(
            name="iseo",
            details=payload["title"],
            state=f"{payload['artist']} - {payload['album']}",
            start=start_time,
            end=end_time,
            activity_type=ActivityType.LISTENING,
            large_image=cover_url or "icon",
            large_text=payload["album"] if len(payload.get("album", "")) >= 2 else "ISEO",
            large_url="https://github.com/ttakiwaki/iseo-player"
    ) 
    
    print(f"RPC Updated: {payload['title']}")

def cooldown_update(payload):
    global pending_timer

    if pending_timer is not None:
        pending_timer.cancel()

    pending_timer = threading.Timer(5.0, to_discord, args=[payload])
    pending_timer.start()

@app.route("/update", methods=["POST"])
def update():
    payload = request.get_json()
    cooldown_update(payload)
    return "", 204

if __name__ == "__main__":
    app.run(port=8000, use_reloader=False)
