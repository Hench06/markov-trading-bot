

def trading_signal(predicted_state):
    if predicted_state == "Increase":
        return "Buy"
    elif predicted_state == "Decrease":
        return "Sell"
    else:
        return "Hold"
    
predicted_states =  ['Increase', 'Increase', 'Increase', 'Increase', 'No Change', 'Decrease']

signals = [trading_signal(state) for state in predicted_states]


