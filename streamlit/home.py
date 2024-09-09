import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# from streamlit_option_menu import option_menu
import os
os.chdir('..')
from src.dbconnection import get_dataFrame_from_database
xdr_data = get_dataFrame_from_database()


# Set page title
st.title("Telecom Data Analysis")

# Show first few rows of the dataset
st.subheader("Initial Telecom Dataset")
st.write(xdr_data.head())

st.title("Exploratory Data Analysis")
st.subheader("Check datatype of extracted dataset")
dataType_of_Dataset = st.selectbox("Choose a column to view its datatype", xdr_data.columns)

if st.button("View Datatype"):
    st.write(xdr_data[dataType_of_Dataset].dtypes)







