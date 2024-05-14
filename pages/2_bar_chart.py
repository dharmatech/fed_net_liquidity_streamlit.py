import datetime
import plotly.express
import plotly.graph_objects
import fed_net_liquidity
import streamlit as st
import plotly

@st.cache_data
def get_dataframe():
    return fed_net_liquidity.load_dataframe()

df = get_dataframe()

fig = plotly.express.bar(df, x='date', y=['WALCL', 'NL', 'RRP', 'TGA', 'REM'], title='Fed Net Liquidity', barmode='overlay')

st.plotly_chart(fig)

st.button('Clear cache', on_click=get_dataframe.clear)

