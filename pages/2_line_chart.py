import datetime
import plotly.express
import plotly.graph_objects
import fed_net_liquidity
import streamlit as st
import plotly

@st.cache_data
def get_dataframe():
    return fed_net_liquidity.load_dataframe()


# df = fed_net_liquidity.load_dataframe()

df = get_dataframe()

fig = plotly.express.line(df, x='date', y=['WALCL', 'RRP', 'TGA', 'REM', 'NL'], title='Fed Net Liquidity')

st.plotly_chart(fig)

st.button('Clear cache', on_click=get_dataframe.clear)