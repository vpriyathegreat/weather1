import streamlit as st
from streamlit_option_menu import option_menu


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import io
import requests



with st.sidebar:
  selected=option_menu(
    menu_title=None,
    options=["overview","how aqi varies with time","highest and lowest aqi analysis","seasonal and remark analysis of aqi","airforecast","AIR"],
    default_index=0)



df=pd.read_csv("air-quality-india.csv")
df.rename(columns = {'PM2.5':'aqi'}, inplace = True)

#ADDING NEW COL REMARK 
def remarkfn(x):
  if x>=0 and x<=50:
    return 'good'
  elif x>50 and x<=100:
    return 'satisfactory'
  elif x>100 and x<=200:
    return 'moderate'
  elif x>200 and x<=300:
    return 'poor'
  elif x>300 and x<=400:
    return 'very poor'
  elif x>400:
    return 'severe'
df['remark']=df['aqi'].apply(remarkfn)

################## OVERVIEW TAB ###################

if selected=="overview":   #overview tab
  st.title( " EDA Of Air Quality Index Data ")

  st.markdown('<hr style="border: 2px solid blue;">', unsafe_allow_html=True)

  st.header("Dataframe")
  st.divider()
  st.write(df)   #dataframe displayed
  st.write("  ")
  st.write("  ")
  
  col1, col2, col3 = st.columns([28,24,60])
  
  with col1:  #for displaying buttn=ons side by side. this is for show info
    a=st.button("***Show Info***")  #creating show info button
    
    if a: #if show info button is clciked then,

      buffer = io.StringIO()
      df.info(buf=buffer)  #storing  df.info values in buffer as its outputs to console not web pg
      info= buffer.getvalue()
      st.text(info)  #displaying content of df.info

      #if st.button('Reset'):   #non conventional way
       #  a=False

  with col2:
    b=st.button("***Check Null Values***")
    
    if b:
      mis=df.isnull().sum()
      st.write(mis)  #displaying content of mis
      
      st.markdown('<p style="font-size: 20px;"><b>There are no missing values in any of the columns of this dataframe</b></p>', unsafe_allow_html=True)
 
  with col3:
    
    c=st.button("***Describe***")

    if c:  
      st.write(df.describe())
      

#ADDING RESET ALL BUTTON
  if a==True or b==True or c==True:
    if st.button("RESET ALL"):
      a=False
      b=False
      c=False
  st.divider()
########## HOW AQI VAORES WITH TIME TAB #########

if selected=="how aqi varies with time":
  st.title("How AQI Varies With Time")
  st.divider()

  aqi_option = st.selectbox("**Select one of the comparisons below and the corrsponding graph will be displayed**",("Year vs aqi", "Month vs aqi", "Hour vs aqi"),
    index=None,
    placeholder="Select",
  )
  st.write("")
  
  st.write('**You selected   :**', aqi_option)
  st.divider()
  #YEAR VS AQI
  if aqi_option=="Year vs aqi":
    st.subheader("Year vs AQI Barplot")
    
    fig,ax=plt.subplots()
    a=sns.barplot(x='Year',y='aqi',data=df,estimator=np.std)
    st.write(fig)
    
    with st.expander("See explanation"):
      st.write(" ->We infer that the aqi was the :red[highest] in year 2018 because of Uncontrolled stubble burning vehicle emissions ")
      st.markdown("-> Hence several measures were taken by government to reduce the aqi such as: **The Supreme Court of India ordered a ban on the sale of petrol and diesel vehicles above 2000 cc in Delhi**")
      st.write("->The Indian government launched the National Clean Air Programme (NCAP)")
      st.markdown('-> Hence several measures were taken by government to reduce the aqi such as: <p style="color:Green; font-size: 20px;">The Supreme Court of India ordered a ban on the sale of petrol and diesel vehicles above 2000 cc in Delhi</p>', unsafe_allow_html=True)

    
    #LINEPLOT
    st.divider()
    st.subheader("Year vs AQI Lineplot")
    grped_hr=df.groupby("Hour").mean(numeric_only=True)
    grped_hr_index=grped_hr.index
    fig,ax=plt.subplots(figsize=(8, 3))
    plt.plot(grped_hr_index, grped_hr.aqi, marker='o', color='red', linestyle='-')
    plt.title('Mean AQI values with Time(Hour)')
    plt.xlabel('Hour')
    plt.ylabel('AQI')
    plt.xticks(grped_hr_index)
    st.write(fig)
    with st.expander("See explanation"):
      st.write(" The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
    
  #MONTH VS AQI
  if aqi_option=="Month vs aqi":
    st.subheader("Month vs AQI Barplot")
    fig,ax=plt.subplots()
    a=sns.barplot(x='Month',y='aqi',data=df,estimator=np.std)
    st.write(fig)
    with st.expander("See explanation"):
      st.write("->air quality in India is  better between june to september months than in other months. This is because of several reasons:")
      st.markdown("->the monsoon season typically runs from June to September, and the rain helps to wash away pollutants from the air.")

      st.write("->Increased Ventilation: During the summer, there is often more wind and natural ventilation, which can help disperse air pollutants and improve air quality")

      st.markdown("->Lower Industrial Emissions: Some industries may reduce their operations or emissions during the summer months due to reduced energy demand for heating and cooling.")
      st.write("->Less Biomass Burning: Apart from crop residue burning, the burning of wood and other biomass for heating is more common during the winter months. This contributes to particulate matter and air pollution") 

    #LINEPLOT
    st.divider()
    st.subheader("Month vs AQI Lineplot")
    grped_month=df.groupby("Month").mean(numeric_only=True)
    grped_month_index=grped_month.index
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(grped_month_index, grped_month.aqi, marker='o', color='red', linestyle='-')
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_title("Line Plot")
    st.write(fig)
    with st.expander("See explanation"):
      st.markdown("we can see that between the months june to october there is a significant drop in aqi compared to its peak values in january and december There are a few reasons why there is a significant drop in AQI between the months of June to October compared to its peak values in January and December in India.")

      st.markdown("->Monsoon season: The monsoon season in India typically runs from June to September. The rain from the monsoon helps to wash away pollutants from the air, which improves air quality.") 

      st.markdown("->Reduced stubble burning: Stubble burning is a common practice among farmers in northern India after harvesting their crops in October-November. The smoke from stubble burning contains high levels of particulate matter, which is a major air pollutant ->Lower temperatures: Temperatures are typically lower during the monsoon season than during the winter months. Lower temperatures can help to reduce the formation of ground-level ozone, which is a harmful air pollutant.")


  #HR VS AQI
  if aqi_option=="Hour vs aqi":
    st.subheader("Hour vs AQI Barplot")
    fig,ax=plt.subplots()
    a=sns.barplot(x='Hour',y='aqi',data=df,estimator=np.std)
    st.write(fig)
    with st.expander("See explanation"):
     st.markdown("""the AQI is worse during the time 4-8 and 14-21, as there are many factors that can affect air qualit:
*increased traffic during these times: 4-8 and 14-21 are typically peak commuting times, so there is more traffic on the roads during these times. This can lead to increased emissions from vehicles, which can worsen air quality.
*Meteorological conditions: Meteorological conditions, such as low wind speeds and temperature inversions, can trap pollutants in the air and make them more concentrated. These conditions are more likely to occur in the early morning and evening hours""")
      
      

    st.divider()
    st.subheader("Hour vs AQI Lineplot")
    grped_hr=df.groupby("Hour").mean(numeric_only=True)
    grped_hr_index=grped_hr.index
    fig,ax=plt.subplots(figsize=(8, 3))
    plt.plot(grped_hr_index, grped_hr.aqi, marker='o', color='red', linestyle='-')
    plt.title('Mean AQI values with Time(Hour)')
    plt.xlabel('Hour')
    plt.ylabel('AQI')
    plt.xticks(grped_hr_index)
    st.write(fig)
    with st.expander("See explanation"):
     st.markdown("""HOURLY ANALYSIS

we can see that the aqi is generally very high between 5pm-7pm and also during 5am in the morning.The aqi gradually dips down after 7pm there r few reasons for this: 
  
->Increased traffic: 5pm-7pm is typically a peak commuting time in India, so there is more traffic on the roads during this time 
            
->Meteorological conditions:these conditions are more likely to occur in the evening hours and early morning, which could explain why the AQI is often highest between 5pm-7pm and 5am. ->Industrial emissions: Some industries may operate 24 hours a day, but they may emit more pollutants during certain times of the day, such as during the evening hours and early morning hours.
            

Its particularly dips down after 7 pm because: 
->Increased wind speeds: Wind speeds are typically higher at night than during the day. This can help to disperse pollutants in the air, which can improve air quality. 

->Decreased temperatures: Temperatures are typically lower at night than during the day. This can help to reduce the formation of ground-level ozone, which is a harmful air pollutant.""")

#checking for null values

########HIGHEST AND LOWEST AQI TAB ####################
if selected=="highest and lowest aqi analysis":
  st.title("Maximum and Minimum AQI Analysis")
  st.divider()
  tab1, tab2, tab3 = st.tabs(["Max and min recorded aqi for each year", "analysis of year with max mean aqi", "In depth analysis of aqi of month and years"])

  with tab1:
    st.header("mean aqi recodered for each year")
    st.write("")
    fig,ax=plt.subplots(figsize=(8,3))
    a=df.groupby("Year")["aqi"].mean()
    a.plot(kind="bar",xlabel="Year",ylabel="maximum recorded aqi",title="Maximum recorded aqi of each year")
    st.write(fig)
    with st.expander("**So was the highest aqi recorded in 2017?**"):
      st.write(" Not quite! Surprisingly the highest aqi was recorded on 7/11/2018 at 9pm with a value of 245.63 ! This could be due to missing daat in the yr 2017")
      st.markdown("""**here we notice that the maximum recorded aqi was in 2017 and the minimum was recorded in the year 2020.**
There are a few reasons why India recorded its maximum AQI in 2017 and its minimum AQI in 2020:
2020
->COVID-19 lockdown: The COVID-19 lockdown in India led to a significant reduction in economic activity, including a reduction in vehicle traffic and industrial activity. This reduction in emissions led to an improvement in air quality.
->Reduced stubble burning: The Indian government took a number of steps to reduce stubble burning in 2020, such as providing financial incentives to farmers for using alternative methods of disposing of their crop stubble
2017:
->Meteorological conditions: India experienced a severe drought in 2016-17, which led to increased dust storms and forest fires
->Vehicle emissions: Vehicle emissions are a major source of air pollution in India. In 2017, India had one of the largest vehicle populations in the world""")

  with tab2:
    st.subheader("The year 2017 has the maximum mean aqi.")
    st.markdown("<ul> <li style='font-size: 20px'>November had the highest aqi in 2017</li> <li style='font-size: 20px'>December had the lowest aqi in 2017</li></ul>",unsafe_allow_html=True)
    st.write("")

    import matplotlib.ticker as ticker
    w=df[df["Year"]==2017].groupby("Month").mean(numeric_only=True)#gives max of every col of a month of the yr 2017

    maxmonth=w.loc[w["aqi"].idxmax()] #gives year day hour corresponding to the overall max aqi. gives the month having max aqi
    minmonth=w.loc[w["aqi"].idxmin()] #gives the month having min aqi
    #print("month having max aqi\n" ,maxmonth, "month having min aqi\n",minmonth,sep="\n")

    #hr vs aqi analysis for 2017

    st.header("Mean hourly analysis of the year 2017")
    st.write("")
    month_time=df[df['Year']==2017].groupby('Hour').mean(numeric_only=True)

    fig,ax=plt.subplots(figsize=(10, 5))
    g=sns.lineplot(x=month_time.index,y=month_time.aqi,data=month_time ,marker='o')
    plt.title("aqi for the yr 2017(hourly analysis)")
    g.xaxis.set_major_locator(ticker.MultipleLocator(1)) #define intervals in x axis(x axis scale)
    g.set_xticks(range(24)) #(tick range)

    g.xaxis.set_major_formatter(ticker.ScalarFormatter())
    st.write(fig)
    with st.expander("See explanation"):
      st.markdown("""we find that the highest aqi in 2017 recorded was 97.71 in the month of November andlowest is 93.20 in the month of December.

there are several reasons:
->Meteorological conditions: The month of November typically has low wind speeds and temperature inversions, which can trap pollutants in the air and make them more concentrated. These conditions are less common in the month of December.
->Diwali: Diwali, the Hindu festival of lights, is typically celebrated in October-November. Diwali is a time when people burn fireworks and candles. The smoke from fireworks and candles can worsen air quality.
->Stubble burning: Stubble burning is a common practice among farmers in northern India after harvesting their crops in October-November. The smoke from stubble burning contains high levels of particulate matter, which is a major air pollutant
  
Whereas it is interesting to note that the AQI in India is often highest at around 5pm. the possible reasons for it are:
->Increased traffic: 5pm is typically a peak commuting time in India, so there is more traffic on the roads during this time
->Industrial emissions: Some industries may operate 24 hours a day, but they may emit more pollutants during certain times of the day, such as during the evening hours. This could also contribute to the higher AQI at around 5pm.
""")


    with tab3:
      st.subheader("average air quality index for each month over the years")
      monthly_avg_air_quality = df.groupby(['Year', 'Month'])['aqi'].mean()
      a=pd.DataFrame(monthly_avg_air_quality)
      table = pd.pivot_table(a, values = 'aqi', index ='Year',
                         columns ='Month')
      st.write(table)
      with st.expander("See explanation"):
       st.markdown("We notice that in the month of November, there's consistently high AQI because of festivals like Diwali.")
       st.markdown("Diwali is a Hindu festival that is celebrated with fireworks and bonfires. The burning of fireworks and bonfires releases large amounts of pollutants into the air.")
       st.markdown("The poor air quality in India in November 2017 had a significant impact on public health. Schools were closed in Delhi and other cities due to the poor air quality. Many people also reported experiencing respiratory problems.")
       st.markdown("Increasing the use of public transportation, promoting the use of electric vehicles, banning the burning of biomass, and implementing stricter emission standards for vehicles and industries are some of the measures to address air pollution.")
       st.markdown("The Indian government has taken a number of steps to address air pollution, including implementing stricter emission standards for vehicles and industries and banning the burning of biomass. However, more needs to be done to improve air quality in India. In January 2018, the Supreme Court of India banned the use of diesel vehicles older than 10 years in Delhi and the National Capital Region (NCR). The court also ordered the government to implement a number of other measures to reduce air pollution.")
  ############## seasonal and remark analysis tab ###############################
if selected=="seasonal and remark analysis of aqi":
    tab1, tab2= st.tabs(["Seasonal Analysis", "Remark analysis"])
    with tab1:
      st.title("Seasonal Analysis")
      st.divider()
      st.write("")
      summer = df[df["Month"].isin([3, 4, 5])]["aqi"].mean()
      monsoon = df[df["Month"].isin([6, 7, 8, 9])]["aqi"].mean()
      autumn = df[df["Month"].isin([10, 11])]["aqi"].mean()
      winter = df[df["Month"].isin([12, 1])]["aqi"].mean()
  
      seasons = ['Summer', 'Monsoon', 'Autumn', 'Winter']
      mean = [ summer,monsoon,autumn,winter]
      fig,ax=plt.subplots(figsize=(1,1))
      ax.patch.set_facecolor('black')
      st.subheader("Air Quality Distribution by Seasons")
      st.write("")
      plt.pie(mean, labels=seasons, autopct="%1.1f%%", startangle=140,textprops={"fontsize":4})
      #plt.title("Air Quality Distribution by Seasons")
      plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
      st.write(fig)
      with st.expander("See explanation"):
       st.markdown("""

Theres a higher AIQ during winter and autumn months because of Weather Patterns: 
->During winter and autumn, certain regions in India experience weather conditions that can contribute to poor air quality. For example, winter often brings temperature inversions, where cold air near the ground traps pollutants, leading to increased pollution levels. 

->Reduced Dispersion: During winter, the lower temperatures and reduced wind speeds can limit the dispersion of pollutants, causing them to accumulate in the atmosphere and leading to higher AQI levels

->Increased use of fossil fuels for heating: During the winter months, people in India use fossil fuels such as coal and wood for heating their homes. This can lead to an increase in the emission of pollutants into the air.

->Geographical location: India is located in a region that is prone to dust storms. Dust storms can carry large amounts of pollutants into the air, which can worsen air quality.""")
       

    
    with tab2:
      st.title("Remark Analysis")
      st.divider()
      st.subheader("barplot of year vs aqi with remark analysis of each year")
      st.write("")
      fig,ax=plt.subplots(figsize=(10, 5))
      sns.barplot(x='Year',y='aqi',data=df,estimator=np.std,hue='remark')
      st.write(fig)
      with st.expander("See explanation"):
        st.markdown("""**we can see that aqi isnt very poor or severe during any of the years. The aqi is poorest in the year 2018 with the maxium no of poor recoded cases**
this was particularly due to:

1.Construction activities: Construction activities can also contribute to air pollution, especially in urban areas. In 2018, there was a significant increase in construction activities in India, which may have contributed to the worsening air quality.
2.Economic growth: India experienced rapid economic growth in 2018, which led to an increase in industrial emissions and vehicle traffic. Both of these factors can contribute to air pollution.

In addition to these factors, the rapid growth of urbanization and industrialization in India is also contributing to worsening air quality.""")

      st.divider()
      st.header("Air Distribution By Ratings")
      poor_count=df[df['remark']=='poor']['Year'].count()
      good_count=df[df['remark']=='good']['Year'].count()
      moderate_count=df[df['remark']=='moderate']['Year'].count()
      satisfactory_count=df[df['remark']=='satisfactory']['Year'].count()
      poor_count,good_count,moderate_count,satisfactory_count
      ratings = ['poor','good','satisfactory','moderate']
      ratings_count= [ poor_count,good_count,moderate_count,satisfactory_count]
  
     
      fig,ax=plt.subplots(figsize=(1,1))
      plt.pie(ratings_count, labels=ratings, autopct="%1.2f%%", startangle=140,textprops={"fontsize":4})
      plt.title("Air Quality Distribution by ratings",fontsize=6)
      plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
      st.write(fig)
      with st.expander("See explanation"):
        st.markdown("""The overall AQI in India is mostly good, with 56.1% of the days having a good AQI rating. However, it is concerning that 40.24% of the days have a moderate AQI rating and 3.73% of the days have a satisfactory AQI rating. This means that on more than half of the days in India, the air quality is not good.

The fact that the AQI is poor on only 0.02% of the days is a positive sign, but it is important to note that even a short exposure to poor air quality can have negative health effects.

The Indian government is taking a number of steps to improve air quality, but more needs to be done to address the root causes of air pollution, such as stubble burning, vehicle emissions, construction dust, and industrial emissions.""")




# Check if the "airforecast" option is selected
if selected == "airforecast":
    # Replace with your OpenWeather API key
    openweather_api_key = "d90fab7004bbe953db2d107c55bb1d81"


    # Set the title of the Streamlit app
    st.title("5-Day Weather Forecast App")

    # User input for the city name
    city_name = st.text_input("Enter the city name:", "Delhi")

    # Check if the "Get Weather Forecast" button is clicked
    if st.button("Get Weather Forecast"):
        # Step 1: Use the Geocoding API to get latitude and longitude by city name
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




# Replace with your OpenWeather API key
api_key = "d90fab7004bbe953db2d107c55bb1d81"

# Streamlit app title
st.title("Air Quality Index")

# Input for city name
city_name = st.text_input("Enter the city name:", "Delhi")

# Button to fetch air quality data
if st.button("Fetch Air Quality Data"):
    # Function to get current air pollution data
    def get_current_air_pollution(city_name, api_key):
        # Step 1: Geocoding API to get latitude and longitude
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"

        # Make the Geocoding API request
        geocoding_response = requests.get(geocoding_url)

        # Check if the Geocoding request was successful
        if geocoding_response.status_code == 200:
            # Parse the JSON response
            geocoding_data = geocoding_response.json()

            # Check if data is available
            if geocoding_data:
                location = geocoding_data[0]
                latitude = location["lat"]
                longitude = location["lon"]
                country = location["country"]
                state = location.get("state", "N/A")

                # Step 2: Air Pollution API to get air quality data (Current)
                air_pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}"

                # Make the Air Pollution API request
                air_pollution_response = requests.get(air_pollution_url)

                # Check if the Air Pollution request was successful
                if air_pollution_response.status_code == 200:
                    # Parse the JSON response
                    air_pollution_data = air_pollution_response.json()

                    # Check if data is available
                    if "list" in air_pollution_data:
                        air_pollution_info = air_pollution_data["list"][0]
                        aqi = air_pollution_info["main"]["aqi"]
                        components = air_pollution_info["components"]
                        current_data = air_pollution_data["list"]
                        timestamp = current_data[0]['dt']

                        # Convert Unix timestamp to date (IST)
                        date = dt.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')

                        # Display current air pollution data
                        st.subheader("Current Air Pollution Data:")
                        st.write(f"City: {city_name}")
                        st.write(f"Latitude: {latitude}")
                        st.write(f"Longitude: {longitude}")
                        st.write(f"Air Quality Index (AQI): {aqi}")
                        st.write(f"Date (IST): {date}")
                        st.subheader("Components:")
                        st.write(f"CO: {components['co']} µg/m³")
                        st.write(f"NO: {components['no']} µg/m³")
                        st.write(f"NO2: {components['no2']} µg/m³")
                        st.write(f"O3: {components['o3']} µg/m³")
                        st.write(f"SO2: {components['so2']} µg/m³")
                        st.write(f"PM2.5: {components['pm2_5']} µg/m³")
                        st.write(f"PM10: {components['pm10']} µg/m³")
                        st.write(f"NH3: {components['nh3']} µg/m³")
                    else:
                        st.error("No current air pollution data available for the specified location.")
                else:
                    st.error("Error: Unable to fetch current air pollution data from the API.")
            else:
                st.error("No geocoding data available for the specified city.")
        else:
            st.error("Error: Unable to fetch geocoding data from the API.")

    # Call the function to get current air pollution data
    get_current_air_pollution(city_name, api_key)
