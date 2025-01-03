from bs4 import BeautifulSoup
import requests
import re
import csv
import json


url="https://www.tayara.tn/ads/c/Immobilier/"
r=requests.get(url)

with open('tayara/test_tayara1.html','wb') as f:
    f.write(r.content)

soup = BeautifulSoup(r.content, 'html.parser')

#removing ad content from the page
target= soup.find('h1',class_="text-2xl font-bold text-gray-700",string="Immobilier")
for sibling in target.previous_siblings:
    sibling.extract()
#finding item links
search=soup.find_all(href=re.compile('item/.*'))
links=[]
for link in search:
    links.append(link.get('href'))
del links[0]

data=[]

for link in links:
    url2="https://www.tayara.tn"+link
    
    r2=requests.get(url2)
    with open('tayara/test_tayara2.html','wb') as f:
        f.write(r2.content)
    soup2 = BeautifulSoup(r2.content, 'html.parser')
    output1=soup2.find_all('span',class_='text-gray-700 text-xs font-medium')
    if output1==[]:
        continue
    type=output1[0].text
    superficie=output1[1].text
    salles_de_bains=output1[2].text
    chambres=output1[3].text
    prix=soup2.find('data',class_="text-red-600 font-bold font-arabic text-2xl")['value']
    description=soup2.find('h1',class_='text-gray-700 font-bold text-2xl font-arabic').text
    temp={
        'type':type,
        'superficie' : superficie,
        'Salles de bains':salles_de_bains,
        'Chambres':chambres,
        'Prix':prix ,
        'Description': description
    }
    data.append(temp)
    
    
    
    
    #extracting the type, superficie, salles de bains and chambres
    """ for element in output1:
        temp.append(element.text)
    #exctracting the price
    prix=soup2.find('data',class_="text-red-600 font-bold font-arabic text-2xl")['value']
    temp.append(prix)
    #extracting the description
    temp.append(soup2.find('h1',class_='text-gray-700 font-bold text-2xl font-arabic').text)
    data.append(temp)
    

with open('tayara/output.csv', mode='w', newline='',encoding='utf-8') as file:
    writer = csv.writer(file)
    for row in data:
        writer.writerow(row) """
        
        
with open("tayara/data.json", "w",encoding="utf-8") as f:
    # write JSON data to file
    json.dump(data, f) 
