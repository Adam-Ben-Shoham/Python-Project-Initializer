import customtkinter as ctk
from tkinter import filedialog
import threading
from gui_components import ValidatedNameInput, PathSelector, ChoiceSelector
from project_orchestrator import ProjectOrchestrator
import constants

MAIN_THEME_PURPLE = '#8A2BE2'
DEEP_PURPLE = '#6A0DAD'
BLACK = '#2b2b2b'
ORANGE = '#E6501B'
GREEN = '#1F7D53'
BLUE = '#1C4D8D'


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
        self.title('Python KickStarter')
        self.geometry('600x700')
        self.grid_columnconfigure(0, weight=1)

        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')

    def setup_header(self):
        self.project_title = ctk.CTkLabel(self, text='Python KickStarter',
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
        self.setup_ide_choice_input()
        self.setup_ide_path_input()

    def setup_name_input(self):
        self.name_section = ValidatedNameInput(self, theme_color=MAIN_THEME_PURPLE,
                                               dir_selector=self.root_dir_selector,
                                               init_button=self.init_button)
        self.name_section.grid(row=3, column=0, sticky='ew', padx=50, pady=(0, 10))

    def setup_root_dir_input(self):
        self.root_dir_selector = PathSelector(self,
                                                   theme_color=MAIN_THEME_PURPLE,
                                                   hover_color=DEEP_PURPLE,
                                                   placeholder_name='Root Directory...',)
        self.root_dir_selector.grid(row=2, column=0, sticky='ew', padx=50, pady=(40,20))

    def setup_project_type_input(self):
        types = list(constants.PROJECT_TEMPLATES.keys())

        self.project_type_selector = ChoiceSelector(self, theme_color=BLUE,
                                                    values=types,
                                                    remember_btn_color=MAIN_THEME_PURPLE,
                                                    hover_color=BLACK,
                                                    text='Project Type'
                                                    )

        self.project_type_selector.grid(row=4, column=0, sticky='ew', padx=50, pady=(0, 10))

    def setup_ide_choice_input(self):
        ide_choices = ['PyCharm', 'VSCode']
        remember_ide = ctk.BooleanVar(value=False)
        self.ide_choice_selector = ChoiceSelector(self, theme_color=GREEN,
                                                  hover_color=BLACK,
                                                  remember_btn_color=MAIN_THEME_PURPLE,
                                                  text='Remember Ide',
                                                  values=ide_choices,
                                                  has_remember=True,
                                                  remember_var=remember_ide,
                                                  )

        self.ide_choice_selector.grid(row=5, column=0, sticky='ew', padx=50, pady=(0, 10))

    def setup_ide_path_input(self):

        self.ide_path_input = PathSelector(self, theme_color=MAIN_THEME_PURPLE,
                                                hover_color=DEEP_PURPLE,
                                                placeholder_name='Select IDE Path...',
                                                ide_choice='VSCode',)
        self.ide_path_input.grid(row=6, column=0, sticky='ew', padx=50, pady=(0, 10))

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
        # check for errors
        pass


gui = AppGui()

gui.mainloop()
