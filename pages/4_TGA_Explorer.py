
import pandas as pd
import treasury_gov_pandas.datasets.deposits_withdrawals_operating_cash.load
import streamlit as st
import plotly.express as px

@st.cache_data
def load_dataframe():
    return treasury_gov_pandas.datasets.deposits_withdrawals_operating_cash.load.load()

df = load_dataframe()

df['transaction_today_amt'] = pd.to_numeric(df['transaction_today_amt'], errors='coerce')
df['transaction_mtd_amt']   = pd.to_numeric(df['transaction_mtd_amt'],   errors='coerce')
df['transaction_fytd_amt']  = pd.to_numeric(df['transaction_fytd_amt'],  errors='coerce')

df = df.query('transaction_catg != "null"')

df = df.query('transaction_catg != "Sub-Total Withdrawals"')

df = df.query('transaction_catg != "Sub-Total Deposits"')

df = df.query('transaction_catg != "Transfers from Depositaries"')
df = df.query('transaction_catg != "Transfers from Federal Reserve Account (Table V)"')
df = df.query('transaction_catg != "Transfers to Depositaries"')
df = df.query('transaction_catg != "Transfers to Federal Reserve Account (Table V)"')
df = df.query('transaction_catg != "ShTransfersCtohFederalmReserve Account (Table V)"')
df = df.query('transaction_catg != "Transfers to Depositaries"')

st.write('# Daily Treasury Statement')
st.write('Deposits and Withdrawals of Operating Cash (TGA)')

# metric = st.selectbox(label='Metrics', options=['transaction_today_amt', 'transaction_mtd_amt', 'transaction_fytd_amt'], index=2)

metric = st.sidebar.selectbox(label='Metrics', options=['transaction_today_amt', 'transaction_mtd_amt', 'transaction_fytd_amt'], index=2)

if st.sidebar.checkbox('Public debt', value=False) == False:
    df = df.query('not transaction_catg.str.contains("public debt", case=False)', engine='python')

year = st.sidebar.number_input('Year start', min_value=1900, value=2022, step=1)

df.loc[df['transaction_type'] == 'Withdrawals', 'transaction_today_amt'] = -df['transaction_today_amt']
df.loc[df['transaction_type'] == 'Withdrawals', 'transaction_mtd_amt']   = -df['transaction_mtd_amt']
df.loc[df['transaction_type'] == 'Withdrawals', 'transaction_fytd_amt']  = -df['transaction_fytd_amt']

df = df.query(f'record_date >= "{year}-10-01"')

df['abs'] = df[metric].abs()

if metric == 'transaction_today_amt':
    default_min_amount = 1000
elif metric == 'transaction_mtd_amt':
    default_min_amount = 10000    
elif metric == 'transaction_fytd_amt':
    default_min_amount = 100000

min_amount = st.sidebar.number_input('Minimum amount', min_value=0, value=default_min_amount, step=1000)

df = df.query(f'abs > {min_amount}')

st.sidebar.write(f'Total records: {len(df):,}')

if st.sidebar.checkbox('Filter', value=False):

    categories = st.sidebar.multiselect(label='transaction_catg', options=df['transaction_catg'].unique())
    
    df = df[df['transaction_catg'].isin(categories)]

fig = px.bar(
    df, 
    x='record_date', 
    y=metric, 
    color='transaction_catg', 
    title='Stacked Bar Chart', 
    labels={metric:'Transaction Amount', 'record_date':'Record Date', 'transaction_catg':'Transaction Category'},
    barmode='relative')

st.plotly_chart(fig, use_container_width=True)

st.button(label='Clear Cache', on_click= lambda: load_dataframe.clear())