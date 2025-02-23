import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
import base64
import numpy as np
import streamlit.components.v1 as components

st.markdown("<h1 style='text-align: center; color: white;'>Coin Afrique Data Scraper!</h1>", unsafe_allow_html=True)

st.markdown("""
 **Source:** [CoinAfrique](https://sn.coinafrique.com/)
""")

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

def load(dataframe, title, key, key1):
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    if st.button(title, key1):
        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
        st.dataframe(dataframe)

def load_chien_data(mul_page):
    df = pd.DataFrame()
    for p_index in range(1, int(mul_page) + 1):
        url = f'https://sn.coinafrique.com/categorie/chiens?page={p_index}'
        res = get(url)
        soup = bs(res.text, 'html.parser')
        containers = soup.find_all('div', class_='col s6 m4 l3')
        data = []
        for container in containers:
            try:
                nom = container.find('p', class_='ad__card-description').text
                prix = container.find('p', class_='ad__card-price').text.replace('CFA', '').replace(' ', '')
                adresse = container.find('p', class_='ad__card-location').text.replace('location_on', '')
                image_lien = container.find('img', class_='ad__card-img')['src']
                dic = {
                    'nom': nom,
                    'prix': prix,
                    'adresse': adresse,
                    'image_lien': image_lien,
                }
                data.append(dic)
            except:
                pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis=0).reset_index(drop=True)
    return df

def load_mouton_data(mul_page):
    df = pd.DataFrame()
    for p_index in range(1, int(mul_page) + 1):
        url = f'https://sn.coinafrique.com/categorie/moutons?page={p_index}'
        res = get(url)
        soup = bs(res.text, 'html.parser')
        containers = soup.find_all('div', class_='col s6 m4 l3')
        data = []
        for container in containers:
            try:
                nom = container.find('p', class_='ad__card-description').text
                prix = container.find('p', class_='ad__card-price').text.replace('CFA', '').replace(' ', '')
                adresse = container.find('p', class_='ad__card-location').text.replace('location_on', '')
                image_lien = container.find('img', class_='ad__card-img')['src']
                dic = {
                    'nom': nom,
                    'prix': prix,
                    'adresse': adresse,
                    'image_lien': image_lien,
                }
                data.append(dic)
            except:
                pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis=0).reset_index(drop=True)
    return df

st.sidebar.header('Préférences')
Pages = st.sidebar.selectbox('Pages', list([int(p) for p in np.arange(1, 20)]))
Choices = st.sidebar.selectbox('Options', ['Scraper avec BeautifulSoup', 'Télécharger les données',  'Remplir le formulaire Kobo','Remplir le formulaire Google Forms'])

add_bg_from_local('background.png')

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css('style.css')

if Choices == 'Scraper avec BeautifulSoup':
    chien_data_mul_pag = load_chien_data(Pages)
    mouton_data_mul_pag = load_mouton_data(Pages)
    
    load(chien_data_mul_pag, 'chien data', '1', '101')
    load(mouton_data_mul_pag, 'mouton data', '2', '102')

elif Choices == 'Télécharger les données': 
    chiens = pd.read_csv('chiens.csv')
    moutons = pd.read_csv('moutons.csv') 

    load(chiens, 'chien data', '1', '101')
    load(moutons, 'mouton data', '2', '102')

elif Choices == 'Remplir le formulaire Kobo':
    components.html("""
    <iframe src=https://ee.kobotoolbox.org/i/XUDAcOMo width="800" height="1100"></iframe>
    """, height=1100, width=800)


else:
    components.html("""
    <iframe src=https://forms.gle/Ysq6HCMWwAd4KqSj6 width="800" height="1100"></iframe>
    """, height=1100, width=800)
