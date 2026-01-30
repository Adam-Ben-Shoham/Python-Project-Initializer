import customtkinter as ctk
from gui_verifications import InputValidator

class ValidatedNameInput(ctk.CTkFrame):
    def __init__(self, master, theme_color, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)
        self.theme_color = theme_color
        self.placeholder = "Project Name..."
        self.placeholder_color = '#808080'

        self.grid_columnconfigure(0, weight=1)

        self.name_var = ctk.StringVar()

        self.name_entry = ctk.CTkEntry(self, textvariable=self.name_var,
                                       height=35, border_color=theme_color)
        self.name_entry.grid(row=0, column=0, sticky='ew')

        self.name_entry.insert(0, self.placeholder)
        self.name_entry.configure(text_color=self.placeholder_color)

        self.name_entry.bind("<FocusIn>", self._clear_placeholder)
        self.name_entry.bind("<FocusOut>", self._add_placeholder)

        self.name_var.trace_add('write', self.on_change)

        self.error_label = ctk.CTkLabel(self, text='', text_color='red',
                                        font=('helvetica', 11, 'bold'))
        self.error_label.grid(row=1, column=0, sticky='w', padx=5, pady=(0, 0))

    def _clear_placeholder(self, event):
        if self.name_var.get() == self.placeholder:
            self.name_entry.delete(0, 'end')
            self.name_entry.configure(text_color='white')

    def _add_placeholder(self, event):
        if self.name_var.get() == "":
            self.name_entry.insert(0, self.placeholder)
            self.name_entry.configure(text_color=self.placeholder_color)

    def on_change(self, *args):
        status, error_message = InputValidator.validate_project_name(self.name_var.get())

        current_text = self.name_var.get()

        if current_text == self.placeholder or current_text == "":
            self.error_label.configure(text="")
            self.name_entry.configure(border_color=self.theme_color)
            return

        if status == 'invalid':
            color = 'red'
        elif status == 'warning':
            color = '#FFCC00'
        else:
            color = self.theme_color

        self.error_label.configure(text=error_message, text_color=color)
        self.name_entry.configure(border_color=color)

    def get(self):
        return self.name_var.get()
