from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
from model import predict_price  

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('predict.html')
    elif request.method == 'POST':
        data = request.form.to_dict()
        data['Year'] = int(data['Year'])
        data['Area'] = float(data['Area'])
        data['Rooms'] = int(data['Property Type'])  # Changed here

        # Проверка года
        if data['Year'] < 2000 or data['Year'] > 2024:
            return render_template('error.html', message="Invalid year. Please enter a year between 2000 and 2024.")

        # Проверка количества комнат
        if data['Rooms'] < 1 or data['Rooms'] > 5:
            return render_template('error.html', message="Invalid number of rooms. Please enter a number between 1 and 5.")

        # Проверка площади
        if data['Area'] < 10 or data['Area'] > 1000:
            return render_template('error.html', message="Invalid area. Please enter an area between 10 and 1000 square meters.")

        new_data = {
            'Property Type': [data['Property Type']],  # Updated here
            'Area': [data['Area']],
            'Region': [data['Region']],
            'Year': [data['Year']],
            'Home Type': [data['Home Type']]
        }
        
        prediction = predict_price(new_data)  
        return render_template('predict.html', prediction_text=f'Predicted Price: {prediction:.0f}₸')


if __name__ == "__main__":
    app.run(debug=True)
