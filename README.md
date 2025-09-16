Weather Flask App with Redis Caching 🌤️
This is a simple Flask web application that fetches weather information from WeatherAPI.com and caches the results using Redis to improve performance. The app also provides endpoints to manage and inspect the cache.

Features
Fetch current weather for any city.

Cache weather data in Redis for 1 hour to reduce API calls.

Clear cache for a specific city or flush all cached data.

Inspect cache statistics and Redis server info.

Ping Redis to check connectivity.

Web frontend for easy access (via index.html).

Technologies Used
Python 3.x

Flask – Lightweight web framework

Redis – In-memory caching

WeatherAPI – Source for weather data

dotenv – Manage environment variables

Requests – HTTP requests to external API

Setup & Installation
Clone the repository

Bash

git clone <repository-url>
cd <repository-folder>
Create a virtual environment (optional but recommended)

Bash

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Install dependencies

Bash

pip install -r requirements.txt

Configure environment variables
Create a .env file in the project root with the following:

WEATHER_API_KEY=<Your WeatherAPI Key>
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=<Your Redis Password (if any)>
REDIS_DB=0
⚠️ Make sure your Redis server is running and accessible.

Run the Flask app

Bash```
python app.py
By default, the app runs on http://127.0.0.1:5000.

API Endpoints
Get Weather
GET /weather/<city>

Response Example:

JSON

{
  "success": true,
  "data": {
    "city": "London",
    "region": "City of London, Greater London",
    "country": "United Kingdom",
    "local_time": "2025-09-16 14:00",
    "temperature_c": 20.5,
    "temperature_f": 68.9,
    "feels_like_c": 19.0,
    "humidity": 65,
    "wind_kph": 12.0,
    "wind_dir": "NW",
    "condition": "Partly cloudy",
    "icon": "//cdn.weatherapi.com/weather/64x64/day/116.png",
    "uv_index": 3,
    "last_updated": "2025-09-16 13:45"
  }
}
Clear Cache for a City
GET /clear-cache/<city>

Flush All Cache
GET /flush-cache

View Cache Stats
GET /stats

Response Example:

JSON

{
  "success": true,
  "cached_cities": ["weather:london", "weather:new york"],
  "cache_size": 2
}
Ping Redis
GET /ping-redis

Response Example:

JSON

{
  "success": true,
  "redis_status": "PONG"
}
Redis Server Info
GET /redis-info

Frontend
The app serves a simple HTML page at the root / route. You can extend templates/index.html to include a search form for weather queries.

Redis Notes
Cached data is stored under keys like weather:<city>.

Cache expiration is set to 3600 seconds (1 hour).

Redis connection issues are gracefully handled in the app.

License
MIT License © 2025