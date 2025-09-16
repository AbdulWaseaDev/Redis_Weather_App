
# Weather Flask App with Redis Caching 🌤️

This is a simple Flask web application that fetches weather information from WeatherAPI.com and caches the results using Redis to improve performance. The app also provides endpoints to manage and inspect the cache.


## Features

- Fetch current weather for any city.
- Cache weather data in Redis for 1 hour to reduce API calls.
- Clear cache for a specific city or flush all cached data.
- Inspect cache statistics and Redis server info.
- Ping Redis to check connectivity.
- Web frontend for easy access (via index.html).


## Tech Stack

- Python 3.x
- Flask – Lightweight web framework
- Redis – In-memory caching
- WeatherAPI – Source for weather data
- dotenv – Manage environment variables
- Requests – HTTP requests to external API

## Setup & Installation

1) Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

2) Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3) Install dependencies

```bash
pip install -r requirements.txt
```

4) Configure environment variables

```bash
WEATHER_API_KEY=<Your WeatherAPI Key>
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=<Your Redis Password (if any)>
REDIS_DB=0
```
⚠️ Make sure your Redis server is running and accessible.

5) Run the Flask app

```bash
python app.py
```
By default, the app runs on http://127.0.0.1:5000.
## API Endpoints

Get Weather
- GET /weather/<city>

Clear Cache for a City
- GET /clear-cache/<city>

Flush All Cache
- GET /flush-cache

View Cache Stats
- GET /stats

Redis Server Info
- GET /redis-info

## Frontend
The app serves a simple HTML page at the root / route. You can extend templates/index.html to include a search form for weather queries.

**Redis Notes**

- Cached data is stored under keys like weather:<city>.
- Cache expiration is set to 3600 seconds (1 hour).
- Redis connection issues are gracefully handled in the app.