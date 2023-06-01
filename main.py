# -*- coding: utf-8 -*-
"""
Created on Wed May 31 21:46:13 2023

@author: dedov
"""

from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from joblib import dump, load
from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

app = FastAPI()

data = load_wine()
X = data.data
y = data.target

scaler = StandardScaler()
X = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


linear_model = LogisticRegression()
linear_model.fit(X_train, y_train)

rf_model = RandomForestClassifier()
rf_model.fit(X_train, y_train)


@app.post("/")
def root():
    return {"message": "Hello World"}

class WineData(BaseModel):
    alcohol: float
    malic_acid: float
    ash: float
    alcalinity_of_ash: float
    magnesium: float
    total_phenols: float
    flavanoids: float
    nonflavanoid_phenols: float
    proanthocyanins: float
    color_intensity: float
    hue: float
    od280_od315_of_diluted_wines: float
    proline: float
    
    
@app.post('/predict')
async def predict(data: WineData):
    try:
        # Preprocess the input data
        input_data = [[
            data.alcohol, data.malic_acid, data.ash, data.alcalinity_of_ash, data.magnesium,
            data.total_phenols, data.flavanoids, data.nonflavanoid_phenols, data.proanthocyanins,
            data.color_intensity, data.hue, data.od280_od315_of_diluted_wines, data.proline
        ]]
        input_data = scaler.transform(input_data)
        
        # Make predictions using Linear Regression
        linear_prediction = linear_model.predict(input_data)
        
        # Make predictions using Random Forest Classifier
        rf_prediction = rf_model.predict(input_data)
        
        return {
            'linear_regression_prediction': int(linear_prediction[0]),
            'random_forest_prediction': int(rf_prediction[0])
        }
    except Exception as e:
        error_message = f'Error: {str(e)}. Please check for the correct format of input data.'
        return {'error': error_message}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
    

