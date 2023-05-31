import yaml
from web3 import Web3

class EthereumConnection:
    def __init__(self, config_file='config.yaml'):
        self.config = self._load_config(config_file)
        self.connection = self._connect_to_ethereum_node()

    def _load_config(self, config_file):
        try:
            with open(config_file, 'r') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
            return config
        except FileNotFoundError:
            print("Error: Config file not found")
            return None

    def _connect_to_ethereum_node(self):
        if self.config is None:
            print("Error: Config file not loaded")
            return None

        infura_api = self.config.get("keys", {}).get("infura_api")
        if infura_api:
            url_eth_mainnet = "https://mainnet.infura.io/v3/"
            try:
                con = Web3(Web3.HTTPProvider(url_eth_mainnet + infura_api))
                print("Successfully connected to the Ethereum node")
                return con
            except:
                print("Error: Connection to the Ethereum node failed")
                return None
        else:
            print("Error: Infura API key not found in config")
            return None

    def get_connection(self):
        return self.connection
