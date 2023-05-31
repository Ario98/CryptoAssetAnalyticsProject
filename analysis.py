import json
import yaml
import requests
from web3 import Web3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
from decimal import Decimal
from infura_con import EthereumConnection

# get the connection to the ethereum node
eth_con = EthereumConnection()  

