import customtkinter
from ui import UI as GraphInterface

# CustomTkInter Setup
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

window = customtkinter.CTk()
window.title("Budjetointisovellus v.1.0.0")
window.geometry("1000x500")

ui = GraphInterface(window)
ui.start()

# start TkInter main loop
window.mainloop()
