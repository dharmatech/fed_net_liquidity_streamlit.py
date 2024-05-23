#!/usr/bin/bash

# 0 14 * * MON-FRI /var/www/dharmatech.dev/data/temp/fed_net_liquidity_streamlit.py/cron/auctions-query-update.sh    # 02:00 PM

. /home/dharmatech/python-environments/env-3.10-streamlit/bin/activate

cd /var/www/dharmatech.dev/data/temp/fed_net_liquidity_streamlit.py

python -m treasury_gov_pandas.datasets.auctions_query.update
