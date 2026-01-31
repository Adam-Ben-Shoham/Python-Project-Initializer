import customtkinter as ctk
from gui_verifications import InputValidator
from tkinter import filedialog
from gui_utils import handle_focus_in, handle_focus_out, validate_variable
from gui_settings import SettingsManager


class ValidatedNameInput(ctk.CTkFrame):
    def __init__(self, master, theme_color, dir_selector=None, init_button=None, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)
        self.theme_color = theme_color
        self.dir_selector = dir_selector
        self.init_button = init_button

        self.placeholder = "Project Name..."
        self.placeholder_color = '#808080'

        self.grid_columnconfigure(0, weight=1)

        self.error_label = ctk.CTkLabel(self, text='', text_color='red',
                                        font=('helvetica', 11, 'bold'))

        self.name_var = ctk.StringVar()

        validate_command = (self.register(self._validate_limit), '%P')

        self.name_entry = ctk.CTkEntry(self, textvariable=self.name_var,
                                       height=35, border_color=theme_color,
                                       validate='key', validatecommand=validate_command,)

        self.name_entry.grid(row=0, column=0, sticky='ew', pady=(0, 5))

        self.name_entry.insert(0, self.placeholder)
        self.name_entry.configure(text_color=self.placeholder_color)

        self.name_entry.bind("<FocusIn>", lambda e: handle_focus_in(self.name_entry, self.name_var, self.placeholder))
        self.name_entry.bind("<FocusOut>", lambda e: handle_focus_out(self.name_entry, self.name_var, self.placeholder))

        self.name_var.trace_add('write', self.on_change)

    def _validate_limit(self,new_text):
        if new_text == self.placeholder:
            return True

        return len(new_text) <= 31

    def on_change(self, *args):

        self.init_button.configure(text=f'Initialize {self.name_var.get()}')
        root_dir = self.dir_selector.get()
        status, error_message = InputValidator.validate_project_name(self.name_var.get(), root_dir)

        validate_variable(variable=self.name_var.get(),
                          placeholder=self.placeholder,
                          entry=self.name_entry,
                          error_label=self.error_label,
                          status=status,
                          error_message=error_message,
                          theme_color=self.theme_color)

        if status != 'valid':
            self.error_label.grid(row=1, column=0, sticky='w')
        else:
            self.error_label.grid_forget()

    def get(self):
        return self.name_var.get()


class DirectorySelector(ctk.CTkFrame):
    def __init__(self, master, theme_color, hover_color, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)
        self.theme_color = theme_color

        self.grid_columnconfigure(0, weight=1)

        self.path_var = ctk.StringVar()

        self.placeholder = 'Root Directory...'
        self.placeholder_color = '#808080'

        self.root_dir_input = ctk.CTkEntry(self, textvariable=self.path_var,
                                           placeholder_text='Project Root Directory...',
                                           height=35,
                                           border_color=self.theme_color)
        self.root_dir_input.grid(row=0, column=0, sticky='ew', padx=(0, 10))

        self.root_dir_input.bind("<FocusIn>",
                                 lambda e: handle_focus_in(self.root_dir_input, self.path_var, self.placeholder))
        self.root_dir_input.bind("<FocusOut>",
                                 lambda e: handle_focus_out(self.root_dir_input, self.path_var, self.placeholder))

        self.root_dir_input.insert(0, self.placeholder)
        self.root_dir_input.configure(text_color=self.placeholder_color)

        self.browse_button = ctk.CTkButton(self, text='Browse...',
                                           width=15,
                                           command=self.browse_dir,
                                           fg_color=theme_color,
                                           hover_color=hover_color)
        self.browse_button.grid(row=0, column=1, padx=0, pady=0)

        self.remember_dir = ctk.BooleanVar(value=False)
        self.remember_button = RememberButton(self,theme_color=self.theme_color,
                                              hover_color=hover_color,
                                              remember_var=self.remember_dir,
                                              name_of_input='Directory')
        self.remember_button.grid(column=0, row=1, sticky='w', padx=0, pady=(10, 0), columnspan=2)

        self.error_label = ctk.CTkLabel(self, text='', text_color='red',
                                        font=('helvetica', 11, 'bold'))

        self.path_var.trace_add('write', self.on_change)

    def browse_dir(self):
        folder_path = filedialog.askdirectory()

        if folder_path:
            self.root_dir_input.delete(0, 'end')
            self.root_dir_input.insert(0, folder_path)

    def get(self):
        return self.path_var.get()

    def on_change(self, *args):
        status, error_message = InputValidator.validate_root_dir(self.path_var.get())

        validate_variable(variable=self.path_var.get(),
                          placeholder=self.placeholder,
                          entry=self.root_dir_input,
                          error_label=self.error_label,
                          status=status,
                          error_message=error_message,
                          theme_color=self.theme_color)

        if status != 'valid':

            self.remember_button.grid(column=0, row=2, sticky='w', padx=0, pady=(2, 0), columnspan=2)
            self.error_label.grid(row=1, column=0, sticky='w', padx=5, pady=(0, 0))

        else:
            self.error_label.grid_forget()
            self.remember_button.grid(column=0, row=1, sticky='w', padx=0, pady=(10, 0), columnspan=2)


class InitButton(ctk.CTkFrame):
    def __init__(self, master, theme_color, **kwargs):
        super().__init__(master, **kwargs)
        self.theme_color = theme_color

class RememberButton(ctk.CTkFrame):
    def __init__(self, master, theme_color,hover_color,remember_var, name_of_input, **kwargs):
        super().__init__(master,fg_color='transparent', **kwargs)

        self.theme_color = theme_color
        self.hover_color = hover_color
        self.remember_var = remember_var
        self.name_of_input = name_of_input

        self.remember_button = ctk.CTkCheckBox(self, text=f'Remember {name_of_input}',
                                               fg_color=theme_color,
                                               hover_color=hover_color,
                                               variable=remember_var,
                                               checkbox_height=22,
                                               checkbox_width=22,
                                               font=('Helvetica', 12, 'bold'))
        self.remember_button.pack(padx=0, pady=0)
