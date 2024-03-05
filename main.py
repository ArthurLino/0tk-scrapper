from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

locais = [
    "Av. Paulo Prado",
    "Av. Ver. José Francisco Damasceno",
    "Bairro Parque Dos Estados",
    "Bairro Terra Nobre",
    "Cond. Santa Isabel",
    "Estrada Atilio Biscuola",
    "Estrada da Boiada",
    "Estrada Miguel Bossi",
    "Estacionamento",
    "Estacionamento Cemitério",
    "Estacionamento Interno da Polícia Civil",
    "Pátio de Balizas das Autos Escolas",
    "Rua Angelo Steck",
    "Rua Antonio Chicalhone",
    "Rua Arthur de Souza Singel",
    "Rua Catarina Calssavara",
    "Rua das Rosas",
    "Rua Francisco Pagotto",
    "Rua Natal Tarallo",
    "Rua Nerina",
    "Rua Nicola Tarallo",
    "Rua Roberto Mazzali",
    "Rua Santo ScarenAe",
    "Rua São Carlos",
    "Rua Treze de Junho",
    "Rua Victorio Finamore"
]

city, state = "LOUVEIRA", "SP"

driver = webdriver.Chrome()
driver.get('https://buscacepinter.correios.com.br/app/localidade_logradouro/index.php')

for l in locais:
    try:
        uf = driver.find_element(By.NAME, "uf")
        uf.send_keys(state)
        local = driver.find_element(By.NAME, 'localidade')
        local.send_keys(city)
        log = driver.find_element(By.NAME, 'logradouro')
        print(f'{l.split(" ", 1)[1]}:')
        log.send_keys(l.split(" ", 1)[1])

        button = driver.find_element(By.ID, 'btn_pesquisar')
        button.send_keys(Keys.ENTER)

        time.sleep(1)

        trs = driver.find_elements(By.TAG_NAME, 'tr')
        for tr in trs[1:-1]:
            print([el.text for el in tr.find_elements(By.XPATH, '*')])

        exit = driver.find_element(By.ID, 'btn_nbusca')
        exit.send_keys(Keys.ENTER)

        time.sleep(1)

    except:
        print('error')
