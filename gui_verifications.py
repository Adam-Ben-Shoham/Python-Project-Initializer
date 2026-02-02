import os
import re

MAX_NAME_LENGTH = 30
SUB_OPTIMAL_LENGTH = 20


class InputValidator:

    @staticmethod
    def validate_project_name(name, root_path=None):

        # allow an empty name
        if name == '' or name == 'Project Name...':
            return 'valid', ''

        # red errors - invalid:

        # dont allow a name longer than 30 chars
        if len(name) > MAX_NAME_LENGTH:
            return 'invalid', 'Project name cannot be over 30 characters long'

        # dont allow name that starts with a digit
        if name[0].isdigit():
            return 'invalid', 'Project name cannot start with a number'

        if not re.match(r'^[a-zA-Z0-9_]*$', name):
            return 'invalid', 'Only use letters,numbers and underscores'


        if not root_path or root_path=='' or root_path == 'Root Directory...':
            pass

        # collision checks - invalid and warnings:
        else:
            full_path = os.path.join(root_path, name)
            if os.path.exists(full_path):
                return 'invalid', 'A folder with this name already exists inside the selected directory'

            parent_folder_name = os.path.basename(root_path).lower()
            if parent_folder_name == name.lower():
                return 'warning', 'Convention: Folder name and Project name cannot be identical'

        # yellow errors - warning:

        if any(char.isupper() for char in name):
            return 'warning', 'Convention: Lowercase characters are conventional in project names'

        if len(name) > SUB_OPTIMAL_LENGTH:
            return 'warning', 'Convention: Try keeping project name under 20 characters'

        if name.startswith('_'):
            return 'warning', 'Convention: "_" in the beginning usually means "private"'

        return 'valid', ''

    @staticmethod
    def validate_directory(path_var):
        if not path_var or path_var == 'Root Directory...' or path_var == '':
            return 'valid', ''

        if path_var.startswith('"') or path_var.endswith('"'):
            return 'invalid', 'Remove quotes from the start or end of the path'

        if not os.path.exists(path_var):
            return 'warning', 'Path does not exist'

        if not os.path.isdir(path_var):
            return 'invalid', 'Path is not a directory'

        if not os.access(path_var, os.W_OK):
            return 'invalid', 'No writing permission for this directory'

        return 'valid', ''

    @staticmethod
    def validate_executable_path(path_var,ide_choice=None,interpreter_choice=None):

        if not path_var or path_var == "Select IDE Path..." or path_var== 'Select Interpreter' or path_var == '':
            return 'valid', ''

        if path_var.startswith('"') or path_var.endswith('"'):
            return 'invalid', 'Remove quotes from the start or end of the path'

        if not os.path.exists(path_var):
            return 'warning', 'Path does not exist'

        if not path_var.lower().endswith('.exe'):
            return 'invalid', 'Path must point to an executable (extension: ".exe")'

        file_name = os.path.basename(path_var)

        if not interpreter_choice:
            if ide_choice=='PyCharm':
                if 'pycharm' not in file_name:
                    return 'invalid', "Looks like this path doesn't point to a PyCharm executable"

            elif ide_choice=='VSCode':
                if 'code' not in file_name.lower():
                    return 'invalid', "Looks like this path doesn't point to a VSCode executable"
        else:
            if file_name != 'python.exe':
                return 'invalid', "Looks like this path doesn't point to a Python interpreter executable"

        return 'valid', ''



