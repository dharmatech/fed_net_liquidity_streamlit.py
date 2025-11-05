#!/usr/bin/bash

# 0 0 15 * * /var/www/dharmatech.dev/data/temp/fed_net_liquidity_streamlit.py/cron/mts-table-4-update.sh    # monthly on the 15th

. /home/dharmatech/python-environments/env-3.10-streamlit/bin/activate

cd /var/www/dharmatech.dev/data/temp/fed_net_liquidity_streamlit.py

python -m treasury_gov_pandas.datasets.mts.mts_table_4.update
