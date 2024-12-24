import pandas as pd
import numpy as np
from collections import Counter
import os
import json

# Load stock data
data = pd.read_csv("markov-trading-bot\data\cleaned_ARM_stock_data.csv")

# Calculate daily returns
data["Daily Return"] = data["Close"].pct_change()

# Calculate rolling volatility (10-day standard deviation of returns)
data["Volatility"] = data["Daily Return"].rolling(window=10).std()

# Calculate momentum (5-day rolling average of returns)
data["Momentum"] = data["Daily Return"].rolling(window=5).mean()

# Calculate RSI (14-day)
def calculate_rsi(prices, window=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

data["RSI"] = calculate_rsi(data["Close"])

# Define state functions
def price_state(daily_return):
    if daily_return > 0.01:
        return "Increase"
    elif daily_return < -0.01:
        return "Decrease"
    else:
        return "No Change"

def volatility_state(volatility):
    if volatility > 0.02:
        return "High"
    elif volatility < 0.01:
        return "Low"
    else:
        return "Medium"

def momentum_state(momentum):
    if momentum > 0:
        return "Positive"
    elif momentum < 0:
        return "Negative"
    else:
        return "Neutral"

def rsi_state(rsi):
    if rsi > 70:
        return "Overbought"
    elif rsi < 30:
        return "Oversold"
    else:
        return "Neutral"

# Create combined state
data["Price State"] = data["Daily Return"].apply(price_state)
data["Volatility State"] = data["Volatility"].apply(volatility_state)
data["Momentum State"] = data["Momentum"].apply(momentum_state)
data["RSI State"] = data["RSI"].apply(rsi_state)

data["Combined State"] = data.apply(
    lambda row: f"{row['Price State']} | {row['Volatility State']} | {row['Momentum State']} | {row['RSI State']}",
    axis=1,
)

# Build the multidimensional transition matrix
combined_states = data["Combined State"].dropna().values
transition_counts = Counter()

for current, next_state in zip(combined_states[:-1], combined_states[1:]):
    transition_counts[(current, next_state)] += 1

# Normalize to probabilities
state_space = data["Combined State"].unique()
transition_matrix = {state: {} for state in state_space}

for (current, next_state), count in transition_counts.items():
    if current not in transition_matrix:
        transition_matrix[current] = {}
    transition_matrix[current][next_state] = count

# Normalize probabilities
for current, transitions in transition_matrix.items():
    total = sum(transitions.values())
    transition_matrix[current] = {state: count / total for state, count in transitions.items()}

# Ensure the 'data' directory exists
if not os.path.exists("data"):
    os.makedirs("data")

# Save the new transition matrix to a JSON file
new_file_path = "data/multidimensional_transition_matrix_v2.json"
with open(new_file_path, "w") as f:
    json.dump(transition_matrix, f)

print(f"New multidimensional transition matrix saved as '{new_file_path}' successfully!")
