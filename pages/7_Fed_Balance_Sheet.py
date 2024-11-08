import sys
import pandas as pd
import fred_pandas
import streamlit as st
import plotly.graph_objects as go

# ----------------------------------------------------------------------
assets = {
    "WGCAL": 'Gold Certificate Account',
    "WOSDRL": 'Special Drawing Rights Certificate Account',
    "WACL": 'Coin',
    "WSHOBL": 'Bills',
    "WSHONBNL": 'Notes and bonds, nominal',
    "WSHONBIIL": 'Notes and bonds, inflation-indexed',
    "WSHOICL": 'Inflation compensation',
    "WSHOFADSL": 'Federal Agency Debt Securities',
    "WSHOMCB": 'Mortgage-backed securities',
    "WUPSHO": 'Unamortized Premiums on Securities Held Outright',
    "WUDSHO": 'Unamortized Discounts on Securities Held Outright', # Negative value
    "WORAL": 'Repurchase Agreements',
    "WLCFLPCL": 'Primary Credit',
    "WLCFOCEL": 'Other Credit Extensions',
    "SWPT": 'Central Bank Liquidity Swaps',
    "WFCDA": 'Foreign Currency Denominated Assets',
    "WAOAL": 'Other Assets',
    'H41RESPPALDKNWW': 'Bank Term Funding Program'
}

liabilities = {
    "WLFN": 'Federal Reserve Notes, net of F.R. Bank holdings',
    "WLRRAL": 'Reverse repurchase agreements',
    "TERMT": 'Term deposits held by depository institutions',
    "WLODLL": 'Other Deposits Held by Depository Institutions',
    "WDTGAL": 'U.S. Treasury, General Account',
    "WDFOL": 'Foreign Official',
    "WLODL": 'Other',
    "H41RESH4ENWW": 'Treasury Contribution to Credit Facilities'
}

all_items = {**assets, **liabilities}

series_items = list(assets.keys()) + list(liabilities.keys())
# ----------------------------------------------------------------------
# python -m fed_balance_sheet_chart update

if __name__ == '__main__':
    if 'update' in sys.argv:
        print('updating series data')

        for elt in series_items:
            fred_pandas.load_records(series=elt, update=True)
        exit()
# ----------------------------------------------------------------------


@st.cache_data
def setup_dataframe():

    tbl = {}

    # for series in assets.keys():
    #     tbl[series] = fred_pandas.load_records(series=series, update=False)


    for series in series_items:
        tbl[series] = fred_pandas.load_records(series=series, update=False)

    for series, df in tbl.items():
        df.rename(columns={'value': series}, inplace=True)
        df.drop(columns='realtime_start',    inplace=True)
        df.drop(columns='realtime_end',      inplace=True)

    ls = list(tbl.values())

    a = ls[0]

    for b in ls[1:]:
        a = a.merge(b, on='date')



    # convert all values to numeric

    for series in a.columns[1:]:
        # a[series] = pd.to_numeric(a[series], errors='coerce')
        a[series] = pd.to_numeric(a[series])

        



    # a

    for series in liabilities.keys():
        a[series] = a[series] * -1


    # a[['date', 'WLFN']]

    return a

# ----------------------------------------------------------------------

a = setup_dataframe()

if st.sidebar.checkbox('Remove series larger than'):

    threshold = st.sidebar.number_input('Threshold', value=200_000)
    
    last_row = a.iloc[-1]

    for column in last_row.index:

        if column == 'date':
            continue

        if abs(last_row[column]) > threshold:
            print(f'Removing {column}')
            a = a.drop(columns=[column])

# Create a Plotly figure
fig = go.Figure()

# Add a bar to the figure for each series in your DataFrame
# for column in a.columns[1:]:
#     fig.add_trace(go.Bar(x=a['date'], y=a[column], name=column))

# for column in a.columns[1:]:
#     name = f'{column} - {assets[column]}'
#     fig.add_trace(go.Bar(x=a['date'], y=a[column], name=name))

# for column in a.columns[1:]:
#     name = f'{column} - {all_items[column]}'
#     # name = column
#     fig.add_trace(go.Bar(x=a['date'], y=a[column], name=name, hovertemplate = '<b>'+name+'</b><br>Date: %{x}<br>Value: %{y}<extra></extra>'))

for column in a.columns[1:]:

    if column in assets.keys():
        name = f'A: {column} - {all_items[column]}'
    elif column in liabilities.keys():
        name = f'L: {column} - {all_items[column]}'
    else:
        name = f'{column} - {all_items[column]}'

    # name = f'{column} - {all_items[column]}'
    # name = column
    fig.add_trace(go.Bar(x=a['date'], y=a[column], name=name, hovertemplate = '<b>'+name+'</b><br>Date: %{x}<br>Value: %{y}<extra></extra>'))

fig.update_layout(barmode='relative', width=1000, height=600)


st.write('# Federal Reserve Balance Sheet')

st.plotly_chart(fig)

st.button('Clear cache', on_click=setup_dataframe.clear)