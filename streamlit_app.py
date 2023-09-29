import streamlit as st
st.title( " EDA ")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

st.markdown("OVERVIEW")
st.sidebar.markdown("VARIATION OF AQI WITH TIME")

#fig, ax = plt.subplots()

df=pd.read_csv("air-quality-india.csv")
df.rename(columns = {'PM2.5':'aqi'}, inplace = True)
df

df.info()

#checking for null values
df.isnull().sum()

#dropping timestamp column
df.drop('Timestamp',axis=1,inplace=True)




#renaming aqi column
df.rename(columns = {'PM2.5':'aqi'}, inplace = True)
df
#fig, ax = plt.subplots()
st.header("Year vs AQI")
fig, ax = plt.subplots()
sns.barplot(x='Year',y='aqi',data=df,estimator=np.std)
sns.pairplot(data=df)
#df[df['Year']==2017]['aqi'].mean()

st.pyplot(fig)
st.markdown("""->We infer that the aqi was the highest in year 2018  because of:
 Uncontrolled stubble burning
 vehicle emissions
 -> hence several measures were taken by government to  reduce the aqi such as:
 *The Supreme Court of India ordered a ban on the sale of petrol and diesel vehicles above 2000 cc in Delhi
 *The Indian government launched the National Clean Air Programme (NCAP) """)


st.header("MONTH vs AQI")

fig, ax = plt.subplots()
sns.barplot(x="Month",y="aqi",data=df)
st.pyplot(fig)
st.markdown("""air quality in India is  better between june to september months than in other months. This is because of several reasons:
            
*the monsoon season typically runs from June to September, and the rain helps to wash away pollutants from the air.

*Increased Ventilation: During the summer, there is often more wind and natural ventilation, which can help disperse air pollutants and improve air quality

*Lower Industrial Emissions: Some industries may reduce their operations or emissions during the summer months due to reduced energy demand for heating and cooling.

*Less Biomass Burning: Apart from crop residue burning, the burning of wood and other biomass for heating is more common during the winter months. This contributes to particulate matter and air pollution""")
fig, ax = plt.subplots()

st.header("HOUR vs AQI")

#w=df[df['Year']==a[0]]

sns.barplot(x='Hour',y='aqi',data=df)


st.pyplot(fig)
st.markdown("""the AQI is worse during the time 4-8 and 14-21, as there are many factors that can affect air qualit:
*increased traffic during these times: 4-8 and 14-21 are typically peak commuting times, so there is more traffic on the roads during these times. This can lead to increased emissions from vehicles, which can worsen air quality.
*Meteorological conditions: Meteorological conditions, such as low wind speeds and temperature inversions, can trap pollutants in the air and make them more concentrated. These conditions are more likely to occur in the early morning and evening hours""")




st.header("count of aqi for each year")
fig, ax = plt.subplots()
a=df.groupby("Year").count()["aqi"]
a.plot(kind="bar",xlabel="Year",ylabel="count", title="DataFrameGroupBy Plot")

st.pyplot(fig)

st.header("max recorded aqi for each year")

#max aqi of every year  #find the mean of all years.

a=df.groupby("Year")["aqi"].mean()
a.plot(kind="bar",xlabel="Year",ylabel="maximum recorded aqi",title="Maximum recorded aqi of each year")

st.markdown("""**here we notice that the maximum recorded aqi was in 2017 and the minimum was recorded in the year 2020.**
There are a few reasons why India recorded its maximum AQI in 2017 and its minimum AQI in 2020:
2020
->COVID-19 lockdown: The COVID-19 lockdown in India led to a significant reduction in economic activity, including a reduction in vehicle traffic and industrial activity. This reduction in emissions led to an improvement in air quality.
->Reduced stubble burning: The Indian government took a number of steps to reduce stubble burning in 2020, such as providing financial incentives to farmers for using alternative methods of disposing of their crop stubble
2017:
->Meteorological conditions: India experienced a severe drought in 2016-17, which led to increased dust storms and forest fires
->Vehicle emissions: Vehicle emissions are a major source of air pollution in India. In 2017, India had one of the largest vehicle populations in the world""")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

# Assuming you have already loaded your DataFrame 'df'

# Create a Streamlit app
st.title("AQI for the Year 2017 (Hourly Analysis)")

# Create the figure and axes
fig, ax = plt.subplots(figsize=(10, 5))

# Perform the groupby and calculate the monthly averages
month_time = df[df['Year'] == 2017].groupby('Hour').mean()

# Create the line plot using Seaborn
g = sns.lineplot(x=month_time.index, y=month_time['aqi'], data=month_time, marker='o', ax=ax)

# Set plot title and labels
plt.title("AQI for the Year 2017 (Hourly Analysis)")
plt.xlabel("Hour of the Day")
plt.ylabel("AQI")

# Customize the x-axis ticks
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.set_xticks(range(24))
ax.xaxis.set_major_formatter(ticker.ScalarFormatter())

# Display the plot in Streamlit
st.pyplot(fig)

st.markdown("""we find that the highest aqi in 2017 recorded was 97.71 in the month of November andlowest is 93.20 in the month of December.

there are several reasons:
->Meteorological conditions: The month of November typically has low wind speeds and temperature inversions, which can trap pollutants in the air and make them more concentrated. These conditions are less common in the month of December.
->Diwali: Diwali, the Hindu festival of lights, is typically celebrated in October-November. Diwali is a time when people burn fireworks and candles. The smoke from fireworks and candles can worsen air quality.
->Stubble burning: Stubble burning is a common practice among farmers in northern India after harvesting their crops in October-November. The smoke from stubble burning contains high levels of particulate matter, which is a major air pollutant
  
Whereas it is interesting to note that the AQI in India is often highest at around 5pm. the possible reasons for it are:
->Increased traffic: 5pm is typically a peak commuting time in India, so there is more traffic on the roads during this time
->Industrial emissions: Some industries may operate 24 hours a day, but they may emit more pollutants during certain times of the day, such as during the evening hours. This could also contribute to the higher AQI at around 5pm.
""")

#*converting months to names**

#converting month nos to names
months_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November',12:'December'}


df["DOW"]= df["Month"].map(months_dict)
#df.drop("DOW",axis=1,inplace=True)



## **How aqi varies with time(hourly),month,year**

#mean aqi with time(hourly)
fig, ax = plt.subplots()
grped_hr=df.groupby("Hour").mean(numeric_only=True)
grped_hr_index=grped_hr.index
fig, ax = plt.subplots(figsize=(10, 5))
#plt.figure(figsize=(8, 3))
#plt.subplot(1,2,1)
plt.plot(grped_hr_index, grped_hr.aqi, marker='o', color='red', linestyle='-')

plt.title('Mean AQI values with Time(Hour)')
plt.xlabel('Hour')
plt.ylabel('AQI')
plt.xticks(grped_hr_index) #??
st.pyplot(fig)
st.markdown("""HOURLY ANALYSIS

we can see that the aqi is generally very high between 5pm-7pm and also during 5am in the morning.The aqi gradually dips down after 7pm there r few reasons for this: 
  
->Increased traffic: 5pm-7pm is typically a peak commuting time in India, so there is more traffic on the roads during this time 
            
->Meteorological conditions:these conditions are more likely to occur in the evening hours and early morning, which could explain why the AQI is often highest between 5pm-7pm and 5am. ->Industrial emissions: Some industries may operate 24 hours a day, but they may emit more pollutants during certain times of the day, such as during the evening hours and early morning hours.
            

Its particularly dips down after 7 pm because: 
->Increased wind speeds: Wind speeds are typically higher at night than during the day. This can help to disperse pollutants in the air, which can improve air quality. 

->Decreased temperatures: Temperatures are typically lower at night than during the day. This can help to reduce the formation of ground-level ozone, which is a harmful air pollutant.""")

# Streamlit app
st.title('Air Quality Analysis')


#st.pyplot(fig)  # Display the plot in Streamlit

# You can add more Streamlit components to display results, such as text, tables, etc.


#mean aqi with month
fig, ax = plt.subplots(figsize=(10, 5))
grped_month=df.groupby("Month").mean(numeric_only=True)
grped_month_index=grped_month.index
#plt.figure(figsize=(10,3))
#plt.subplot(1,2,1)
plt.plot(grped_month_index, grped_month.aqi, marker='o', color='red', linestyle='-')
plt.title('Mean AQI values with Month')
plt.xlabel('Month')
plt.ylabel('AQI')
st.pyplot(fig)

#mean aqi with year
grped_yr=df.groupby("Year").mean(numeric_only=True)
grped_yr_index=grped_yr.index
grped_month_index=grped_month.index
plt.subplot(1,2,2)
plt.plot(grped_yr_index, grped_yr.aqi, marker='o', color='red', linestyle='-')
plt.title('Mean AQI values with Year')
plt.xlabel('Year')
plt.ylabel('AQI')
st.pyplot(fig)




st.header("MONTHLY ANALYSIS")

st.markdown("""

we can see that between the months june to october there is a significant drop in aqi compared to its peak values in january and december There are a few reasons why there is a significant drop in AQI between the months of June to October compared to its peak values in January and December in India.

->Monsoon season: The monsoon season in India typically runs from June to September. The rain from the monsoon helps to wash away pollutants from the air, which improves air quality. 

->Reduced stubble burning: Stubble burning is a common practice among farmers in northern India after harvesting their crops in October-November. The smoke from stubble burning contains high levels of particulate matter, which is a major air pollutant ->Lower temperatures: Temperatures are typically lower during the monsoon season than during the winter months. Lower temperatures can help to reduce the formation of ground-level ozone, which is a harmful air pollutant.""")

st.header("weekend vs weekday")

p = df.groupby(df["Day"]%7==0).agg({"Day": "first", "aqi": "mean"})
i=df.groupby(~df["Day"].isin([5, 6])).agg({"Day": "first", "aqi": "mean"}) #weekday
print(p,i,sep="\n")



df[df["Day"]%7==0]["Day"].unique()

st.header("average air quality index for each month over the years")

monthly_avg_air_quality = df.groupby(['Year', 'Month'])['aqi'].mean()
a=pd.DataFrame(monthly_avg_air_quality)
a.head()

st.markdown("""Theres a higher AIQ during winter and autumn months because of Weather Patterns: 
->During winter and autumn, certain regions in India experience weather conditions that can contribute to poor air quality. For example, winter often brings temperature inversions, where cold air near the ground traps pollutants, leading to increased pollution levels. 

->Reduced Dispersion: During winter, the lower temperatures and reduced wind speeds can limit the dispersion of pollutants, causing them to accumulate in the atmosphere and leading to higher AQI levels

->Increased use of fossil fuels for heating: During the winter months, people in India use fossil fuels such as coal and wood for heating their homes. This can lead to an increase in the emission of pollutants into the air.

->Geographical location: India is located in a region that is prone to dust storms. Dust storms can carry large amounts of pollutants into the air, which can worsen air quality.
""")

# **converting above df to pivot table**

table = pd.pivot_table(a, values = 'aqi', index ='Year',
                         columns ='Month')
table

st.markdown("""we notice that in the month of november theres a high aqi consistently because of festivals like diwali
Diwali is a Hindu festival that is celebrated with fireworks and bonfires. The burning of fireworks and bonfires releases large amounts of pollutants into the air.

The poor air quality in India in November 2017 had a significant impact on public health. Schools were closed in Delhi and other cities due to the poor air quality. Many people also reported experiencing respiratory problems.

Increasing the use of public transportation Promoting the use of electric vehicles Banning the burning of biomass Implementing stricter emission standards for vehicles and industries


The Indian government has taken a number of steps to address air pollution, including implementing stricter emission standards for vehicles and industries, and banning the burning of biomass. However, more needs to be done to improve air quality in India
es, there was a major restriction imposed after November 2017 to control air pollution in India. In January 2018, the Supreme Court of India banned the use of diesel vehicles older than 10 years in Delhi and the National Capital Region (NCR). The court also ordered the government to implement a number of other measures to reduce air pollution, including:

""")

# **highest aqi recorded along with the month and year** ::::

max_aqi=df['aqi'].max()#max aqi recorded
#which yr and month
df[(df['aqi']==max_aqi)][['Year','Month','aqi']]

st.markdown("""There are a number of reasons why the highest AQI recorded in India was in the year 2018 in the month of November because of  Construction activities: Construction activities can also contribute to air pollution, especially in urban areas. In 2018, there was a significant increase in construction activities in India, which may have contributed to the worsening air quality.""")





# **adding new col remark**

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
df

# **barplot of year vs aqi with remark analysis of each year**


sns.barplot(x='Year',y='aqi',data=df,estimator=np.std,hue='remark')







import pandas as pd



season_totals = df.groupby("Month")["aqi"].sum()
plt.figure(figsize=(8, 8))
plt.pie(season_totals, labels=season_totals.index, autopct="%1.1f%%", startangle=140)
plt.title("Air Quality Distribution by Season")
plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()



summer = df[df["Month"].isin([3, 4, 5])]["aqi"].mean()
monsoon = df[df["Month"].isin([6, 7, 8, 9])]["aqi"].mean()
autumn = df[df["Month"].isin([10, 11])]["aqi"].mean()
winter = df[df["Month"].isin([12, 1])]["aqi"].mean()

st.header("seasonal analysis of aqi")

import pandas as pd
st.header("Air Quality Distribution by Seasons")
seasons = ['Summer', 'Monsoon', 'Autumn', 'Winter']
mean = [ summer,monsoon,autumn,winter]

b=plt.figure(figsize=(1.5, 1.5))
plt.pie(mean, labels=seasons, autopct="%1.2f%%", startangle=140,textprops={"fontsize":4})
#plt.pie(mean, labels=seasons, autopct="%1.1f%%", startangle=140)
#plt.title("Air Quality Distribution by Seasons")
plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(b)
st.header("SEASONAL ANALYSIS")
st.markdown("""

Theres a higher AIQ during winter and autumn months because of Weather Patterns: 
->During winter and autumn, certain regions in India experience weather conditions that can contribute to poor air quality. For example, winter often brings temperature inversions, where cold air near the ground traps pollutants, leading to increased pollution levels. 

->Reduced Dispersion: During winter, the lower temperatures and reduced wind speeds can limit the dispersion of pollutants, causing them to accumulate in the atmosphere and leading to higher AQI levels

->Increased use of fossil fuels for heating: During the winter months, people in India use fossil fuels such as coal and wood for heating their homes. This can lead to an increase in the emission of pollutants into the air.

->Geographical location: India is located in a region that is prone to dust storms. Dust storms can carry large amounts of pollutants into the air, which can worsen air quality.""")
import seaborn as sns
import matplotlib.pyplot as plt


pivot_data = df.pivot_table(index='remark', columns='Month', values='aqi', aggfunc='mean')


plt.figure(figsize=(20,7))
sns.heatmap(pivot_data, cmap='YlGnBu', annot=True, fmt=".1f")
plt.title('Hourly and Daily AQI Levels')
plt.xlabel('Day of the Month')
plt.ylabel('Hour of the Day')
st.pyplot(fig)
st.markdown("""**we can see that aqi isnt very poor or severe during any of the years. The aqi is poorest in the year 2018 with the maxium no of poor recoded cases**
this was particularly due to:

1.Construction activities: Construction activities can also contribute to air pollution, especially in urban areas. In 2018, there was a significant increase in construction activities in India, which may have contributed to the worsening air quality.
2.Economic growth: India experienced rapid economic growth in 2018, which led to an increase in industrial emissions and vehicle traffic. Both of these factors can contribute to air pollution.

In addition to these factors, the rapid growth of urbanization and industrialization in India is also contributing to worsening air quality.""")


df[(df['Hour']==18) & (df['remark']=='moderate')]['aqi'].mean()



import pandas as pd
st.header("Air Quality Distribution by ratings")
poor_count=df[df['remark']=='poor']['Year'].count()
good_count=df[df['remark']=='good']['Year'].count()
moderate_count=df[df['remark']=='moderate']['Year'].count()
satisfactory_count=df[df['remark']=='satisfactory']['Year'].count()
poor_count,good_count,moderate_count,satisfactory_count
ratings = ['poor','good','satisfactory','moderate']
ratings_count= [ poor_count,good_count,moderate_count,satisfactory_count]

a=plt.figure(figsize=(1.5,1.5))
#a.patch.set_facecolor('black')
plt.pie(ratings_count, labels=ratings, autopct="%1.2f%%", startangle=140,textprops={"fontsize":4})
#plt.figure(facecolor='salmon')
#plt.title("Air Quality Distribution by ratings",fontsize=20)
plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(a)
st.markdown("""The overall AQI in India is mostly good, with 56.1% of the days having a good AQI rating. However, it is concerning that 40.24% of the days have a moderate AQI rating and 3.73% of the days have a satisfactory AQI rating. This means that on more than half of the days in India, the air quality is not good.

The fact that the AQI is poor on only 0.02% of the days is a positive sign, but it is important to note that even a short exposure to poor air quality can have negative health effects.

The Indian government is taking a number of steps to improve air quality, but more needs to be done to address the root causes of air pollution, such as stubble burning, vehicle emissions, construction dust, and industrial emissions.""")


