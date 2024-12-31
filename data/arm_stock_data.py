import yfinance as yf

# Define the stock ticker and date range
stock_ticker = "ARM"  # ARM Holdings ticker
start_date = "2022-01-01"  # Adjust the start date as needed
end_date = "2024-12-30"  # Adjust the end date as needed

# Fetch historical stock data
try:
    data = yf.download(stock_ticker, start=start_date, end=end_date)
    print("Data fetched successfully!")
    
    # Preview the first few rows
    print(data.head())
    
    # Save data to CSV for future use
    data.to_csv(f"{stock_ticker}_stock_data.csv")
    print(f"Data saved to {stock_ticker}_stock_data.csv")
except Exception as e:
    print(f"An error occurred: {e}")


