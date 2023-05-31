from owlracle import OwlracleConnection

# Create an instance of the OwlracleConnection class
eth_gas = OwlracleConnection()

# Get the average gas price for the provided time period in Unix timestamps
data = eth_gas.get_average_gas_price('eth', 1609459261, 1640822461)

print(data)


