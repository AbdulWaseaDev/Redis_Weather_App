// async function getWeather() {
//   const city = document.getElementById("city").value;
//   console.log("Fetching weather for city:", city);
//   if (!city) {
//     alert("Please enter a city name.");
//     return;
//   }

//   try {
//     const response = await fetch(`/weather/${city}`);
//     const result = await response.json();
//     if (!result) {
//       document.getElementById("weatherResult").innerHTML = "<p>⚠ No data received.</p>";
//       return;
//     }
// const w = result.data;
// document.getElementById("weatherResult").innerHTML = `
//     <h2>Weather in ${w.city}, ${w.country}</h2>
//     🕒 Local Time: ${w.local_time}<br>
//     🌡 Temperature: ${w.temperature_c}°C (Feels like ${w.feels_like_c}°C)<br>
//     ☁ Condition: ${w.condition} <img src="https:${w.icon}" alt="${w.condition}"><br>
//     💨 Wind: ${w.wind_kph} km/h (${w.wind_dir})<br>
//     💧 Humidity: ${w.humidity}%<br>
//     🔆 UV Index: ${w.uv_index}<br>
//     ⏱ Last Updated: ${w.last_updated}
// `;
//         showStats();
//   } catch (error) {
//     console.error("Error fetching weather:", error);
//     document.getElementById("weatherResult").innerHTML = "<p>⚠ Failed to fetch weather data.</p>";
//   }
// }
async function getWeather() {
    const city = document.getElementById("city").value.trim();
    if (!city) {
        alert("Please enter a city name!");
        return;
    }

    try {
        const res = await fetch(`/weather/${encodeURIComponent(city)}`);
        const result = await res.json();

        if (!result.success) {
            alert(result.error || "Failed to fetch weather data");
            return;
        }

        const w = result.data;

        const weatherDiv = document.getElementById("weatherResult");
        weatherDiv.classList.remove("hidden");
        weatherDiv.innerHTML = `
            <h2>Weather in ${w.city}, ${w.country}</h2>
            <div class="weather-row">
                <span>🕒 Local Time:</span> <span>${w.local_time}</span>
            </div>
            <div class="weather-row">
                <span>🌡 Temperature:</span> <span>${w.temperature_c}°C (Feels like ${w.feels_like_c}°C)</span>
            </div>
            <div class="weather-row">
                <span>☁ Condition:</span>
                <span>${w.condition} <img src="https:${w.icon}" alt="${w.condition}"></span>
            </div>
            <div class="weather-row">
                <span>💨 Wind:</span> <span>${w.wind_kph} km/h (${w.wind_dir})</span>
            </div>
            <div class="weather-row">
                <span>💧 Humidity:</span> <span>${w.humidity}%</span>
            </div>
            <div class="weather-row">
                <span>🔆 UV Index:</span> <span>${w.uv_index}</span>
            </div>
            <div class="weather-row">
                <span>⏱ Last Updated:</span> <span>${w.last_updated}</span>
            </div>
        `;
    } catch (err) {
        console.error("Error fetching weather:", err);
        alert("Something went wrong. Please try again later.");
    }
}



async function showStats() {
  try {
    const response = await fetch(`/stats`);
    const data = await response.json();
    document.getElementById("stats").innerHTML = `
      <p>Cached Cities: ${data.cached_cities.join(", ") || "None"}</p>
      <p>Cache Size: ${data.cache_size}</p>
    `;
  } catch (error) {
    console.error("Error fetching stats:", error);
    document.getElementById("stats").innerHTML = "<p>⚠ Failed to fetch stats.</p>";
  }
}

async function flushCache() {
  try {
    const response = await fetch(`/flush-cache`);
    const data = await response.json();
    alert(data.message);
    showStats();
  } catch (error) {
    console.error("Error flushing cache:", error);
    alert("⚠ Failed to flush cache.");
  }
}
