import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import joblib

def train_and_save_model():
    df = pd.read_csv('cleaned_krysha.csv')
    df = df.drop(columns=['Complex Name'])
    
    df['Area'] = df['Area'].str.replace(' м²', '').astype(float)

    df['Rooms'] = df['Property Type'].str.extract(r'(\d+)').astype(int)

    df.drop(columns=['Property Type'], inplace=True)

    df = pd.get_dummies(df, columns=['Region', 'Home Type'], drop_first=True)

    X = df.drop(columns=['Price'])
    y = df['Price']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = RandomForestRegressor(n_estimators=100, random_state=42)

    model.fit(X_scaled, y)

    joblib.dump(model, 'model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(X.columns, 'columns.pkl')

def predict_price(new_data):
    model = joblib.load('model.pkl')
    scaler = joblib.load('scaler.pkl')
    columns = joblib.load('columns.pkl')

    new_df = pd.DataFrame(new_data)

    new_df['Rooms'] = new_df['Property Type'].str.extract(r'(\d+)').astype(int)
    new_df.drop(columns=['Property Type'], inplace=True)
    new_df = pd.get_dummies(new_df, columns=['Region', 'Home Type'], drop_first=False)

    for col in columns:
        if col not in new_df.columns:
            new_df[col] = 0

    new_df = new_df[columns]

    new_df_scaled = scaler.transform(new_df)

    new_pred = model.predict(new_df_scaled)
    return new_pred[0]


