 # -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 15:54:41 2024

@author: TallonCommoditiesINT
"""

import streamlit as st
from xbbg import blp
import datetime as dt
from datetime import datetime
import streamlit_authenticator as stauth
from streamlit_authenticator import Authenticate



st.set_page_config(layout='wide')

passwords_to_hash = ['fashion@123']
hashed_passwords = stauth.Hasher(passwords_to_hash).hash('fashion@123')

import yaml
from yaml.loader import SafeLoader
with open('../config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    
authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)


name = authenticator.login('main')


st.title('Daily Overlook')


# df = pd.read_excel("C:/Users/TallonCommoditiesINT/Desktop/Spread ULSD CIF MED Sept - Nov 24 Analysis.xlsx",sheet_name="Sheet2")
# df = df.set_index('Date', inplace = False)


def live(prod,dt,r):
    try:
        df = blp.bdib(product, dt=dt,ref=r)
    except:
        st.write("Product can not be found on Bloomberg")
    return df

month_ = datetime.now().month
month = datetime.now().replace(month=month_+1).strftime("%B")



st.sidebar.header("Parameters")
st.sidebar.write("_________________________")
rolling = st.sidebar.number_input('Enter Rolling Days',value=22)
st.sidebar.write("_________________________")


tickers = {"Gasoil ICE Futures":"QS Comdty",
           "ICE Brent":"CO Comdty","ICE Brent Spread":"CO_CO Comdty", 
           "ICE WTI":"EN Comdty","ICE WTI Spread":"EN_EN Comdty",
           "Murban Crude Oil":"MUC Comdty", "Gasoil Spreads":"QS_QS Comdty", 
           "Gasoil - Brent Crack":"QS_CO Comdty", "Brent - WTI Spread":"EN_CO Comdty ",
           "Light Sweet Crude WTI":"CL Comdty","Light Sweet Crude WTI Sread":"CL_CL Comdty",
           "Heating Oil":"HO Comdty","Heating Oil Spread":"HO_HO Comdty"}


n = st.sidebar.number_input('Enter Number of Products',value=1)


    # enddate= datetime.today().strftime("%Y-%m-%d")
    # startdate_ = datetime.today()-dt.timedelta(days=600)
    # startdate =startdate_.strftime("%Y-%m-%d")
data=[]
data_live=[]
for i in range(0,n):
    product = st.sidebar.text_input("Product {}".format(i+1), "CO1 Comdty")
    ref = st.sidebar.text_input("Reference of Product {}".format(i+1), "CO1 Comdty")
    d1 = st.sidebar.date_input("Select Start Date {}".format(i+1),key="{}".format(i), value=datetime.today()-dt.timedelta(days=600))
    d2 = st.sidebar.date_input("Select End Date{}".format(i+1),key="k{}".format(i), value=datetime.today())
    st.sidebar.write("_________________________")
    try:
        data = blp.bdh(product,flds=['open','high','low','Last_Price'],start_date=d1.strftime("%Y%m%d"), end_date=d2.strftime("%Y%m%d"))
    except:
        st.write("Product can not be found on Bloomberg")
    data_live = live(product,d2.strftime("%Y%m%d"),ref)
    
    st.dataframe(data)
    st.dataframe(data_live)
            
    