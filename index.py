from datetime import date
import datetime
import yfinance as yf
import numpy as np
import pandas as pd
from GUI import *
import streamlit as st
from bot import *

st.set_page_config(layout="wide", )
# streamlit run StreamLit/streamlit.py

# À SAISIR :
###############################################################
start = "2020-05-25" # début des graphiques                   #
###############################################################

today = date.today()+ datetime.timedelta(days=1)
d1 = today.strftime("%Y-%m-%d")
current_year, current_month, current_day= today.strftime("%Y"), today.strftime("%m"), today.strftime("%d")


def dowload_actif(actif):
  df = yf.download(actif, start=start, end="{}".format(d1))
  df['Date']=df.index

  df.insert(6, "m_a_5d", df["Close"].rolling(window=5).mean().fillna(df["Close"]), allow_duplicates=False) # Ajout moyenne mobile 5j au dataframe
  df.insert(6, "m_a_9d", df["Close"].rolling(window=9).mean().fillna(df["Close"]), allow_duplicates=False) # Ajout moyenne mobile 9j au dataframe

  return df

SP = {
    'Apple':"AAPL",
    'Microsoft':"MSFT",
    'Intel':"INTC",
    'Tesla':"TSLA",
    'Gold':"GOLD",
    'Google':"GOOG",
    'Nintendo':"NTDOY",
}

# STREAMLIT :
###############################################################
# selectbox à gauche 

st.sidebar.header("Réglages")
slider_1 = st.sidebar.selectbox(
    'Choisissez un cours',
    ('Apple', 'Microsoft', 'Intel', 'Tesla', 'Gold', 'Google', 'Nintendo'),
)

df1 = dowload_actif(SP[slider_1]) # Création du dataframe



fenetre = st.sidebar.slider('Durée du backtest (jours):', min_value=2,max_value=len(df1['Close']), value=50)

#nombre d'actifs
try:
  i0 = float(st.sidebar.text_input("Investissement initial pour l'actif "+slider_1+ " En USD", value="0"))
except:
  st.sidebar.warning("Une valeure décimale est attendue")
  i0 = 0


st.header("Investissement initial de "+str(i0)+ " USD à compté du "+str(df1["Date"].iloc[-1*fenetre]))


df1 = df1[df1["Date"] >= df1["Date"].iloc[-1*fenetre]]

backtest_df = behaviour(df1, i0, fenetre)


If = round(backtest_df["recette"].iloc[-1], 2)
delta = round((If-i0)/i0 * 100, 2)

gui(backtest_df, slider_1, fenetre)
st.header("Valeur du portefeuille : " +str(If) + " -- " +str(delta))
st.dataframe(backtest_df)

