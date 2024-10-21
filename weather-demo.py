#weather-demo.py


import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Define the coordinates for Lafayette, CA
lat = 37.8933
lon = -122.1239

# Load your climate data (you would replace this with your actual data source)
# For this demo, I'm simulating some data. You'd typically load real historical weather data.
def load_weather_data():
    # Simulated data for demonstration purposes (create your actual data retrieval logic here)
    np.random.seed(0)  # For reproducibility
    dates = pd.date_range(start='2010-01-01', end='2023-01-01', freq='M')
    temperatures = 20 + 10 * np.sin(np.linspace(0, 3 * np.pi, len(dates))) + np.random.normal(0, 1, len(dates))
    return pd.DataFrame({'Date': dates, 'Temperature': temperatures})

# Load the data
weather_data = load_weather_data()

# CLIMATE ANALYSIS
st.title("Climate Analysis and Predictive Modeling for Lafayette, CA")
st.subheader("Historical Temperature Data")

# Plot the historical temperatures
st.line_chart(weather_data.set_index('Date')['Temperature'])

# PREDICTIVE MODELING
st.subheader("Predictive Modeling of Future Temperature")

# Preparing the data for modeling
weather_data['Month'] = weather_data['Date'].dt.month
X = weather_data[['Month']]
y = weather_data['Temperature']

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fitting a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predicting temperature
y_pred = model.predict(X_test)

# Display predicted vs actual temperatures
st.write("Predicted vs Actual Temperatures:")
results = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
st.line_chart(results)

# Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
st.write(f"Mean Squared Error: {mse:.2f}")

# Predict future temperature (example: for all months in the following year)
future_months = np.array([[i] for i in range(1, 13)])
future_temps = model.predict(future_months)
future_temps_df = pd.DataFrame({'Month': range(1, 13), 'Predicted Temperature': future_temps})

st.subheader("Predicted Future Temperatures for Lafayette, CA")
st.table(future_temps_df)