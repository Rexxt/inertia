import os, json, tkinter as tk, requests
from tkinter import ttk
from tkinter import messagebox

class DownloaderWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # root window
        self.title("Pack Downloader")
        self.geometry('400x300')
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.list = tk.Listbox(self)
        self.list.pack(side='top', expand=True, fill='both')
        self.progress_var = tk.IntVar()
        self.progress = ttk.Progressbar(self)
        self.progress.pack(side='bottom', expand=True, fill='both')

    def download_cat(self, pack_name, name, programs):
        self.list.delete(0, tk.END)
        self.title("Downloading and installing from " + name + " in " + pack_name)

        i = 1
        for program in programs:
            self.list.insert(i, program['name'])

        self.progress['maximum'] = len(programs)
        self.progress_var.set(0)

        for program in programs:
            r = requests.get(program['installer'], allow_redirects=True)
            if not os.path.isdir('installers/' + pack_name + '/' + name):
                os.makedirs('installers/' + pack_name + '/' + name)
            open('installers/' + pack_name + '/' + name + '/' + program['name'] + '.exe', 'wb').write(r.content)
            self.progress.step(1)

        messagebox.showinfo(name + " in " + pack_name, 'Installers downloaded.')

        self.destroy()
