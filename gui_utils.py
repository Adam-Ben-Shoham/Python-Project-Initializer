def handle_focus_in(entry, string_var, placeholder, text_color='white'):
    if string_var.get() == placeholder:
        entry.delete(0, 'end')
        entry.configure(text_color=text_color)


def handle_focus_out(entry, string_var, placeholder, placeholder_color='#808080'):
    if string_var.get() == "":
        entry.insert(0, placeholder)
        entry.configure(text_color=placeholder_color)


def validate_variable(variable, placeholder, entry, error_label, status, error_message, theme_color):
    if variable == placeholder or variable == "":
        error_label.configure(text="")
        entry.configure(border_color=theme_color)
        return

    if status == 'invalid':
        color = 'red'
    elif status == 'warning':
        color = '#FFCC00'  # warning yellow
    else:
        color = theme_color

    error_label.configure(text=error_message, text_color=color)
    entry.configure(border_color=color)
