import pandas as pd
import numpy as np

# Read the csv file into a pandas DataFrame
df = pd.read_csv('INSERT CSV HERE')

# Define a function to convert a value from K/M/B format to a regular number, and handle empty or non-numeric values
def kmb_to_number(value):
    if value == "":
        return 0
    else:
        try:
            if isinstance(value, str):
                if value.endswith('K'):
                    return float(value[:-1]) * 1000
                elif value.endswith('M'):
                    return float(value[:-1]) * 1000000
                elif value.endswith('B'):
                    return float(value[:-1]) * 1000000000
                else:
                    return float(value)
            elif isinstance(value, (int, float)):
                return value
            else:
                return 0
        except ValueError:
            return 0

# Apply the conversion function to the values in the 'INSERT COLUMN NAME HERE' column
df['INSERT COLUMN NAME HERE'] = df['INSERT COLUMN NAME HERE'].apply(kmb_to_number)

# Replace any NaN values in the DataFrame with 0
df = df.fillna(0)

# Write the updated DataFrame back to the csv file
df.to_csv('NEW_CSV_NAME.csv', index=False)
