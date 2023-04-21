from retrieve_details import retrieve_details 
from detail_links import find_all_links_for_details
import requests
from bs4 import BeautifulSoup



url = 'http://www.tunisie-annonce.com/AnnoncesImmobilier.asp'
r = requests.get(url)

soup = BeautifulSoup(r.content,'html.parser')

links = find_all_links_for_details(soup)
links = ['http://www.tunisie-annonce.com/'+link for link in links]

for link in links:
    print(retrieve_details(link))
    print('-------------------')
    print('-------------------')
    