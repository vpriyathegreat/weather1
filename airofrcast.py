
import requests
from datetime import datetime

# Replace with your OpenWeather API key
openweather_api_key = "d90fab7004bbe953db2d107c55bb1d81"

# Step 1: Use the Geocoding API to get latitude and longitude by city name
city_name = "Delhi"  # Replace with your desired city
geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={openweather_api_key}"

response = requests.get(geocoding_url)

if response.status_code == 200:
    geocoding_data = response.json()
    
    if geocoding_data:
        # Extract latitude and longitude from the geocoding response
        latitude = geocoding_data[0]["lat"]
        longitude = geocoding_data[0]["lon"]
        
        # Step 2: Get 5-day forecast data using latitude and longitude
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={openweather_api_key}&units=metric"
        
        forecast_response = requests.get(forecast_url)
        
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            
            if forecast_data:
                # Extract and print the 5-day forecast
                print(f"5-Day Weather Forecast for {city_name}\n")
                
                for forecast in forecast_data["list"]:
                    dt_txt_utc = datetime.utcfromtimestamp(forecast["dt"])
                    dt_txt_local = dt_txt_utc.strftime('%Y-%m-%d %H:%M:%S')
                    weather_main = forecast["weather"][0]["main"]
                    temperature = forecast["main"]["temp"]
                    pressure = forecast["main"]["pressure"]
                    humidity = forecast["main"]["humidity"]
                    wind_speed = forecast["wind"]["speed"]
                    
                    print(f"Date/Time (Local): {dt_txt_local} IST")
                    print(f"Weather Main: {weather_main}")
                    print(f"Temperature: {temperature}°C")
                    print(f"Pressure: {pressure} hPa")
                    print(f"Humidity: {humidity}%")
                    print(f"Wind Speed: {wind_speed} m/s")
                    print("\n")
else:
    print("Error fetching data from the Geocoding API.")
