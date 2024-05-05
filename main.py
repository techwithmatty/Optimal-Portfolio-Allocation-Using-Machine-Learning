import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
import pandas as pd
import yfinance as yf

# Page title
st.set_page_config(page_title="S&P500 - Stock Portfolio Selection System", page_icon=":chart_with_upwards_trend:")

st.markdown("<h1 style='text-align: center; color: grey;'>S&P500 - Stock Portfolio Selection System (powered by ML)</h1>", unsafe_allow_html=True)


# Formatting
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #808080;
    color: white;
    height: 3em;
    width: 12em;
    border-radius:10px;
    border:2px solid #000000;
    font-size:20px;
    margin: auto;
    display: block;
}

div.stButton > button:hover {
    background:linear-gradient(to bottom, #808080 15%, #C8C8C8 100%);
}

div.stButton > button:active {
    position:relative;
    top:3px;
}


</style>""", unsafe_allow_html=True)

st.markdown('<p></p>', unsafe_allow_html = True)
st.markdown('<p></p>', unsafe_allow_html = True)
st.markdown('<p></p>', unsafe_allow_html = True)

# Count which will be used in the rebalancing
if 'count' not in st.session_state:
    st.session_state.count = 0

# Stores dataframe for portfolio
if 'portfolio_df' not in st.session_state:
    st.session_state.portfolio_df = {}

# Stores dataframe for current_holdings
if 'current_holdings' not in st.session_state:
    st.session_state.current_holdings = {}

# Stores list of stocks for final_portfolio in dictionary
if 'final_portfolio' not in st.session_state:
    st.session_state.final_portfolio = {}

# Stores currrent portfolio total 
if 'curr_total_portfolio' not in st.session_state:
    st.session_state.curr_total_portfolio = []

# Stores currrent date format
if 'curr_date_format' not in st.session_state:
    st.session_state.curr_date_format = []

# Stores initial amount entered
if 'initial_amount' not in st.session_state:
    st.session_state.initial_amount = 0

def increment_counter(increment_value=0):
    st.session_state.count += increment_value

# Compute the pct_change of each stock for a given window
def calculate_pct_change(window_number, d):
    
    # Define key for dictionary as "w(x)" where x is the window number
    window_no = "w" + str(window_number)
    
    # Store list of tickers associated with portfolio
    curr_list_of_tickers = st.session_state.final_portfolio[window_no]
    
    # Store list that stores the percentage change in that window for the current portfolio
    curr_portfolio_pct_change = []
    
    # Compute pct change and store it in list
    for ticker in curr_list_of_tickers:
        percent_change = 1 + close_df[ticker].loc[w_start[window_number-1]: w_end[window_number-1]].pct_change(d).dropna().iloc[0]
        curr_portfolio_pct_change.append(percent_change)
    
    return curr_portfolio_pct_change

def round_2dp(x):
    return round(x, 2)

# Current during rebalancing
curr_date = ""

# Holds close price data
close_df = pd.DataFrame()

# Store pct change for portfolios 
portfolio_pct_change = {}

# Store portfolio dataframe
portfolio_df = {}

# Define dates for windows (element 0 is window 1, element 1 is window 2, etc..) for the trading year
w_start = ["2021-1-4", "2021-2-3", "2021-3-5", "2021-4-6", "2021-5-5", "2021-6-4", "2021-7-6", "2021-8-4", "2021-9-2", "2021-10-4", "2021-11-2", "2021-12-2"]
w_end = ["2021-2-3", "2021-3-5", "2021-4-6", "2021-5-5", "2021-6-4", "2021-7-6", "2021-8-4", "2021-9-2", "2021-10-4", "2021-11-2", "2021-12-2", "2021-12-31"]

# Define dates in appropriate format
st.session_state.curr_date_format = ["4/1/2021", "3/2/2021", "5/3/2021", "6/4/2021", "5/5/2021", "4/6/2021", "6/7/2021", "4/8/2021", "2/9/2021", "4/10/2021", "2/11/2021", "2/12/2021", "31/12/2021"]

# Final stocks decided by process (process of working these out not included because it is computationally intensive but can be found in the 'Stock Portfolio Construction using Machine Learning - FULL VERSION.ipynb' jupyter notebook)
st.session_state.final_portfolio = {'w1': ['CTAS', 'DIS', 'HES', 'PG', 'FIS', 'ROST', 'ADP'],
 'w2': ['WAT', 'SYY', 'EXPE', 'UNH', 'NEE', 'COST', 'TXN'],
 'w3': ['CTAS', 'XRAY', 'OXY', 'UNH', 'NEE', 'ROST', 'TXN'],
 'w4': ['PAYX', 'VFC', 'EXPE', 'UNH', 'NEE', 'TJX', 'INTU'],
 'w5': ['SYK', 'UPS', 'OXY', 'UNH', 'NEE', 'TJX', 'INTU'],
 'w6': ['ADI', 'TAP', 'SLB', 'UNH', 'FIS', 'WMT', 'ADBE'],
 'w7': ['NKE', 'VFC', 'OXY', 'UNH', 'FIS', 'TJX', 'ORLY'],
 'w8': ['AMGN', 'MAR', 'CCL', 'PFE', 'FIS', 'TJX', 'AMZN'],
 'w9': ['DHR', 'HRL', 'CCL', 'UNH', 'FIS', 'ROST', 'MSFT'],
 'w10': ['SYK', 'SYY', 'OXY', 'UNH', 'MRK', 'TJX', 'ADBE'],
 'w11': ['CTAS', 'ECL', 'OXY', 'UNH', 'FISV', 'DRI', 'MSFT'],
 'w12': ['CTAS', 'BLL', 'HES', 'UNH', 'WM', 'TJX', 'INTU']}

 # MVO optimal weights generated (process of working these out not included because it is computationally intensive but can be found in the 'Stock Portfolio Construction using Machine Learning - FULL VERSION.ipynb' jupyter notebook)
MVO_optimal_weights = {'w1': np.array([0.2    , 0.16102, 0.     , 0.2    , 0.03898, 0.2    , 0.2    ]),
 'w2': np.array([0.16531, 0.01861, 0.04809, 0.2    , 0.2    , 0.2    , 0.16799]),
 'w3': np.array([0.2, 0. , 0. , 0.2, 0.2, 0.2, 0.2]),
 'w4': np.array([0.12739, 0.02621, 0.0464 , 0.2    , 0.2    , 0.2    , 0.2    ]),
 'w5': np.array([0.06898, 0.13102, 0.     , 0.2    , 0.2    , 0.2    , 0.2    ]),
 'w6': np.array([0.2, 0. , 0. , 0.2, 0.2, 0.2, 0.2]),
 'w7': np.array([0.2   , 0.0261, 0.    , 0.2   , 0.1739, 0.2   , 0.2   ]),
 'w8': np.array([0.2    , 0.12377, 0.     , 0.2    , 0.07623, 0.2    , 0.2    ]),
 'w9': np.array([0.2, 0.2, 0. , 0.2, 0. , 0.2, 0.2]),
 'w10': np.array([0.2    , 0.02608, 0.     , 0.2    , 0.17392, 0.2    , 0.2    ]),
 'w11': np.array([0.2    , 0.19465, 0.     , 0.2    , 0.2    , 0.00535, 0.2    ]),
 'w12': np.array([0.2    , 0.12745, 0.     , 0.2    , 0.16382, 0.10872, 0.2    ])}

# Generate equal weights
equal_weights = {}
# Loop through each window
for i in range(1, 13):
    # Define key for dictionary as "w(x)" where x is the window number
    window_no = "w" + str(i)
    # Store equal weights
    equal_weights[window_no] = [1/7] * 7

# Final tickers 
tickers_list = ['CTAS','DIS','HES','PG','FIS','ROST','ADP','WAT','SYY','EXPE','UNH','NEE','COST','TXN','XRAY','OXY','PAYX','VFC','TJX','INTU','SYK','UPS','ADI','TAP','SLB','WMT','ADBE','NKE','ORLY','AMGN','MAR','CCL','PFE','AMZN','DHR','HRL','MSFT','MRK','ECL','FISV','DRI','BLL','WM']

# Store the holding of each stock for each window (first element (0) is window 1) and each strategy
MVO_holdings = {}
equal_weight_holdings = {}

st.markdown("<h3 style='text-align: left; color: grey;'>Portfolio Summary</h3>", unsafe_allow_html=True)

# Define placeholders and buttons 
plc_holder_curr_date = st.empty()
plc_holder_port = st.empty()
plc_holder_pl = st.empty()

plc_holder_curr_date.text("Date: ")
plc_holder_port.text("Current Portfolio Value (in $): ")
plc_holder_pl.text("Profit/Loss: ")

st.markdown("<h3 style='text-align: left; color: grey;'>Current Holdings</h3>", unsafe_allow_html=True)

plc_holder_df = st.empty()
st.write("")

btn_rebalance = st.button('Rebalance Portfolio', on_click=increment_counter, kwargs=dict(increment_value=1))

st.markdown("<h3 style='text-align: center; color: grey;'>Portfolio Allocation</h3>", unsafe_allow_html=True)


# side-menu which contains components for user input

with st.sidebar:
    for i in range(0, 11):
        st.write("")
    st.header("Menu")
    alloc_strat = st.selectbox("Select Allocation Strategy: ", ("MVO", "Equal Weight"))
    amount_invested = st.number_input("Enter Amount in $ (min 100):")
    btn_gen_port = st.button('Generate Portfolio')

# If generate portfolio button clicked
if btn_gen_port:
    # Output error if amount entered is too low
    if (amount_invested < 100):
        st.error("FAILED TRANSACTION: You must invest at least 100 dollars")
    else:
        # Assign amount invested to global variable
        st.session_state.initial_amount = amount_invested

        # Display initial date of investment 
        plc_holder_curr_date.text("Date: " + st.session_state.curr_date_format[0])

        # Clear potfolio df
        st.session_state.portfolio_df = {}

        # Download stock data
        for ticker in tickers_list:
            close_df[ticker] = yf.download(ticker, start=w_start[0], end="2022-1-3")['Close']

        # Specify number of days to calculate returns for
        no_of_days = 21

        # Loop through each window
        for i in range(1, 13):
            # Define key for dictionary as "w(x)" where x is the window number
            window_no = "w" + str(i)

            # 12 month has 20 trading days
            if (i == 11):
                no_of_days = 20

            # Generate and store pct_change of each stock in the portfolio
            portfolio_pct_change[window_no] = calculate_pct_change(i, no_of_days)

        if (alloc_strat == "MVO"):
            curr_total_MVO_portfolio = [amount_invested]

            # Simulate MVO portfolio returns
            # Loop through each window
            for i in range(1, 13):
                # Define key for dictionary as "w(x)" where x is the window number
                window_no = "w" + str(i)
                # Calculate current holdings and store it in dictionary
                MVO_holdings[window_no] = curr_total_MVO_portfolio[i-1] * MVO_optimal_weights[window_no]
                # Calculate total value of portoflio after simulation
                curr_total_MVO_portfolio.append(np.sum(MVO_holdings[window_no] * portfolio_pct_change[window_no]))

            st.session_state.curr_total_portfolio = curr_total_MVO_portfolio

            # Create portfolio df
            for i in range(1, 13):
                curr_window_df = pd.DataFrame()
                # Define key for dictionary as "w(x)" where x is the window number
                window_no = "w" + str(i)
                for i in (1, 8):
                    curr_window_df['Ticker'] = st.session_state.final_portfolio[window_no]
                    curr_holdings = list(map(round_2dp, MVO_holdings[window_no]))
                    curr_window_df['Position Amount (in $)'] = curr_holdings

                # Once portfolio holding is stored assign to dict and reindex
                st.session_state.portfolio_df[window_no] = curr_window_df
                st.session_state.portfolio_df[window_no].index += 1
            
            # Store current holdings
            st.session_state.current_holdings = MVO_holdings

            # Display current portfolio value
            plc_holder_port.text("Current Portfolio Value (in $): " + str(st.session_state.curr_total_portfolio[0]))

        elif (alloc_strat == "Equal Weight"):
            curr_total_equal_weight_portfolio = [amount_invested]

            # Simulate Equal Weight portfolio returns
            # Loop through each window
            for i in range(1, 13):
                # Define key for dictionary as "w(x)" where x is the window number
                window_no = "w" + str(i)
                # Calculate current holdings and store it in dictionary
                equal_weight_holdings[window_no] = curr_total_equal_weight_portfolio[i-1] * np.array(equal_weights[window_no])
                # Calculate total value of portoflio after simulation
                curr_total_equal_weight_portfolio.append(np.sum(equal_weight_holdings[window_no] * portfolio_pct_change[window_no]))

            st.session_state.curr_total_portfolio = curr_total_equal_weight_portfolio

            # Create portfolio df
            for i in range(1, 13):
                curr_window_df = pd.DataFrame()
                # Define key for dictionary as "w(x)" where x is the window number
                window_no = "w" + str(i)
                for i in (1, 8):
                    curr_window_df['Ticker'] = st.session_state.final_portfolio[window_no]
                    curr_holdings = list(map(round_2dp, equal_weight_holdings[window_no]))
                    curr_window_df['Position Amount (in $)'] = curr_holdings

                # Once portfolio holding is stored assign to dict and reindex
                st.session_state.portfolio_df[window_no] = curr_window_df
                st.session_state.portfolio_df[window_no].index += 1

            # Store current holdings
            st.session_state.current_holdings = equal_weight_holdings

            # Display current portfolio value
            plc_holder_port.text("Current Portfolio Value (in $): " + str(st.session_state.curr_total_portfolio[0]))
        
        # Initialise profit loss with N/A
        plc_holder_pl.text("Profit/Loss: N/A")

        # Display dataframe
        st.session_state.portfolio_df['w1']['Position Amount (in $)'] = st.session_state.portfolio_df['w1']['Position Amount (in $)'].apply("{:.02f}".format)
        plc_holder_df.dataframe(st.session_state.portfolio_df['w1'])

        pie_chart = px.pie(st.session_state.portfolio_df['w1'], values=st.session_state.current_holdings['w1'], names=st.session_state.final_portfolio['w1'])

        st.plotly_chart(pie_chart)

curr_month = st.session_state.count

# If rebalancing portfolio button clicked
if (btn_rebalance):

    # End the simulation if at end of rebalancing cycle
    if (st.session_state.count == 13):
        st.session_state.count = 12
        curr_month = 12
        st.markdown("<h3 style='text-align: center; color: grey;'> END OF SIMULATION: ALL STOCKS HAVE BEEN SOLD!</h3>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'> (Clear the cache using the settings on the top right of the screen) </h3>", unsafe_allow_html=True)

    # Define key for dictionary as "w(x)" where x is the window number
    window_no = "w" + str(curr_month+1)
   
    # Place holder 
    if st.session_state.count != 12:
        st.session_state.portfolio_df[window_no]['Position Amount (in $)'] = st.session_state.portfolio_df[window_no]['Position Amount (in $)'].apply("{:.02f}".format)
        plc_holder_df.dataframe(st.session_state.portfolio_df[window_no])

        new_pie_chart = px.pie(st.session_state.portfolio_df[window_no], values=st.session_state.current_holdings[window_no], names=st.session_state.final_portfolio[window_no])
        st.plotly_chart(new_pie_chart)

    plc_holder_curr_date.text("Date: " + str(st.session_state.curr_date_format[curr_month]))
    plc_holder_port.text("Current Portfolio Value (in $): " + "{:.2f}".format(st.session_state.curr_total_portfolio[curr_month]))
    plc_holder_pl.text("Profit/Loss: " + "{:.2f}".format(st.session_state.curr_total_portfolio[curr_month] - st.session_state.initial_amount))

    st.markdown("<h3 style='text-align: center; color: grey;'>Portfolio History</h3>", unsafe_allow_html=True)

    curr_df = pd.DataFrame(dict(x = st.session_state.curr_date_format[0:12], y = st.session_state.curr_total_portfolio[0:12]))
    fig = px.line(curr_df, x=curr_df['x'].loc[0:curr_month], y=curr_df['y'].loc[0:curr_month], labels={'x': 'Date', 'y':'Total Portfolio Value'})

    st.write(fig)


