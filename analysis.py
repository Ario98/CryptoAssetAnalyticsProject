from owlracle import OwlracleConnection
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Create an instance of the OwlracleConnection class
eth_gas = OwlracleConnection()

# Get the average gas price for the provided time period in Unix timestamps
#data_before = eth_gas.get_average_gas_price('eth', 1625090400, 1627768800)
#data_after = eth_gas.get_average_gas_price('eth', 1630447200, 1633039200)
#data_complete = eth_gas.get_average_gas_price('eth', 1619820000, 1640818800, candles=500) # from 2021-05-01 to 2021-12-30

# Save the data to a csv file
#data_complete.to_csv('data/data_complete.csv', index=False)

# In case the API is not responding load the data locally
data_complete = pd.read_csv('data/data_complete.csv', nrows=243)

# Convert the timestamp to a datetime object
data_complete['Timestamp'] = pd.to_datetime(data_complete['Timestamp']).dt.date

# Calculate the average gas price as a new colunm from the 4 columns that contain the gas price
data_complete['average_gas_price'] = data_complete[['GasPriceOpen', 'GasPriceClose', 'GasPriceLow', 'GasPriceHigh']].mean(axis=1)

# Compute trend line (a line in this case)
z = np.polyfit(range(len(data_complete)), data_complete['average_gas_price'], 1)
p = np.poly1d(z)

# Then plot it
plt.figure(figsize=(10,6))
plt.plot(data_complete['Timestamp'], data_complete['average_gas_price'], label='Average Gas Price')
plt.title('Average Gas Price Over Time')
plt.xlabel('Time')
plt.ylabel('Average Gas Price (Gwei))')
plt.legend()
plt.grid()

# Rotate and resize X-axis labels
plt.xticks(rotation=45, fontsize='small')

plt.show()


