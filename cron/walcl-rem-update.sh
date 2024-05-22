#!/usr/bin/bash

# 50 13 * * MON-FRI /var/www/dharmatech.dev/data/temp/fed_net_liquidity_streamlit.py/cron/walcl-rem-update.sh    # 01:50 PM   THUR

. /home/dharmatech/python-environments/env-3.10-streamlit/bin/activate

cd /var/www/dharmatech.dev/data/temp/fed_net_liquidity_streamlit.py

python -m fred_pandas.fred_pandas WALCL
python -m fred_pandas.fred_pandas RESPPLLOPNWW

