import os
import platform
import re
import subprocess
import sys

from project_constructor import ProjectConstructor

CREATE_NO_WINDOW = 0x08000000


class ProjectOrchestrator:
    def __init__(self, input_dict):
        self._clean_inputs(input_dict)

    def _clean_inputs(self, input_dict):
        ## clean and validate the project name chosen by the user

        self.project_name = clean_and_validate_project_name(input_dict['project_name'])

        ## clean and validate the root directory chosen by the user

        self.root_dir = validate_directory(input_dict['root_dir'])

        ## check if the final path is valid and if it already exists
        final_path = os.path.join(self.root_dir, self.project_name)

        if len(final_path) > 260:
            raise ValueError('The project final path cannot be longer than 260 characters.')

        if os.path.exists(final_path):
            raise ValueError('The project folder already exists.')

        self.final_path = final_path

        ## validate the executables

        self.ide_path = validate_executable(input_dict['ide_path'])

        self.py_interpreter = validate_executable(input_dict['py_interpreter'])

        ## validate the git section

        self.init_git = input_dict['init_git']

        if self.init_git:

            self.connect_repo = input_dict['connect_repo']

            if self.connect_repo:
                self.remote_git_url = validate_git_url(input_dict['remote_git_url'])

        ## assign variables for the rest

        self.ide_choice = input_dict['ide_choice']

        self.project_type = input_dict['project_type']

        self.install_libs = input_dict['install_libs']

    def create_project(self):

        try:
            ProjectConstructor.build_folder(self.final_path)

            venv_path = ProjectConstructor.build_venv(self.py_interpreter, self.final_path)

            from constants import PROJECT_TEMPLATES

            template = PROJECT_TEMPLATES.get(self.project_type, PROJECT_TEMPLATES['Basic'])
            libraries = '\n'.join(template['libraries'])
            ProjectConstructor.write_file('requirements.txt', self.final_path, libraries)

            gitignore_content = self.generate_gitignore()

            ProjectConstructor.write_file('.gitignore', self.final_path, gitignore_content)

            main_content = template['content']
            ProjectConstructor.write_file('main.py', self.final_path, main_content)

            if self.install_libs and libraries:
                ProjectConstructor.install_required_libs(venv_path, self.final_path)

            if self.init_git:
                ProjectConstructor.create_local_git_repo(self.final_path)

                if self.connect_repo and self.remote_git_url:
                    ProjectConstructor.connect_remote_git_repo(self.final_path, self.remote_git_url)

            if self.ide_choice == 'VS Code':
                vscode_folder = os.path.join(self.final_path, '.vscode')

                if not os.path.exists(vscode_folder):
                    os.makedirs(vscode_folder)

                trust_json = '{\n    "security.workspace.trust.enabled": false\n}'
                ProjectConstructor.write_file('settings.json', vscode_folder, trust_json)

            return True, 'success'
        except Exception as e:

            return False, f"Project Creation Error: {str(e)}"

    def launch_ide(self):

        ProjectConstructor.launch_ide(self.ide_path, self.final_path)

    def generate_gitignore(self):
        from constants import IGNORE_DICT

        gitignore_file = [IGNORE_DICT.get('python', '## Python block missing ##')]

        current_os = platform.system().lower()

        os_map = {
            'windows': 'windows',
            'darwin': 'macos',
            'linux': 'linux'
        }

        selected_os = os_map.get(current_os, None)

        if selected_os:
            gitignore_file.append(IGNORE_DICT.get(selected_os, f'## {selected_os} block missing ##'))

        if self.ide_choice == 'PyCharm':
            gitignore_file.append(IGNORE_DICT.get('pycharm', '## PyCharm block missing ##'))
        elif self.ide_choice == 'VS Code':
            gitignore_file.append(IGNORE_DICT.get('vscode', '## VS-Code block missing ##'))

        return '\n\n'.join(gitignore_file)

    def _run_silent_command(self, command):

        return subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,

            creationflags=CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )


def clean_and_validate_project_name(name):
    chars_to_clean = r'<>:"/\|?*'
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

    dir_input = os.path.normpath(dir_input)

    dir_input = os.path.abspath(dir_input)

    drive, path_tail = os.path.splitdrive(dir_input)

    # check if the
    if drive:
        if not os.path.exists(drive + os.sep):
            raise ValueError(f'The directory {drive} does not exist or not connected to your computer')

    if len(dir_input) > 260:
        raise ValueError('Directory path cannot contain more than 260 characters')

    if not os.path.exists(dir_input):
        raise ValueError(f'Directory path does not exist: {dir_input}')

    if not os.path.isdir(dir_input):
        raise ValueError('Root directory is not a directory')

    if not os.access(dir_input, os.W_OK):
        raise ValueError('Root directory is not writable')

    return dir_input


def validate_executable(executable):
    executable = executable.strip().strip('"')

    if not executable:
        raise ValueError(f'The executable path cannot be empty')

    executable = os.path.normpath(executable)

    executable = os.path.abspath(executable)

    if not os.path.isfile(executable):
        raise ValueError(f'{executable} is not a file')

    if not os.access(executable, os.X_OK):
        raise ValueError(f'{executable} is not permitted for execution')

    return executable


def validate_git_url(url):
    pattern = r"^https://[a-zA-Z0-9.-]+/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+\.git$"
    if not re.match(pattern, url.strip()):
        url = ''
        raise ValueError(f'{url} is not a valid git url')

    return url


