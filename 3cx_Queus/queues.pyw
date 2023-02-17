# Program to force user stay on queues 3CX.

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep
import datetime

# Set navegador - oculto
options = webdriver.ChromeOptions()
options.add_argument("headless")

# Atulizando a versão do DriverChrome
serv = Service(ChromeDriverManager().install())
nav = webdriver.Chrome(service=serv, chrome_options=options)

now = datetime.datetime.now()
print(now)

# Login in site
nav.get("https://garbuio.my3cx.com.br/#/login")
nav.find_element('xpath','//*[@id="content"]/login-component/div/div/form/div/div[1]/input').send_keys('5201') # Login
nav.find_element('xpath','//*[@id="content"]/login-component/div/div/form/div/div[2]/input').send_keys('L7jWz9qZGs')# Password
nav.find_element('xpath','//*[@id="content"]/login-component/div/div/form/button').click()
sleep(3)
while True:
    # Navegate for force user on the queues:
    nav.find_element('xpath','//*[@id="app-container"]/div[1]/div/div/nav/ul/app-nav-item[2]/a').click()
    sleep(1)
    nav.find_element('xpath','//*[contains(concat( " ", @class, " " ), concat( " ", "mc-select", " " ))]//i').click()
    nav.find_element('xpath','//*[(@id = "btnStatus")]').click()
    sleep(15)
    nav.find_element('xpath','/html/body/div[1]/div/div/div/div[2]/select[2]/option[3]').click()
    sleep(1)
    nav.find_element('xpath','/html/body/div[1]/div/div/div/div[1]/button').click()
    sleep(1)
    nav.get('https://garbuio.my3cx.com.br/#/app/extensions')
    sleep(10)

