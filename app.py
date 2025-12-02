import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# Load data
data = pd.read_csv('skyriver_matchback.csv')

# Set custom CSS to make the map fullscreen and adjust the layout
st.markdown("""
    <style>
    .main {
        padding-top: 30px;
        text-align: center;
    }
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 20px;
        color: white;
    }
    .info {
        display: flex;
        justify-content: center;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 30px;
    }
    .info > div {
        margin: 0 20px;
    }
    iframe {
        width: 100% !important;
        height: 80vh !important;  /* 80% height of the screen */
    }
    .map-container {
        width: 100%;
        height: 80vh;  /* 80% height of the screen */
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit UI for user input
st.markdown('<div class="title">Sky Rivers Data </div>', unsafe_allow_html=True)

# Calculate total locations and total IPs
total_locations = data['zipcode'].nunique()
total_ips = data['OTT IP Matchback'].nunique()

# Display total locations and IPs in a horizontal layout
st.markdown(f"""
<div class="info">
    <div>Total Locations: {total_locations}</div>
    <div>Avg Latitude: {data['latitude'].mean():.6f}</div>
    <div>Avg Longitude: {data['longitude'].mean():.6f}</div>
</div>
""", unsafe_allow_html=True)

# Create a map centered around the average latitude and longitude of the full dataset
map_center = [data['latitude'].mean(), data['longitude'].mean()]
map_object = folium.Map(location=map_center, zoom_start=6)

# Add marker cluster
marker_cluster = MarkerCluster().add_to(map_object)

# Add IP markers for all data
for _, row in data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"IP: {row['OTT IP Matchback']}, Zipcode: {row['zipcode']}, Region: {row['Region']}",
    ).add_to(marker_cluster)

# Render the map inside a div that makes it fullscreen
st.write("Map displaying all IPs in the dataset::")
folium_static(map_object, height=800)

# Optional: Add map legend below (uncomment if needed)
# st.markdown("""
# <div class="map-legend">
#     <div><span style="color:green;">●</span> URL Data (Green)</div>
#     <div><span style="color:blue;">●</span> Store Data (Blue)</div>
# </div>
# """, unsafe_allow_html=True)
