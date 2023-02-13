from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep
import pyautogui as pg
import pandas as pd
import csv



# Intall update for browser Chrome
serv = Service(ChromeDriverManager().install())
nav = webdriver.Chrome(service=serv)

# Create archive .csv
with open(r'C:\Users\guilhermemachado\Documents\GitHub\Fontes_workspace\Selenium\Lans_Translate\file.csv','w',newline='',encoding='utf-8') as archive:
    archive_csv = csv.writer(archive,delimiter='\n')
         
    # Login in lansweeper
    nav.get("https://192.168.0.250:82/login.aspx?lo=1")
    sleep(10)
    nav.find_element('xpath','//*[(@id = "NameTextBox")]').send_keys('guilhermemachancoses')
    nav.find_element('xpath','//*[(@id = "PasswordTextBox")]').send_keys('Gui@19=')
    nav.find_element('xpath','//*[@id="LoginButton"]').click()
    sleep(2)

    # Navigate to translate page
    nav.get("https://192.168.0.250:82/Configuration/Translations/Translations.aspx")
    sleep(2)
    nav.find_element('xpath','//*[@id="selectedLanguage"]/option[5]').click()
    sleep(2)

    # Create list with content to be translated
    list_content = ['Column1']

    for i in range(1,1049):
        for element in nav.find_elements('xpath', f'//*[@id="tblTranslations"]/tbody/tr[{i}]/td[3]'):
            list_content.append(str(element.text).strip('"').lstrip().rstrip())

    
    archive_csv.writerow(list_content)
    
# Send for google translate
with open(r'C:\Users\guilhermemachado\Documents\GitHub\Fontes_workspace\Selenium\Lans_Translate\file2.csv','w',newline='',encoding='utf-8') as archive2:
    archive_csv2 = csv.writer(archive2,delimiter='\n')

    # Import table.csv
    table = pd.read_csv(
        r'C:\Users\guilhermemachado\Documents\GitHub\Fontes_workspace\Selenium\Lans_Translate\file.csv'
        , encoding='utf-8'
        , sep=';'
        )
    
    list_translate = ['Column1']
    
    for line in table.index:
        name = table.loc[line,'Column1']
    
        # Using Bs4 for transtations
        nav.get('https://translate.google.com.br/?hl=pt-BR&sl=en&tl=pt&op=translate')
        nav.find_element('xpath','//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea').send_keys(f'{name}')
        sleep(15)
        span = nav.find_element('xpath','//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div/div[8]/div[1]/div[1]/span[1]')
        list_translate.append(str(span.text).strip('"').lstrip().rstrip())
        
    archive_csv2.writerow(list_translate)
        
# Back to site lansweeper and paste the translation
nav.get("https://192.168.0.250:82/Configuration/Translations/Translations.aspx")
sleep(2)
nav.find_element('xpath','//*[@id="selectedLanguage"]/option[5]').click()
sleep(2)
table2 = pd.read_csv(
        r'C:\Users\guilhermemachado\Documents\GitHub\Fontes_workspace\Selenium\Lans_Translate\file2.csv'
        , encoding='utf-8'
        , sep=';'
        )
id=1
for linet2 in table2.index:
    name = table2.loc[linet2,'Column1']   
    # id=id
    nav.find_element('xpath', f'//*[@id="tblTranslations"]/tbody/tr[{id}]/td[4]').click()
    sleep(1)
    nav.find_element('xpath', f'//*[@id="tblTranslations"]/tbody/tr[{id}]/td[4]/form/input').send_keys(f'{name}')
    id+=1
    sleep(1)
    pg.press('enter')



