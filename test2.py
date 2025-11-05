from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
import time


class Message():
    def __init__(self, user, message):
        self.user = user
        self.message = message

    def __eq__(self, other):
        return self.message == other.message


# Configurar opções do Chrome
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# Abrir WhatsApp Web
driver.get('https://web.whatsapp.com')
driver.execute_script("window.open('','_blank');")
driver.switch_to.window(driver.window_handles[1])

# Abrir Mitsuku Chatbot
driver.get('http://www.square-bear.co.uk/mitsuku/nfchat.htm')
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.TAB)

input("Escolha um chat no WhatsApp e pressione Enter: ")
chatHistory = []
replyQueue = []
firstRun = True

print("Iniciando...")

while True:
    try:
        driver.switch_to.window(driver.window_handles[0])
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "side"))
        )

        messageDiv = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "main"))
        )

        messageList = messageDiv.find_elements(By.CLASS_NAME, "msg")

        newMessages = []
        for message in reversed(messageList):
            try:
                bubbleText = message.find_element(
                    By.CLASS_NAME, "message-chat").find_element(By.CLASS_NAME, "bubble")
                author = "Unknown"
                msgObj = None

                if "has-author" in bubbleText.get_attribute("class"):
                    try:
                        author = bubbleText.find_element(
                            By.CLASS_NAME, "message-author").find_element(By.CLASS_NAME, "emojitext").text
                    except:
                        pass

                try:
                    text_message = bubbleText.find_element(
                        By.CLASS_NAME, "message-text").find_element(By.CLASS_NAME, "emojitext").text
                    if text_message:
                        msgObj = Message(author, text_message)
                except:
                    pass

                if chatHistory and msgObj and msgObj == chatHistory[-1]:
                    break
                elif msgObj:
                    newMessages.append(msgObj)

            except Exception as e:
                continue

        for message in reversed(newMessages):
            chatHistory.append(message)

        for i in range(len(chatHistory)):
            if i > 0 and chatHistory[i].user == "Unknown":
                chatHistory[i].user = chatHistory[i - 1].user

        for message in reversed(newMessages):
            if not firstRun:
                replyQueue.append(message)

        firstRun = False
        if not replyQueue:
            time.sleep(3)
            continue

        driver.switch_to.window(driver.window_handles[1])
        driver.switch_to.default_content()
        driver.switch_to.frame('input')

        textField = driver.find_elements(By.TAG_NAME, "input")[1]
        responses = []

        for message in replyQueue:
            textField.send_keys(message.message[1:] + Keys.ENTER)
            time.sleep(2)
            responseBody = None
            fontTags = driver.find_elements(By.TAG_NAME, "font")

            for tag in fontTags:
                if tag.get_attribute("face") == "Trebuchet MS,Arial" and tag.get_attribute("color") == "#000000":
                    responseBody = tag
                    break

            if responseBody:
                start = responseBody.text.find("Μitsuku")
                end = responseBody.text.find("You", 4)
                firstName = message.user.split(' ')[0]
                resp = responseBody.text[start + 10:end - 2]
                responses.append(f"@{firstName} : {resp}")

        replyQueue = []

        driver.switch_to.window(driver.window_handles[0])
        inputMessage = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[title='Digite uma mensagem']"))
        )

        for response in responses:
            for line in response.split("\n"):
                inputMessage.send_keys(line)
                inputMessage.send_keys(Keys.SHIFT, Keys.ENTER)
            inputMessage.send_keys(Keys.ENTER)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        time.sleep(5)
