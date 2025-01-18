import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import google.generativeai as genai

url = 'https://www.suno.com.br/noticias/'

conteudo_site = requests.get(
    url,
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}
).text

soup = BeautifulSoup(conteudo_site, 'html.parser')

news = []

for a_tag in soup.find_all('a', href=True):

    title = a_tag.get_text(strip=True)
    link = a_tag['href']
    
    if title and len(title) >= 30:

        if not link.startswith('http'):
            link = f'https://www.suno.com.br{link}'
        
        news.append({'Title': title, 'URL': link})

df_news = pd.DataFrame(news)

df_news = df_news.drop_duplicates(subset='Title', keep='first').reset_index(drop=True)

data_hoje = datetime.now().date().strftime('%d/%m/%Y')

print('-'*60, '\n', f'Notícias via Suno - {data_hoje}', '\n', '-'*60)

for id, row in df_news.iterrows():
    
    print(row['Title'])
    print('Link:', row['URL'])
    print(' ')

list_news = list(df_news['Title'])

genai.configure(api_key="...")

model = genai.GenerativeModel("gemini-1.5-flash")

prompt = f"Dadas os seguintes títulos de notícias, por favor, forneça um resumo geral separado por: MACROECONOMIA; AÇÕES; FIIS; INTERNACIONAL; DEMAIS".join(list_news)

response = model.generate_content(prompt)

print('-'*60, '\n', 'Resumo do dia via Google Gemini 1.5 Flash', '\n', '-'*60)

print(response.text)