import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import os

API_URL = st.secrets["API_URL"]
if not API_URL:
    st.error("Missing API_URL environment variable")
    st.stop()

st.set_page_config(
    page_title="Taxi Fare Prediction",
    page_icon="🚕",
    layout="wide"
)

st.title("🚕 Taxi Fare Prediction")
st.caption("Select a date, the number of passengers, then click two points on the map: pickup and drop-off.")

NYC = [40.730610, -73.935242]

if "points" not in st.session_state:
    st.session_state.points = []

if "center" not in st.session_state:
    st.session_state.center = NYC

if "zoom" not in st.session_state:
    st.session_state.zoom = 10

left, right = st.columns([1, 1.4], gap="large")

with left:
    with st.container():
        st.subheader("Ride details")

        pickup_datetime = st.datetime_input("Pickup date and time")

        passenger_count = st.number_input(
            "Passengers",
            min_value=1,
            max_value=4,
            value=1,
            step=1
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Clear points", use_container_width=True):
                st.session_state.points = []
                st.rerun()
        with c2:
            if st.button("Reset map", use_container_width=True):
                st.session_state.center = NYC
                st.session_state.zoom = 10
                st.session_state.points = []
                st.rerun()

        st.divider()
        st.subheader("Selected points")

        if len(st.session_state.points) >= 1:
            lat1, lon1 = st.session_state.points[0]
            st.success(f"Pickup: {lat1:.5f}, {lon1:.5f}")
        else:
            st.info("Pickup not selected yet")

        if len(st.session_state.points) >= 2:
            lat2, lon2 = st.session_state.points[1]
            st.success(f"Drop-off: {lat2:.5f}, {lon2:.5f}")
        else:
            st.info("Drop-off not selected yet")

        st.divider()

        run_prediction = st.button("Estimate fare", type="primary", use_container_width=True)

with right:
    st.subheader("Map")
    st.caption("Click once for pickup, click a second time for drop-off.")

    m = folium.Map(location=st.session_state.center, zoom_start=st.session_state.zoom)

    if len(st.session_state.points) >= 1:
        folium.Marker(
            st.session_state.points[0],
            tooltip="Pickup",
            popup="Pickup location",
            icon=folium.Icon(color="green", icon="play", prefix="fa")
        ).add_to(m)

    if len(st.session_state.points) >= 2:
        folium.Marker(
            st.session_state.points[1],
            tooltip="Drop-off",
            popup="Drop-off location",
            icon=folium.Icon(color="red", icon="stop", prefix="fa")
        ).add_to(m)

        folium.PolyLine(
            locations=st.session_state.points,
            color="#4F8BF9",
            weight=4,
            opacity=0.8
        ).add_to(m)

    map_data = st_folium(
        m,
        width=900,
        height=520,
        key="map",
        returned_objects=["last_clicked", "zoom", "center"]
    )

if map_data:
    if map_data.get("center"):
        st.session_state.center = [
            map_data["center"]["lat"],
            map_data["center"]["lng"]
        ]
    if map_data.get("zoom"):
        st.session_state.zoom = map_data["zoom"]

if map_data and map_data.get("last_clicked"):
    clicked = map_data["last_clicked"]
    new_point = (clicked["lat"], clicked["lng"])

    if len(st.session_state.points) < 2 and new_point not in st.session_state.points:
        st.session_state.points.append(new_point)
        st.rerun()

st.divider()

result_col1, result_col2, result_col3 = st.columns([1, 1, 1])

if run_prediction:
    if len(st.session_state.points) != 2:
        st.warning("Please select pickup and drop-off points on the map.")
    else:
        lat1, lon1 = st.session_state.points[0]
        lat2, lon2 = st.session_state.points[1]

        params = {
            "pickup_datetime": str(pickup_datetime),
            "pickup_latitude": lat1,
            "pickup_longitude": lon1,
            "dropoff_latitude": lat2,
            "dropoff_longitude": lon2,
            "passenger_count": passenger_count,
        }

        try:
            response = requests.get(f"{API_URL}/predict", params=params, timeout=30)

            if response.ok:
                data = response.json()
                fare = data.get("fare")

                if fare is not None:
                    with result_col2:
                        st.metric("Estimated fare", f"${fare:.2f}")
                else:
                    st.error("The API response does not contain 'fare'.")
                    st.json(data)
            else:
                st.error(f"API error: {response.status_code}")
                st.text(response.text)

        except requests.RequestException as e:
            st.error(f"Request failed: {e}")