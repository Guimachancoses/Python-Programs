from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep
import datetime

def login(nav):
    nav.get("https://garbuio.my3cx.com.br/#/login")
    nav.find_element('xpath','//*[@id="content"]/login-component/div/div/form/div/div[1]/input').send_keys('5201')
    nav.find_element('xpath','//*[@id="content"]/login-component/div/div/form/div/div[2]/input').send_keys('L7jWz9qZGs')
    nav.find_element('xpath','//*[@id="content"]/login-component/div/div/form/button').click()
    sleep(3)

def navigate_to_queues(nav):
    nav.find_element('xpath','//*[@id="app-container"]/div[1]/div/div/nav/ul/app-nav-item[2]/a').click()
    sleep(1)

def navigate_to_status_dropdown(nav):
    nav.find_element('xpath','//*[contains(concat( " ", @class, " " ), concat( " ", "mc-select", " " ))]//i').click()

def navigate_to_status_button(nav):
    nav.find_element('xpath','//*[(@id = "btnStatus")]').click()

def change_status(nav):
    sleep(3)
    nav.find_element('xpath','//*[contains(concat( " ", @class, " " ), concat( " ", "ng-valid-parse", " " ))]').click()
    sleep(1)
    nav.find_element('xpath','/html/body/div[1]/div/div/div/div[1]/button').click()
    sleep(1)

def navigate_to_extensions(nav):
    nav.get('https://garbuio.my3cx.com.br/#/app/extensions')
    sleep(3)

def navigate_to_forced_queues(nav):
    navigate_to_queues(nav)
    navigate_to_status_dropdown(nav)
    navigate_to_status_button(nav)
    sleep(15)
    nav.find_element('xpath','/html/body/div[1]/div/div/div/div[2]/select[2]/option[3]').click()
    sleep(1)
    nav.find_element('xpath','/html/body/div[1]/div/div/div/div[1]/button').click()
    sleep(1)
    navigate_to_extensions(nav)
    sleep(15)

def navigate_to_change_status(nav):
    navigate_to_queues(nav)
    navigate_to_status_dropdown(nav)
    navigate_to_status_button(nav)
    change_status(nav)
    sleep(1)
    navigate_to_extensions(nav)
    sleep(3)

# Set navegador - oculto
options = webdriver.ChromeOptions()
options.add_argument("headless")

# Atulizando a versão do DriverChrome
serv = Service(ChromeDriverManager().install())
nav = webdriver.Chrome(service=serv, chrome_options=options)

now = datetime.datetime.now()
current_time = now.strftime("%H:%M:%S")

print(now)

login(nav)

while True:
    if current_time != '13:30:00' and current_time != '07:00:00':
        navigate_to_forced_queues(nav)
    else:
        print(now)
        navigate_to_change_status(nav)
    
    sleep(60)
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
