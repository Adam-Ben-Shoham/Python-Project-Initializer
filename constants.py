IGNORE_DICT = {
    'python': """# --- Python Essentials ---
__pycache__/
*.py[cod]
*$py.class
*.so
.idea/
.vscode/

# --- Environments ---
.venv/
venv/
env/
.env

# --- Distribution / Packaging ---
dist/
build/
*.egg-info/
*.egg
MANIFEST

# --- Logs & Databases ---
*.log
db.sqlite3
db.sqlite3-journal

# --- Unit Test / Coverage ---
.pytest_cache/
.coverage
htmlcov/
""",
    'macos': """# --- macOS OS ---
.DS_Store
.AppleDouble
.LSOverride
._*
.DocumentRevisions-V100
.fseventsd
.Spotlight-V100
.TemporaryItems
.Trashes
.VolumeIcon.icns
""",

    'linux': """# --- Linux OS ---
*~
.fuse_hidden*
.directory
.trash
.nfs*
""",
    'windows': """# --- Windows OS ---
Bin/
obj/
Generated\ Files/
[Bb]in/
[Oo]bj/
# Windows image thumbnails
Thumbs.db
ehthumbs.db
ehthumbs_kit.db
# Folder config file
desktop.ini
# Recycle Bin used on FAT drives
$RECYCLE.BIN/
# Windows Installer logs
*.cab
*.msi
*.msm
*.msp
# Windows shortcuts
*.lnk
""",

               'pycharm': """# --- PyCharm / JetBrains ---
*.iws
*.iml
*.ipr
out/
""",

'vscode': """# --- VS Code ---
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
*.code-workspace
"""
}

PROJECT_TEMPLATES = {
    'Basic': {
        'content': "\n\nif __name__ == \'__main__\':\n",
        'libraries': []
    },
    'Automation': {
        'content': """import requests
import os
from dotenv import load_dotenv

def main():
    pass

if __name__ == "__main__":
    main()
""",
        'libraries': ['requests', 'python-dotenv']
    },
    'Flask': {
        'content': """from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello, Flask!</h1><p>Welcome to your new web app.</p>"

if __name__ == "__main__":
    
    app.run(debug=True)
""",
        'libraries': ['flask', 'gunicorn']
    },
    'FastAPI': {
        'content': """from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}

if __name__ == "__main__":

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
""",
        'libraries': ['fastapi', 'uvicorn', 'pydantic']
    },
    'Data Science': {
        'content': """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    pass

if __name__ == "__main__":
    main()
""",
        'libraries': ['pandas', 'numpy', 'matplotlib', 'seaborn']
    },
    'Web Scraping': {
        'content': """import requests
from bs4 import BeautifulSoup

def main():
    pass

if __name__ == "__main__":
    main()
""",
        'libraries': ['requests', 'beautifulsoup4', 'lxml']
    }
}
