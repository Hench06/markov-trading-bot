import pandas as pd

# Update the path to the file's location
file_path = "data/ARM_stock_data.csv"  # Adjust if needed


    # Load the CSV file
data = pd.read_csv(file_path)
print(data.head())
