
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

# df = df.query('transaction_catg != "null"')

# df = df.query('transaction_catg != "Sub-Total Withdrawals"')

# df = df.query('transaction_catg != "Sub-Total Deposits"')

# df = df.query('transaction_catg != "Transfers from Depositaries"')
# df = df.query('transaction_catg != "Transfers from Federal Reserve Account (Table V)"')
# df = df.query('transaction_catg != "Transfers to Depositaries"')
# df = df.query('transaction_catg != "Transfers to Federal Reserve Account (Table V)"')
# df = df.query('transaction_catg != "ShTransfersCtohFederalmReserve Account (Table V)"')
# df = df.query('transaction_catg != "Transfers to Depositaries"')

st.write('# Daily Treasury Statement')
st.write('Deposits and Withdrawals of Operating Cash (TGA)')

metric = st.sidebar.selectbox(label='Metrics', options=['transaction_today_amt', 'transaction_mtd_amt', 'transaction_fytd_amt'], index=2)

# columns_to_drop = [
#     'record_calendar_quarter',
#     'record_calendar_month',
#     'record_calendar_day',
#     'record_fiscal_year',
#     'record_fiscal_quarter',
#     'record_calendar_year',
#     'src_line_nbr',
#     'table_nbr',
#     'table_nm'
# ]

# df.drop(columns=columns_to_drop)



# categories = st.sidebar.multiselect(label='transaction_catg', options=df['transaction_catg'].unique())

# categories = ['Federal Retirement Thrift Savings Plan']

# df = df[df['transaction_catg'].isin(categories)]

category = st.sidebar.selectbox(label='transaction_catg', options=df['transaction_catg'].unique())

# df = df[df['transaction_catg'].isin(categories)]

# category = 'Agriculture Loan Repayments (misc)'

df = df[df['transaction_catg'] == category]

tmp = df.pivot_table(index='record_date', columns='transaction_type', values=metric)

if len(tmp.columns) == 1:
    # tmp['Withdrawals'] = 0
    st.write(f'Category {category} does not have both Deposits and Withdrawals')
    st.stop()

tmp.columns.name = None

tmp = tmp.reset_index()

tmp['diff'] = tmp['Deposits'] - tmp['Withdrawals']

tmp['Withdrawals'] = -tmp['Withdrawals']

fig = px.line(tmp, x='record_date', y=['Deposits', 'Withdrawals', 'diff'], title='TGA')

fig.update_traces(selector=dict(name='Deposits'), visible='legendonly')
fig.update_traces(selector=dict(name='Withdrawals'), visible='legendonly')

st.plotly_chart(fig, use_container_width=True)

st.sidebar.button(label='Clear Cache', on_click= lambda: load_dataframe.clear())

st.sidebar.markdown('[source code](https://github.com/dharmatech/tga_explorer.py)')