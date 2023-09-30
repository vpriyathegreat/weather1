import streamlit as st
import requests
from datetime import datetime


openweather_api_key = "d90fab7004bbe953db2d107c55bb1d81"

st.title("5-Day Weather Forecast App")

    # User input for the city name
city_name = st.text_input("Enter the city name:", "Delhi")

if st.button("Get Weather Forecast"):# Step 1: Use the Geocoding API to get latitude and longitude by city name
    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={openweather_api_key}"
    response = requests.get(geocoding_url)
    if response.status_code == 200:
        geocoding_data = response.json()
        if geocoding_data:# Extract latitude and longitude from the geocoding response
                latitude = geocoding_data[0]["lat"]
                longitude = geocoding_data[0]["lon"]

                # Step 2: Get 5-day forecast data using latitude and longitude
                forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={openweather_api_key}&units=metric"

                forecast_response = requests.get(forecast_url)

                if forecast_response.status_code == 200:
                    forecast_data = forecast_response.json()

                    if forecast_data:
                        # Display the 5-day forecast
                        st.subheader(f"5-Day Weather Forecast for {city_name}")
                        for forecast in forecast_data["list"]:
                            dt_txt_utc = dt.utcfromtimestamp(forecast["dt"])
                            dt_txt_local = dt_txt_utc.strftime('%Y-%m-%d %H:%M:%S')
                            weather_main = forecast["weather"][0]["main"]
                            temperature = forecast["main"]["temp"]
                            pressure = forecast["main"]["pressure"]
                            humidity = forecast["main"]["humidity"]
                            wind_speed = forecast["wind"]["speed"]

                            st.write(f"Date/Time (Local): {dt_txt_local} IST")
                            st.write(f"Weather Main: {weather_main}")
                            st.write(f"Temperature: {temperature}°C")
                            st.write(f"Pressure: {pressure} hPa")
                            st.write(f"Humidity: {humidity}%")
                            st.write(f"Wind Speed: {wind_speed} m/s")
                            st.write("\n")
                else:
                    st.error("Error fetching weather forecast data.")
            else:
                st.error("No data found for the provided city name.")
        else:
            st.error("Error fetching data from the Geocoding API.")

