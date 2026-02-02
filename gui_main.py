import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from gui_components import ValidatedNameInput, PathSelector, ChoiceSelector, CheckBoxButton,CustomWarningBox
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
        self.remember_ide_path = ctk.BooleanVar(value=self.saved_settings.get("remember_ide_path", False))
        self.remember_interpreter = ctk.BooleanVar(value=self.saved_settings.get("remember_interpreter", False))
        self.init_git = ctk.BooleanVar(value=True)

        self.is_creating = False

        self.setup_inputs()

    def setup_window(self):
        self.title('Python KickStarter')
        self.geometry('700x850')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_container = ctk.CTkFrame(self,width=700,height=850,fg_color='transparent')
        self.main_container.grid(row = 0,column=0, pady = 20,sticky='n')
        self.main_container.grid_propagate(False)
        self.main_container.grid_columnconfigure(0, weight=1)

        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')

    def clear_window(self):

        for widget in self.main_container.winfo_children():
            widget.grid_forget()

    def show_window_one(self):
        self.clear_window()
        self.setup_header()

        self.root_dir_selector.grid(row=2,column=0,sticky = 'ew', padx= 50, pady=(20,20))
        self.name_section.grid(row=3,column=0,sticky = 'ew', padx= 50, pady=(0,10))
        self.project_type_selector.grid(row=4,column=0,sticky = 'ew', padx= 50, pady=(20,20))

        self.next_btn = ctk.CTkButton(self.main_container, text="Next: Environment",
                                      command=self.validate_window_one,
                                      fg_color=BLUE, hover_color="#143766")
        self.next_btn.grid(row=5, column=0, pady=30, padx=100, sticky='ew')

    def show_window_two(self):
        self.clear_window()

        self.window_two_label = ctk.CTkLabel(self.main_container, text=f'Environment',font=('Helvetica', 24, 'bold'),text_color='white')
        self.window_two_label.grid(row=0,column=0, pady=30, padx=100, sticky='ew')

        self.ide_choice_selector.grid(row=1, column=0, sticky='ew', padx=50, pady=(20, 10))
        self.ide_path_input.grid(row=2, column=0, sticky='ew', padx=50, pady=(0, 10))
        self.interpreter_path_input.grid(row=3, column=0, sticky='ew', padx=50, pady=(0, 10))

        self.nav_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.nav_frame.grid(row=4, column=0, pady=30, sticky="ew", padx=50)
        self.nav_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(self.nav_frame, text="Back", command=self.show_window_one,
                      fg_color="gray", hover_color="#3d3d3d").grid(row=0, column=0, padx=5, sticky='ew')

        ctk.CTkButton(self.nav_frame, text="Next: Git", command=self.validate_window_two,
                      fg_color=MAIN_THEME_PURPLE, hover_color=DEEP_PURPLE).grid(row=0, column=1, padx=5, sticky='ew')

    def show_window_three(self):
        self.clear_window()

        self.nav_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.nav_frame.grid(row=4, column=0, pady=30, sticky="ew", padx=50)
        self.nav_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(self.nav_frame, text="Back", command=self.show_window_two,
                      fg_color="gray", hover_color="#3d3d3d").grid(row=0, column=0, padx=5, sticky='ew')

        ctk.CTkButton(self.nav_frame, text="Next: Git", command=self.validate_window_three,
                      fg_color=MAIN_THEME_PURPLE, hover_color=DEEP_PURPLE).grid(row=0, column=1, padx=5, sticky='ew')

    def setup_header(self):
        self.project_title = ctk.CTkLabel(self.main_container, text='Python KickStarter',
                                          font=('Helvetica', 24, 'bold'),
                                          text_color='white')
        self.project_title.grid(column=0, row=0, sticky='NSEW', padx=10, pady=(30, 0))

        self.subheader = ctk.CTkLabel(self.main_container, text='Automate Your Project Creation',
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
        self.setup_interpreter_path_input()
        self.setup_init_git_button()

    def setup_name_input(self):
        self.name_section = ValidatedNameInput(self.main_container, theme_color=MAIN_THEME_PURPLE,
                                               dir_selector=self.root_dir_selector,
                                               init_button=self.init_button,
                                               init_error_label=self.init_error_label)
        self.name_section.grid(row=3, column=0, sticky='ew', padx=50, pady=(0, 10))

    def setup_root_dir_input(self):

        saved_root_path = self.saved_settings.get('root_dir','')

        self.root_dir_selector = PathSelector(self.main_container,
                                              theme_color=MAIN_THEME_PURPLE,
                                              hover_color=DEEP_PURPLE,
                                              placeholder_name='Root Directory...',
                                              init_error_label=self.init_error_label,
                                              remember_var=self.remember_root_dir,)

        if saved_root_path:
            self.root_dir_selector.path_var.set(saved_root_path)
            self.root_dir_selector.root_dir_input.configure(text_color='white')

        self.root_dir_selector.grid(row=2, column=0, sticky='ew', padx=50, pady=(20, 20))

    def setup_project_type_input(self):
        types = list(constants.PROJECT_TEMPLATES.keys())

        self.project_type_selector = ChoiceSelector(self.main_container, theme_color=BLUE,
                                                    values=types,
                                                    remember_btn_color=MAIN_THEME_PURPLE,
                                                    hover_color=BLUE,
                                                    text='Project Type'
                                                    )

        self.project_type_selector.grid(row=4, column=0, sticky='ew', padx=50, pady=(0, 10))

    def setup_ide_choice_input(self):

        ide_choices = ['PyCharm', 'VSCode']
        saved_ide_choice = self.saved_settings.get("ide_choice", 'PyCharm')

        self.ide_choice_selector = ChoiceSelector(self.main_container, theme_color=GREEN,
                                                  hover_color=GREEN,
                                                  remember_btn_color=MAIN_THEME_PURPLE,
                                                  text='IDE',
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

        self.ide_path_input = PathSelector(self.main_container, theme_color=MAIN_THEME_PURPLE,
                                           hover_color=DEEP_PURPLE,
                                           placeholder_name='Select IDE Path...',
                                           ide_choice=self.ide_choice_selector.button.get(),
                                           init_error_label=self.init_error_label,
                                           tip='Tip: Right click your IDE and press "open file location", look for an exe file',
                                           remember_var=self.remember_ide_path)

        if saved_ide_path:
            self.ide_path_input.path_var.set(saved_ide_path)
            self.ide_path_input.root_dir_input.configure(text_color='white')

        self.ide_path_input.grid(row=6, column=0, sticky='ew', padx=50, pady=(0, 10))

    def setup_interpreter_path_input(self):
        saved_interpreter = self.saved_settings.get("interpreter", '')

        self.interpreter_path_input = PathSelector(self.main_container, theme_color=MAIN_THEME_PURPLE,
                                             hover_color=DEEP_PURPLE,
                                             placeholder_name='Select Interpreter...',
                                             init_error_label=self.init_error_label,
                                             tip='Tip: In your IDE terminal, type "python where", look for python.exe at the end of the path',
                                             remember_var=self.remember_interpreter,
                                                   interpreter_choice=True)
        if saved_interpreter:
            self.interpreter_path_input.path_var.set(saved_interpreter)
            self.interpreter_path_input.root_dir_input.configure(text_color='white')

        self.interpreter_path_input.grid(row=7, column=0, sticky='ew', padx=50, pady=(0, 10))



    def setup_init_git_button(self):
        self.remember_git = ctk.BooleanVar(value=True)
        self.init_git_button = CheckBoxButton(self.main_container, text='Initialize Local Git Repository',
                                              theme_color=MAIN_THEME_PURPLE,
                                              hover_color=DEEP_PURPLE,
                                              remember_var=self.remember_git,
                                              )
        self.init_git_button.grid(row=8, column=0, sticky='w', padx=50, pady=(0, 10))

    def setup_initialize_button(self):
        self.init_button = ctk.CTkButton(self.main_container, text="Launch",
                                         height=50,
                                         font=('Helvetica', 16, 'bold'),
                                         fg_color=MAIN_THEME_PURPLE,
                                         hover_color=DEEP_PURPLE,
                                         command=self.initialize
                                         )
        self.init_button.grid(row=9, column=0, pady=(40, 10), padx=100, sticky='ew')

        self.init_error_label = ctk.CTkLabel(self.main_container, text_color='red',
                                             font=('Helvetica', 11, 'bold'),
                                             )
        self.init_error_label.grid(row=10, column=0, sticky='ew', padx=50)

    def initialize(self):
        # check for errors
        current_name = self.name_section.name_var.get().strip()
        if current_name=='' or current_name==self.name_section.placeholder:
            self.init_error_label.configure(text='Project name cannot be blank')
            self.init_error_label.grid(row=10, column=0, sticky='ew', padx=50)
            self.name_section.name_entry.configure(border_color='red')
            self.name_section.name_status= 'invalid'
            return

        if self.name_section.name_status == 'invalid':
            self.init_error_label.configure(text='Invalid Name')
            self.init_error_label.grid(row=10, column=0, sticky='ew', padx=50)
            return

        if self.root_dir_selector.root_dir_status == 'invalid':
            self.init_error_label.configure(text='Invalid Root Directory')
            self.init_error_label.grid(row=10, column=0, sticky='ew', padx=50)
            return

        if self.ide_path_input.ide_status == 'invalid':
            self.init_error_label.configure(text='Invalid IDE .exe Path')
            self.init_error_label.grid(row=10, column=0, sticky='ew', padx=50)
            return

        if self.interpreter_path_input.interpreter_status == 'invalid':
            self.init_error_label.configure(text='Invalid Interpreter Input')
            self.init_error_label.grid(row=10, column=0, sticky='ew', padx=50)
            return

        if self.name_section.name_status == 'warning':
            pop = CustomWarningBox(self, "Heads Up",
                                   "Project Name Not Up To Standard Python conventions. Proceed?",
                                   MAIN_THEME_PURPLE, DEEP_PURPLE)
            self.wait_window(pop)
            if not pop.result:
                return

        self.init_error_label.grid_forget()

        settings_to_save = {
            "root_dir": self.root_dir_selector.get(),
            "remember_root_dir": self.remember_root_dir.get(),

            "ide_choice": self.ide_choice_selector.button.get(),
            "remember_ide_choice": self.remember_ide.get(),

            "ide_path": self.ide_path_input.get(),
            "remember_ide_path": self.remember_ide_path.get(),

            "interpreter": self.interpreter_path_input.get(),
            "remember_interpreter": self.remember_interpreter.get()
        }

        self.settings_manager.save_settings(settings_to_save)

        user_input = {
            'project_name': self.name_section.name_var.get(),
            'root_dir': self.root_dir_selector.root_dir_input.get(),
            'ide_choice': self.ide_choice_selector.button.get(),
            'py_interpreter': self.interpreter_path_input.get(),
            'ide_path': self.ide_path_input.get(),
            'init_git': self.init_git.get(),
            'project_type': self.project_type_selector.button.get(),
            'install_libs': True
        }
        self.is_creating = True
        self.init_button.configure(state="disabled", text="Creating Project...")
        self.animate_button()

        threading.Thread(target=self.run_creation, args=(user_input,), daemon=True).start()

    def run_creation(self,user_input):

        self.project_orchestrator = ProjectOrchestrator(user_input)

        success,message = self.project_orchestrator.create_project()

        self.is_creating = False

        if success:
            self.after(0,self.show_success_popup)
            self.after(0, lambda: self.init_button.configure(text=f"Launch {self.name_section.name_var.get()}", state="normal"))

        else:
            self.after(0, lambda: self.init_error_label.configure(text=f"Error: {message}", text_color="red"))
            self.after(0, lambda: self.init_error_label.grid(row=10, column=0, sticky='ew',
                                                             padx=50))
            self.after(0, lambda: self.init_button.configure(state="normal", text="Launch"))

    def show_success_popup(self):
        pop = CustomWarningBox(self, "Success!",
                               message=f"Project Created Successfully, would you like to launch {self.name_section.name_var.get()}?",
                               theme_color=GREEN,
                               hover_color="#1a6341")
        self.wait_window(pop)

        if pop.result:
            # make orchestrator launch
            self.project_orchestrator.launch_ide()
            self.destroy()
        else:
            self.destroy()

    def animate_button(self, count=1):
        if not self.is_creating:
            return

        dots = "." * count
        self.init_button.configure(text=f"Initializing{dots}")

        next_count = count + 1 if count < 3 else 1

        self.after(200, lambda: self.animate_button(next_count))


gui = AppGui()

gui.mainloop()
