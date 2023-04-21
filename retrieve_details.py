from bs4 import BeautifulSoup
import re
import os
import requests

def retrieve_details(url):
    
    # url = 'http://www.tunisie-annonce.com/DetailsAnnonceImmobilier.asp?cod_ann=3194091'


    # with open('test.html', 'wb') as f:
    #     f.write(r.content)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    output=soup.find_all('td',class_='da_field_text')
    elements=[]
    for element in output:
        # print(element.text)
        elements.append(element.text)

    # print(elements)

    offer_type, estate_type =re.search(r'.*  > (?P<offer_type>.*)  > (?P<estate_type>.*)',elements[0].replace(' ',' ')).groups()
    state, city , address =re.search(r'.*  > (?P<state>.*)  > (?P<city>.*)  > (?P<address>.*)',elements[1].replace(' ',' ')).groups()
    precise_address = elements[2]
    surface_in_meters = re.search(r'(?P<surface_in_meters>\d+)',elements[3]).group('surface_in_meters')
    price_in_TND = re.search(r'(?P<price_in_TND>\d+)',elements[4].replace(' ','')).group('price_in_TND')
    description_text = elements[5]
    offer_date = elements[7]

    result= {
        'offer_type':offer_type,
        'estate_type':estate_type,
        'state':state,
        'city':city,
        'address':address,
        'precise_address':precise_address,
        'surface':surface_in_meters,
        'price_in_TND':price_in_TND,
        'description_text':description_text,
        'offer_date':offer_date

    }
    return(result)
    # print(result)










   
