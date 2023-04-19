from bs4 import BeautifulSoup
import requests
import re

url="https://www.tayara.tn/ads/c/Immobilier/"
r=requests.get(url)

with open('tayara/test_tayara1.html','wb') as f:
    f.write(r.content)

soup = BeautifulSoup(r.content, 'html.parser')

search = soup.find_all(href=re.compile('item/.*'))
links=[]
for link in search:
    links.append(link.get('href'))
print(links)