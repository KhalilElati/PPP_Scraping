from bs4 import BeautifulSoup
import requests


    
url="https://www.tayara.tn/item/location_S2_haut_standing_borj_louzir_prs_MG_643cc499a4cb3b2e7a3e66f9/"
r=requests.get(url)

with open('tayara/test_tayara.html','wb') as f:
    f.write(r.content)
    
soup = BeautifulSoup(r.content, 'html.parser')

#values
ourput1=soup.find_all('span',class_='text-gray-700 text-xs font-medium')
#headers
output2=soup.find_all('span',class_='text-gray-600 text-3xs font-light')

output={}

output['titre']=soup.find('h1',class_='text-gray-700 font-bold text-2xl font-arabic').text

for elemnt,header in  zip(ourput1,output2):
    output[header.text]=elemnt.text
    
print(output)
