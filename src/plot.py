import os
import requests
import sqlite3
import matplotlib.pyplot as plt

app_dir = os.path.dirname(os.path.realpath(__file__))

interval = 1000
url_latestblock = 'https://blockstream.info/api/blocks'
resp = requests.get(url_latestblock)
latest_block = resp.json()[0]
latest_height = latest_block['height']

one_thousandth_block_count = latest_height // interval
tx_counts = [0] * interval


con = sqlite3.connect(f'file:{app_dir}/block-stat.sqlite?mode=ro', uri=True)
cur = con.cursor()
for i in range(interval):
    res = cur.execute(
        '''
        SELECT SUM(tx_count) FROM block_test_result
        WHERE block_height >= ? AND block_height < ?
        ''',
        (i * interval, (i+1) * interval)
    )
    rows = res.fetchall()
    # tx_counts[i] = 0 if rows[0][0] is None else rows[0][0]
    tx_counts[i] = rows[0][0]

fig, ax = plt.subplots(figsize=(48, 6))

ax.tick_params(axis='both', which='major', labelsize=32)
ax.plot(tx_counts, linewidth=4)
plt.savefig(os.path.join(app_dir, 'public/img/chart.png'), bbox_inches='tight')
