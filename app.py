import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

'''
# Taxi fare prediction
'''

pickup_datetime = st.datetime_input("Select date and time")
st.write(" ")
st.write("Select your pickup and drop-off locations")

# New York default center
NYC = [40.730610, -73.935242]

if "points" not in st.session_state:
    st.session_state.points = []

if "center" not in st.session_state:
    st.session_state.center = NYC

if "zoom" not in st.session_state:
    st.session_state.zoom = 10

# Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Clear points"):
        st.session_state.points = []
with col2:
    if st.button("Reset to New York"):
        st.session_state.center = NYC
        st.session_state.zoom = 10
        st.session_state.points = []

# Build map
m = folium.Map(location=st.session_state.center, zoom_start=st.session_state.zoom)

# Existing markers
for i, (lat, lon) in enumerate(st.session_state.points, start=1):
    folium.Marker(
        [lat, lon],
        tooltip=f"Point {i}",
        popup=f"Point {i}: {lat:.6f}, {lon:.6f}",
    ).add_to(m)

# Render map
map_data = st_folium(
    m,
    width=700,
    height=500,
    key="map",
    returned_objects=["last_clicked", "zoom", "center"]
)

# Save view state
if map_data:
    if map_data.get("center"):
        st.session_state.center = [
            map_data["center"]["lat"],
            map_data["center"]["lng"]
        ]
    if map_data.get("zoom"):
        st.session_state.zoom = map_data["zoom"]

# Add up to 2 clicked points
if map_data and map_data.get("last_clicked"):
    clicked = map_data["last_clicked"]
    new_point = (clicked["lat"], clicked["lng"])

    if len(st.session_state.points) < 2:
        if new_point not in st.session_state.points:
            st.session_state.points.append(new_point)
            st.rerun()

# passenger_count = st.text_area("Number of passengers")
passenger_count = st.number_input(
    "Number of passengersr", value=1, placeholder="Type a number...", min_value=1, max_value=4
)
if st.button("Validate"):
    if len(st.session_state.points) == 2:
        params = {
            "pickup_datetime": pickup_datetime,
            "pickup_latitude": st.session_state.points[0][0],
            "pickup_longitude": st.session_state.points[0][1],
            "dropoff_latitude": st.session_state.points[1][0],
            "dropoff_longitude": st.session_state.points[1][1],
            "passenger_count": passenger_count
        }

        response = requests.get("http://127.0.0.1:8000/predict", params=params)

        if response.ok:
            if response.ok:
                data = response.json()
                fare = data["fare"]
                st.write(f"Fare: ${round(fare, 2)}")
        else:
            st.error(f"API error: {response.status_code}")
    else:
        st.warning("Please fill all inputs")