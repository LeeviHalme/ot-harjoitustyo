from tkinter import Tk
from ui import UI as GraphInterface

window = Tk()
window.title("Budjetointisovellus v.1.0.0")
window.geometry("1000x500")

ui = GraphInterface(window)
ui.start()

# start TkInter main loop
window.mainloop()
