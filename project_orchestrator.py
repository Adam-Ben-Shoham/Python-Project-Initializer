import os

# project_name,root_dir,ide_choice,py_interpreter,ide_path,init_git,project_type
class ProjectOrchestrator:
    def __init__(self,input_dict):
        self._clean_inputs(input_dict)

    def _clean_inputs(self,input_dict):

        ## clean and validate the project name chosen by the user

        project_name = clean_and_validate_project_name(input_dict['project_name'])

        ## clean and validate the root directory chosen by the user

        root_dir = validate_directory(input_dict['root_dir'])


def clean_and_validate_project_name(name):

    chars_to_clean = '<>:"/\|?*'
    reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'LPT1']

    name = name.strip().replace(' ', '_')

    if not name:
        raise ValueError('Project name cannot be empty')

    if name.upper() in reserved_names:
        raise ValueError(f'Project can not be named: {reserved_names}')

    for char in name:
        if char in chars_to_clean:
            raise ValueError(f'Project name cannot contain these characters: {chars_to_clean}')

    return name

def validate_directory(dir_input):
    dir_input = dir_input.strip()

    if not dir_input:
        raise ValueError('Directory path cannot be empty')

    if len(dir_input) > 260:
        raise ValueError('Directory path cannot contain more than 260 characters')

    dir_input = os.path.normpath(dir_input)

    dir_input = os.path.abspath(dir_input)

    drive, path_tail = os.path.splitdrive(dir_input)

    # check if the
    if drive:
        if not os.path.exists(drive + os.sep):
            raise ValueError(f'The directory {drive} does not exist or not connected to your computer')

    if not os.path.exists(dir_input):
        raise ValueError(f'Directory path does not exist: {dir_input}')

    if not os.path.isdir(dir_input):
        raise ValueError('Root directory is not a directory')

    if not os.access(dir_input, os.W_OK):
        raise ValueError('Root directory is not writable')

    return dir_input
