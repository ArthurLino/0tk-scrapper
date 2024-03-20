from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from enum import Enum

import time


class ScrapperModes(Enum):
    CEP = "cep"
    NEIGHBOURHOOD = "neighbourhood"


class Scrapper:

    def __init__(self, mode, uf, city, locality):
        self.driver = None
        self.modes = {
            "cep": "https://www2.correios.com.br/sistemas/buscacep/buscaEndereco.cfm",
            "neighbourhood": "https://buscacepinter.correios.com.br/app/logradouro_bairro/index.php",
        }
        self.current_mode, self.inputs = self.setup_scrapper_mode(mode.value)
        self.scrap_params = dict(zip(self.inputs, [uf, city, locality]))
        print(self.current_mode)

    def setup_scrapper_mode(self, selected_mode):
        input_ids_by_mode = {
            "cep": ["cep"],
            "neighbourhood": ["uf", "localidade", "bairro", "javascript:pesquisarPróximo"],
        }

        return self.modes[selected_mode], input_ids_by_mode[selected_mode]

    def start_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.current_mode)

    def fetch(self):
        self.start_driver()
        d = self.driver

        if self.current_mode == self.modes["neighbourhood"]:

            for form_inputs in self.inputs[:-1]:
                current_input = d.find_element(By.ID, form_inputs)
                current_input.send_keys(self.scrap_params[form_inputs])

            d.find_element(By.ID, 'btn_pesquisar').send_keys(Keys.ENTER)

            response = []
            has_next_page = True

            while has_next_page:

                time.sleep(.5)

                trs = d.find_elements(By.TAG_NAME, 'tr')

                for tr in trs[1:-2]:

                    sub_address = tr.find_elements(By.XPATH, '*')[1].text
                    if len(tr.find_elements(By.XPATH, '*')[0].text.split(" ", 1)[1].split("(", 1)) > 1:
                        sub_address = tr.find_elements(By.XPATH, '*')[0].text.split(" ", 1)[1].split("(", 1)[1][:-1]

                    new_address = {
                        "tipo_de_endereco": tr.find_elements(By.XPATH, '*')[0].text.split(" ", 1)[0],
                        "endereco": tr.find_elements(By.XPATH, '*')[0].text.split(" ", 1)[1].split("(", 1)[0],
                        "bairro": tr.find_elements(By.XPATH, '*')[1].text,
                        "cep": tr.find_elements(By.XPATH, '*')[-1].text,
                        "sub_endereco": sub_address,
                    }

                    response.append(new_address)
                    d.implicitly_wait(10)
                    ActionChains(d).move_to_element(tr)

                '''response, can_get_more = self.get_data()
                if can_get_more:
                    self.get_data(data=response)'''

                if d.find_element(By.XPATH, '/html/body/main/form/div[1]/div[2]/div/div[3]/div/a[2]').text == "Próximo":
                    d.find_element(By.XPATH, '/html/body/main/form/div[1]/div[2]/div/div[3]/div/a[2]').send_keys(Keys.ENTER)
                    has_next_page = True
                else:
                    has_next_page = False

            return response
