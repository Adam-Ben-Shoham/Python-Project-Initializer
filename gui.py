import customtkinter as ctk
from tkinter import filedialog
import threading
import re

from project_orchestrator import ProjectOrchestrator
import constants

MAIN_THEME_PURPLE = '#8A2BE2'
MAIN_THEME_CYAN = '#008000'
DEEP_PURPLE = '#6A0DAD'
BLACK = '#2b2b2b'


class AppGui(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.setup_window()

        self.project_title = None
        self.subheader = None
        self.setup_header()

        self.name_input = None
        self.remember_root_dir = ctk.BooleanVar(value=False)
        self.remember_ide = ctk.BooleanVar(value=False)
        self.init_git = ctk.BooleanVar(value=True)
        self.setup_inputs()

    def setup_window(self):
        self.title = 'Python Project Initializer'
        self.geometry('600x700')
        self.grid_columnconfigure(0, weight=1)

        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')

    def setup_header(self):
        self.project_title = ctk.CTkLabel(self, text='Python Kickstarter',
                                          font=('Helvetica', 24, 'bold'),
                                          text_color='white')
        self.project_title.grid(column=0, row=0, sticky='NSEW', padx=10, pady=(30, 0))

        self.subheader = ctk.CTkLabel(self, text='Automate Your Project Creation',
                                      font=('Helvetica', 16, 'bold'),
                                      text_color='white')
        self.subheader.grid(column=0, row=1, sticky='NSEW', padx=10)

    def setup_inputs(self):
        self.setup_name_input()
        self.setup_root_dir_input()
        self.setup_project_type_input()

    def setup_name_input(self):

        self.name_var = ctk.StringVar()
        self.name_var.trace_add('write',self.on_name_change)

        self.name_input = ctk.CTkEntry(self, placeholder_text='Project Name...',
                                       height=35,
                                       border_color=MAIN_THEME_PURPLE)
        self.name_input.grid(column=0, row=2, sticky='NSEW', padx=50, pady=(30, 10))

        self.name_error = ctk.CTkLabel(self, text='skibidv',
                                       text_color='red',
                                       font=('Helvetica', 11),)
        self.name_error.grid(column=0, row=3, sticky='w', padx=55, pady=(2, 0))


    def on_name_change(self,*args):

        text = self.name_var.get()
        if text == '':
            self.name_error.config(text='')
            return

        if len(text) > 30:
            self.name_error.config(text='project name cant be longer than 30 characters')
            return

        if text[0].isdigit():
            self.name_error.config(text='First character of project cant be a number')
            return

        for char in text:
            if not char.isalnum() or char == '_':
                self.name_error.config(text='Only use letters, numbers and underscores')
                return

        self.show_name_error('')




    def setup_root_dir_input(self):
        self.frame = ctk.CTkFrame(self, fg_color='transparent',
                                  bg_color='transparent')
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid(row=3, column=0, sticky='ew', padx=50, pady=10)

        self.root_dir_input = ctk.CTkEntry(self.frame, placeholder_text='Project Root Directory...',
                                           height=35,
                                           border_color=MAIN_THEME_PURPLE)
        self.root_dir_input.grid(row=0, column=0, sticky='ew', padx=(0, 5), pady=0)

        self.browse_button = ctk.CTkButton(self.frame, text='Browse...',
                                           width=15,
                                           command=self.browse_dir,
                                           fg_color=MAIN_THEME_PURPLE,
                                           hover_color=DEEP_PURPLE)
        self.browse_button.grid(row=0, column=1, padx=0, pady=0)

        self.remember_button = ctk.CTkCheckBox(self.frame, text='Remember This Directory',
                                              fg_color=MAIN_THEME_PURPLE,
                                              hover_color=DEEP_PURPLE,
                                              variable=self.remember_root_dir,
                                              checkbox_height=22,
                                              checkbox_width=22,
                                              font=('Helvetica', 12, 'bold'), )
        self.remember_button.grid(column=0, row=1, sticky='w', padx=0, pady=(10, 0), columnspan=2)

    def browse_dir(self):
        folder_path = filedialog.askdirectory()

        if folder_path:
            self.root_dir_input.delete(0, 'end')
            self.root_dir_input.insert(0, folder_path)

    def setup_project_type_input(self):
        self.type_row_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.type_row_frame.grid(row=4, column=0, sticky='w', padx=50, pady=0)

        self.type_label = ctk.CTkLabel(self.type_row_frame, text='Project Type:',
                                       font=('Helvetica', 12, 'bold'),
                                       text_color='white')

        self.type_label.grid(column=0, row=2, sticky='w', padx=(0, 5), pady=0)

        types = list(constants.PROJECT_TEMPLATES.keys())

        self.type_input = ctk.CTkSegmentedButton(self.type_row_frame,
                                                 values=types,
                                                 selected_color=MAIN_THEME_PURPLE,
                                                 selected_hover_color=DEEP_PURPLE,
                                                 unselected_color=BLACK,
                                                 unselected_hover_color="#333333",
                                                 text_color="white",
                                                 fg_color=BLACK,
                                                 font=('Helvetica', 11, 'bold'),
                                                 height=35)
        self.type_input.set(types[0])
        self.type_input.grid(row=2, column=1, sticky='w', pady=0)


gui = AppGui()

gui.mainloop()
