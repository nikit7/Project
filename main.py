import tkinter as tk
from Sapper import Sapper as sp


root = tk.Tk()
root.title('Сапёр 8x8')
root.resizable(width=False, height=False)
rows = 8
cols = 8
mines = 9
sp(root, rows, cols, mines)
root.mainloop()
