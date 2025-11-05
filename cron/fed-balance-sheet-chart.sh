#!/usr/bin/bash

#  0 14 * * THU     /var/www/dharmatech.dev/data/temp/fed_net_liquidity_streamlit.py/cron/fed-balance-sheet-chart.sh  # 02:00 PM   THU

. /home/dharmatech/keys

. /home/dharmatech/python-environments/env-3.10-streamlit/bin/activate

cd /var/www/dharmatech.dev/data/temp/fed_net_liquidity_streamlit.py

python -m pages.7_Fed_Balance_Sheet update
