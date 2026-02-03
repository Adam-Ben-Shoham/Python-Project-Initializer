import os, subprocess
import platform

CREATE_NO_WINDOW = 0x08000000

class ProjectConstructor:

    @staticmethod
    def _run_silent(command, cwd=None, is_popen=False):
        """Helper to execute subprocesses without flashing console windows."""
        flags = CREATE_NO_WINDOW if platform.system() == 'Windows' else 0
        if is_popen:
            return subprocess.Popen(command, creationflags=flags)
        return subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True, creationflags=flags)

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
            ProjectConstructor._run_silent(command_list)
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
            ProjectConstructor._run_silent(command, cwd=path)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f'Git repo not initialized. Git may not be installed. error:{e.stderr}')
        except FileNotFoundError:
            raise RuntimeError(f'Git command not found. Make sure you have git installed in {path}')

    @staticmethod
    def connect_remote_git_repo(project_path, remote_git_url):
        try:
            if not os.path.exists(os.path.join(project_path, ".git")):
                ProjectConstructor._run_silent(["git", "init"], cwd=project_path)

            check_remote = ProjectConstructor._run_silent(["git", "remote"], cwd=project_path)

            if 'origin' in check_remote.stdout:
                ProjectConstructor._run_silent(["git", "remote", "set-url", "origin", remote_git_url], cwd=project_path)
            else:
                ProjectConstructor._run_silent(["git", "remote", "add", "origin", remote_git_url], cwd=project_path)

            ProjectConstructor._run_silent(["git", "branch", "-M", "main"], cwd=project_path)

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f'Remote git repo not initialized. error:{e.stderr}')
        except FileNotFoundError:
            raise RuntimeError(f'Git command not found. Make sure you have git installed in {project_path}')

    @staticmethod
    def install_required_libs(venv_path, project_path):
        if platform.system() == 'Windows':
            python_venv_exe = os.path.join(venv_path, 'Scripts', 'python.exe')
        else:
            python_venv_exe = os.path.join(venv_path, 'bin', 'python')

        required_libs_file = os.path.join(project_path, 'requirements.txt')
        if not os.path.exists(required_libs_file) or os.path.getsize(required_libs_file) == 0:
            return

        upgrade_pip_command = [python_venv_exe, '-m', 'pip', 'install', '--upgrade', 'pip']
        install_command = [python_venv_exe, '-m', 'pip', 'install', '-r', required_libs_file]
        try:
            ProjectConstructor._run_silent(upgrade_pip_command)
            ProjectConstructor._run_silent(install_command)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f'Required libraries installation failed. error:{e.stderr}')

    @staticmethod
    def launch_ide(ide_path, project_path):
        command = [ide_path, project_path]
        try:
            subprocess.Popen(command, shell=False)
        except Exception as e:
            raise RuntimeError(f'Launching IDE failed: {e}')