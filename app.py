from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image as Img


class App(Tk):

    def __init__(self):
        super().__init__()
        self.title("otk-crawler | informações de ruas - correios")
        self.geometry('400x360')
        self.maxsize(400, 360)
        self.resizable(False, False)

        self.window = MainFrame(parent=self)

        self.mainloop()


class MainFrame(Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.grid(column=0, row=0, columnspan=8, rowspan=8, sticky=(N, S, W, E), padx=8, pady=8)

    def create_widgets(self):
        uf_label = ttk.Label(self, text="UF:")
        city_label = ttk.Label(self, text="Cidade:")
        locality_label = ttk.Label(self, text="Bairro: ")

        uf_entry = ttk.Entry(self)
        city_entry = ttk.Entry(self)
        locality_entry = ttk.Entry(self)

        treeview_process_screen = ttk.Treeview(self, show="tree")
        treeview_process_screen.state(['readonly'])

        #btn_search = ttk.Button(self, text="Pesquisar", command=lambda: create_new_scrapper())

        # download_btn = ttk.Button(self, text="Baixar Resultado", command=lambda: create_files())
        # download_btn.state(['disabled'])

        reset_icon = ImageTk.PhotoImage(Img.open('./assets/reset.png'), ('16', '16'))
        new_query_btn = ttk.Button(self, image=reset_icon, compound='image')

        uf_label.grid(column=1, row=1, sticky=(N, W))
        city_label.grid(column=3, row=1, sticky=(N, W), padx=8)
        locality_label.grid(column=1, row=2, sticky=(N, W, E, S))

        uf_entry.grid(column=2, row=1, sticky=(N, W))
        city_entry.grid(column=4, row=1, sticky=(N, W))
        locality_entry.grid(column=2, columnspan=2, row=2, sticky=(W, E))

        treeview_process_screen.grid(column=1, row=6, rowspan=2, columnspan=2, sticky=(N, S, W, E))

        #btn_search.grid(column=1, columnspan=4, row=3, sticky=(N, S, W, E), pady=12)

        #download_btn.grid(column=3, columnspan=2, row=6, sticky=(N, S, W, E), padx=(16, 0), pady=8)

        new_query_btn.grid(column=4, row=2, sticky=(W, E), padx=4, pady=(4, 6))

    def set_layout(self):
        self.grid(column=0, row=0, columnspan=8, rowspan=8, sticky=(N, S, W, E), padx=8, pady=8)
        self.columnconfigure(1, weight=8)
        self.columnconfigure(2, weight=8)
        self.columnconfigure(3, weight=5)
        self.columnconfigure(4, weight=5)
        self.rowconfigure(1, weight=1, pad=12)
        self.rowconfigure(2, weight=1, pad=12)
        self.rowconfigure(3, weight=1, pad=12)
        self.rowconfigure(4, weight=1, pad=12)
        self.rowconfigure(5, weight=1, pad=12)
        self.rowconfigure(6, weight=1, pad=12)
        self.rowconfigure(7, weight=1, pad=12)



n = App()
