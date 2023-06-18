from owlracle import OwlracleConnection
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Create an instance of the OwlracleConnection class
eth_gas = OwlracleConnection()

# Get the average gas price for the provided time period in Unix timestamps
#data_owlracle = eth_gas.get_average_gas_price('eth', 1577833200, 1672354800, candles=1094) 

# Save the data to a csv file
#data_owlracle.to_csv('data/data_owlracle.csv', index=False)

# In case the API is not responding load the data locally
gas_data = pd.read_csv('data/data_owlracle.csv', nrows=243)

# Load the trading volume data - USD - https://www.kaggle.com/datasets/kapturovalexander/bitcoin-and-ethereum-prices-from-start-to-2023?select=Ethereum+prices.csv
trading_volume = pd.read_csv('data/pricesdata.csv', sep=',')
print(trading_volume.head())

# Convert the timestamp to a datetime object
gas_data['Timestamp'] = pd.to_datetime(gas_data['Timestamp']).dt.date
trading_volume['Date'] = pd.to_datetime(trading_volume['Date']).dt.date

# Calculate the average gas price as a new colunm from the 4 columns that contain the gas price
gas_data['average_gas_price'] = gas_data[['GasPriceOpen', 'GasPriceClose', 'GasPriceLow', 'GasPriceHigh']].mean(axis=1)

# Print the data
print(gas_data.head())

# Merge the data on date
data_complete = pd.merge(gas_data, trading_volume, how='left', left_on='Timestamp', right_on='Date')
print(data_complete.head())

