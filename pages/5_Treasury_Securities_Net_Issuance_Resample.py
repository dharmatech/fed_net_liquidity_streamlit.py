import pandas as pd
import treasury_gov_pandas

import streamlit as st
import plotly
import plotly.express

# @st.cache_data
def get_dataframe():
    return treasury_gov_pandas.load_records('https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query', lookback=10, update=False)

@st.cache_data
def build_pivot():

    df = treasury_gov_pandas.load_records('https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query', lookback=10, update=False)

    # df = get_dataframe()

    # ----------------------------------------------------------------------
    df['issue_date']    = pd.to_datetime(df['issue_date']) 
    df['maturity_date'] = pd.to_datetime(df['maturity_date'])

    df['total_accepted'] = pd.to_numeric(df['total_accepted'], errors='coerce')
    # ----------------------------------------------------------------------

    # change all instances of 'TIPS Note' to 'Note' in 'security_type' column

    df['security_type'] = df['security_type'].replace('TIPS Note', 'Note')
    df['security_type'] = df['security_type'].replace('FRN Note',  'Note')
    df['security_type'] = df['security_type'].replace('TIPS Bond', 'Bond')
    df['security_type'] = df['security_type'].replace('CMB',       'Bill')
    
    # ----------------------------------------------------------------------
    # group by 'issue_date' and 'security_type' and sum 'total_accepted'

    issued = df.groupby(['issue_date', 'security_type'])['total_accepted'].sum().reset_index()

    # group by 'maturity_date' and 'security_type' and sum 'total_accepted'

    maturing = df.groupby(['maturity_date', 'security_type'])['total_accepted'].sum().reset_index()

    # join issued and maturing on 'issue_date' = 'maturity_date' and 'security_type' = 'security_type'

    merged = pd.merge(issued, maturing, how='outer', left_on=['issue_date', 'security_type'], right_on=['maturity_date', 'security_type'])

    merged.rename(columns={'total_accepted_x': 'issued', 'total_accepted_y': 'maturing'}, inplace=True)

    merged['change'] = merged['issued'].fillna(0) - merged['maturing'].fillna(0)

    merged['date'] = merged['issue_date'].combine_first(merged['maturity_date'])
    # ----------------------------------------------------------------------
    tmp = merged

    agg = tmp.groupby(['date', 'security_type'])['change'].sum().reset_index()
    
    pivot_df = agg.pivot(index='date', columns='security_type', values='change').fillna(0)
    
    # pivot_df = pivot_df.resample('YE').sum()

    # pivot_df = pivot_df.resample(group_by).sum()
    
    # pivot_df['total'] = pivot_df.sum(axis=1)
    
    # pivot_df['bill_pct_12m_sum'] = pivot_df['Bill'] / pivot_df['total'] * 100
     
    return pivot_df

# group_by = st.selectbox(label='group by', options=['ME', 'YE'])

group_by = st.sidebar.selectbox(label='group by', options=['D', 'W', 'ME', 'QE', 'YE'], index=2)

pivot_df = build_pivot()

pivot_df = pivot_df.resample(group_by).sum()

fig = plotly.express.bar(pivot_df, x=pivot_df.index, y=pivot_df.columns, title='Treasury Securities Net Issuance', 
                         labels={'value': 'change', 'date': 'date'}
                        #  width=1000, 
                        #  height=600
                         )

st.plotly_chart(fig, use_container_width=True)

st.button('Clear cache', on_click=build_pivot.clear)


