import _tkinter
import os
import csv
import tkinter.filedialog as fd

from PIL import ImageTk, Image as Img

from scrapper import Scrapper, ScrapperModes

import pandas as pd

from ttkbootstrap import ttk
from tkinter import *

global last_addresses


def clear_entries():
    try:
        uf_entry.delete(0, END)
        city_entry.delete(0, END)
        locality_entry.delete(0, END)
        locality_check_1.option_clear()
        locality_check_2.option_clear()
        treeview_process_screen.delete("main")
        search_btn.state(["!disabled"])
        search_btn.configure(text="PESQUISAR")

    except _tkinter.TclError:
        pass


def create_new_scrapper():
    """
    Create a new Scrapper using the values of the GUI entries as parameters of the query.
    Proceeds to show the scrapper creation and run logs.
    """

    search_btn.state(["disabled"])
    search_btn.configure(text="AGUARDE")

    scrapper_mode = ScrapperModes[locality_var.get()]

    scrapper = Scrapper(mode=scrapper_mode,
                        uf=uf_entry.get(),
                        city=city_entry.get(),
                        locality=locality_entry.get())

    tree_view_log = treeview_process_screen.insert(parent="",
                                                   index='end',
                                                   text="Criando uma nova busca...",
                                                   iid="main")
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
    search_btn.configure(text="PRONTO")

    global last_addresses
    last_addresses = response


def download_files():
    directory = fd.asksaveasfilename(confirmoverwrite=True)
    print(directory)

    sorted_addresses = sorted(last_addresses, key=lambda d: d["sub_endereco"])

    os.mkdir(directory)

    df_by_sub_addresses = pd.DataFrame.from_records(sorted_addresses)
    df_by_sub_addresses.to_csv(f"{directory}/informacoes-{locality_entry.get()}.csv", index=False)
    df_by_sub_addresses.to_excel(f"{directory}/informacoes-{locality_entry.get()}.xlsx")

    with open(f"{directory}/informacoes-{locality_entry.get()}.csv", 'r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)

        newfile = f"{directory}/informacoes-{locality_entry.get()}.txt"

        for line in csv_reader:
            with open(newfile, mode='a') as new_txt:
                txt_writer = csv.writer(new_txt, delimiter='\t')
                txt_writer.writerow(line)

    treeview_process_screen.insert(parent='main', index=END, text="Arquivos Baixados.")
    download_btn.state(['!disabled'])


root = Tk()
root.title("otk-crawler | informações de ruas - correios")
root.resizable(False, False)

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, columnspan=8, rowspan=8, padx=8, pady=8)

uf_label = ttk.Label(mainframe, text="UF:")
city_label = ttk.Label(mainframe, text="CIDADE:")
locality_label_1 = ttk.Label(mainframe, text="PESQUISAR POR: ")
locality_label_2 = ttk.Label(mainframe, text="INSIRA: ")

uf_entry = ttk.Entry(mainframe)
city_entry = ttk.Entry(mainframe)

locality_entry = ttk.Entry(mainframe)

locality_var = StringVar()

locality_check_1 = ttk.Checkbutton(mainframe,
                                   text="RUA",
                                   variable=locality_var,
                                   onvalue="STREET",
                                   offvalue="")
locality_check_2 = ttk.Checkbutton(mainframe,
                                   text="BAIRRO",
                                   variable=locality_var,
                                   onvalue="NEIGHBOURHOOD",
                                   offvalue="")

locality_check_2.invoke()

treeview_process_screen = ttk.Treeview(mainframe, show="tree")
treeview_process_screen.state(['readonly'])

search_btn = ttk.Button(mainframe, text="PESQUISAR", command=lambda: create_new_scrapper())

download_btn = ttk.Button(mainframe, text="BAIXAR ARQUIVOS", command=lambda: download_files())
download_btn.state(['disabled'])

new_query_btn = ttk.Button(mainframe, text="LIMPAR", command=lambda: clear_entries())

uf_label.grid(column=1, row=1)
uf_entry.grid(column=2, row=1)

city_label.grid(column=1, row=2, padx=8)
city_entry.grid(column=2, row=2)

locality_label_1.grid(column=1, row=3, columnspan=2)

locality_check_1.grid(column=1, columnspan=1, row=4)
locality_check_2.grid(column=2, columnspan=1, row=4)

locality_label_2.grid(column=1, columnspan=1, row=5)
locality_entry.grid(column=2, columnspan=2, row=5)

treeview_process_screen.grid(column=5, row=1, rowspan=5, columnspan=3, padx=(16, 0))

search_btn.grid(column=1, columnspan=4, row=6, pady=12)
download_btn.grid(column=5, columnspan=1, row=6, padx=(16, 0), pady=8)
new_query_btn.grid(column=6, columnspan=2, row=6, padx=8)

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
