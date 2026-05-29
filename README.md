# Taxi Fare Prediction

A simple Streamlit web app that predicts a taxi fare from a pickup datetime, a pickup location, a drop-off location, and a passenger count. The interface uses an interactive Folium map centered on New York City by default so users can select two points and estimate the ride fare through a FastAPI backend.

## Project context

This project was built during the **Data Scientist bootcamp at Le Wagon** as part of the coding challenges. It combines data science deployment basics with a lightweight frontend built in Streamlit and a prediction API served separately.

## Features

- Select a pickup date and time
- Choose the number of passengers
- Click two points on a map for pickup and drop-off
- Send the trip information to a prediction API
- Display the estimated fare in the app
- Reset the map or clear selected points easily

## Tech stack

- **Frontend:** Streamlit
- **Map:** Folium + streamlit-folium
- **Backend API:** FastAPI
- **HTTP requests:** Python `requests`
- **Deployment:** Streamlit/Vercel or similar cloud setup

## How it works

1. The user selects a pickup date and time.
2. The user selects the passenger count.
3. The user clicks once on the map for the pickup point.
4. The user clicks a second time for the drop-off point.
5. The app sends these values to the prediction API.
6. The API returns a predicted fare.
7. The app displays the fare in a clean UI.

## Environment variable

The app expects the backend URL in an environment variable named `API_URL`.

Example:

```bash
API_URL=https://your-fastapi.app
```

The prediction request is then sent to:

```text
{API_URL}/predict
```

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/GuerillaUmNeon/taxifare-website.git
cd taxifare-website
pip install -r requirements.txt
```

## Run locally

Start the Streamlit app with:

```bash
make streamlit  
```

If needed, define the environment variable before running:

```bash
export API_URL=https://your-fastapi-app.app
make streamlit  
```

## Example usage

- Pickup datetime: `2026-05-29 12:00`
- Passenger count: `2`
- Pickup point: selected on the map
- Drop-off point: selected on the map
- Output: estimated taxi fare

## Possible improvements

- Add address search and reverse geocoding
- Show route distance and duration
- Improve map styling and markers
- Add input validation and loading states
- Support mobile-friendly layout refinements
- Add unit tests and API health checks

## Learning goals

This project is a practical example of:

- connecting a machine learning API to a simple user interface,
- handling user interactions on a map,
- managing environment variables securely,
- and deploying a small end-to-end data product.

## Author

Built as part of the **Le Wagon Data Scientist bootcamp** challenges.