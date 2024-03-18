from dotenv import load_dotenv
load_dotenv()

import os
api_key = os.environ.get('DUNE_DAI_KEY')

from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import QueryBase

query = QueryBase(
    query_id=3523957,
)

dune = DuneClient.from_env()
results = dune.run_query(query)

results_d = dune.run_query_dataframe(query)
results_df = results_d.copy()

import pandas as pd
superData = pd.DataFrame(columns=['From', 'Amount', 'To', 'Input'])

totalDai = round(results_df['total_balance'].iloc[0], 1)

hopOne = []

results_df_sortedOne = results_df.sort_values('balance', ascending=False)

for index, row in results_df_sortedOne.iterrows():
    if row['wallet'] not in hopOne:
        hopOne.append(row['wallet'])
        hopOneAmount = round(row['balance'], 1)
        hopeOnePercent = round((hopOneAmount/totalDai)*100, 1)
        new_row = pd.DataFrame({'From': ['DAI'], 'Amount': [hopOneAmount], 'To': [row['wallet']], 'Input': [f"DAI 100% [{hopOneAmount}] {row['wallet']} {hopeOnePercent}%"]})
        superData = pd.concat([superData, new_row])

results_df_sortedTwo = results_df.sort_values('balance_protocol', ascending=False)
for index, row in results_df_sortedTwo.iterrows():
    if row['balance_protocol'] > 1000000:
        hopOneAmount = round(row['balance'], 1)
        hopeOnePercent = round((hopOneAmount/totalDai)*100, 1)
        hopTwoAmount = round(row['balance_protocol'], 1)
        hopeTwoPercent = round((hopTwoAmount/totalDai)*100, 1)
        new_row = pd.DataFrame({'From': [row['wallet']], 'Amount': [hopTwoAmount], 'To': [row['protocol']], 'Input': [f"{row['wallet']} {hopeOnePercent}% [{hopTwoAmount}] {row['protocol']} {hopeTwoPercent}%"]})
        superData = pd.concat([superData, new_row])
        
for index, row in superData.iterrows():
    print(row['Input'])
