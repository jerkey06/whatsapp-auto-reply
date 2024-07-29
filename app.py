import openai
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuración de OpenAI usando variable de entorno
openai.api_key = os.getenv('OPENAI_API_KEY')

# Función para obtener una respuesta de OpenAI
def obtener_respuesta_de_openai(mensaje):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=mensaje,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Configuración de Selenium en Codespaces
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=options)
driver.get('https://web.whatsapp.com')

# Esperar a que el usuario escanee el código QR
print("Escanea el código QR y presiona Enter")
input()

# Función para enviar mensajes
def enviar_mensaje(contacto, mensaje):
    search_box = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
    )
    search_box.clear()
    search_box.send_keys(contacto)
    search_box.send_keys(Keys.ENTER)
    
    message_box = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="6"]'))
    )
    message_box.send_keys(mensaje)
    message_box.send_keys(Keys.ENTER)

# Monitorear mensajes entrantes
def monitorear_mensajes():
    while True:
        try:
            unread_chats = driver.find_elements(By.XPATH, '//span[@class="P6z4j"]')
            for chat in unread_chats:
                chat.click()
                time.sleep(2)
                mensajes = driver.find_elements(By.XPATH, '//div[@class="copyable-text"]')
                ultimo_mensaje = mensajes[-1].text
                respuesta = obtener_respuesta_de_openai(ultimo_mensaje)
                enviar_mensaje(ultimo_mensaje, respuesta)
                time.sleep(5)
        except Exception as e:
            print(f'Error: {e}')
            time.sleep(5)

monitorear_mensajes()
