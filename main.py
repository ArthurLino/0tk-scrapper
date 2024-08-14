import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from subprocess import Popen

import pandas as pd
import time as tm


def scrap(scraping_driver, existing_table_data=None):

    if existing_table_data is None:
        print("There is no existing data.")
        print("Creating new empty list.")
        existing_table_data = list()

    print("Starting to scrap, please wait.")
    table_data = existing_table_data

    table_body = scraping_driver.find_element(By.TAG_NAME, "tbody")
    table_rows = table_body.find_elements(By.TAG_NAME, "tr")

    for row in table_rows:

        row_cells = row.find_elements(By.TAG_NAME, "td")
        row_content = [cell.text for cell in row_cells]

        address, neighbourhood, city_and_uf, cep = row_content[0], row_content[1], row_content[2], row_content[3]

        if address.find("(") >= 0:
            address, neighbourhood = row_content[0].split("(")
            neighbourhood = neighbourhood.split(")")[0]

        address_type, address_name = address.split(" ")[0], ''.join(address.split(" ", maxsplit=1)[1:])

        row_content = [address_type, address_name, neighbourhood, cep]
        table_data.append(row_content)

    return table_data


chrome_ref = Popen("open_chrome.bat")
stdout, stderr = chrome_ref.communicate()

webdriver_options = Options()
webdriver_options.add_experimental_option("debuggerAddress", "localhost:8989")

driver = webdriver.Chrome(options=webdriver_options)
driver.get("https://buscacepinter.correios.com.br/app/logradouro_bairro/index.php")

start_scraping = input("Are you ready to scrap? S / N:   ").lower()

if start_scraping == "s":

    next_list_of_addresses_button = driver.find_element(By.XPATH, '//*[@id="navegacao-resultado"]/a[2]')
    prev_list_of_addresses_button = driver.find_element(By.XPATH, '//*[@id="navegacao-resultado"]/a[1]')

    data_scraps = list()

    while next_list_of_addresses_button:

        data_scraps = scrap(driver, data_scraps)

        try:

            next_list_of_addresses_button.click()
            wait = WebDriverWait(driver, timeout=10)
            wait.until(
                lambda x: prev_list_of_addresses_button.is_displayed()
            )

        except:

            break

    print("The scraping process has ended. Enjoy your .xlsx :)")
    df_scraps = pd.DataFrame(data_scraps, index=None)
    df_scraps.to_excel("data.xlsx")

driver.close()
chrome_ref.kill()
