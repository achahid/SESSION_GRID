

import MetaTrader5 as mt
import datetime
import pandas as pd
import numpy as np
import streamlit as st


def option_to_model(level_number,options):
  try:
    return options[level_number]
  except Exception as e:
    return e

# These are some model options for sentence transformers:f
option_models = {
    "<select>": '<select>',
    "test_0": 51138301,
    "test_1": 51140684
}

option_passwords = {
    "<select>": '<select>',
    "test_0": 'ex5Meg5E',
    "test_1": 'eP38EwpZ'
}

option_mt = {
    "<select>": '<select>',
    "test_0": 'ex5Meg5E',
    "test_1": 'swdesf'
}

html_temp = """
<div style="background-color:blue;padding:1.5px">
<h1 style="color:white;text-align:center;"> BALANCE SHEET </h1>
</div><br>"""
st.markdown(html_temp,unsafe_allow_html=True)

account_name = ["<select>", "test_0", "test_1" ]
select_box = st.selectbox('SELECT AN ACCOUNT', options=account_name)
selected_account = option_to_model(select_box, option_models)
selected_password = option_to_model(select_box, option_passwords)
# selected_mt = option_to_model(select_box, option_passwords)
st.write('You selected model:', selected_account)
# connect to MetaTrader 5
# mt.initialize('C:\\MetaTrader\\SESSION_GRID_0\\terminal64.exe')
# mt.initialize('')

load_account = st.button('GENERATE BALANCE-SHEET')

if load_account:
    mt.initialize('')
    login = selected_account
    password = selected_password
    server ='ICMarketsSC-Demo'
    authorized = mt.login(login,password,server)



    if authorized:
        account_info = mt.account_info()
        if account_info != None:
            account_info_dict = mt.account_info()._asdict()
            # convert the dictionary into DataFrame and print
            df = pd.DataFrame(list(account_info_dict.items()), columns=['property', 'value'])
            df.rename(columns={'value': 'VALUE'}, inplace=True)
            df = df[df.property.isin(['login', 'balance', 'profit', 'equity'])]

            Values = df.VALUE.to_list()
            account = Values[0]
            equity =  Values[3]
            current_balance = float(Values[1])
            Unrealized_pnl = float(Values[2])
            initial_balance = 6000
            profit =  round(current_balance - initial_balance,2)

            # calculate the drawdown
            if equity < current_balance:
                drawdown = round(abs((equity - current_balance) / current_balance), 2) * 100
            else:
                drawdown = 0
            # calculate the profit percent growth
            profit_percent_growth = profit / initial_balance * 100

            # Results:
            data = { 'Info' :['Account','Profit','Profit grouwth %','Drawdown %','Equity','Current balance','Unrealized profit'],
                     'VALUES':[account,profit,profit_percent_growth,drawdown,equity,current_balance,Unrealized_pnl] }

            results = pd.DataFrame(data)
            results['VALUES'] = results['VALUES'].apply(lambda x: '{:.2f}'.format(x) if isinstance(x, float) else x)

            st.table(results)

    else:
        print("failed to connect to trade account 25115284 with password=gqz0343lbdm, error code =", mt.last_error())


