import yaml
import requests

class OwlracleConnection:
    def __init__(self, config_file='config.yaml'):
        self.config = self._load_config(config_file)
        self.api_key = self._load_api_key()

    def _load_config(self, config_file):
        try:
            with open(config_file, 'r') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
            return config
        except FileNotFoundError:
            print("Error: Config file not found")
            return None
    
    def _load_api_key(self):
        api_key = self.config.get("keys", {}).get("owlracle_api")
        if api_key:
            return api_key
        else:
            print("Error: Owlracle API key not found in config")
            return None
        
    def get_average_gas_price(self, network, from_time, to_time, candles=100, timeframe=1440):
        """Returns the average gas price for a given network and time period

        For more in-depth guidelines check - https://owlracle.info/docs

        network: 'eth' or 'bsc'
        from_time: unix timestamp
        to_time: unix timestamp
        candles: number of candles to use for the average
        timeframe: timeframe of the candles in minutes
        
        Returns: json"""
        if self.api_key is None:
            print("Error: Owlracle API key not loaded")
            return None
        
        url = 'https://api.owlracle.info/v4/{}/history?from={}&to={}&candles={}&apikey={}&timeframe={}'.format(network, from_time, to_time, candles, self.api_key, timeframe)
        try:
            res = requests.get(url)
            data = res.json()
            return data
        except:
            print("Error: Connection to the Owlracle API failed")
            return None

    