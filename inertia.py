import os, json, tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd
import downloader

INERTIA_VERSION = [0, 1, 0, "alpha"]
INERTIA_VERSION_STR = [str(e) for e in INERTIA_VERSION]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # root window
        self.title("Inertia version " + ".".join(INERTIA_VERSION_STR))
        self.geometry('400x300')
        self.style = ttk.Style(self)
        self.style.theme_use('vista')

        self.inertia_pack = {}
        self.categories = {}

        control_menu = tk.Menu(self, tearoff=0)
        self.config(menu=control_menu)
        inertia_menu = tk.Menu(control_menu, tearoff=0)
        control_menu.add_cascade(label='Inertia', menu=inertia_menu)
        inertia_menu.add_command(label='Exit', command=exit)

        packs_menu = tk.Menu(control_menu, tearoff=0)
        control_menu.add_cascade(label='Software Pack', menu=packs_menu)
        packs_menu.add_command(label='Open from file', command=self.import_pack_file)

        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand = 1, fill = "both")
        
    def build_pack(self):
        self.title("Inertia version " + ".".join(INERTIA_VERSION_STR) + " - " + self.inertia_pack['name'])
        for tab in self.tab_control.tabs():
            self.tab_control.forget(tab)
        self.categories = {}
        for category in self.inertia_pack['programs']:
            self.categories[category] = {}
            self.categories[category]['tab'] = ttk.Frame(self.tab_control)
            self.tab_control.add(self.categories[category]['tab'], text=category)

            self.categories[category]['btns'] = {}
            self.categories[category]['btns']['installCat'] = tk.Button(self.categories[category]['tab'], text='Install checked', command=self.start_downloader)
            self.categories[category]['btns']['installCat'].grid(row=0, column=1, sticky="NE")
            self.categories[category]['btns']['uncheckAll'] = tk.Button(self.categories[category]['tab'], text='Uncheck all', command=self.cat_uncheck_all)
            self.categories[category]['btns']['uncheckAll'].grid(row=2, column=1, sticky="NE")
            self.categories[category]['btns']['checkAll'] = tk.Button(self.categories[category]['tab'], text='Check all', command=self.cat_check_all)
            self.categories[category]['btns']['checkAll'].grid(row=3, column=1, sticky="NE")
            
            self.categories[category]['boxes'] = {}
            self.categories[category]['vars'] = {}
            row_index = 0
            for program in self.inertia_pack['programs'][category]:
                if self.inertia_pack['programs'][category][program]['default']:
                    self.categories[category]['vars'][program] = tk.IntVar(value=1)
                else:
                    self.categories[category]['vars'][program] = tk.IntVar(value=0)
                self.categories[category]['boxes'][program] = tk.Checkbutton(
                    self.categories[category]['tab'],
                    text=program + ' (' + self.inertia_pack['programs'][category][program]['version'] + ')',
                    variable=self.categories[category]['vars'][program])
                self.categories[category]['boxes'][program].grid(row=row_index, column=0, sticky="NW")
                row_index += 1
        
            self.categories[category]['tab'].columnconfigure(1, weight=1)
            self.categories[category]['tab'].rowconfigure(1, weight=1)
        messagebox.showinfo('Inertia', 'Pack "' + self.inertia_pack['name'] + '" imported successfully.')

    def cat_uncheck_all(self):
        selected_category = self.tab_control.tab(self.tab_control.select(), 'text')
        for program in self.categories[selected_category]['boxes']:
            self.categories[selected_category]['vars'][program].set(0)

    def cat_check_all(self):
        selected_category = self.tab_control.tab(self.tab_control.select(), 'text')
        for program in self.categories[selected_category]['boxes']:
            self.categories[selected_category]['vars'][program].set(1)

    def start_downloader(self):
        selected_category = self.tab_control.tab(self.tab_control.select(), 'text')
        programs_list = []
        for program in self.inertia_pack['programs'][selected_category]:
            if self.categories[selected_category]['vars'][program].get() == 1:
                programs_list.append({'name': program, 'installer': self.inertia_pack['programs'][selected_category][program]['installer']})
        window = downloader.DownloaderWindow()
        window.grab_set()
        window.download_cat(self.inertia_pack['name'], selected_category, programs_list)

    def import_pack_file(self):
        filename = fd.askopenfilename(title="Import Inertia pack", filetypes=(('JSON', '*.json'),("All files", "*.*")))
        with open(filename, 'r') as f:
            self.inertia_pack = json.loads(f.read())
        self.build_pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()
