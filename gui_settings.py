import json
import os

SETTINGS_FILE = "settings.json"


class SettingsManager:
    @staticmethod
    def load_settings():

        defaults = {
            "root_dir": "",
            "remember_root_dir": False,
            "ide_choice": "None",
            "remember_ide_choice": False,
            "ide_path": "",
            "remember_ide_path": False,
            "interpreter": "",
            "remember_interpreter": False,
        }

        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    data = json.load(f)
                    return {**defaults, **data}
            except (json.JSONDecodeError, IOError):
                return defaults
        return defaults

    @staticmethod
    def save_settings(settings_dict):

        final_data = {
            "root_dir": settings_dict["root_dir"] if settings_dict.get("remember_root_dir") else "",
            "remember_root_dir": settings_dict.get("remember_root_dir", False),

            "ide_choice": settings_dict["ide_choice"] if settings_dict.get("remember_ide_choice") else "None",
            "remember_ide_choice": settings_dict.get("remember_ide_choice", False),

            "ide_path": settings_dict["ide_path"] if settings_dict.get("remember_ide_path") else "",
            "remember_ide_path": settings_dict.get("remember_ide_path", False),

            "interpreter": settings_dict["interpreter"] if settings_dict.get("remember_interpreter") else "",
            "remember_interpreter": settings_dict.get("remember_interpreter", False)
        }

        with open(SETTINGS_FILE, "w") as f:
            json.dump(final_data, f, indent=4)
