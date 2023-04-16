from bs4 import BeautifulSoup
import re
import os
import requests


url = 'http://www.tunisie-annonce.com/AnnoncesImmobilier.asp'
r = requests.get(url)

with open('test.html', 'wb') as f:
    f.write(r.content)

soup = BeautifulSoup(r.content, 'html.parser')

def find_all_links_for_details(soup):
    search = soup.find_all(href=re.compile('DetailsAnnonceImmobilier.asp?.*'))
    links = []
    for link in search:
        links.append(link.get('href'))
    return links
print(find_all_links_for_details(soup))




   
