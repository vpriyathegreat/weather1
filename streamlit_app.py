import streamlit as st
from streamlit_option_menu import option_menu


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import io


with st.sidebar:
  selected=option_menu(
    menu_title=None,
    options=["overview","how aqi varies with time","highest and lowest aqi analysis","seasonal and remark analysis of aqi"],
    default_index=0)

st.balloons()

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
      st.write(" The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
    
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
      st.write(" The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
    
  #HR VS AQI
  if aqi_option=="Hour vs aqi":
    st.subheader("Hour vs AQI Barplot")
    fig,ax=plt.subplots()
    a=sns.barplot(x='Hour',y='aqi',data=df,estimator=np.std)
    st.write(fig)
    with st.expander("See explanation"):
      st.write(" The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
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
      st.write(" The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
    
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

    with tab3:
      st.subheader("average air quality index for each month over the years")
      monthly_avg_air_quality = df.groupby(['Year', 'Month'])['aqi'].mean()
      a=pd.DataFrame(monthly_avg_air_quality)
      table = pd.pivot_table(a, values = 'aqi', index ='Year',
                         columns ='Month')
      st.write(table)
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
  with tab2:
    st.title("Remark Analysis")
    st.divider()
    st.subheader("barplot of year vs aqi with remark analysis of each year")
    st.write("")
    fig,ax=plt.subplots(figsize=(10, 5))
    sns.barplot(x='Year',y='aqi',data=df,estimator=np.std,hue='remark')
    st.write(fig)
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
