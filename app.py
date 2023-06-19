import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sklearn import datasets
import numpy as np
import requests

@st.cache_data
def load_data():
    data = pd.read_csv('data/data_complete.csv')
    return data

class EthereumAnalysisApp:

    def __init__(self):
        st.title('Ethereum Gas Fees Analysis: Pre and Post London Upgrade')
        st.sidebar.image('https://ethereum.org/static/8ea7775026f258b32e5027fe2408c49f/57723/ethereum-logo-landscape-black.png', use_column_width=True)
        self.page_selection = st.sidebar.selectbox("Choose a page", ["Homepage", "Graphical Comparison", "Statistical Comparison"])

        st.sidebar.markdown("Data by")
        st.sidebar.image("https://etherscan.io/assets/svg/logos/logo-etherscan.svg?v=0.0.5", use_column_width=True)
        st.sidebar.image("https://owlracle.info/img/owl.webp", width=50)

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

    def graphical_comparison(self):
        data = load_data()

        data['Date'] = pd.to_datetime(data['Date'])

        # Resample data on a weekly basis
        data = data.resample('W', on='Date').mean()

        st.header("Graphical Comparison")

        st.subheader("Gas Price")
        st.write("The average gas price (in Gwei) graph illustrates the fluctuation in gas prices over time, providing insights into the cost of Ethereum network transactions. This visual representation helps users analyze trends and make informed decisions based on historical gas price data.")
            
        # Select the gas price metric
        selected_metric = st.selectbox("Select Gas Price Metric", ['average_gas_price', 'GasPriceOpen', 'GasPriceClose', 'GasPriceLow', 'GasPriceHigh'])

        # Highlight the date of the update (August 5th, 2021)
        update_date = pd.to_datetime('2021-08-05')

        # Filter data after the update date
        data_after_update = data[data.index >= update_date]

        # Calculate average gas price before and after the update
        avg_gas_price_before_update = data[data.index < update_date][selected_metric].mean()
        avg_gas_price_after_update = data_after_update[selected_metric].mean()

        # Determine the color for the average gas price text based on the price change
        avg_gas_price_color = "red" if avg_gas_price_after_update > avg_gas_price_before_update else "green"

        # Determine the arrow symbol based on the price change
        arrow_symbol = "↑" if avg_gas_price_after_update > avg_gas_price_before_update else "↓"

        # Calculate Volatility of selected metric before and after the update
        volatility_before_update = data[data.index < update_date][selected_metric].std()
        volatility_after_update = data_after_update[selected_metric].std()

        # Determine the color for the volatility text based on the price change
        volatility_color = "red" if volatility_after_update > volatility_before_update else "green"

        # Determine the arrow symbol for volatility based on the price change
        volatility_arrow_symbol = "↑" if volatility_after_update > volatility_before_update else "↓"

        # Display average gas price before and after the update
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"Average ({selected_metric}) Before Update")
            st.markdown(f"<h2>{avg_gas_price_before_update:.2f} Gwei</h2>", unsafe_allow_html=True)
            st.subheader(f"Volatility Before Update")
            st.markdown(f"<h2>{volatility_before_update:.2f}%</h2>", unsafe_allow_html=True)
        with col2:
            st.subheader("Average Gas Price After Update")
            st.markdown(f"<h2 style='color:{avg_gas_price_color}'>{avg_gas_price_after_update:.2f} Gwei {arrow_symbol}</h2>", unsafe_allow_html=True)
            st.subheader("Volatility After Update")
            st.markdown(f"<h2 style='color:{volatility_color}'>{volatility_after_update:.2f}% {volatility_arrow_symbol}</h2>", unsafe_allow_html=True)

        # Create the graph
        fig = go.Figure()

        # Add a trace for the selected metric
        fig.add_trace(go.Scatter(x=data.index, y=data[selected_metric], mode='lines', name=selected_metric, fill='tozeroy',
                                fillcolor='rgba(0, 100, 80, 0.2)'))  # Choose an RGBA color for the gradient

        # Add a vertical line for the update date
        fig.add_shape(type='line', x0=update_date, x1=update_date, y0=0, y1=data[selected_metric].max(),
                    line=dict(color='orange', dash='dash'), name='Update Date')

        # Configure the layout
        fig.update_layout(title='Gas Price Analysis', xaxis_title='Date', yaxis_title='Gas Price (Gwei)',
                        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

        # Show the graph
        st.plotly_chart(fig)


    def statistical_comparison(self):
        st.header("Statistical Comparison")
        st.markdown("Here, we compare pre-upgrade and post-upgrade data.")

    def app_run(self):
        if self.page_selection == "Homepage":
            self.display_homepage()
        elif self.page_selection == "Graphical Comparison":
            self.graphical_comparison()
        elif self.page_selection == "Statistical Comparison":
            self.statistical_comparison()


if __name__ == "__main__":
    app = EthereumAnalysisApp()
    app.app_run()
