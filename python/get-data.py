from dotenv import load_dotenv
load_dotenv()

import os
api_key = os.environ.get('DUNE_API_KEY')

from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import QueryBase

query = QueryBase(
    query_id=3561468,
)

dune = DuneClient.from_env()
bresults = dune.run_query(query)

bresults_d = dune.run_query_dataframe(query)
bresults_df = bresults_d.copy()
assets = 0
liabilities = 0
for x in bresults_df['balance']:
    if x > 0:
        assets += x
    else:
        liabilities += x*-1
        
assets = round(assets,1)
liabilities = round(liabilities,1)
minpercent = assets*0.001

import pandas as pd
superData = pd.DataFrame(columns=['From', 'Amount', 'To', 'Input'])

assetsList = []
liabilitiesList = []
count = 0
for x in bresults_df['balance']:
    if x <= 0:
        liabilitiesList.append([bresults_df['item'][count],x*-1])
    else:
        assetsList.append([bresults_df['item'][count],x])
    count += 1

assetsListSorted = sorted(assetsList, key=lambda x: x[1], reverse=True)
liabilitiesListSorted = sorted(liabilitiesList, key=lambda x: x[1], reverse=True)

for x in range(len(assetsListSorted)):
    assetN = assetsListSorted[x][0]
    assetV = assetsListSorted[x][1]
    assetP = (assetsListSorted[x][1] / assets) * 100
    new_row = pd.DataFrame({'From': [assetN], 'Amount': [assetV], 'To': ['Assets'], 'Input': f"{assetN} {round(assetP,1)}% [{round(assetV,1)}] Assets 100%"})
    superData = pd.concat([superData, new_row])

new_row = pd.DataFrame({'From': ['Assets'], 'Amount': [assetV], 'To': ['Liabilities'], 'Input': f"Assets 100% [{assets}] Liabilities 100%"})
superData = pd.concat([superData, new_row])

daiP = ''
dsrP = ''
for x in range(len(liabilitiesListSorted)):
    liabilityN = liabilitiesListSorted[x][0]
    liabilityV = liabilitiesListSorted[x][1]
    liabilityP = (liabilitiesListSorted[x][1] / assets) * 100
    if liabilityN == 'DAI':
        daiP =f"{liabilityN} {round(liabilityP,1)}%"
    if liabilityN == 'DSR':
        dsrP =f"{liabilityN} {round(liabilityP,1)}%"
    if liabilityN == 'Equity':
        liabilityN = 'Surplus Buffer'
    new_row = pd.DataFrame({'From': ['Liabilities'], 'Amount': [liabilityV], 'To': [liabilityN], 'Input': f"Liabilities 100% [{round(liabilityV,1)}] {liabilityN} {round(liabilityP,1)}%"})
    superData = pd.concat([superData, new_row])

query = QueryBase(
    query_id=3560801,
)

dune = DuneClient.from_env()
results = dune.run_query(query)
results_d = dune.run_query_dataframe(query)
results_df = results_d.copy()

totalDai = round(results_df['total_balance'].iloc[0], 1)
results_df['wallet'] = results_df['wallet'].replace('<nil>', 'EOA')
results_df['protocol'] = results_df['protocol'].replace('<nil>', 'Other')

totalDaiWallet = results_df.groupby('wallet')['balance'].sum()
totalDaiWalletsorted = totalDaiWallet.sort_values(ascending=False)

for wallet, balance in totalDaiWalletsorted.items():
    if wallet != "DSR":
        walletP = (balance / assets) *100

walletTotalDic = {}
for wallet, balance in totalDaiWalletsorted.items():
    if wallet != "DSR":
        walletTotalDic[wallet] = balance

query = QueryBase(
    query_id=3561218,
)

dune = DuneClient.from_env()
sresults = dune.run_query(query)
sresults_d = dune.run_query_dataframe(query)
sresults_df = sresults_d.copy()
print(sresults_df)

sresults_df['wallet'] = sresults_df['wallet'].replace('<nil>', 'EOA')
sresults_df['protocol'] = sresults_df['protocol'].replace('<nil>', 'Other')
totalsDaiWallet = sresults_df.groupby('wallet')['balance'].sum()
totalsDaiWalletsorted = totalsDaiWallet.sort_values(ascending=False)

totalswalletB = 0

for wallet, balance in totalsDaiWalletsorted.items():
    if wallet in walletTotalDic.keys():
        walletTotalDic[wallet] += balance
    else:
        walletTotalDic[wallet] = balance
    totalswalletB += balance
    
dsr_balance = bresults_df[bresults_df['item'] == 'DSR']['balance'].values[0]
walletTotalDic['EOA'] += ((dsr_balance * -1) - totalswalletB)

for wallet, balance in totalDaiWalletsorted.items():
    if wallet != "DSR":
        if walletTotalDic[wallet] > minpercent:
            walletP = (walletTotalDic[wallet] / assets) * 100
            new_row = pd.DataFrame({'From': [daiP], 'Amount': [balance], 'To': [wallet], 'Input': f"{daiP} [{round(balance,1)}] {wallet} {round(walletP,1)}%"})
            superData = pd.concat([superData, new_row])

dsrEOA = walletTotalDic['EOA'] - totalDaiWallet['EOA']

for wallet, balance in totalsDaiWalletsorted.items():
    if wallet != 'EOA':
        if walletTotalDic[wallet] > minpercent:
            walletP = (walletTotalDic[wallet] / assets) * 100
            new_row = pd.DataFrame({'From': [dsrP], 'Amount': [balance], 'To': [wallet], 'Input': f"{dsrP} [{round(balance,1)}] {wallet} {round(walletP,1)}%"})
            superData = pd.concat([superData, new_row])
    else:
        if walletTotalDic[wallet] > minpercent:
            walletP = (walletTotalDic[wallet] / assets) * 100
            new_row = pd.DataFrame({'From': [dsrP], 'Amount': [dsrEOA], 'To': [wallet], 'Input': f"{dsrP} [{round(dsrEOA,1)}] {wallet} {round(walletP,1)}%"})
            superData = pd.concat([superData, new_row])

comboDF = pd.concat([results_df,sresults_df])
totalProtocol = comboDF.groupby('protocol')['balance'].sum()
totalProtocolSorted = totalProtocol.sort_values(ascending=False)

for protocol, balance in totalProtocolSorted.items():
    pRow = comboDF[comboDF['protocol'] == protocol].iloc[0]
    pWallet = pRow['wallet']
    if balance > minpercent:
        if pWallet != 'DSR' and pWallet != 'EOA':
            pWalletP = walletTotalDic[pWallet]
            balanceP = (balance / assets) * 100
            walletP = (walletTotalDic[pWallet] / assets) * 100
            new_row = pd.DataFrame({'From': [pWallet], 'Amount': [balance], 'To': [protocol], 'Input': f"{pWallet} {round(walletP,1)}% [{round(balance,1)}] {protocol} {round(balanceP,1)}%"})
            superData = pd.concat([superData, new_row])

for index, row in superData.iterrows():
    print(row['Input'])

with open('output.txt', 'w') as f:
    for index, row in superData.iterrows():
        f.write(str(row['Input']) + '\n')

print("Data written to output.txt successfully.")
