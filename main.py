import os
import csv
import tkinter.filedialog as fd

from PIL import ImageTk, Image as Img

from scrapper import Scrapper, ScrapperModes

import pandas as pd

from tkinter import ttk
from tkinter import *

global last_addresses


def create_new_scrapper():
    """
    Create a new Scrapper using the values of the GUI entries as parameters of the query.
    Proceeds to show the scrapper creation and run logs.
    """

    uf, city, local = uf_entry.get(), city_entry.get(), locality_entry.get()
    scrapper = Scrapper(ScrapperModes.NEIGHBOURHOOD, uf, city, local)

    tree_view_log = treeview_process_screen.insert(parent="", index='end', text="Criando uma nova busca...")
    treeview_process_screen.item(tree_view_log, open=TRUE)

    treeview_process_screen.insert(parent=tree_view_log, index=END, text="Procurando informações...")

    return root.after(1, lambda: fetch_with_scrapper(scrapper, tree_view_log))


def fetch_with_scrapper(s, logger):
    """
    Uses a scrapper to fetch the list of addresses from https://buscacepinter.correios.com.br.
    Finalizes the fetching process showing a log.
    """

    response = s.fetch()
    root.after(100)
    treeview_process_screen.insert(parent=logger, index=END, text="Processo finalizado.")
    treeview_process_screen.insert(parent=logger, index=END, text="Arquivos disponíveis para download.")
    download_btn.state(['!disabled'])

    global last_addresses
    last_addresses = response


def create_files():
    directory = fd.askdirectory()

    sorted_addresses = sorted(last_addresses, key=lambda d: d["sub_endereco"])

    df_by_sub_addresses = pd.DataFrame.from_records(sorted_addresses)
    df_by_sub_addresses.to_csv(f"{directory}/prototype_s.csv", index=False)
    # df_by_sub_addresses.to_excel(f"{directory}/prototype_s.xlsx")

    with open(f"{directory}/prototype_s.csv", 'r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)

        newfile = f"{directory}/prototype_s.txt"

        for line in csv_reader:
            with open(newfile, 'w+') as new_txt:
                txt_writer = csv.writer(new_txt, delimiter='\t')
                txt_writer.writerow(line)


root = Tk()
root.title("otk-crawler | informações de ruas - correios")
root.geometry('400x360')
root.maxsize(400, 360)
root.resizable(False, False)

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, columnspan=8, rowspan=8, sticky=(N, S, W, E), padx=8, pady=8)

uf_label = ttk.Label(mainframe, text="UF:")
city_label = ttk.Label(mainframe, text="Cidade:")
locality_label = ttk.Label(mainframe, text="Bairro: ")

uf_entry = ttk.Entry(mainframe)
city_entry = ttk.Entry(mainframe)
locality_entry = ttk.Entry(mainframe)

treeview_process_screen = ttk.Treeview(mainframe, show="tree")
treeview_process_screen.state(['readonly'])

uf_label.grid(column=1, row=1, sticky=('N', 'W'))
city_label.grid(column=3, row=1, sticky=(N, W), padx=8)
locality_label.grid(column=1, row=2, sticky=(N, W, E, S))

uf_entry.grid(column=2, row=1, sticky=(N, W))
city_entry.grid(column=4, row=1, sticky=(N, W))
locality_entry.grid(column=2, columnspan=2, row=2, sticky=(W, E))

treeview_process_screen.grid(column=1, row=6, rowspan=2, columnspan=3, sticky=(N, S, W, E))

btn_search = ttk.Button(mainframe, text="Pesquisar", command=lambda: create_new_scrapper())
btn_search.grid(column=1, columnspan=4, row=3, sticky=(N, S, W, E), pady=12)

download_btn = ttk.Button(mainframe, text="Baixar Resultado", command=lambda: create_files())
download_btn.state(['disabled'])
download_btn.grid(column=4, columnspan=1, row=6, sticky=(N, S, W, E), padx=(16, 0), pady=8)

reset_icon = ImageTk.PhotoImage(Img.open('./assets/reset.png'), ('16', '16'))
new_query_btn = ttk.Button(mainframe, image=reset_icon, compound='image')
new_query_btn.grid(column=4, row=2, sticky=(W, E), padx=4, pady=(4, 6))

uf_entry.focus()

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=8)
mainframe.columnconfigure(2, weight=8)
mainframe.columnconfigure(3, weight=5)
mainframe.columnconfigure(4, weight=5)
mainframe.rowconfigure(1, weight=1, pad=12)
mainframe.rowconfigure(2, weight=1, pad=12)
mainframe.rowconfigure(3, weight=1, pad=12)
mainframe.rowconfigure(4, weight=1, pad=12)
mainframe.rowconfigure(5, weight=1, pad=12)
mainframe.rowconfigure(6, weight=1, pad=12)
mainframe.rowconfigure(7, weight=1, pad=12)

root.mainloop()
