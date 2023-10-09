import customtkinter
from CTkMessagebox import CTkMessagebox
from time import sleep


def msgbox(title, text):
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")
    root=customtkinter.CTk()
    root.geometry("5x5")
    root.title("DolbyUI")
    root.withdraw()
    CTkMessagebox(title=title, message=text, icon="info")
    sleep(20)
    root.destroy()
