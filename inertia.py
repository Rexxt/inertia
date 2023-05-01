import os, json, tkinter as tk
from tkinter import ttk

INERTIA_VERSION = [0, 1, 0, "alpha"]
INERTIA_VERSION_STR = [str(e) for e in INERTIA_VERSION]

root = tk.Tk()
root.title("Inertia version " + ".".join(INERTIA_VERSION_STR))
root.geometry("400x300")

control_menu = tk.Menu(root, tearoff=0)
root.config(menu=control_menu)
inertia_menu = tk.Menu(control_menu, tearoff=0)
control_menu.add_cascade(label='Inertia', menu=inertia_menu)
inertia_menu.add_command(label='Exit', command=exit)

tab_control = ttk.Notebook(root)

tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)

tab_control.add(tab1, text ='Gaming')
tab_control.add(tab2, text ='Video')
tab_control.pack(expand = 1, fill = "both")
ttk.Label(tab1, 
          text = "Steam n shit").grid(column = 0, 
                               row = 0,)  
ttk.Label(tab2,
          text = "OBS n shit").grid(column = 0,
                                    row = 0)
  
root.mainloop()