import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from gui_components import ValidatedNameInput, PathSelector, ChoiceSelector, CheckBoxButton
from project_orchestrator import ProjectOrchestrator
import constants
from gui_settings import SettingsManager

MAIN_THEME_PURPLE = '#8A2BE2'
DEEP_PURPLE = '#6A0DAD'
BLACK = '#2b2b2b'
GREEN = '#1F7D53'
BLUE = '#1C4D8D'


class AppGui(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.setup_window()
        self.setup_header()

        self.settings_manager = SettingsManager()
        self.saved_settings = self.settings_manager.load_settings()

        self.remember_root_dir = ctk.BooleanVar(value=self.saved_settings.get("remember_root_dir", False))
        self.remember_ide = ctk.BooleanVar(value=self.saved_settings.get("remember_ide_choice", False))
        self.init_git = ctk.BooleanVar(value=True)

        self.setup_inputs()

    def setup_window(self):
        self.title('Python KickStarter')
        self.geometry('600x750')
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

        self.setup_initialize_button()
        self.setup_root_dir_input()
        self.setup_name_input()
        self.setup_project_type_input()
        self.setup_ide_choice_input()
        self.setup_ide_path_input()
        self.setup_init_git_button()

    def setup_name_input(self):
        self.name_section = ValidatedNameInput(self, theme_color=MAIN_THEME_PURPLE,
                                               dir_selector=self.root_dir_selector,
                                               init_button=self.init_button,
                                               init_error_label=self.init_error_label)
        self.name_section.grid(row=3, column=0, sticky='ew', padx=50, pady=(0, 10))

    def setup_root_dir_input(self):

        saved_root_path = self.saved_settings.get('root_dir','')

        self.root_dir_selector = PathSelector(self,
                                              theme_color=MAIN_THEME_PURPLE,
                                              hover_color=DEEP_PURPLE,
                                              placeholder_name='Root Directory...',
                                              init_error_label=self.init_error_label)

        if saved_root_path:
            self.root_dir_selector.path_var.set(saved_root_path)
            self.root_dir_selector.root_dir_input.configure(text_color='white')

        self.root_dir_selector.grid(row=2, column=0, sticky='ew', padx=50, pady=(40, 20))

    def setup_project_type_input(self):
        types = list(constants.PROJECT_TEMPLATES.keys())

        self.project_type_selector = ChoiceSelector(self, theme_color=BLUE,
                                                    values=types,
                                                    remember_btn_color=MAIN_THEME_PURPLE,
                                                    hover_color=BLUE,
                                                    text='Project Type:'
                                                    )

        self.project_type_selector.grid(row=4, column=0, sticky='ew', padx=50, pady=(0, 10))

    def setup_ide_choice_input(self):

        ide_choices = ['PyCharm', 'VSCode']
        saved_ide_choice = self.saved_settings.get("ide_choice", 'PyCharm')

        self.ide_choice_selector = ChoiceSelector(self, theme_color=GREEN,
                                                  hover_color=GREEN,
                                                  remember_btn_color=MAIN_THEME_PURPLE,
                                                  text='Remember Ide',
                                                  values=ide_choices,
                                                  initial_value=saved_ide_choice,
                                                  has_remember=True,
                                                  remember_var=self.remember_ide,
                                                  command=self.update_ide_choice_input
                                                  )
        self.ide_choice_selector.button.set(saved_ide_choice)
        self.ide_choice_selector.grid(row=5, column=0, sticky='ew', padx=50, pady=(0, 10))

    def update_ide_choice_input(self,selected_value):
        self.ide_path_input.ide_choice = selected_value

        self.ide_path_input.on_change()

    def setup_ide_path_input(self):

        saved_ide_path = self.saved_settings.get("ide_path", '')

        self.ide_path_input = PathSelector(self, theme_color=MAIN_THEME_PURPLE,
                                           hover_color=DEEP_PURPLE,
                                           placeholder_name='Select IDE Path...',
                                           ide_choice=self.ide_choice_selector.button.get(),
                                           init_error_label=self.init_error_label,
                                           tip='Tip: Right click your IDE and press "open file location"')

        if saved_ide_path:
            self.ide_path_input.path_var.set(saved_ide_path)
            self.ide_path_input.root_dir_input.configure(text_color='white')

        self.ide_path_input.grid(row=6, column=0, sticky='ew', padx=50, pady=(0, 10))



    def setup_init_git_button(self):
        self.remember_git = ctk.BooleanVar(value=True)
        self.init_git_button = CheckBoxButton(self, text='Initialize Local Git Repository',
                                              theme_color=MAIN_THEME_PURPLE,
                                              hover_color=DEEP_PURPLE,
                                              remember_var=self.remember_git,
                                              )
        self.init_git_button.grid(row=7, column=0, sticky='w', padx=50, pady=(0, 10))

    def setup_initialize_button(self):
        self.init_button = ctk.CTkButton(self, text="Launch",
                                         height=50,
                                         font=('Helvetica', 16, 'bold'),
                                         fg_color=MAIN_THEME_PURPLE,
                                         hover_color=DEEP_PURPLE,
                                         command=self.initialize
                                         )
        self.init_button.grid(row=8, column=0, pady=(40, 10), padx=100, sticky='ew')

        self.init_error_label = ctk.CTkLabel(self, text_color='red',
                                             font=('Helvetica', 11, 'bold'),
                                             )

    def initialize(self):
        # check for errors
        if self.name_section.name_status == 'invalid':
            self.init_error_label.configure(text='Invalid Name')
            self.init_error_label.grid(row=9, column=0, sticky='ew', padx=50)
            return

        if self.root_dir_selector.root_dir_status == 'invalid':
            self.init_error_label.configure(text='Invalid Root Directory')
            self.init_error_label.grid(row=9, column=0, sticky='ew', padx=50)
            return

        if self.ide_path_input.ide_status == 'invalid':
            self.init_error_label.configure(text='Invalid IDE .exe Path')
            self.init_error_label.grid(row=9, column=0, sticky='ew', padx=50)
            return

        if 'warning' in [self.name_section.name_status, self.root_dir_selector.root_dir_status, self.ide_path_input.ide_status]:
            confirm = messagebox.askyesno("Just A Heads Up",
                                          "Your project name doesn't follow standard Python conventions.\n\nDo you wish to proceed anyway?")
            if not confirm:
                return

        self.init_error_label.grid_forget()

        settings_to_save = {
            "root_dir": self.root_dir_selector.get(),
            "remember_root_dir": self.remember_root_dir.get(),

            "ide_choice": self.ide_choice_selector.button.get(),
            "remember_ide_choice": self.remember_ide.get(),

            "ide_path": self.ide_path_input.get(),
            "remember_ide_path": self.remember_ide.get()
        }

        self.settings_manager.save_settings(settings_to_save)

        return


gui = AppGui()

gui.mainloop()
