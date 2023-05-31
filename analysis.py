from owlracle import OwlracleConnection
import requests

"""network = 'eth'; # could be any supported network
key = 'c8d65f83319b4b04837d2b1cdca73e64'; # fill your api key here
res = requests.get('https://api.owlracle.info/v4/{}/history?from=1609459261&to=1640822461&candles=100&apikey={}'.format(network, key))
data = res.json()
print(data)"""

conn = OwlracleConnection()
data = conn.get_average_gas_price('eth', 1609459261, 1640822461)
print(data)

