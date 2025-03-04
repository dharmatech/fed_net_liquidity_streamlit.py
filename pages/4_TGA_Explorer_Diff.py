
import pandas as pd
import treasury_gov_pandas.datasets.deposits_withdrawals_operating_cash.load
import streamlit as st
import plotly.express as px

# python -m treasury_gov_pandas.datasets.deposits_withdrawals_operating_cash.update

st.set_page_config(layout='wide')

@st.cache_data
def load_dataframe():
    return treasury_gov_pandas.datasets.deposits_withdrawals_operating_cash.load.load()

df = load_dataframe()
# ----------------------------------------------------------------------
df['transaction_today_amt'] = pd.to_numeric(df['transaction_today_amt'], errors='coerce')
df['transaction_mtd_amt']   = pd.to_numeric(df['transaction_mtd_amt'],   errors='coerce')
df['transaction_fytd_amt']  = pd.to_numeric(df['transaction_fytd_amt'],  errors='coerce')
# ----------------------------------------------------------------------

transaction_value = st.sidebar.selectbox(label='Value', options=['transaction_today_amt', 'transaction_mtd_amt', 'transaction_fytd_amt'], index=2)

# ----------------------------------------------------------------------
tmp_b = df.query('transaction_catg.str.contains("public debt cash", case=False)', engine='python')

tmp_b = tmp_b.pivot_table(index='record_date', columns='transaction_type', values=transaction_value)

tmp_b.columns.name = None

tmp_b = tmp_b.reset_index()

tmp_b = tmp_b.rename(columns={'Deposits' : 'issues', 'Withdrawals' : 'redemp'})

# ----------------------------------------------------------------------
tmp = df.query('transaction_catg == "null"')

tmp_a = tmp.pivot_table(index='record_date', columns='transaction_type', values=transaction_value)

tmp_a.columns.name = None

tmp_a = tmp_a.reset_index()

tmp_a['diff'] = tmp_a['Deposits'] - tmp_a['Withdrawals']
# ----------------------------------------------------------------------
tbl = pd.merge(tmp_a, tmp_b, on='record_date')

tbl = tbl.rename(columns={
    'Deposits'    : 'dep',
    'Withdrawals' : 'wit',
    'issues'      : 'debt_dep',
    'redemp'      : 'debt_wit'
    })

tbl['debt_diff'] = tbl['debt_dep'] - tbl['debt_wit']

tbl['dep_ex_pub_debt'] = tbl['dep'] - tbl['debt_dep']
tbl['wit_ex_pub_debt'] = tbl['wit'] - tbl['debt_wit']

tbl['diff_ex_pub_debt'] = tbl['dep_ex_pub_debt'] - tbl['wit_ex_pub_debt']

tbl.iloc[:, 1:] = tbl.iloc[:, 1:] * 1_000_000

# ----------------------------------------------------------------------
tmp_c = tbl[['record_date', 'diff_ex_pub_debt']].copy(deep=True)

tmp_c['record_date'] = pd.to_datetime(tmp_c['record_date'])

tmp_c['year'] = tmp_c['record_date'].dt.year

tmp_c['record_date_'] = tmp_c['record_date'].apply(lambda x: x.replace(year=2000))

pivot = tmp_c.pivot(index='record_date_', columns='year', values='diff_ex_pub_debt')

melted = pivot.reset_index().melt(id_vars='record_date_', var_name='year', value_name='diff_ex_pub_debt')

melted = melted.dropna()

fig = px.line(melted, x='record_date_', y='diff_ex_pub_debt', color='year', title='TGA : Deposits - Withdrawals (excluding public debt) : Year Comparison')

fig.update_xaxes(tickformat='%b %d')

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------

fig = px.line(tbl, x='record_date', y=['dep', 'wit', 'diff'], title='TGA : Deposits and Withdrawals')

st.plotly_chart(fig, use_container_width=True)


fig = px.line(tbl, x='record_date', y=['debt_dep', 'debt_wit', 'debt_diff'], title='TGA : Public Debt Deposits and Withdrawals')

st.plotly_chart(fig, use_container_width=True)


fig = px.line(tbl, x='record_date', y=['dep_ex_pub_debt', 'wit_ex_pub_debt', 'diff_ex_pub_debt'], title='TGA : Deposits and Withdrawals (excluding public debt)')

st.plotly_chart(fig, use_container_width=True)



fig = px.line(tbl, x='record_date', y='diff_ex_pub_debt', title='TGA : Deposits - Withdrawals (excluding public debt)')

st.plotly_chart(fig, use_container_width=True)



fig = px.line(tbl, x='record_date', y=tbl.columns[1:].tolist(), title='TGA Data')

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------

st.sidebar.button(label='Clear Cache', on_click= lambda: load_dataframe.clear())

st.stop()

