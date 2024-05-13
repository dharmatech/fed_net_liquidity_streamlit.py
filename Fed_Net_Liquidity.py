import datetime
import fed_net_liquidity
import streamlit as st

# st.markdown('# Fed Net Liquidity')

st.set_page_config(page_title='Fed Net Liquidity', page_icon=':moneybag:', layout='wide')

@st.cache_data
def get_dataframe():
    return fed_net_liquidity.load_dataframe()

# df = fed_net_liquidity.load_dataframe()

df = get_dataframe()

df = df[['date', 'WALCL', 'WALCL_diff', 'RRP', 'RRP_diff', 'TGA', 'TGA_diff', 'REM', 'REM_diff', 'NL', 'NL_diff']]

df = df.rename(columns={ 'WALCL_diff': 'diff', 'RRP_diff': 'diff ', 'TGA_diff': 'diff  ', 'REM_diff': 'diff   ', 'NL_diff': 'diff    '})

def format_billions(x):
    return '{:,.0f}'.format(x / 1_000_000_000)

def color_values(val):
    if val > 0:
        return 'color: green'
    elif val < 0:
        return 'color: red'
    else:
        return ''

date_input = st.sidebar.date_input('Show records after:', value=datetime.date(2020, 1, 1))

date_input.strftime('%Y-%m-%d')

df = df[df['date'] > date_input.strftime('%Y-%m-%d')]

st.dataframe(
    df.style
        .format({
            'WALCL':      format_billions,
            'RRP':        format_billions,
            'TGA':        format_billions,
            'REM':        format_billions,
            'NL':         format_billions,
            'diff':       format_billions,
            'diff ':      format_billions,
            'diff  ':     format_billions,
            'diff   ':    format_billions,
            'diff    ':   format_billions
        })
        .map(color_values, subset=['diff', 'diff ', 'diff  ', 'diff   ', 'diff    ']),
    hide_index=True
)


