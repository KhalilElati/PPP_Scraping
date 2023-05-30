from bs4 import BeautifulSoup
import requests
import re
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

#Initialize cities and delegations dictionary
villes=dict()
villes["Zaghouan"]=["Zaghouen", "Zaghouan", "Saouaf", "Ez Zeriba", "En Nadhour", "El Fahs", "Bir Mchergua"]
villes["Tozeur"] =["Tozeur","Tameghza","Nefta","Hazoua","Degache"] 
villes["Tataouine"] = ["Tataouine Sud", "Tataouine Nord", "Tataouine", "Smâr", "Remada","Dehiba", "Bir Lahmar"]
villes["Kébili"]=["Souk Lahad","Kébili Sud","Kébili Nord","Kébili","Faouar","Douz Sud","Douz Nord","Autres Villes"]
villes["Béja"]=["Téboursouk","Thibar","Testour","Nefza","Medjez El Bab","Goubellat","El Ksar","Béja Sud","Béja Nord","Béja","Autres Villes","Amdoun"]
villes["Ariana"]=["Les Jardins El Menzah 2","Sidi Thabet","Riadh Andalous","Raoued","Nouvelle Ariana","Mnihla","Ariana","Ariana Essoughra","Ariana Ville","Autres Villes","Borj Louzir","Charguia 1","Charguia 2","Chotrana","Chotrana 1","Chotrana 3","Chotrana 2","Cite Ennkhilet","Cité Ennasr 1","Cité Ennasr 2","Cité Hedi Nouira","Dar Fadhal","El Menzah 5","El Menzah 6","El Menzah 7","El Menzah 8","Ennasr","Ettadhamen","Ghazela","Jardins El Menzah","Kalâat Andalous","La Soukra","Les Jardins El Menzah 1"]
villes["Ben Arous"]=["Sidi Rezig","Radès","Mégrine","Mornag","Mohamedia","Medina Jedida","Hammam Lif","Hammam Chott","Fouchana","Ezzahra","El Mourouj 6","El Mourouj 5","El Mourouj 4","El Mourouj 3","El Mourouj 1","El Mourouj","Boumhel","Borj Cedria","Ben Arous","Autres Villes"]
villes["Bizerte"]=["Zarzouna","Utique","Autres Villes","Bizerte","Bizerte Nord","Bizerte Sud","Djoumime","El Alia","Ghar El Melh","Ghezala","Mateur","Menzel Bourguiba","Menzel Jemil","Ras Jebel","Sejenane","Tinja"]
villes["Gabès"]=["Nouvelle Matmata","Métouia","Matmata","Mareth","Ghanouch","Gabès Sud","Gabès Ouest","Gabès Médina","Gabès","El Hamma","Autres Villes"]
villes["Gafsa"]=["Sidi Aïch","Sened","Redeyef","Oum El Araies","Métlaoui","Mdhila","Gafsa","Gafsa Sud","Gafsa Nord","El Ksar","El Guettar","Belkhir","Autres Villes"]
villes["Jendouba"]=["Tabarka","Oued Meliz","Jendouba Nord","Jendouba","Ghardimaou","Fernana","Bou Salem","Balta Bou Aouane","Autres Villes","Ain Draham"]
villes["Kairouan"]=["Sbikha","Nasrallah","Kairouan Sud","Kairouan Nord","Kairouan","Hajeb El Ayoun","Haffouz","El Ouslatia","El Alâa","Echrarda","Chebika","Bouhajla","Autres Villes"]
villes["Kasserine"]=["Thala","Sbiba","Sbeïtla","Majel Bel Abbès","Kasserine Sud","Kasserine Nord","Kasserine","Hidra","Hassi Ferid","Fériana","Foussana","El Ayoun","Ezzouhour","Djedeliane","Autres Villes"]
villes["La Manouba"]=["Tebourba","Oued Ellil","Mornaguia","Menzel El Habib","Manouba Ville","La Manouba","El Battan","Douar Hicher","Djedeida","Denden","Borj El Amri","Autres Villes"]
villes["Le Kef"]=["Tajerouine","Nebeur","Sakiet Sidi Youssef","Le Kef","Kef Ouest","Kef Est","Kalâat Snan","Kalâat Khasbah","Es Sers","El Ksour","Djerissa","Dahmani","Autres Villes"]
villes["Mahdia"]=["Sidi Alouane","Ouled Chamekh","Melloulèche","Mahdia","Ksour Essef","Hebira","Essouassi","El Jem","Chorbane","Chebba","Bou Merdès","Autres Villes"]
villes["Monastier"]=["Zéramdine","Téboulba","Sayada Lamta Bou Hajar","Sahline","Ouerdanine","Monastir","Moknine","Ksibet El Médiouni","Ksar Hellal","Jemmal","Beni Hassen","Bembla","Bekalta","Autres Villes"]
villes["Médenine"]=["Zarzis","Sidi Makhloulf","Médenine Sud","Médenine Nord","Médenine","Djerba Midoun","Djerba Houmt Souk","Djerba Ajim","Beni Khedech","Ben Gardane","Autres Villes"]
villes["Tunis"] = ["Tunis Belvedere", "Tunis", "Séjoumi", "Sidi Hassine", "Sidi El Béchir", "Sidi Daoud", "Sidi Bou Said", "Médina", "Mutuelleville", "Monfleury", "Montplaisir", "Menzah", "Manar", "Le Kram", "Le Bardo", "Lac 2", "Lac 1", "La Marsa", "La Goulette", "L Aouina", "Ksar Said", "Kheireddine Pacha", "Khaznadar", "Jardins De Carthage", "Hraïria", "Gammarth", "Ezzouhour", "Ettahrir", "El Ouardia", "El Omrane Supérieur", "El Omrane", "El Menzah 9", "El Menzah 4", "El Menzah 1", "El Manar 2", "El Manar 1", "El Kabaria", "Djebel Jelloud", "Cité Olympique", "Cité El Khadra", "Centre Ville Lafayette", "Centre Urbain Nord", "Carthage", "Bellevue", "Bab Souika", "Autres Villes", "Ain Zaghouen", "Ain Zaghouan Sud", "Ain Zaghouan Nord", "Agba"]
villes["Sousse"] = ["Zaouit Ksibat Thrayett", "Sousse Sidi Abdelhamid", "Sousse Riadh", "Sousse Médina", "Sousse Jawhara", "Sousse", "Sidi El Héni", "Sidi Bou Ali", "Sahloul", "M Saken", "Kondar", "Kantaoui", "Khzema", "Kalaâ Sghira", "Kalaâ Kebira", "Hergla", "Hammam Sousse", "Enfidha", "Bouficha", "Chatt mariem", "Akouda"]
villes["Siliana"] = ["Siliana Sud","Siliana Nord", "Sidi Bou Rouis", "Rouhia", "Makthar", "Kesra", "Gaâfour", "El Krib", "El Aroussa", "Bargou", "Bou Arada"]
villes["Sidi Bouzid"] = ["Souk Jedid","Sidi Bouzid Ouest", "Sidi Bouzid Est", "Sidi Bouzid", "Sidi Ali Ben Aoun", "Regueb", "Ouled Haffouz", "Mezzouna", "Menzel Bouzaiane", "Jilma", "Meknassy", "Cebbala Ouled Asker", "Bir El Hafey"]
villes["Sfax"] = ["Sfax Ouest", "Sfax Nord", "Sfax Est", "Sfax", "Sakiet Ezzit", "Sakiet Eddaïer", "Route de l'aéroport", "Route de GABES", "Route Tunis", "Route TANIOUR", "Route Soukra", "Route SOKRA", "Route Menzel Chaker", "Route Mehdia", "Route MHARZA", "Route MANZEL CHAKER", "Route GREMDA", "Route El Ain", "Route El Afrane", "ROUTE SALTANIA", "Menzel Chaker", "Mahrès", "Kerkennah", "Jebiniana", "Ghraiba", "El Hencha", "El Amra", "Bir Ali Ben Khalifa", "Agareb"]

for ville in villes:
    #reset data list
    data=[]
    for deleg in villes[ville]:
        #reset links list
        links=[]
        url="https://www.tayara.tn/ads/c/Immobilier/l/"+ville.replace(" ","%20")+"/"+deleg.replace(" ","%20") #specific url for each delegation
        webdriver_path= r'C:\Users\Moham\Documents\RT3\S2\PPP\PPP_Scraping\chromedriver.exe'
        service = Service(webdriver_path)
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        #scrolling down to load all items
        while True:
            driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);') 
            time.sleep(10)  # Adjust the delay based on the website's behavior
            if driver.execute_script('return window.pageYOffset + window.innerHeight >= document.documentElement.scrollHeight'):
                break
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        #finding the element to start scraping after it
        target= soup.find('h1',class_="text-2xl font-bold text-gray-700",string="Immobilier à "+deleg)
        for sibling in target.previous_siblings:
            sibling.extract()
        #finding item links
        search=soup.find_all(href=re.compile('item/.*'))
        for link in search:
            links.append(link.get('href'))
        #scraping each item 
        for link in links:
            url="https://www.tayara.tn"+link
            r=requests.get(url)
            with open('test_tayara.html','wb') as f:
                f.write(r.content)
            soup = BeautifulSoup(r.content, 'html.parser')
            output1=soup.find_all('span',class_='text-gray-700 text-xs font-medium')
            if output1==[]:
                continue
            location=soup.find('div',class_='flex items-center space-x-1 mb-1').span.text.split(',')[0]
            type=output1[0].text
            superficie=output1[1].text
            salles_de_bains=output1[2].text
            chambres=output1[3].text
            prix=soup.find('data',class_="text-red-600 font-bold font-arabic text-2xl")['value']
            description=soup.find('h1',class_='text-gray-700 font-bold text-2xl font-arabic').text
            temp={
                'offer_type':type,
                'ville':ville,
                'delegation':deleg,
                'superficie' : superficie,
                'Salles de bains':salles_de_bains,
                'Chambres':chambres,
                'Prix':prix ,
                'Description': description
            }
            data.append(temp)
            print(temp)
    #dumping data in json file for each city        
    with open(ville+".json", "w",encoding="utf-8") as f:
        json.dump(data, f)