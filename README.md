# CricketDash AI (VS Code / Windows)

A beginner-friendly Django website for cricket squad management, player performance, teams, tournaments, comparison, and rule-based Playing XI recommendations. Uses SQLite so it starts locally without installing MySQL.


## 1. Install
- Install Python 3.11+ from https://www.python.org/downloads/ and tick **Add Python to PATH**.
- Install VS Code from https://code.visualstudio.com/.

## 2. Open the folder
Extract the project folder. In VS Code, choose File → Open Folder → `CricketDashAI`.
Open Terminal → New Terminal.

## 3. Create and activate the virtual environment (Windows)
CMD:
```bat
py -m venv .venv
.venv\Scripts\activate
```
PowerShell activation command:
```powershell
.\.venv\Scripts\Activate.ps1
```

## 4. Install Django
```bat
python -m pip install -r requirements.txt
```

## 5. Create database tables
```bat
python manage.py makemigrations core
python manage.py migrate
```

## 6. Add demo data (optional but recommended)
```bat
python manage.py seed_demo
```

## 7. Start the website
```bat
python manage.py runserver
```
Open http://127.0.0.1:8000/ in your browser.

## Pages
- Dashboard: `/`
- Players: `/players/`
- Add player: `/players/add/`
- Teams: `/teams/`
- Tournaments: `/tournaments/`
- Player comparison: `/compare/`
- Smart Playing XI: `/playing-xi/`
- Admin: `/admin/` (create an admin account using `python manage.py createsuperuser`)

## Notes
- This is a local demo/college project starter. SQLite is configured for easier setup.
- The recommendation algorithm is a transparent rules-based demo, not a machine-learning model.
- Before public deployment, set `DEBUG=False`, configure a real secret key, allowed hosts, HTTPS, and appropriate security settings.
