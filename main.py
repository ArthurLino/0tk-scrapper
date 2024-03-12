from scrapper import Scrapper, ScrapperModes

import pandas as pd

from tkinter import ttk
from tkinter import *


def create_new_scrapper(u, c, l):
    print("creating new scrapper...")
    s = Scrapper(ScrapperModes.NEIGHBOURHOOD, u, c, l)
    print("starting to scrap")
    s.fetch()
    print("scrapping finished")


root = Tk()
root.title("thornscrub | informações de ruas - correios")

mainframe = ttk.Frame(root,)

mainframe.grid(column=0, row=0, columnspan=8, rowspan=8)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

uf_label = ttk.Label(mainframe, text="UF:")
city_label = ttk.Label(mainframe, text="Cidade:")
locality_label = ttk.Label(mainframe, text="Bairro: ")

uf_entry = ttk.Entry(mainframe)
city_entry = ttk.Entry(mainframe)
locality_entry = ttk.Entry(mainframe)

uf_label.grid(column=1, row=1, padx=4, pady=4 )
city_label.grid(column=3, row=1, padx=4, pady=4)
locality_label.grid(column=1, row=2, padx=4, pady=4, sticky='w')

uf_entry.grid(column=2, row=1, padx=4, pady=4)
city_entry.grid(column=4, row=1, padx=4, pady=4)
locality_entry.grid(column=2, columnspan=3, row=2, padx=4, pady=4)

btn_search = ttk.Button(mainframe, text="Pesquisar", command=lambda: create_new_scrapper(uf_entry.get(), city_entry.get(), locality_entry.get()))
btn_search.grid(column=2, columnspan=2, row=7, padx=4, pady=4)

root.mainloop()

'''addresses = s.fetch()'''

"""
df_of_addresses = pd.DataFrame.from_records(addresses)
'''df_of_addresses.to_csv("prototype.csv", index=False)
df_of_addresses.to_excel("prototype.xlsx")'''

sorted_addresses = sorted(addresses, key=lambda d: d["sub_endereco"])

df_by_sub_addresses = pd.DataFrame.from_records(sorted_addresses)
'''df_by_sub_addresses.to_csv("prototype_s.csv", index=False)
df_by_sub_addresses.to_excel("prototype_s.xlsx")'''"""
