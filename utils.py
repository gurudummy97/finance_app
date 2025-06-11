import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import datetime

def preprocess_data(df):
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # handles bad dates
    df.dropna(subset=['Date'], inplace=True)  # drops rows with invalid dates
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    return df

def forecast_expense(df):
    df = df[df['Type'] == 'Expense']
    monthly = df.groupby('Month')['Amount'].sum().reset_index()
    monthly['Month'] = monthly['Month'].astype(str)
    monthly['Month'] = pd.to_datetime(monthly['Month'])

    monthly['Month_Num'] = range(len(monthly))
    X = monthly[['Month_Num']]
    y = monthly['Amount']

    model = LinearRegression()
    model.fit(X, y)

    future = pd.DataFrame({'Month_Num': range(len(monthly), len(monthly)+6)})
    future['Forecast'] = model.predict(future[['Month_Num']])
    future['Month'] = pd.date_range(start=monthly['Month'].max()+pd.offsets.MonthBegin(1), periods=6, freq='MS')

    return monthly, future

def goal_progress(df, goal=100000):
    savings = df[df['Type'] == 'Income']['Amount'].sum() - df[df['Type'] == 'Expense']['Amount'].sum()
    percent = (savings / goal) * 100
    return savings, percent

def recommend_opportunities(df):
    recs = []
    if df[df['Category'] == 'Mobile Recharge']['Amount'].mean() > 250:
        recs.append("Consider switching to a cheaper mobile plan.")
    if df[df['Category'] == 'Groceries']['Amount'].mean() > 1000:
        recs.append("Look for monthly grocery deals or local markets.")
    return recs
