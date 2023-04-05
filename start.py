from bs4 import BeautifulSoup
import re
import os
import sys
import time
import json
import requests


url = 'http://www.tunisie-annonce.com/AnnoncesImmobilier.asp?rech_cod_cat=1&rech_cod_rub=&rech_cod_typ=&rech_cod_sou_typ=&rech_cod_pay=TN&rech_cod_reg=&rech_cod_vil=&rech_cod_loc=&rech_prix_min=&rech_prix_max=&rech_surf_min=&rech_surf_max=&rech_age=&rech_photo=&rech_typ_cli=&rech_order_by=31&rech_page_num=2'
r = requests.get(url, allow_redirects=True)

#print(r.content)
with open('test.html', 'wb') as f:
    f.write(r.content)
    # i want to get the tr which class contains Tableau 1

soup = BeautifulSoup(r.content, 'html.parser')
#print(soup.prettify())
search = soup.find_all('tr', class_=re.compile('Tableau'))
print(search)
with open('output.html', 'w', encoding='utf-8') as f:
    #html=search.prettify('utf-8')
    f.write(str(search))

   
# print(soup.find_all('tr', class_='Tableau 1')