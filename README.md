# Crypto Asset Analytics Project - SS23

This project focuses on analyzing the impact of the Ethereum London Upgrade on Ethereum fees and trading activity. We use data provided by the Owlracle API to examine and interpret changes in gas prices and trading volume that have occurred as a result of the upgrade.

### Project Overview
The London Upgrade was a significant event in the Ethereum network that included Ethereum Improvement Proposals (EIPs), notably EIP-1559, which introduced a mechanism to burn a part of every transaction fee, thereby decreasing the supply of Ether and potentially leading to significant economic implications.

This project's main goal is to scrutinize the aftermath of this upgrade, interpreting how these changes have affected the average transaction fees on the network and the overall trading activity.

### Installation
Before you get started, you'll need to install a few packages. Here's how to do it:
```
pip install requests pandas pyyaml
```

### Usage
1 - Set your API key in `config.example.yaml` and rename the file to `config.yaml`:
```
api_key: "your_api_key_here"
```

2 - Run the `analysis.py`.

### Owlracle API
We're currently using the Owlracle API to fetch data about gas prices. The API provides detailed data about Ethereum gas prices, including opening, closing, lowest, and highest prices over specified periods, as well as the average gas price and the number of samples taken.
