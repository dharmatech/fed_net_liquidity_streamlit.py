#!/usr/bin/bash

# 25 10 * * MON-FRI /var/www/dharmatech.dev/data/temp/fed_net_liquidity_streamlit.py/cron/rrp-update.sh    # 10:25 AM

. /home/dharmatech/python-environments/env-3.10-streamlit/bin/activate

cd /var/www/dharmatech.dev/data/temp/fed_net_liquidity_streamlit.py

python -m newyorkfed_pandas.rrp
