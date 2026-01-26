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
            raise RuntimeError(f'Unexpected error ocurred while creating project folder at {path}')

    @staticmethod
    def build_venv(path):
        venv_path = os.path.join(path, '.venv')