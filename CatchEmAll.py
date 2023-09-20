# pip install BeautifulSoup4, pandas, requests, openpyxl

from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_National_Pokédex_number'
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, 'html.parser')
tables_list = soup.findAll('table', class_="roundy")

main_df = pd.DataFrame()

for table in range(len(tables_list)):
    n = table
    table = tables_list[n]
    data = []
    for row in table.find_all('tr'):
        cols = [col.text.strip() for col in row.find_all(['th', 'td'])]
        data.append(cols)
    cols = data[0][0:3] + ['Type1', 'Type2']
    df = pd.DataFrame(data[1:], columns=cols)
    if n == 0:
        main_df = df
    else:
        main_df = pd.concat([main_df, df], ignore_index=True)

main_df = main_df[['Ndex', 'Pokémon', 'Type1', 'Type2']]
main_df = main_df.dropna(how='any', axis=0, inplace=False)
main_df.to_excel('Pokemon_List.xlsx', index=False)


