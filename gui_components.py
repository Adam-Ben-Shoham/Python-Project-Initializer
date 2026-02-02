import customtkinter as ctk
from gui_verifications import InputValidator
from tkinter import filedialog
from gui_utils import handle_focus_in, handle_focus_out, validate_variable
from gui_settings import SettingsManager


class ValidatedNameInput(ctk.CTkFrame):
    def __init__(self, master, theme_color, init_error_label, dir_selector=None, init_button=None, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)
        self.name_status = None
        self.init_error_label = init_error_label
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
                                       validate='key', validatecommand=validate_command, )

        self.name_entry.grid(row=0, column=0, sticky='ew', pady=(0, 5))

        self.name_entry.insert(0, self.placeholder)
        self.name_entry.configure(text_color=self.placeholder_color)

        self.name_entry.bind("<FocusIn>", lambda e: handle_focus_in(self.name_entry, self.name_var, self.placeholder))
        self.name_entry.bind("<FocusOut>", lambda e: handle_focus_out(self.name_entry, self.name_var, self.placeholder))

        self.name_var.trace_add('write', self.on_change)

    def _validate_limit(self, new_text):
        if new_text == self.placeholder:
            return True

        return len(new_text) <= 31

    def on_change(self, *args):

        if self.name_var.get() != 'Project Name...':
            self.init_button.configure(text=f'Initialize {self.name_var.get()}')
        else:
            self.init_button.configure(text='Initialize')

        root_dir = self.dir_selector.get()
        status, error_message = InputValidator.validate_project_name(self.name_var.get(), root_dir)
        self.name_status = status

        validate_variable(variable=self.name_var.get(),
                          placeholder=self.placeholder,
                          entry=self.name_entry,
                          error_label=self.error_label,
                          status=status,
                          error_message=error_message,
                          theme_color=self.theme_color)

        if status != 'valid' and error_message.strip():
            self.error_label.grid(row=1, column=0, sticky='w')
        else:
            self.error_label.grid_forget()
            self.init_error_label.grid_forget()

    def get(self):
        return self.name_var.get()


class PathSelector(ctk.CTkFrame):
    def __init__(self, master, theme_color, hover_color, placeholder_name, init_error_label, ide_choice=None,
                 remember_var=None,tip=None,interpreter_choice=None, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)
        self.ide_status = None
        self.root_dir_status = None
        self.interpreter_status = None

        self.tip = tip
        self.init_error_label = init_error_label
        self.remember_var = remember_var
        self.interpreter_choice = interpreter_choice

        self.theme_color = theme_color

        self.grid_columnconfigure(0, weight=1)

        self.path_var = ctk.StringVar()

        self.placeholder = placeholder_name
        self.placeholder_color = '#808080'

        self.ide_choice = ide_choice

        self.root_dir_input = ctk.CTkEntry(self, textvariable=self.path_var,
                                           placeholder_text=self.placeholder,
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

        self.remember_dir = self.remember_var if self.remember_var else ctk.BooleanVar(value=False)

        self.remember_button = CheckBoxButton(self, theme_color=self.theme_color,
                                              hover_color=hover_color,
                                              remember_var=self.remember_dir,
                                              text='Remember Path')
        self.remember_button.grid(column=0, row=2, sticky='w', padx=0, pady=(10, 0), columnspan=2)

        if self.tip:
            self.tip_label = ctk.CTkLabel(self, text=tip, text_color='white',
                                        font=('helvetica', 11, 'bold'))
            self.tip_label.grid(column=0, row=1, sticky='w')

        self.error_label = ctk.CTkLabel(self, text='', text_color='red',
                                            font=('helvetica', 11, 'bold'))

        self.path_var.trace_add('write', self.on_change)

    def browse_dir(self):
        if self.ide_choice or self.interpreter_choice:
            folder_path = filedialog.askopenfilename(
                title="Select File",
                filetypes=[("All files", "*.*")]
            )
        else:
            folder_path = filedialog.askdirectory()
        if folder_path:
            self.root_dir_input.delete(0, 'end')
            self.root_dir_input.insert(0, folder_path)

    def get(self):
        return self.path_var.get()

    def on_change(self, *args):

        if self.interpreter_choice:
            status,error_message = InputValidator.validate_executable_path(path_var=self.path_var.get(),interpreter_choice= self.interpreter_choice)
            self.interpreter_status = status
        elif self.ide_choice:
            status, error_message = InputValidator.validate_executable_path(path_var= self.path_var.get(), ide_choice= self.ide_choice)
            self.ide_status = status
        else:
            status, error_message = InputValidator.validate_directory(self.path_var.get())
            self.root_dir_status = status

        validate_variable(variable=self.path_var.get(),
                          placeholder=self.placeholder,
                          entry=self.root_dir_input,
                          error_label=self.error_label,
                          status=status,
                          error_message=error_message,
                          theme_color=self.theme_color,
                          )

        if status != 'valid':

            self.remember_button.grid(column=0, row=3, sticky='w', padx=0, pady=(2, 0), columnspan=2)
            self.error_label.grid(row=2, column=0, sticky='w', padx=5, pady=(0, 0))

        else:

            self.error_label.grid_forget()
            self.remember_button.grid(column=0, row=2, sticky='w', padx=0, pady=(10, 0), columnspan=2)
            self.init_error_label.grid_forget()


class ChoiceSelector(ctk.CTkFrame):
    def __init__(self, master, values, theme_color, hover_color, remember_btn_color, text, initial_value=None,
                 has_remember=False, remember_var=None, command=None, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)

        self.values = values
        self.theme_color = theme_color
        self.hover_color = hover_color
        self.text = text
        self.has_remember = has_remember
        self.remember_var = remember_var
        self.command=command

        self.type_label = ctk.CTkLabel(self, text=f'{text}:',
                                       font=('Helvetica', 12, 'bold'),
                                       text_color='white')

        self.type_label.grid(column=0, row=0, sticky='w', padx=(0, 20), pady=0)

        self.button = ctk.CTkSegmentedButton(self,
                                             values=self.values,
                                             selected_color=theme_color,
                                             selected_hover_color=hover_color,
                                             unselected_color='#2b2b2b',
                                             unselected_hover_color=theme_color,
                                             text_color="white",
                                             fg_color='#2b2b2b',
                                             font=('Helvetica', 12, 'bold'),
                                             height=35,
                                             command=self.command
                                                )
        start_val = initial_value if initial_value in self.values else self.values[0]
        self.after(10, lambda: self.button.set(start_val))

        self.button.grid(row=0, column=1, sticky='w', pady=(10, 0))

        if has_remember:
            self.remember_btn_color = remember_btn_color
            self.remember_button = CheckBoxButton(self, theme_color=self.remember_btn_color,
                                                  hover_color=remember_btn_color,
                                                  remember_var=self.remember_var,
                                                  text=f'Remember {self.text}',
                                                  )
            self.remember_button.grid(column=0, row=1, sticky='w', columnspan=2, pady=(5, 0))


class InitButton(ctk.CTkFrame):
    def __init__(self, master, theme_color, **kwargs):
        super().__init__(master, **kwargs)
        self.theme_color = theme_color


class CheckBoxButton(ctk.CTkFrame):
    def __init__(self, master, theme_color, hover_color, remember_var, text, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)

        self.theme_color = theme_color
        self.hover_color = hover_color
        self.remember_var = remember_var
        self.text = text

        self.remember_button = ctk.CTkCheckBox(self, text=f'{text}',
                                               fg_color=theme_color,
                                               hover_color=hover_color,
                                               variable=remember_var,
                                               checkbox_height=18,
                                               checkbox_width=18,
                                               font=('Helvetica', 12, 'bold'))
        self.remember_button.pack(padx=0, pady=0)

class CustomWarningBox(ctk.CTkToplevel):
    def __init__(self, master, title, message, theme_color, hover_color):
        super().__init__(master)
        self.title(title)
        self.geometry("400x200")
        self.result = False  # Track user choice

        # Center the window
        self.attributes("-topmost", True)
        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text=message, font=('Helvetica', 12), wraplength=350)
        self.label.pack(pady=30)

        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        self.yes_btn = ctk.CTkButton(self.btn_frame, text="Proceed", fg_color=theme_color,
                                     hover_color=hover_color, width=100, command=self.on_yes)
        self.yes_btn.grid(row=0, column=0, padx=10)

        self.no_btn = ctk.CTkButton(self.btn_frame, text="Cancel", fg_color="#444",
                                    width=100, command=self.on_no)
        self.no_btn.grid(row=0, column=1, padx=10)

    def on_yes(self):
        self.result = True
        self.destroy()

    def on_no(self):
        self.result = False
        self.destroy()
