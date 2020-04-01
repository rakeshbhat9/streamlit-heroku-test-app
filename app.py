import pandas as pd
import streamlit as st

@st.cache
def get_data():
    d = pd.read_html('https://simple.wikipedia.org/wiki/List_of_countries')[0]
    d = d.iloc[2:,:]
    d.reset_index(drop=True,inplace=True)
    return d

st.title("Sample Streamlit app to test Heroku Deployment")
st.info("This is a sample app to test heroku deployment from github")    

with st.spinner("Extracting source data..."):
    data = get_data()
    st.write(data)