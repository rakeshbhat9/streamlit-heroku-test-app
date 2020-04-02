import requests
import re
import time

import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

def calc_total_review_pages(asin):
    
    base_url=f"https://www.amazon.co.uk/review/{asin}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    page=requests.get(base_url,headers=header)
    if page.status_code==200:
        soup=BeautifulSoup(page.content)
        total_page_count_text = soup.find("span",{'data-hook':"cr-filter-info-review-count"}).text
        
        patt ="(\d*) reviews"
        reg = re.compile(patt)
        last_page = reg.findall(total_page_count_text)[0]
        last_page_int = round(int(last_page)/10)
        links = [base_url+'&pageNumber='+str(x) for x in range(1,last_page_int+1)]
        return links
        
    else:
        return "Something went wrong."

def scrape_reviews(links):
    
    print(f'''There are total of {len(links)} links to source data from.''')
    count = 0

    reviews = []
    place = []
    date = []

    for url in links:
        count += 1
        if count == 5:
            count = 0
            print("Sleeping for 10 secs")
            time.sleep(10)
            
        print(url)
        page=requests.get(url,headers=header)
        if page.status_code==200:
            soup=BeautifulSoup(page.content)
            temp_reviews = [i.text for i in soup.findAll("span",{'data-hook':"review-body"})]
            temp_reviews = [x.replace("\n","") for x in temp_reviews]
            reviews.extend(temp_reviews)
            
            place_patt = 'in the (\w*\s?\w*) on'
            place_reg = re.compile(place_patt)
            temp_place = [place_reg.findall(i.text)[0] for i in soup.findAll("span",{'data-hook':"review-date"})]
            place.extend(temp_place)

            date_patt = 'on (\w*\s\w*\s\d*)'
            date_reg = re.compile(date_patt)
            temp_date = [date_reg.findall(i.text)[0] for i in soup.findAll("span",{'data-hook':"review-date"})]
            date.extend(temp_date)
        else:
            return "Error"

        data = zip(date,place,reviews)
        df = pd.DataFrame(data,columns=['date','place','review'])
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values('date',ascending=False,inplace=True)
        df.reset_index(inplace=True,drop=True)
    
    return df


st.title("Sample Streamlit app to test Heroku Deployment")
st.info("This is a sample app which scrapes review from Amazon based on ASIN id provided")
st.markdown(''' 
            To Do: \n
                1. Handle products with no review.
                2. Add sentiment analysis, thats the whole point.
            ''')

asin = st.text_input('Please input the asin code:')

if asin:
    links = calc_total_review_pages(asin)
    st.write(f'Please see the data below for ASIN {asin}')
    with st.spinner("Extracting data from Amazon..."):
        data = scrape_reviews(links)
        st.table(data.style.set_properties(**{'text-align': 'left'}))
        
