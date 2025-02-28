
import pandas as pd
import treasury_gov_pandas.datasets.deposits_withdrawals_operating_cash.load
import streamlit as st
import plotly.express as px

@st.cache_data
def load_dataframe():
    return treasury_gov_pandas.datasets.deposits_withdrawals_operating_cash.load.load()

df = load_dataframe()

# ----------------------------------------------------------------------
df['record_date'] = pd.to_datetime(df['record_date'])

df['transaction_today_amt'] = pd.to_numeric(df['transaction_today_amt'], errors='coerce')
df['transaction_mtd_amt']   = pd.to_numeric(df['transaction_mtd_amt'],   errors='coerce')
df['transaction_fytd_amt']  = pd.to_numeric(df['transaction_fytd_amt'],  errors='coerce')
# ----------------------------------------------------------------------

# drop_columns = [
#     # 'transaction_catg_desc',
#     # 'account_type',
#     'record_calendar_quarter',
#     'record_calendar_year', 'record_calendar_month', 'record_calendar_day', 'src_line_nbr', 'record_fiscal_year', 'record_fiscal_quarter',
#     'table_nbr', 'table_nm']

# tmp = df.copy(deep=True)

# tmp = tmp[tmp['record_date'] == '2025-02-26']

# tmp = tmp[tmp['transaction_type'] == 'Withdrawals']

# tmp.sort_values('transaction_fytd_amt').drop(columns=drop_columns).drop(columns=['account_type'])

# tmp.drop(columns=drop_columns)
# ----------------------------------------------------------------------
# df = df.query('transaction_catg != "null"')

df = df.query('transaction_catg != "Sub-Total Withdrawals"')

df = df.query('transaction_catg != "Sub-Total Deposits"')

df = df.query('transaction_catg != "Transfers from Depositaries"')
df = df.query('transaction_catg != "Transfers from Federal Reserve Account (Table V)"')
df = df.query('transaction_catg != "Transfers to Depositaries"')
df = df.query('transaction_catg != "Transfers to Federal Reserve Account (Table V)"')
df = df.query('transaction_catg != "ShTransfersCtohFederalmReserve Account (Table V)"')
df = df.query('transaction_catg != "Transfers to Depositaries"')
# ----------------------------------------------------------------------
st.write('# Daily Treasury Statement')
st.write('Deposits and Withdrawals of Operating Cash (TGA)')
st.write('Year Comparison')

st.sidebar.write(f'Total records: {len(df):,}')

tmp = df[~df['transaction_catg'].str.startswith('Change in Balance of Uncollected Funds')]

categories = tmp['transaction_catg'].unique()

st.sidebar.write(f'Total categories: {len(categories)}')

selected_category = st.sidebar.selectbox(label='transaction_catg', options=categories)

df = df.query(f'transaction_catg == "{selected_category}"')

st.sidebar.write(f'Filtered records: {len(df):,}')

# tmp = df.query(f'transaction_catg == "Federal Deposit Insurance Corp (FDIC)"')

# tmp.drop(columns=[
#     'transaction_catg_desc',
#     'account_type',
#     'record_calendar_quarter',
#     'record_calendar_year', 'record_calendar_month', 'record_calendar_day', 'src_line_nbr', 'record_fiscal_year', 'record_fiscal_quarter',
#     'table_nbr', 'table_nm']).tail(30)

df_deposits    = df.query('transaction_type == "Deposits"')
df_withdrawals = df.query('transaction_type == "Withdrawals"')

st.sidebar.write(f'Deposits: {len(df_deposits):,}')
st.sidebar.write(f'Withdrawals: {len(df_withdrawals):,}')

larger_transaction_type = 'Deposits' if len(df_deposits) > len(df_withdrawals) else 'Withdrawals'

selected_transaction_type = st.sidebar.radio(label='transaction_type', options=['Deposits', 'Withdrawals'], index=['Deposits', 'Withdrawals'].index(larger_transaction_type))

df = df.query(f'transaction_type == "{selected_transaction_type}"')

df['transaction_fytd_amt'] = df['transaction_fytd_amt'] * 1_000_000
df['transaction_mtd_amt']  = df['transaction_mtd_amt']  * 1_000_000

# if st.sidebar.checkbox('Public debt', value=False) == False:
#     df = df.query('not transaction_catg.str.contains("public debt", case=False)', engine='python')

amount_type = st.sidebar.selectbox('amount_type', ['transaction_mtd_amt', 'transaction_fytd_amt'])

tmp = df

tbl = tmp.groupby('record_date')[amount_type].sum().reset_index()

tbl['year'] = tbl['record_date'].dt.year

tbl['record_date_'] = tbl['record_date'].apply(lambda x: x.replace(year=2000))

pivot = tbl.pivot(index='record_date_', columns='year', values=amount_type)

melted = pivot.reset_index().melt(id_vars='record_date_', var_name='year', value_name=amount_type)

melted = melted.dropna()

fig = px.line(melted, x='record_date_', y=amount_type, color='year', title=f'TGA Year Comparison : {selected_category}')

fig.update_xaxes(tickformat='%b %d')

st.plotly_chart(fig, use_container_width=True)



# df.loc[df['transaction_type'] == 'Withdrawals', 'transaction_today_amt'] = -df['transaction_today_amt']
# df.loc[df['transaction_type'] == 'Withdrawals', 'transaction_mtd_amt']   = -df['transaction_mtd_amt']
# df.loc[df['transaction_type'] == 'Withdrawals', 'transaction_fytd_amt']  = -df['transaction_fytd_amt']

# df['transaction_fytd_amt'] = df['transaction_fytd_amt'] * 1_000_000

# st.plotly_chart(fig, use_container_width=True)

st.sidebar.button(label='Clear Cache', on_click= lambda: load_dataframe.clear())

st.sidebar.markdown('[source code](https://github.com/dharmatech/tga_explorer.py)')