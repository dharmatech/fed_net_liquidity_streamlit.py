
import pandas as pd
import treasury_gov_pandas
import streamlit as st

st.set_page_config(layout='wide')

url = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/deposits_withdrawals_operating_cash'

@st.cache_data
def get_dataframe():
    return treasury_gov_pandas.load_records(url = url)

# df = treasury_gov_pandas.load_records(url = url)


df = get_dataframe()

# df.drop(columns=['account_type', 'table_nbr', 'table_nm', 'src_line_nbr', 'record_fiscal_year', 'record_fiscal_quarter', 'record_calendar_year', 'record_calendar_quarter', 'record_calendar_month', 'record_calendar_day'])

df['record_date'] = pd.to_datetime(df['record_date'])

df['transaction_today_amt'] = pd.to_numeric(df['transaction_today_amt'])
df['transaction_mtd_amt'] = pd.to_numeric(df['transaction_mtd_amt'])
df['transaction_fytd_amt'] = pd.to_numeric(df['transaction_fytd_amt'])

# ----------------------------------------------------------------------

def get_rows_for_date_and_type(df, date, transaction_type):

    tmp = df.query('record_date == @date').query('transaction_type == @transaction_type').sort_values(by = 'transaction_today_amt', ascending = False)

    columns_to_drop = [
        'record_calendar_quarter', 'record_calendar_year', 'record_fiscal_year', 'record_fiscal_quarter', 'record_calendar_month', 'record_calendar_day', 
        'src_line_nbr', 'table_nbr', 'account_type', 'table_nm', 'transaction_type', 'transaction_catg_desc', 
        'record_date'
    ]

    tmp = tmp.rename(columns = {'transaction_today_amt': 'today', 'transaction_mtd_amt': 'mtd', 'transaction_fytd_amt': 'fytd'})
    
    return tmp.drop(columns = columns_to_drop)
# ----------------------------------------------------------------------

'# Treasury General Account'

most_recent_date = df['record_date'].max()

date = st.date_input('Select a date', value = most_recent_date)

col_1, col_2 =st.columns(2)

col_1.write('### Deposits')

# st.dataframe(get_rows_for_date_and_type(df, date, 'Deposits'), hide_index=True)



# get_rows_for_date_and_type(df, date, 'Deposits')






col_1.dataframe(get_rows_for_date_and_type(df, date, 'Deposits'), hide_index=True)

col_2.write('### Withdrawals')

# st.dataframe(get_rows_for_date_and_type(df, date, 'Withdrawals'), hide_index=True)

col_2.dataframe(get_rows_for_date_and_type(df, date, 'Withdrawals'), hide_index=True)

st.button('Clear cache', on_click=get_dataframe.clear)

# ----------------------------------------------------------------------

# df.drop(columns=['account_type', 'table_nbr', 'table_nm', 'src_line_nbr', 'record_fiscal_year', 'record_fiscal_quarter', 'record_calendar_year', 'record_calendar_quarter', 'record_calendar_month', 'record_calendar_day'])

# df[['record_date', 'transaction_type', 'transaction_catg', 'transaction_today_amt']]
tmp = df[['record_date', 'transaction_type', 'transaction_catg', 'transaction_fytd_amt']]

transaction_type = 'Withdrawals'

tmp = df.query('record_date == @date').query('transaction_type == @transaction_type')

tmp = tmp.query('transaction_catg != "null"')

tmp = tmp[tmp['transaction_catg'].str.contains(pat='Public Debt Cash Redemp', case=False) == False]

# tmp[['record_date', 'transaction_type', 'transaction_catg', 'transaction_fytd_amt']]

tmp['transaction_fytd_amt'] = tmp['transaction_fytd_amt'] / 1000

tmp['transaction_fytd_amt'] = tmp['transaction_fytd_amt'].round(0)

tmp['transaction_fytd_amt'] = tmp['transaction_fytd_amt'].astype(int)

import plotly.express as px

fig = px.pie(
    data_frame=tmp, 
    names='transaction_catg', 
    values='transaction_fytd_amt', 
    title=f'Withdrawals FYTD as of {date} (in billions USD)')

fig.update_traces(textposition='inside', textinfo='percent+label+value')

st.plotly_chart(fig)

# ----------------------------------------------------------------------

# df.drop(columns=['account_type', 'table_nbr', 'table_nm', 'src_line_nbr', 'record_fiscal_year', 'record_fiscal_quarter', 'record_calendar_year', 'record_calendar_quarter', 'record_calendar_month', 'record_calendar_day'])

# df[['record_date', 'transaction_type', 'transaction_catg', 'transaction_today_amt']]
tmp = df[['record_date', 'transaction_type', 'transaction_catg', 'transaction_fytd_amt']]

transaction_type = 'Withdrawals'

tmp = tmp.query('record_date == @date').query('transaction_type == @transaction_type')

tmp = tmp.query('transaction_catg != "null"')

tmp = tmp[tmp['transaction_catg'].str.contains(pat='Public Debt Cash Redemp', case=False) == False]

# tmp[tmp['transaction_catg'].str.contains(pat='HHS', case=True)]

# tmp[tmp['transaction_catg'].str.contains(pat='HHS', case=True)]['transaction_catg'] = 'HHS'

tmp.loc[tmp['transaction_catg'].str.contains(pat='HHS',   case=True), 'transaction_catg'] = 'HHS'
tmp.loc[tmp['transaction_catg'].str.contains(pat='USDA',  case=True), 'transaction_catg'] = 'USDA'
tmp.loc[tmp['transaction_catg'].str.contains(pat='DoD',   case=True), 'transaction_catg'] = 'DoD'
tmp.loc[tmp['transaction_catg'].str.contains(pat='SSA',   case=True), 'transaction_catg'] = 'SSA'
tmp.loc[tmp['transaction_catg'].str.contains(pat='VA',    case=True), 'transaction_catg'] = 'VA'
tmp.loc[tmp['transaction_catg'].str.contains(pat='OPM',   case=True), 'transaction_catg'] = 'OPM'
tmp.loc[tmp['transaction_catg'].str.contains(pat='TREAS', case=True), 'transaction_catg'] = 'TREAS'
tmp.loc[tmp['transaction_catg'].str.contains(pat='DOT',   case=True), 'transaction_catg'] = 'DOT'
tmp.loc[tmp['transaction_catg'].str.contains(pat='DHS',   case=True), 'transaction_catg'] = 'DHS'
tmp.loc[tmp['transaction_catg'].str.contains(pat='DOL',   case=True), 'transaction_catg'] = 'DOL'


tmp.sort_values(by='transaction_fytd_amt', ascending=False).head(10)

# tmp.groupby('transaction_catg')['transaction_fytd_amt'].sum().sort_values(ascending=False).head(10)

summed = tmp

summed['transaction_fytd_amt'] = summed.groupby('transaction_catg')['transaction_fytd_amt'].transform('sum')

summed = summed.drop_duplicates(subset=['transaction_catg'], keep='first')

summed.sort_values(by='transaction_fytd_amt', ascending=False).head(10)

tmp = summed

tmp['transaction_fytd_amt'] = tmp['transaction_fytd_amt'] / 1000

tmp['transaction_fytd_amt'] = tmp['transaction_fytd_amt'].round(0)

tmp['transaction_fytd_amt'] = tmp['transaction_fytd_amt'].astype(int)


fig = px.pie(
    data_frame=tmp, 
    names='transaction_catg', 
    values='transaction_fytd_amt', 
    title=f'Withdrawals FYTD as of {date} (in billions USD) [grouped by agency]')

fig.update_traces(textposition='inside', textinfo='percent+label+value')

st.plotly_chart(fig)

# ----------------------------------------------------------------------

# df[['record_date', 'transaction_type', 'transaction_catg', 'transaction_fytd_amt']]

# tmp[tmp['transaction_catg'].str.contains(pat='HHS',  case=True)][['record_date', 'transaction_type', 'transaction_catg', 'transaction_fytd_amt']]['transaction_fytd_amt'].sum()