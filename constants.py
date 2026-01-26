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
