# Program to force user stay on queues 3CX.

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep

serv = Service(ChromeDriverManager().install())

nav = webdriver.Chrome(service=serv)


# Login in site
nav.get("https://garbuio.my3cx.com.br/#/login")
nav.find_element('xpath','//*[@id="content"]/login-component/div/div/form/div/div[1]/input').send_keys('---') # Login
nav.find_element('xpath','//*[@id="content"]/login-component/div/div/form/div/div[2]/input').send_keys('------')# Password
nav.find_element('xpath','//*[@id="content"]/login-component/div/div/form/button').click()
sleep(2)
while True:
    # Navegate
    nav.find_element('xpath','//*[@id="app-container"]/div[1]/div/div/nav/ul/app-nav-item[2]/a').click()
    sleep(1)
    nav.find_element('xpath','//*[contains(concat( " ", @class, " " ), concat( " ", "mc-select", " " ))]//i').click()
    nav.find_element('xpath','//*[(@id = "btnStatus")]').click()
    sleep(2)
    nav.find_element('xpath','/html/body/div[1]/div/div/div/div[2]/select[2]/option[3]').click()
    sleep(1)
    nav.find_element('xpath','/html/body/div[1]/div/div/div/div[1]/button').click()
    sleep(1)
    nav.get('https://garbuio.my3cx.com.br/#/app/extensions')
    sleep(2)

