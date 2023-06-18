import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
import requests

@st.cache_data
def load_data():
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    data = pd.DataFrame(X, columns=iris.feature_names)

    gas_price_data = pd.read_csv('data/data_complete.csv')
    return data

class EthereumAnalysisApp:

    def __init__(self):
        st.title('Ethereum Gas Fees Analysis: Pre and Post London Upgrade')
        st.sidebar.image('https://ethereum.org/static/8ea7775026f258b32e5027fe2408c49f/57723/ethereum-logo-landscape-black.png', use_column_width=True)
        self.page_selection = st.sidebar.selectbox("Choose a page", ["Homepage", "Pre Upgrade Data", "Post Upgrade Data", "Comparison"])

    def fetch_eth_price(self):
        url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return data['ethereum']['usd']

    def fetch_gas_price(self):
        url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=MY1ZUXNND2FTM1T14ZVZ9QRT1D95PAVQUI"
        response = requests.get(url)
        data = response.json()
        return data['result']['FastGasPrice']

    def display_homepage(self):
        st.header("Homepage")

        eth_price = self.fetch_eth_price()
        gas_price = self.fetch_gas_price()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Live Ethereum Price (USD):** {eth_price}")

        with col2:
            st.markdown(f"**Live Fast Gas Price (Gwei):** {gas_price}")

        st.markdown("""
        ## Introduction 

        Welcome to the Ethereum Gas Fees Analysis app! This app aims to examine the state of Ethereum's gas fees before and after the London Upgrade. 

        ## Why this Analysis?

        The Ethereum network underwent a major upgrade in August 2021, dubbed the "London Upgrade". One of the significant changes in this upgrade was the introduction of EIP-1559, which aimed to overhaul the transaction fee market. This analysis aims to quantify the impact of the London Upgrade on transaction fees, also known as gas fees.

        ## How to Use This App

        On the left sidebar, you will see several options: 

        - **Homepage**: Provides an overview and instructions for the app (you are here now).

        - **Pre Upgrade Data**: Presents a detailed view of the gas fees before the London upgrade.

        - **Post Upgrade Data**: Presents a detailed view of the gas fees after the London Upgrade.

        - **Comparison**: Compares the pre-upgrade and post-upgrade data, highlighting the impact of the London Upgrade on gas fees.

        Feel free to navigate between these pages to explore the analysis. Each page will offer visualizations and insights about the data.
        """)

    def display_pre_upgrade_data(self):
        st.header("Pre Upgrade Data")
        data = load_data()
        st.write(data)

    def display_post_upgrade_data(self):
        st.header("Post Upgrade Data")
        data = load_data()
        st.write(data)

    def display_comparison(self):
        st.header("Comparison")
        st.markdown("Here, we compare pre-upgrade and post-upgrade data.")

    def app_run(self):
        if self.page_selection == "Homepage":
            self.display_homepage()
        elif self.page_selection == "Pre Upgrade Data":
            self.display_pre_upgrade_data()
        elif self.page_selection == "Post Upgrade Data":
            self.display_post_upgrade_data()
        elif self.page_selection == "Comparison":
            self.display_comparison()


if __name__ == "__main__":
    app = EthereumAnalysisApp()
    app.app_run()
