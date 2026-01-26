import os, subprocess
import platform


class ProjectConstructor:

    @staticmethod
    def build_folder(path):
        try:
            os.makedirs(path, exist_ok=False)
        except FileExistsError:
            raise ValueError('The project folder already exists.')
        except PermissionError:
            raise RuntimeError(f'The project folder cannot be created. Permission denied at {path}')
        except Exception as e:
            raise RuntimeError(f'Unexpected error occurred while creating project folder at {path}')

    @staticmethod
    def build_venv(py_path, path):
        venv_path = os.path.join(path, '.venv')

        command_list = [py_path, '-m', 'venv', venv_path]

        try:
            subprocess.run(command_list, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip()
            raise RuntimeError(error_msg)
        except PermissionError:
            raise RuntimeError(f'The virtual environment cannot be created. Permission denied at {path}')

        if platform.system() == 'Windows':
            activation_script_path = os.path.join(venv_path, 'Scripts', 'activate')
        else:
            activation_script_path = os.path.join(venv_path, 'bin', 'activate')

        if not os.path.exists(activation_script_path):
            raise RuntimeError(f'Activation script missing in {venv_path}, virtual environment may be corrupted.')

        return venv_path

    @staticmethod
    def write_file(file_name, file_path, content):
        complete_path = os.path.join(file_path, file_name)

        try:
            with open(complete_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise RuntimeError(f'Unable to create {file_name} at {file_path} due to an error: {e}')

    @staticmethod
    def create_local_git_repo(path):

        command = ['git', 'init']

        try:
            subprocess.run(command, cwd=path, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f'Git repo not initialized. Git may not be installed. error:{e.stderr}')
        except FileNotFoundError:
            raise RuntimeError(f'Git command not found. Make sure you have git installed in {path}')

    @staticmethod
    def install_required_libs(venv_path,project_path):

        if platform.system() == 'Windows':
            pip_path = os.path.join(venv_path, 'Scripts', 'pip.exe')
        else:
            pip_path = os.path.join(venv_path, 'bin', 'pip')

        required_libs_file = os.path.join(project_path, 'requirements.txt')

        if not os.path.exists(required_libs_file) or os.path.getsize(required_libs_file) == 0:
            return

        install_command = [pip_path,'install', '-r', required_libs_file]
        upgrade_pip_command = [pip_path, 'install', '--upgrade', 'pip']
        try:
            subprocess.run(upgrade_pip_command,check=True, capture_output=True, text=True)

            subprocess.run(install_command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f'Required libraries installation failed. error:{e.stderr}')