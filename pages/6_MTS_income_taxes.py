
import pandas as pd
import treasury_gov_pandas.datasets.mts.mts_table_4.load
import streamlit as st
import plotly.express as px
import numpy as np

@st.cache_data
def load_dataframe():
    df = treasury_gov_pandas.datasets.mts.mts_table_4.load.load()

    df['record_date'] = pd.to_datetime(df['record_date'])

    df['current_month_net_rcpt_amt']   = pd.to_numeric(df['current_month_net_rcpt_amt'], errors='coerce')
    df['current_month_gross_rcpt_amt'] = pd.to_numeric(df['current_month_gross_rcpt_amt'], errors='coerce')
    df['current_fytd_net_rcpt_amt']    = pd.to_numeric(df['current_fytd_net_rcpt_amt'], errors='coerce')
    df['prior_fytd_net_rcpt_amt']      = pd.to_numeric(df['prior_fytd_net_rcpt_amt'], errors='coerce')

    return df

df = load_dataframe()

'Data is from the [Monthly Treasury Statement](https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/receipts-of-the-u-s-government) dataset on treasury.gov.'

tmp = df.query('classification_desc == "Total -- Individual Income Taxes"')[['record_date', 'classification_desc', 'current_month_net_rcpt_amt', 'current_fytd_net_rcpt_amt', 'prior_fytd_net_rcpt_amt']]

with st.expander(label='dataframe'):
    st.dataframe(tmp, hide_index=True)

with st.expander(label='Unique values of classification_desc'):
    st.dataframe(pd.DataFrame(df['classification_desc'].unique()), hide_index=True)




colunns_to_exclude = [
    'parent_id',
    'classification_id',
    
    "table_nbr",
    "src_line_nbr",
    "print_order_nbr",
    "line_code_nbr",
    "data_type_cd",
    "record_type_cd",
    "sequence_level_nbr",
    "sequence_number_cd",
    "record_fiscal_year",
    "record_fiscal_quarter",
    "record_calendar_year",
    "record_calendar_quarter",
    "record_calendar_month",
    "record_calendar_day"
]

desc = 'Total -- Individual Income Taxes'

# df.query('classification_desc == @desc').drop(columns=colunns_to_exclude + ['classification_desc']).iloc[-1]

# record_date                           2024-04-30
# current_month_gross_rcpt_amt     556507119650.53
# current_month_refund_amt          74580543634.82
# current_month_net_rcpt_amt       481926576015.71
# current_fytd_gross_rcpt_amt     1812511378855.04
# current_fytd_refund_amt          241282769556.44
# current_fytd_net_rcpt_amt       1571228609298.60
# prior_fytd_gross_rcpt_amt       1676082840455.62
# prior_fytd_refund_amt            265760582660.48
# prior_fytd_net_rcpt_amt         1410322257795.14

tmp = df.query('classification_desc == "Total -- Individual Income Taxes"')[['record_date', 'current_month_net_rcpt_amt']]

fig = px.bar(tmp, x='record_date', y='current_month_net_rcpt_amt', title='Total -- Individual Income Taxes')

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------

tmp = df.query('classification_desc == "Total -- Individual Income Taxes"')[['record_date', 'current_month_net_rcpt_amt', 'record_calendar_month', 'record_calendar_year']]

pivot = tmp.pivot_table(values='current_month_net_rcpt_amt', index='record_calendar_month', columns='record_calendar_year')

melted = pivot.reset_index().melt(id_vars='record_calendar_month', value_name='current_month_net_rcpt_amt')

fig = px.line(melted, x='record_calendar_month', y='current_month_net_rcpt_amt', color='record_calendar_year', title='Total -- Individual Income Taxes')

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------

tmp = df.query('classification_desc == "Total -- Individual Income Taxes"')[['record_date', 'current_month_net_rcpt_amt']]

tmp = tmp.rename(columns={'current_month_net_rcpt_amt': 'curr'})

tmp['prev'] = tmp['curr'].shift(12)

tmp['diff'] = tmp['curr'] - tmp['prev']

tmp['yoy_pct'] = tmp['diff'] / tmp['prev'] * 100


fig = px.bar(tmp, x='record_date', y=['prev', 'curr'], title='Total -- Individual Income Taxes : current and year ago values', barmode='group')

st.plotly_chart(fig, use_container_width=True)


fig = px.bar(tmp, x='record_date', y=['yoy_pct'], title='Total -- Individual Income Taxes : YoY % Change')

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------

tmp = df.query('classification_desc == "Total -- Individual Income Taxes"')[['record_date', 'current_fytd_net_rcpt_amt', 'prior_fytd_net_rcpt_amt']]

fig = px.line(tmp, x='record_date', y=['current_fytd_net_rcpt_amt', 'prior_fytd_net_rcpt_amt'], title='Total -- Individual Income Taxes')

st.plotly_chart(fig, use_container_width=True)

st.button('Clear cache', on_click=load_dataframe.clear)

# ----------------------------------------------------------------------

# df.drop(columns=colunns_to_exclude + ['current_month_gross_rcpt_amt', 'current_month_refund_amt', 'current_fytd_gross_rcpt_amt', 'current_fytd_refund_amt', 'prior_fytd_gross_rcpt_amt', 'prior_fytd_refund_amt'])

# # unique values of classification_desc

# pd.DataFrame(df['classification_desc'].unique())

# df.query('classification_desc == "Total -- Individual Income Taxes"').drop(columns=colunns_to_exclude + ['current_month_gross_rcpt_amt', 'current_month_refund_amt', 'current_fytd_gross_rcpt_amt', 'current_fytd_refund_amt', 'prior_fytd_gross_rcpt_amt', 'prior_fytd_refund_amt'])