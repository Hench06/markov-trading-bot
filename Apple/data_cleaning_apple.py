import yfinance as yf
import pandas as pd
import numpy as np
import json
import os

# Step 1: Download stock data for Apple
ticker = "AAPL"
start_date = "2018-01-01"
end_date = "2023-12-31"

# Fetch historical data
data = yf.download(ticker, start=start_date, end=end_date)

# Save raw data as CSV
os.makedirs("data", exist_ok=True)  # Create 'data' directory if it doesn't exist
raw_data_path = "data/AAPL_stock_data.csv"
data.to_csv(raw_data_path)
print(f"Raw data saved to {raw_data_path}")

# Step 2: Process data
def calculate_indicators(df):
    df['Daily Return'] = df['Adj Close'].pct_change()
    df['Momentum'] = df['Adj Close'] - df['Adj Close'].shift(5)
    df['Volatility'] = df['Daily Return'].rolling(window=10).std()
    df['RSI'] = 100 - (100 / (1 + df['Daily Return'].rolling(window=14).mean() / 
                                    abs(df['Daily Return'].rolling(window=14).mean())))
    df.dropna(inplace=True)  # Remove rows with NaN values
    return df

processed_data = calculate_indicators(data)

# Save cleaned data
cleaned_data_path = "data/cleaned_AAPL_stock_data.csv"
processed_data.to_csv(cleaned_data_path)
print(f"Processed data saved to {cleaned_data_path}")

# Step 3: Define states and create the transition matrix
def define_state(row):
    if row['Daily Return'] > 0.01:
        return "High Gain"
    elif row['Daily Return'] < -0.01:
        return "High Loss"
    elif row['Volatility'] > 0.02:
        return "High Volatility"
    elif row['RSI'] > 70:
        return "Overbought"
    elif row['RSI'] < 30:
        return "Oversold"
    else:
        return "Stable"

processed_data['State'] = processed_data.apply(define_state, axis=1)

def build_transition_matrix(df):
    states = df['State'].unique()
    transition_matrix = {state: {next_state: 0 for next_state in states} for state in states}
    
    for i in range(len(df) - 1):
        current_state = df.iloc[i]['State']
        next_state = df.iloc[i + 1]['State']
        transition_matrix[current_state][next_state] += 1

    # Normalize probabilities
    for state, transitions in transition_matrix.items():
        total = sum(transitions.values())
        if total > 0:
            for next_state in transitions:
                transitions[next_state] /= total
    
    return transition_matrix

transition_matrix = build_transition_matrix(processed_data)

# Step 4: Save transition matrix as JSON
transition_matrix_path = "data/multidimensional_transition_matrix_AAPL.json"
with open(transition_matrix_path, "w") as f:
    json.dump(transition_matrix, f, indent=4)
print(f"Transition matrix saved to {transition_matrix_path}")
