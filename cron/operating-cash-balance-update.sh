#!/usr/bin/bash

# 10 13 * * MON-FRI /var/www/dharmatech.dev/data/temp/fed_net_liquidity_streamlit.py/cron/operating-cash-balance-update.sh    # 01:10 PM

. /home/dharmatech/python-environments/env-3.10-streamlit/bin/activate

cd /var/www/dharmatech.dev/data/temp/fed_net_liquidity_streamlit.py

python -m treasury_gov_pandas.datasets.operating_cash_balance.update
