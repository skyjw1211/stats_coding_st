import streamlit as st
import os, sys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
import pandas as pd

base_url = sheet_url = st.secrets["private_url"]

@st.experimental_singleton
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.9/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

_ = installff()

@st.cache_data
def crawling():
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    browser = webdriver.Firefox(options=opts)

    browser.get(base_url)

    data = browser.find_elements(By.CSS_SELECTOR, '.count-by-user-body')

    data_split = list(map(lambda x: x.split(), data[0].text.split('\n')))
    column_name = ['rank', 'user_id', 'email', 'Editing', 'Completion', 'Total']
    df = pd.DataFrame(data_split, columns = column_name)

    return df

df = crawling()

# email 입력창
if st.button('Update!'):
    df = crawling()

email = st.text_input('Email Addr', '')

if st.button('Enter Email'):
    # email로 query, query한 df 보여주기
    temp_df = df.loc[df['email'] == email][['rank','email', 'Editing', 'Completion', 'Total']]
    st.dataframe(temp_df, use_container_width=True)


