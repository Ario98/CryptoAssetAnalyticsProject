import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn import datasets
import numpy as np
import requests

@st.cache_data
def load_data():
    data = pd.read_csv('data/data_complete.csv')

    # Convert the Date column to datetime
    data['Date'] = pd.to_datetime(data['Date'])

    # Resample data on a weekly basis and forward fill any missing values
    data = data.resample('W', on='Date').mean().ffill()

    # Highlight the date of the update (August 5th, 2021)
    update_date = pd.to_datetime('2021-08-05')

    return data, update_date

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

    def gas_fee_section(self):
        data, update_date = load_data()

        st.header("Graphical Comparison")

        st.subheader("Gas Price")
        st.write("""
        The average gas price (in Gwei) graph illustrates the fluctuation in gas prices over time, 
        providing insights into the cost of Ethereum network transactions. This visual representation helps users analyze trends 
        and make informed decisions based on historical gas price data. 
        The data is resampled on a weekly basis to reduce noise and make the graph more readable.""")
            
        # Select the gas price metric
        selected_metric = st.selectbox("Select Gas Price Metric", ['average_gas_price', 'GasPriceOpen', 'GasPriceClose', 'GasPriceLow', 'GasPriceHigh'])

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
            st.subheader(f"Average Gas Metric Before Update")
            st.markdown(f"<h2>{avg_gas_price_before_update:.2f} Gwei</h2>", unsafe_allow_html=True)
            st.subheader(f"Volatility Before Update")
            st.markdown(f"<h2>{volatility_before_update:.2f}%</h2>", unsafe_allow_html=True)
        with col2:
            st.subheader("Average Gas Metric After Update")
            st.markdown(f"<h2 style='color:{avg_gas_price_color}'>{avg_gas_price_after_update:.2f} Gwei {arrow_symbol}</h2>", unsafe_allow_html=True)
            st.subheader("Volatility After Update")
            st.markdown(f"<h2 style='color:{volatility_color}'>{volatility_after_update:.2f}% {volatility_arrow_symbol}</h2>", unsafe_allow_html=True)

        # Create the graph
        fig = go.Figure()

        # Add a trace for the selected metric
        fig.add_trace(go.Scatter(x=data.index, y=data[selected_metric], mode='lines', name=selected_metric, fill='tozeroy',
                                fillcolor='rgba(173, 216, 230, 0.2)'))  # Choose an RGBA color for the gradient

        # Add a vertical line for the update date
        fig.add_shape(type='line', x0=update_date, x1=update_date, y0=0, y1=data[selected_metric].max(),
                    line=dict(color='orange', dash='dash'), name='Update Date')

        # Configure the layout
        fig.update_layout(title='Gas Price Analysis', xaxis_title='Date', yaxis_title='Gas Price (Gwei)',
                        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

        # Show the graph
        st.plotly_chart(fig)    

    def volume_section(self):
        data, update_date = load_data()
        
        st.subheader("Trading Volume")
        st.write("""
        The Ethereum Trading Volume analysis provides insights into the total number of contracts or shares traded over time. 
        Trading volume is a critical metric for traders and investors as it reflects market activity and liquidity. Higher trading 
        volumes often indicate a more active market, which can result in narrower spreads and better transaction execution. 
        It also provides a sense of the market's strength and intensity, where sudden increases in trading volume could mean a price trend is gaining momentum, 
        while decreases could signify a trend reversal. By examining the trend of Ethereum's trading volume, users can gain a deeper understanding of the market dynamics, 
        which can aid in making more informed trading decisions.
        """)

        # Calculate average trading volume before and after the update
        avg_trading_volume_before_update = data[data.index < update_date]['EthVolume'].mean()
        avg_trading_volume_after_update = data[data.index >= update_date]['EthVolume'].mean()

        # Determine the color for the average trading volume text based on the volume change
        avg_trading_volume_color = "green" if avg_trading_volume_after_update > avg_trading_volume_before_update else "red"

        # Determine the arrow symbol based on the volume change
        arrow_symbol = "↑" if avg_trading_volume_after_update > avg_trading_volume_before_update else "↓"

        # Display average trading volume before and after the update
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Average Trading Volume Before Update")
            st.markdown(f"<h2>{avg_trading_volume_before_update:.2f}</h2>", unsafe_allow_html=True)
        with col2:
            st.subheader("Average Trading Volume After Update")
            st.markdown(f"<h2 style='color:{avg_trading_volume_color}'>{avg_trading_volume_after_update:.2f} {arrow_symbol}</h2>", unsafe_allow_html=True)

        # Create the graph for trading volume
        fig = go.Figure()

        # Add a trace for the trading volume
        fig.add_trace(go.Scatter(x=data.index, y=data['EthVolume'], mode='lines', name='Trading Volume', fill='tozeroy',
                                fillcolor='rgba(173, 216, 230, 0.2)'))  # Choose an RGBA color for the gradient

        # Add a vertical line for the update date
        fig.add_shape(type='line', x0=update_date, x1=update_date, y0=0, y1=data['EthVolume'].max(),
                    line=dict(color='orange', dash='dash'), name='Update Date')

        # Configure the layout
        fig.update_layout(title='Ethereum Trading Volume Analysis', xaxis_title='Date', yaxis_title='Trading Volume',
                        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

        # Show the graph
        st.plotly_chart(fig)

    def tx_user_section(self):
        data, update_date = load_data()

        st.subheader("Transaction and User Analysis")
        st.write("""
        The Transaction and User Analysis section provides insights into the number of transactions and unique users over time. 
        Monitoring these metrics can help in understanding the Ethereum network's activity and growth. The transaction count reflects the number of Ethereum 
        transactions conducted within a specific period, indicating the network's utilization and adoption. The growth of unique users, 
        represented by the total count of unique addresses, signifies the expansion of the Ethereum user base. Analyzing these trends can provide valuable 
        information about the network's popularity, user engagement, and potential market opportunities. By examining transaction volume and unique address growth, 
        users can gain insights into the Ethereum ecosystem's dynamics and make informed decisions.
        """)

        # Calculate average transactions and user growth before and after the update
        avg_transactions_before_update = data[data.index < update_date]['TransactionsAmount'].mean()
        avg_transactions_after_update = data[data.index >= update_date]['TransactionsAmount'].mean()

        unique_addresses_growth_before_update = ((data[data.index < update_date]['UniqueAddressTotalCount'].iloc[-1] - data[data.index < update_date]['UniqueAddressTotalCount'].iloc[0]) / data[data.index < update_date]['UniqueAddressTotalCount'].iloc[0]) * 100
        unique_addresses_growth_after_update = ((data[data.index >= update_date]['UniqueAddressTotalCount'].iloc[-1] - data[data.index >= update_date]['UniqueAddressTotalCount'].iloc[0]) / data[data.index >= update_date]['UniqueAddressTotalCount'].iloc[0]) * 100

        # Determine the color for the metrics text based on the change
        avg_transactions_color = "green" if avg_transactions_after_update > avg_transactions_before_update else "red"
        unique_addresses_growth_color = "green" if unique_addresses_growth_after_update > unique_addresses_growth_before_update else "red"

        # Determine the arrow symbol based on the change
        arrow_symbol_trans = "↑" if avg_transactions_after_update > avg_transactions_before_update else "↓"
        arrow_symbol_addr = "↑" if unique_addresses_growth_after_update > unique_addresses_growth_before_update else "↓"

        # Display average transactions 
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Average Transactions Amount Before Update")
            st.markdown(f"<h2>{avg_transactions_before_update:.2f}</h2>", unsafe_allow_html=True)
        with col2:
            st.subheader("Average Transactions Amount After Update")
            st.markdown(f"<h2 style='color:{avg_transactions_color}'>{avg_transactions_after_update:.2f} {arrow_symbol_trans}</h2>", unsafe_allow_html=True)

        # Create the graph for transactions analysis
        fig1 = go.Figure()

        # Add a trace for the transaction amounts
        fig1.add_trace(go.Scatter(x=data.index, y=data['TransactionsAmount'], mode='lines', name='Transactions Amount', fill='tozeroy',
                                fillcolor='rgba(173, 216, 230, 0.2)'))  # Choose an RGBA color for the gradient

        # Add a vertical line for the update date
        fig1.add_shape(type='line', x0=update_date, x1=update_date, y0=0, y1=data['TransactionsAmount'].max() * 1.5,
                    line=dict(color='orange', dash='dash'), name='Update Date')

        fig1.update_layout(title='Transaction Analysis', xaxis_title='Date', yaxis_title='Transactions Amount',
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

        # Set custom y-axis range for the Transactions Amount graph
        fig1.update_yaxes(range=[0, data['TransactionsAmount'].max() * 1.5])

        # Show the graph
        st.plotly_chart(fig1)

        # Display unique addresses growth
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Unique Addresses Growth Before Update")
            st.markdown(f"<h2>{unique_addresses_growth_before_update:.2f}%</h2>", unsafe_allow_html=True)
        with col2:
            st.subheader("Unique Addresses Growth After Update")
            st.markdown(f"<h2 style='color:{unique_addresses_growth_color}'>{unique_addresses_growth_after_update:.2f}% {arrow_symbol_addr}</h2>", unsafe_allow_html=True)

        # Create the graph for user analysis
        fig2 = go.Figure()

        # Define the color gradients for each line
        colors = ['rgba(173, 216, 230, 0.2)', 'rgba(144, 238, 144, 0.2)', 'rgba(255, 192, 203, 0.2)']

        # Select the lines to display
        selected_lines = st.multiselect("Select User Analysis Lines", ['UniqueAddressTotalCount', 'UniqueAddressReceiveCount', 'UniqueAddressSentCount'],
                                        default=['UniqueAddressTotalCount'])

        # Add the selected traces to the graph
        for line in selected_lines:
            fig2.add_trace(go.Scatter(x=data.index, y=data[line], mode='lines', name=line, fill='tozeroy',
                                    fillcolor=colors[selected_lines.index(line)]))

        # Add a vertical line for the update date
        fig2.add_shape(type='line', x0=update_date, x1=update_date, y0=0, y1=data['UniqueAddressTotalCount'].max(),
                    line=dict(color='orange', dash='dash'), name='Update Date')

        # Configure the layout
        fig2.update_layout(title='User Analysis', xaxis_title='Date', yaxis_title='Unique Addresses Count',
                        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

        # Show the graph
        st.plotly_chart(fig2)


    def eth_burnt_section(self):
        data, update_date = load_data()
        
        st.subheader("Daily ETH Burned Analysis")
        st.write("""
        The Daily ETH Burned analysis provides insights into the amount of Ethereum (ETH) burned on a daily basis. ETH burning refers to the process of permanently removing ETH from circulation, typically through token burning mechanisms, smart contracts, or network fees. ETH burning became more prevalent with the implementation of the London upgrade. Monitoring the daily ETH burned metric can offer valuable information about the overall deflationary supply dynamics of Ethereum and the network's economic activity. By analyzing the average ETH burned, users can gain insights into the network's deflationary mechanisms and the impact on supply and demand dynamics.
        """)

        # Filter data for the "after" period
        data_after_update = data[data.index >= update_date]

        # Calculate average ETH burned
        avg_eth_burned = data_after_update['DailyEthBurnt'].mean()

        # Display average ETH burned
        st.subheader("Average ETH Burned")
        st.markdown(f"<h2>{avg_eth_burned:.2f} ETH</h2>", unsafe_allow_html=True)

        # Create the graph for Daily ETH Burned (after period)
        fig3 = go.Figure()

        # Add a trace for the Daily ETH Burned
        fig3.add_trace(go.Scatter(x=data_after_update.index, y=data_after_update['DailyEthBurnt'], mode='lines', name='Daily ETH Burned', fill='tozeroy',
                                fillcolor='rgba(173, 216, 230, 0.2)'))  # Light blue color for the gradient

        # Configure the layout
        fig3.update_layout(title='Daily ETH Burned Analysis', xaxis_title='Date', yaxis_title='ETH Burned',
                        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

        # Show the graph
        st.plotly_chart(fig3)

    def block_size_section(self):
        data, update_date = load_data()

        st.subheader("Block Size Analysis")
        st.write("""
        The Block Size analysis provides insights into the size of Ethereum blocks. Block size refers to the amount of data that can be included in a single block on the Ethereum blockchain. Monitoring the block size can offer valuable information about the network's capacity, efficiency, and scalability. By analyzing the average block size before and after a specific update, users can gain insights into changes in the network's capacity to process transactions and handle data. Understanding block size trends can be useful for evaluating the performance and scalability of the Ethereum network.
        """)

        # Calculate average block size before and after the update
        avg_block_size_before_update = data[data.index < update_date]['BlockSize'].mean()
        avg_block_size_after_update = data[data.index >= update_date]['BlockSize'].mean()

        # Determine the color for the average block size text based on the change
        avg_block_size_color = "green" if avg_block_size_after_update > avg_block_size_before_update else "red"

        # Determine the arrow symbol based on the change
        arrow_symbol = "↑" if avg_block_size_after_update > avg_block_size_before_update else "↓"

        # Display average block size before and after the update
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Average Block Size Before Update")
            st.markdown(f"<h2>{avg_block_size_before_update:.2f}</h2>", unsafe_allow_html=True)
        with col2:
            st.subheader("Average Block Size After Update")
            st.markdown(f"<h2 style='color:{avg_block_size_color}'>{avg_block_size_after_update:.2f} {arrow_symbol}</h2>", unsafe_allow_html=True)

        # Create the graph for Block Size
        fig4 = go.Figure()

        # Add a vertical line for the update date
        fig4.add_shape(type='line', x0=update_date, x1=update_date, y0=0, y1=data['BlockSize'].max(),
                    line=dict(color='orange', dash='dash'), name='Update Date')

        # Add a trace for the Block Size
        fig4.add_trace(go.Scatter(x=data.index, y=data['BlockSize'], mode='lines', name='Block Size', fill='tozeroy',
                                fillcolor='rgba(173, 216, 230, 0.2)'))  # Purple color for the gradient

        # Configure the layout
        fig4.update_layout(title='Block Size Analysis', xaxis_title='Date', yaxis_title='Block Size',
                        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

        # Show the graph
        st.plotly_chart(fig4)

    def eth_price_section(self):
        data, update_date = load_data()

        st.subheader("Ethereum Price Analysis")
        st.write("""
        The Ethereum Price Analysis section provides insights into the price movement of Ethereum (ETH) over time. Monitoring the price of ETH is crucial for understanding market trends, volatility, and potential investment opportunities. By analyzing the average ETH price and price fluctuations, users can gain insights into the overall performance and market sentiment surrounding Ethereum. This analysis can help inform decisions related to trading, investing, and market entry or exit points.
        """)

        # Select the Ethereum price column to display on the graph
        selected_column = st.selectbox("Select Ethereum Price Metric", ['EthPriceOpenUSD', 'EthPriceHighUSD', 'EthPriceLowUSD', 'EthPriceCloseUSD'])

        # Calculate average ETH price before and after the update
        avg_eth_price_before_update = data[data.index < update_date][selected_column].mean()
        avg_eth_price_after_update = data[data.index >= update_date][selected_column].mean()

        # Determine the color for the average ETH price text based on the price change
        avg_eth_price_color = "green" if avg_eth_price_after_update > avg_eth_price_before_update else "red"

        # Determine the arrow symbol based on the price change
        arrow_symbol = "↑" if avg_eth_price_after_update > avg_eth_price_before_update else "↓"

        # Display average ETH price before and after the update
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Average ETH Price Before Update")
            st.markdown(f"<h2>${avg_eth_price_before_update:.2f}</h2>", unsafe_allow_html=True)
        with col2:
            st.subheader("Average ETH Price After Update")
            st.markdown(f"<h2 style='color:{avg_eth_price_color}'>${avg_eth_price_after_update:.2f} {arrow_symbol}</h2>", unsafe_allow_html=True)

        # Create the graph for Ethereum Price
        fig5 = go.Figure()

        # Add a vertical line for the update date
        fig5.add_shape(type='line', x0=update_date, x1=update_date, y0=0, y1=data[selected_column].max(),
                    line=dict(color='orange', dash='dash'), name='Update Date')

        # Add a trace for the selected Ethereum price column
        fig5.add_trace(go.Scatter(x=data.index, y=data[selected_column], mode='lines', name=selected_column, fill='tonexty',
                                fillcolor='rgba(173, 216, 230, 0.2)'))  # Steel blue color for the gradient

        # Configure the layout
        fig5.update_layout(title='Ethereum Price Analysis', xaxis_title='Date', yaxis_title='ETH Price (USD)',
                        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

        # Show the graph
        st.plotly_chart(fig5)


    def statistical_comparison(self):
        st.header("Statistical Comparison")
        st.markdown("Here, we compare pre-upgrade and post-upgrade data.")

    def hypothesis_one_section(self, title, result):
        st.markdown(f"## {title}")

        # Hypothesis testing
        if result.lower() == 'reject':    # if result is 'reject', we reject the null hypothesis
            st.markdown('<p style="font-size:30px;font-weight:bold;color:red;">Rejected</p>', unsafe_allow_html=True)
        else:   # if result is 'accept', we accept the null hypothesis
            st.markdown('<p style="font-size:30px;font-weight:bold;color:green;">Accepted</p>', unsafe_allow_html=True)

        # Short explanation
        st.markdown(f"""
            ### Metrics used
            Put the metrics here
            """)
        
        # Short explanation
        st.markdown(f"""
            ### Explanation
            A hypothesis is a statement that can be tested. Here, we present the result of such a test. If 'Rejected' is displayed, 
            this means that based on the data and the specific statistical test applied, the evidence suggests the hypothesis 
            does not hold. Conversely, if 'Accepted' is displayed, the available data did not provide sufficient evidence to 
            refute the hypothesis, according to the specific statistical test used.
            """)

    def app_run(self):
        if self.page_selection == "Homepage":
            self.display_homepage()
        elif self.page_selection == "Graphical Comparison":
            self.gas_fee_section()
            self.eth_price_section()
            self.volume_section()
            self.tx_user_section()
            self.eth_burnt_section()
            self.block_size_section()
        elif self.page_selection == "Statistical Comparison":
            self.statistical_comparison()
            self.hypothesis_one_section('Hypothesis: Average Gas Price was lowered with the London Upgrade', 'reject')


if __name__ == "__main__":
    app = EthereumAnalysisApp()
    app.app_run()
