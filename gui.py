import customtkinter as ctk
from tkinter import filedialog
import threading

from project_orchestrator import ProjectOrchestrator
import constants


class AppGui(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.setup_window()
        self.setup_header()



    def setup_window(self):
        self.title = 'Python Project Initializer'
        self.geometry('600x700')
        self.grid_columnconfigure(0, weight=1)

        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')

    def setup_header(self):
        self.title = ctk.CTkLabel(self, text='Python Kickstarter',
                                  font=('Helvetica', 24, 'bold'),
                                  text_color='white')
        self.title.grid(column=0, row=0, sticky='NSEW', padx=10, pady=(30, 0))

        self.subheader = ctk.CTkLabel(self, text='Automate Your Project Creation',
                                      font=('Helvetica', 12, 'bold'),
                                      text_color='white')
        self.subheader.grid(column=0, row=1, sticky='NSEW', padx=10)

    def setup_name_input(self):
        pass



gui = AppGui()

gui.mainloop()
