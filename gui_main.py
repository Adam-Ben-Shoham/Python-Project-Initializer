import customtkinter as ctk
from tkinter import filedialog
import threading
from gui_components import ValidatedNameInput, DirectorySelector
from project_orchestrator import ProjectOrchestrator
import constants

MAIN_THEME_PURPLE = '#8A2BE2'
DEEP_PURPLE = '#6A0DAD'
BLACK = '#2b2b2b'


class AppGui(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.setup_window()
        self.setup_header()
        self.setup_initialize_button()

        # variables
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
        self.setup_root_dir_input()
        self.setup_name_input()
        self.setup_project_type_input()

    def setup_name_input(self):
        self.name_section = ValidatedNameInput(self, theme_color=MAIN_THEME_PURPLE, dir_selector=self.root_dir_selector,
                                               init_button=self.init_button)
        self.name_section.grid(row=3, column=0, sticky='ew', padx=50, pady=(10, 0))

    def setup_root_dir_input(self):
        self.root_dir_selector = DirectorySelector(self, theme_color=MAIN_THEME_PURPLE, hover_color=DEEP_PURPLE)
        self.root_dir_selector.grid(row=2, column=0, sticky='ew', padx=50, pady=(10, 0))

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
                                                 font=('Helvetica', 12, 'bold'),
                                                 height=35)
        self.type_input.set(types[0])
        self.type_input.grid(row=2, column=1, sticky='w', pady=(10, 0))

    def setup_initialize_button(self):
        self.init_button = ctk.CTkButton(self, text="Initialize",
                                         height=50,
                                         font=('Helvetica', 16, 'bold'),
                                         fg_color=MAIN_THEME_PURPLE,
                                         hover_color=DEEP_PURPLE,
                                         command=self.initialize
                                         )
        self.init_button.grid(row=10, column=0, pady=40, padx=100, sticky='ew')

    def initialize(self):
        #check for errors
        pass


gui = AppGui()

gui.mainloop()
