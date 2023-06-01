# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 14:51:06 2023

@author: dedov
"""

import requests

# Define the input data for prediction
input_data = {
    "alcohol": 13.75,
    "malic_acid": 1.73,
    "ash": 2.41,
    "alcalinity_of_ash": 16.0,
    "magnesium": 89.0,
    "total_phenols": 2.6,
    "flavanoids": 2.76,
    "nonflavanoid_phenols": 0.29,
    "proanthocyanins": 1.81,
    "color_intensity": 5.6,
    "hue": 1.15,
    "od280_od315_of_diluted_wines": 2.9,
    "proline": 1320.0
}

# Send POST request to the prediction endpoint
response = requests.post("http://localhost:5000/predict", json=input_data)

# Check the response
if response.status_code == 200:
    predictions = response.json()
    print("Linear Regression Prediction:", predictions["linear_regression_prediction"])
    print("Random Forest Prediction:", predictions["random_forest_prediction"])
else:
    print("Error:", response.text)