from flask import Flask, jsonify, render_template, request
import redis
import json
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# 🔑 API Key
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if not WEATHER_API_KEY:
    raise ValueError("❌ WEATHER_API_KEY is not set in .env")

# Redis connection
r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    password=os.getenv("REDIS_PASSWORD"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_DB", 0)),
    decode_responses=True
)

def fetch_weather_from_api(city):
    """Fetch weather data from WeatherAPI.com"""
    print(f"Fetching weather data from WeatherAPI for {city}...")

    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
    response = requests.get(url)

    if response.status_code != 200:
        return {"success": False, "error": f"Could not fetch data for {city}"}

    data = response.json()
    return {
        "success": True,
        "data": {
            "city": data["location"]["name"],
            "region": data["location"]["region"],
            "country": data["location"]["country"],
            "local_time": data["location"]["localtime"],
            "temperature_c": data["current"]["temp_c"],
            "temperature_f": data["current"]["temp_f"],
            "feels_like_c": data["current"]["feelslike_c"],
            "humidity": data["current"]["humidity"],
            "wind_kph": data["current"]["wind_kph"],
            "wind_dir": data["current"]["wind_dir"],
            "condition": data["current"]["condition"]["text"],
            "icon": data["current"]["condition"]["icon"],
            "uv_index": data["current"]["uv"],
            "last_updated": data["current"]["last_updated"]
        }
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather/<city>")
def get_weather_query(city):
    if not city:
        return jsonify({"success": False, "error": "City parameter is required"}), 400

    cache_key = f"weather:{city.lower()}"

    # 1. Try Redis
    try:
        cached_data = r.get(cache_key)
    except redis.exceptions.ConnectionError:
        cached_data = None

    if cached_data:
        print(f"Cache hit for {city} ✅")
        return jsonify(json.loads(cached_data))

    # 2. Fetch API
    weather_data = fetch_weather_from_api(city)

    # 3. Cache it
    if weather_data["success"]:
        try:
            r.setex(cache_key, 3600, json.dumps(weather_data))
            print(f"Cache set for {city} ⏱️ (expires in 3600s)")
        except redis.exceptions.ConnectionError:
            print("⚠️ Redis not available, skipping cache")

    return jsonify(weather_data)

@app.route("/clear-cache/<city>")
def clear_cache(city):
    cache_key = f"weather:{city.lower()}"
    try:
        r.delete(cache_key)
    except redis.exceptions.ConnectionError:
        return jsonify({"success": False, "error": "Redis unavailable"}), 500
    return jsonify({"success": True, "message": f"Cache cleared for {city}"})

@app.route("/stats")
def stats():
    try:
        keys = r.keys("weather:*")
        return jsonify({"success": True, "cached_cities": keys, "cache_size": len(keys)})
    except redis.exceptions.ConnectionError:
        return jsonify({"success": False, "error": "Redis unavailable"}), 500

@app.route("/flush-cache")
def flush_cache():
    try:
        keys = r.keys("weather:*")
        for key in keys:
            r.delete(key)
        return jsonify({"success": True, "message": "All weather cache cleared"})
    except redis.exceptions.ConnectionError:
        return jsonify({"success": False, "error": "Redis unavailable"}), 500

@app.route("/ping-redis")
def ping_redis():
    try:
        response = r.ping()
        return jsonify({"success": True, "redis_status": "PONG" if response else "No response"})
    except redis.exceptions.ConnectionError as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/redis-info")
def redis_info():
    try:
        info = r.info()
        return jsonify({"success": True, "info": info})
    except redis.exceptions.ConnectionError as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/favicon.ico")
def favicon():
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
