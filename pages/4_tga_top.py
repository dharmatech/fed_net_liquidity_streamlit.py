
import pandas as pd
import treasury_gov_pandas
import streamlit as st

url = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/deposits_withdrawals_operating_cash'

@st.cache_data
def get_dataframe():
    return treasury_gov_pandas.load_records(url = url)

# df = treasury_gov_pandas.load_records(url = url)

df = get_dataframe()

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

col_1.dataframe(get_rows_for_date_and_type(df, date, 'Deposits'), hide_index=True)

col_2.write('### Withdrawals')

# st.dataframe(get_rows_for_date_and_type(df, date, 'Withdrawals'), hide_index=True)

col_2.dataframe(get_rows_for_date_and_type(df, date, 'Withdrawals'), hide_index=True)
