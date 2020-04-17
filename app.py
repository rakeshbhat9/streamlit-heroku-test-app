import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

@st.cache
def read_in_data():
    d = pd.read_csv('coronavirus-cases.csv', parse_dates=['Specimen date'])
    return d

d = read_in_data()

st.header('''COVID Chart based on UK Gov Data''')
st.markdown(f'''Data as of {str(d['Specimen date'].max()).split(" ")[0]}
    ''')

area_type = st.selectbox(
    'Select Area Type', d['Area type'].unique().tolist())

d = d[d['Area type'] == area_type]

select_area = st.selectbox(
    'Select your area', d['Area name'].unique().tolist())

trigger = st.button('Get chart')


if trigger:
    fil_data = d[(d['Area type'] == area_type) & (d['Area name']==select_area)]
    fig = plt.figure()
    plt.plot(fil_data[['Specimen date', 'Daily lab-confirmed cases',
                                            'Cumulative lab-confirmed cases']].set_index('Specimen date'))
    st.plotly_chart(fig)
    
    st.subheader(f'''Data for last 10 days''')
    st.write(fil_data.head(10))
