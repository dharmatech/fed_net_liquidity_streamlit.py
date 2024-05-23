#!/usr/bin/bash

. /home/dharmatech/python-environments/env-3.10-streamlit/bin/activate

cd /var/www/dharmatech.dev/data/temp/fed_net_liquidity_streamlit.py

python -m treasury_gov_pandas.datasets.deposits_withdrawals_operating_cash.update
