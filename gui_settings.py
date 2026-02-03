import json
import os

class SettingsManager:
    def __init__(self, filepath="settings.json"):
        self.filepath = filepath

    def load_settings(self):
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

        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    data = json.load(f)
                    return {**defaults, **data}
            except (json.JSONDecodeError, IOError):
                return defaults
        return defaults

    def save_settings(self, settings_dict):
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

        with open(self.filepath, "w") as f:
            json.dump(final_data, f, indent=4)