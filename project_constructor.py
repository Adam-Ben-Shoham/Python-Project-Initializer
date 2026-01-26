import os,subprocess

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
    def build_venv(py_path,path):
        venv_path = os.path.join(path, '.venv')

        command_list = [py_path,'-m','venv',venv_path]

        try:
            subprocess.run(command_list,check=True,capture_output=True,text=True)
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip()
            raise RuntimeError(error_msg)
        except PermissionError:
            raise RuntimeError(f'The virtual environment cannot be created. Permission denied at {path}')

        activation_script_path = os.path.join(venv_path,'Scripts','activate')

        if not os.path.exists(activation_script_path):
            raise RuntimeError(f'Activation script missing, virtual environment may be corrupted.')

        return venv_path