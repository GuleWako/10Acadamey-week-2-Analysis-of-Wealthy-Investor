import streamlit as st
import pandas as pd
import plotly.express as px
# from streamlit_option_menu import option_menu
import os
os.chdir('..')
from src.dbconnection import get_dataFrame_from_database
xdr_data = get_dataFrame_from_database()
st.dataframe(xdr_data)