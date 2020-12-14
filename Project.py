"""
Zach D'Addabbo
CS230 - Final Project
Fall 2020
Data Set: AirBnB
December 13, 2020
URL:
Description: This program runs a streamlit web application using AirBnB data to allow users to select from 2 possible
seach queries to search for listings within the Boston area. Query 1, allows them to search by price per night and the
room type, the displays a table and a map of the listings within the criteria. Query 2, allows the user to search
by price per night and by the neighborhood and displays a table and a map of the listings, the user can also look up
the number of reviews that the host has on each of their property
"""

#imports
import pandas as pd
import matplotlib as plt
import streamlit as st
import numpy as np
import statistics
import csv
import datetime
import pydeck as pdk

#csv file with AirBnB lissting data
listings = "airbnb_cambridge_listings_20201123.csv"
listing_options = []

st.title("AirBnB Search Tool")
st.sidebar.header("Search Criteria")
df_li = pd.read_csv("airbnb_cambridge_listings_20201123.csv")

def roomtype():         #Selectbox for room type search criteria
    df_li = pd.read_csv("airbnb_cambridge_listings_20201123.csv")
    roomTypes = df_li["room_type"].unique()     #list of unique room types
    roomSelect = st.sidebar.selectbox("Please select a room type", roomTypes)
    df_li = df_li.loc[df_li['room_type'] == roomSelect]
    #st.write("Search by Room Type")

    #Slider bar for price per night
    minPrice = df_li["price"].min()
    maxPrice = df_li["price"].max()
    priceSelect = st.sidebar.slider("Please select the nightly price range", int(minPrice), int(maxPrice), (1, 1000))
    st.text(priceSelect)
    df_li = df_li.loc[df_li['price'] >= priceSelect[0]]
    df_li = df_li.loc[df_li['price'] <= priceSelect[1]]
    st.write("Search by Room Type and Nightly Price")
    st.dataframe(df_li)

    #st.dataframe(df_li)
    st.write("Map of AirBnB listings by price per night and neighborhood")
    st.map(df_li)
    view_state = pdk.ViewState(
        latitude=42.3601,
        longitude=71.0589,
        zoom=10,
        pitch=10)

    layer1 = pdk.Layer('ScatterplotLayer',
                       data=df_li,
                       get_position='[lon, lat]',
                       get_radius=300,
                       #get_color=[0,0,255],
                       pickable=True,
                       opacity=0.8,
                       get_line_color=[0, 0, 0],
                       get_fill_color=[255, 0, 0],
                       filled=True,
                       stroked=True,
                      )

def neighbourhoods():     #Multiselect of neighbourhoods
    df_li = pd.read_csv("airbnb_cambridge_listings_20201123.csv")

     #Slider bar for price per night
    minPrice = df_li["price"].min()
    maxPrice = df_li["price"].max()
    priceSelect = st.sidebar.slider("Please select the nightly price range", int(minPrice), int(maxPrice), (1, 1000))
    st.text(priceSelect)
    df_li = df_li.loc[df_li['price'] >= priceSelect[0]]
    df_li = df_li.loc[df_li['price'] <= priceSelect[1]]


    neighbourhoods = df_li["neighbourhood"].unique()     #list of unique neighbourhoods
    neighbourhoodSelect = st.sidebar.multiselect("Please select the desired neighbourhoods", neighbourhoods)
    df_li = df_li.loc[df_li['neighbourhood'].isin(neighbourhoodSelect)]
    st.write("Search by Neighbourhood(s) and price per night")
    st.dataframe(df_li)
    #Map of listings within neighborhoods - adjustable by user
    st.write("Map of AirBnB listings by neighborhood and price per night")
    st.map(df_li)

    view_state = pdk.ViewState(
        latitude=42.3601,
        longitude=71.0589,
        zoom=10,
        pitch=10)

    layer1 = pdk.Layer('ScatterplotLayer',
                       data=df_li,
                       get_position='[lon, lat]',
                       get_radius=300,
                       #get_color=[0,0,255],
                       pickable=True,
                       opacity=0.8,
                       get_line_color=[0,0,0],
                       get_fill_color=[0,0,255],
                       filled=True,
                       stroked=True,
                      )

def popularListings(host_id):
    data = pd.read_csv("airbnb_cambridge_listings_20201123.csv")
    data_df = pd.DataFrame(data=df_li, columns=['host_id', 'host_name', 'name', 'number_of_reviews'])
    data_df['host_id'] = data_df['host_id'].astype(str)
    data_df = data_df[(data_df['host_id'] == host_id)]
    data_df = data_df.set_index('name')
    return data_df

def barChart():
    data = pd.read_csv("airbnb_cambridge_listings_20201123.csv")
    data_df = pd.DataFrame(data=df_li, columns=['host_id', 'number_of_reviews'])
    total_per_host = data_df.groupby(['host_id',])['number_of_reviews'].sum()
    top_hosts = total_per_host.nlargest(5, keep="first")
    top_hosts.plot(kind="bar")
    return plt

CHOICE = ["Listing Search Criteria 1", "Listing Search Criteria 2"]
selection = st.sidebar.radio("Please select an option:", CHOICE)
if selection == CHOICE[0]:
    roomtype()

if selection == CHOICE[1]:
    neighbourhoods()
    barChart()

    st.write("Chart of reviews by Host ID")
    host_id = st.text_input("Enter Host ID number:")
    st.area_chart(popularListings(host_id))
