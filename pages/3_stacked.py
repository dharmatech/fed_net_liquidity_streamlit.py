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

fig = plotly.graph_objects.Figure()

fig.add_trace(plotly.graph_objects.Bar(x=df['date'], y=df['REM'] * -1, name='REM'))
fig.add_trace(plotly.graph_objects.Bar(x=df['date'], y=df['WALCL'],    name='NL'))
fig.add_trace(plotly.graph_objects.Bar(x=df['date'], y=df['RRP'] * -1, name='RRP'))
fig.add_trace(plotly.graph_objects.Bar(x=df['date'], y=df['TGA'] * -1, name='TGA'))

fig.update_layout(barmode='stack', title='Fed Net Liquidity')

st.plotly_chart(fig)

st.button('Clear cache', on_click=get_dataframe.clear)