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

# Login in lansweeper
nav.get("https://192.168.0.250:82/login.aspx?lo=1")
sleep(10)
nav.find_element('xpath','//*[(@id = "NameTextBox")]').send_keys('guilhermemachancoses')
nav.find_element('xpath','//*[(@id = "PasswordTextBox")]').send_keys('Gui@19=')
nav.find_element('xpath','//*[@id="LoginButton"]').click()
sleep(2)

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

id=499
for linet2 in table2.index:
    name = table2.loc[linet2,'Column1']   
    # id=id
    nav.find_element('xpath', f'//*[@id="tblTranslations"]/tbody/tr[{id}]/td[4]').click()
    sleep(1)
    nav.find_element('xpath', f'//*[@id="tblTranslations"]/tbody/tr[{id}]/td[4]/form/input').send_keys(f'{name}')
    id+=1
    sleep(1)
    pg.press('enter')
