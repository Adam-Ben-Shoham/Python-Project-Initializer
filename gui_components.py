import customtkinter as ctk
from gui_verifications import InputValidator
from tkinter import filedialog
from gui_utils import handle_focus_in, handle_focus_out, validate_variable


class ValidatedNameInput(ctk.CTkFrame):
    def __init__(self, master, theme_color, error_feedback_label, dir_selector=None, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)
        self.name_status = None
        self.error_feedback_label = error_feedback_label
        self.theme_color = theme_color
        self.dir_selector = dir_selector

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

        if status == 'valid':
            self.name_entry.configure(border_color=self.theme_color)
            self.error_feedback_label.grid_forget()
            self.error_label.grid_forget()

        elif status == 'warning':
            self.name_entry.configure(border_color='#FFCC00')
            self.error_feedback_label.grid_forget()

            if error_message.strip():
                self.error_label.configure(text=error_message, text_color='#FFCC00')
                self.error_label.grid(row=1, column=0, sticky='w')

        else:
            if error_message.strip():
                self.error_label.configure(text=error_message, text_color='red')
                self.error_label.grid(row=1, column=0, sticky='w')

    def get(self):
        val = self.name_var.get()
        return "" if val == self.placeholder else val.strip()


class PathSelector(ctk.CTkFrame):
    def __init__(self, master, theme_color, hover_color, placeholder_name, error_feedback_label, ide_choice=None,
                 remember_var=None, tip=None, interpreter_choice=None, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)
        self.ide_status = None
        self.root_dir_status = None
        self.interpreter_status = None

        self.tip = tip
        self.error_feedback_label = error_feedback_label
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
                                              variable=self.remember_dir,
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
        val = self.path_var.get()
        return "" if val == self.placeholder else val.strip()

    def on_change(self, *args):

        if self.interpreter_choice:
            status, error_message = InputValidator.validate_executable_path(path_var=self.path_var.get(),
                                                                            interpreter_choice=self.interpreter_choice)
            self.interpreter_status = status
        elif self.ide_choice:
            status, error_message = InputValidator.validate_executable_path(path_var=self.path_var.get(),
                                                                            ide_choice=self.ide_choice)
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
            self.error_feedback_label.grid_forget()


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
        self.command = command

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
                                                  variable=self.remember_var,
                                                  text=f'Remember {self.text}',
                                                  )
            self.remember_button.grid(column=0, row=1, sticky='w', columnspan=2, pady=(5, 0))


class CheckBoxButton(ctk.CTkFrame):
    def __init__(self, master, theme_color, hover_color, variable, text, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)

        self.theme_color = theme_color
        self.hover_color = hover_color
        self.variable = variable
        self.text = text

        self.remember_button = ctk.CTkCheckBox(self, text=f'{text}',
                                               fg_color=theme_color,
                                               hover_color=hover_color,
                                               variable=variable,
                                               checkbox_height=18,
                                               checkbox_width=18,
                                               font=('Helvetica', 12, 'bold'))
        self.remember_button.pack(padx=0, pady=0)

    def set_text(self, new_text):
        self.remember_button.configure(text=new_text)


class CustomWarningBox(ctk.CTkToplevel):
    def __init__(self, master, title, message, theme_color, hover_color):
        super().__init__(master)
        self.title(title)

        master_x = master.winfo_x()
        master_y = master.winfo_y()
        master_width = master.winfo_width()

        pop_width = 350
        pop_height = 200

        x = master_x + master_width + 50
        y = master_y + 280

        self.geometry(f"{pop_width}x{pop_height}+{x}+{int(y)}")

        self.result = False

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


class ValidatedUrlField(ctk.CTkFrame):
    def __init__(self, master, theme_color, error_feedback_label, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)

        self.url_status = None
        self.error_feedback_label = error_feedback_label
        self.theme_color = theme_color

        self.placeholder = "https://github.com/user/repository.git"
        self.placeholder_color = '#808080'

        self.grid_columnconfigure(0, weight=1)

        self.error_label = ctk.CTkLabel(self, text='', text_color='red',
                                        font=('Helvetica', 11, 'bold'))

        self.url_var = ctk.StringVar()

        self.url_entry = ctk.CTkEntry(self, textvariable=self.url_var,
                                      height=35, border_color=theme_color)
        self.url_entry.grid(row=0, column=0, sticky='ew', pady=(0, 5))

        self.url_entry.insert(0, self.placeholder)
        self.url_entry.configure(text_color=self.placeholder_color)

        self.url_entry.bind("<FocusIn>", lambda e: handle_focus_in(self.url_entry, self.url_var, self.placeholder))
        self.url_entry.bind("<FocusOut>", lambda e: handle_focus_out(self.url_entry, self.url_var, self.placeholder))

        self.url_var.trace_add('write', self.on_change)

    def on_change(self, *args):
        current_val = self.url_var.get()

        status, error_message = InputValidator.validate_git_url(current_val)
        self.url_status = status

        validate_variable(variable=current_val,
                          placeholder=self.placeholder,
                          entry=self.url_entry,
                          error_label=self.error_label,
                          status=status,
                          error_message=error_message,
                          theme_color=self.theme_color)

        if status != 'valid' and current_val != self.placeholder and current_val.strip() != "":
            self.error_label.grid(row=1, column=0, sticky='w')
        else:
            self.error_label.grid_forget()
            if status == 'valid':
                self.error_feedback_label.grid_forget()

    def get(self):
        val = self.url_var.get()
        return "" if val == self.placeholder else val.strip()


class LoadingPopup(ctk.CTkToplevel):
    def __init__(self, master, project_name):
        super().__init__(master)
        self.title("Progress")

        master_x = master.winfo_x()
        master_y = master.winfo_y()
        master_width = master.winfo_width()

        pop_width = 350
        pop_height = 200

        x = master_x + master_width + 50
        y = master_y + 280

        self.geometry(f"{pop_width}x{pop_height}+{x}+{int(y)}")

        self.attributes("-topmost", True)
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)

        self.transient(master)
        self.grab_set()

        self.label = ctk.CTkLabel(self, text=f"Initializing {project_name}",
                                  font=('Helvetica', 18, 'bold'))
        self.label.grid(row=0, column=0, pady=(30, 5))

        self.dots_label = ctk.CTkLabel(self, text="...", font=('Helvetica', 24, 'bold'))
        self.dots_label.grid(row=1, column=0, pady=5)

        self.sub_label = ctk.CTkLabel(self,
                                      text="This may take a minute...   \n",
                                      font=('Helvetica', 12), text_color="gray")
        self.sub_label.grid(row=2, column=0, pady=(10, 20))

        self.dot_count = 0
        self.animate_dots()

    def animate_dots(self):
        if not self.winfo_exists(): return
        self.dot_count = (self.dot_count + 1) % 4
        self.dots_label.configure(text="." * self.dot_count)
        self.after(500, self.animate_dots)

class DescriptionBox(ctk.CTkFrame):
    def __init__(self, master, theme_color, hover_color,max_chars):
        super().__init__(master,fg_color='transparent')
        self.theme_color = theme_color
        self.hover_color = hover_color
        self.max_chars = max_chars

        self.height = 90


        self.box_label = ctk.CTkLabel(self,text='Optional: Describe your project to get AI generated name suggestions')
        self.box_label.grid(row=0, column=0,sticky = 'w', pady=(10,5))

        self.placeholder = 'Project Description...'
        self.placeholder_color = '#808080'
        self.description_var = ctk.StringVar()

        self.grid_columnconfigure(0, weight=1)

        self.counter_label = ctk.CTkLabel(self, text=f"0/{self.max_chars}", font=("helvetica", 11),
                                          text_color="#808080")
        self.counter_label.grid(row=0, column=0, sticky='e', pady=(10, 5))

        self.description_entry = ctk.CTkTextbox(self,height=self.height,
                                              border_color=theme_color,
                                                border_width=2,
                                                fg_color='#333333',
                                               )

        self.description_entry.insert(0.0, self.placeholder)
        self.description_entry.configure(text_color=self.placeholder_color)

        self.description_entry.bind("<FocusIn>", self.handle_focus_in)
        self.description_entry.bind("<FocusOut>", self.handle_focus_out)
        self.description_entry.bind("<KeyRelease>", self.update_counter)
        self.description_entry.bind("<Key>", self.check_limit)

        self.description_entry.grid(row=1, column=0, sticky='ew', pady=(10, 5))


    def update_counter(self,event=None):

        content = self.description_entry.get("0.0", "end-1c")

        if content == self.placeholder:
            count = 0
        else:
            count = len(content)

        if count > self.max_chars:
            self.description_entry.delete("0.0 + 200 chars", "end")
            count = self.max_chars

        self.counter_label.configure(text=f"{count}/{self.max_chars}")

        if count >= self.max_chars:
            self.counter_label.configure(text_color="#FF4B4B")
        else:
            self.counter_label.configure(text_color="#808080")

    def check_limit(self, event):

        if event.keysym in ("BackSpace", "Delete", "Left", "Right", "Up", "Down"):
            return

        current_text = self.description_entry.get("0.0", "end-1c")

        if len(current_text) >= self.max_chars:
            try:
                if not self.description_entry.tag_ranges("sel"):
                    return "break"
            except:
                return "break"

    def handle_focus_in(self, event):
        current_text = self.description_entry.get("0.0", "end-1c")
        if current_text == self.placeholder:
            self.description_entry.delete("0.0", "end")
            self.description_entry.configure(text_color='white')
        self.update_counter()

    def handle_focus_out(self, event):
        current_text = self.description_entry.get("0.0", "end-1c").strip()
        if not current_text:
            self.description_entry.insert("0.0", self.placeholder)
            self.description_entry.configure(text_color=self.placeholder_color)
        self.update_counter()

    def get(self):
        val = self.description_entry.get("0.0", "end-1c")
        return "" if val == self.placeholder else val

