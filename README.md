# solar_system
Solar system

## Open Study Hub

In PowerShell, from this repository folder, run:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Keep that terminal open, then visit http://127.0.0.1:8000/ in your browser.
Click **Science** or visit http://127.0.0.1:8000/science/.
Press Ctrl+C in the terminal to stop the server.

### Where the pages live

- `config/settings.py`: project settings; `learning` is registered here.
- `config/urls.py`: sends page addresses to the learning app.
- `learning/urls.py`: maps addresses (URLs) to Python functions (views).
- `learning/views.py`: chooses which HTML page (template) to display.
- `learning/templates/learning/`: shared layout, home page, and Science page.
- `learning/static/learning/style.css`: shared page styling (a static asset).

To add Math or English later, add a view, a named URL, and a template,
then replace its Coming soon label on the home page with a link.
New templates can extend `learning/base.html` to reuse the layout.

The original `solar-system.html` is preserved in the repository root,
including its existing styling and online asset links. Click **Open Solar
System Explorer** on the Science page or visit http://127.0.0.1:8000/solar-system/.
Django serves the original file without changing it. The simulator's online
libraries require an internet connection.

## Python setup (Windows PowerShell)

This repository uses Python 3.14.10. The `.venv` folder keeps this
project's Python packages separate and is ignored by Git.

To activate the existing environment, open PowerShell in this folder and run:

```powershell
.\.venv\Scripts\Activate.ps1
python -m django --version
```

If PowerShell blocks activation, allow scripts for the current terminal only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Run `deactivate` when you are finished. Activation is optional: you can always
use `.\.venv\Scripts\python.exe` instead of `python`.

To recreate the environment with Python 3.14.10 installed:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```
