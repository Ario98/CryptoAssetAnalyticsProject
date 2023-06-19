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
gas_data = pd.read_csv('data/data_owlracle.csv')

# Calculate the average gas price as a new colunm from the 4 columns that contain the gas price
gas_data['average_gas_price'] = gas_data[['GasPriceOpen', 'GasPriceClose', 'GasPriceLow', 'GasPriceHigh']].mean(axis=1)

# Load the trading volume data - USD - https://www.kaggle.com/datasets/kapturovalexander/bitcoin-and-ethereum-prices-from-start-to-2023?select=Ethereum+prices.csv
trading_volume = pd.read_csv('data/pricesdata.csv', sep=',')
trading_volume.rename(columns={'Open': 'EthPriceOpenUSD', 'High': 'EthPriceHighUSD', 'Low': 'EthPriceLowUSD', 'Close': 'EthPriceCloseUSD', 'Adj Close': 'EthPriceAdjustedCloseUSD', 'Volume': 'EthVolumeUSD'}, inplace=True)

# Load etherscan data - https://etherscan.io/charts
# Load average transaction data
tx_growth = pd.read_csv('data/export-TxGrowth.csv', sep=',')
tx_growth.drop(columns=['UnixTimeStamp'], inplace=True)
tx_growth.rename(columns={'Value': 'TransactionsAmount'}, inplace=True)

# Load Daily Eth Burnt
eth_burnt = pd.read_csv('data/export-DailyEthBurnt.csv', sep=',')
eth_burnt.rename(columns={'BurntFees': 'DailyEthBurnt'}, inplace=True)

# Load Block Size
block_size = pd.read_csv('data/export-BlockSize.csv', sep=',')
block_size.drop(columns=['UnixTimeStamp'], inplace=True)
block_size.rename(columns={'Value': 'BlockSize'}, inplace=True)

# Load DailyActiveAddress
daily_active_address = pd.read_csv('data/export-DailyActiveEthAddress.csv', sep=',')
daily_active_address.rename(columns={'Unique Address Total Count': 'UniqueAddressTotalCount', 'Unique Address Receive Count': 'UniqueAddressReceiveCount', 'Unique Address Sent Count': 'UniqueAddressSentCount'}, inplace=True)

# Convert the timestamp to a datetime object
gas_data['Timestamp'] = pd.to_datetime(gas_data['Timestamp']).dt.date
trading_volume['Date'] = pd.to_datetime(trading_volume['Date']).dt.date
tx_growth['Date(UTC)'] = pd.to_datetime(tx_growth['Date(UTC)']).dt.date
eth_burnt['Date(UTC)'] = pd.to_datetime(eth_burnt['Date(UTC)']).dt.date
block_size['Date(UTC)'] = pd.to_datetime(block_size['Date(UTC)']).dt.date
daily_active_address['Date(UTC)'] = pd.to_datetime(daily_active_address['Date(UTC)']).dt.date

# Rename the date columns to match
gas_data = gas_data.rename(columns={'Timestamp': 'Date'})
trading_volume = trading_volume.rename(columns={'Date': 'Date'})
tx_growth = tx_growth.rename(columns={'Date(UTC)': 'Date'})
eth_burnt = eth_burnt.rename(columns={'Date(UTC)': 'Date'})
block_size = block_size.rename(columns={'Date(UTC)': 'Date'})
daily_active_address = daily_active_address.rename(columns={'Date(UTC)': 'Date'})

# Merge the data on date
print(f'Number of rows in gas_data: {gas_data.shape[0]}')

merged_df = gas_data.merge(trading_volume, on='Date', how='inner')
print(f'Number of rows after merging gas_data and trading_volume: {merged_df.shape[0]}')

merged_df = merged_df.merge(tx_growth, on='Date', how='inner')
print(f'Number of rows after merging with tx_growth: {merged_df.shape[0]}')

merged_df = merged_df.merge(block_size, on='Date', how='inner')
print(f'Number of rows after merging with block_size: {merged_df.shape[0]}')

merged_df = merged_df.merge(eth_burnt, on='Date', how='left')
print(f'Number of rows after merging with eth_burnt: {merged_df.shape[0]}')

merged_df = merged_df.merge(daily_active_address, on='Date', how='inner')
print(f'Number of rows after merging with daily_active_address: {merged_df.shape[0]}')


# Save data to csv
merged_df.to_csv('data/data_complete.csv', index=False)



