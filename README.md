# 🖥️ OCS Inventory CSV Exporter GUI

A **Windows desktop application** (Python + PySide6) that automates scheduled CSV exports from **OCS Inventory NG**, with a resizable 3-section GUI, encrypted credential storage, automatic cleanup of old exports, and unattended autostart after a server reboot.

This project is the desktop/GUI evolution of [`OCS_Inventory_CSV_Exporter`](https://github.com/R0mb0/OCS_Inventory_CSV_Exporter) (the original PowerShell + Playwright script): same underlying automation logic, now wrapped in a self-contained scheduler with a graphical interface, meant to run unattended on a Windows machine or server.

<!-- Badges: add Codacy / build / release badges here once the repo is published -->
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-Qt%20for%20Python-41CD52?logo=qt&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-Automation-2EAD33?logo=playwright&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)

---

## 🚀 Why this project exists

OCS Inventory NG doesn't always allow direct database access in enterprise/school environments. Exporting from the web UI is often the only realistic, policy-compliant way to get inventory data out for reporting or downstream integrations — but doing that by hand, on a schedule, on a server nobody is watching, doesn't scale. This app turns that manual export into a background service with its own control panel: configure it once, press **Start**, and it keeps exporting on schedule, cleans up after itself, and comes back on its own after a reboot.

## ✨ Features

- **Layered, resizable GUI**: three stacked sections (Connection → Loop → Output), each resizable by dragging the dividers
- **Scheduled extraction loop**: configurable interval (minutes/hours), runs immediately on start and then on every cycle — green **Start** / red **Stop** controls
- **Automatic CSV cleanup**: keep only the last *N* files and/or delete files older than a configurable period (days/weeks/months/years); both rules can be active at once (OR logic), independently toggleable
- **Encrypted credentials**: the OCS password is never written to disk in plain text — encrypted at rest with **Windows DPAPI**
- **Live log viewer**: same timestamped log format as the original script, capped to the last 1000 lines so memory stays bounded on a server that runs 24/7
- **Automatic light/dark theme**: follows the OS theme by default, with a manual override in the **Edit → Theme** menu (persisted across restarts)
- **Single-instance guard**: a second launch on the same machine detects the running instance and exits cleanly instead of starting a duplicate loop
- **Unattended autostart**: `--autostart` flag + example `.bat` launcher to resume exporting automatically after a Windows server reboot (Startup folder or Task Scheduler)
- **No hardcoded environment details**: OCS URL, credentials and output folder are all configured from the app itself — nothing project-specific is baked into the code
- **CLI companion tool** (`run_export.py`): run a single export from the command line, useful for first-time setup and debugging without opening the GUI

## 🖼️ Screenshots

<!-- Add screenshots here, e.g.:
![Main window](docs/assets/img/screenshot-main.png)
![Settings panel](docs/assets/img/screenshot-settings.png)
-->

## 📁 Repository structure

```
ocs_exporter/
├── main.py                  → GUI entry point (supports --autostart)
├── run_export.py            → CLI entry point, for testing/debugging without the GUI
├── requirements.txt
├── autostart.bat            → launcher for the compiled .exe
├── autostart_dev.bat        → launcher for the Python sources
├── core/
│   ├── exporter.py          → login + column selection + CSV export (Playwright)
│   ├── scheduler.py         → background worker thread, loop + cleanup orchestration
│   ├── cleanup.py           → old CSV cleanup logic (max count / max age)
│   ├── config.py            → persistent JSON configuration (%APPDATA%)
│   ├── crypto.py            → DPAPI password encryption
│   └── single_instance.py   → single-instance guard (named mutex)
├── gui/
    ├── main_window.py       → menu, layout, wiring
    ├── settings_panel.py    → connection / loop / output settings
    ├── control_panel.py     → Avvia/Stop + status
    ├── log_panel.py         → capped log viewer
    └── theme.py             → light/dark theme detection & switching
```

## 🔧 Requirements

- **Windows 10/11** (DPAPI encryption and OS theme detection are Windows-specific; the export engine itself is cross-platform)
- **Python 3.10+**
- Network access to your OCS Inventory instance
- Valid OCS Inventory user credentials

## ▶️ Quick start

### 1) Install dependencies

```powershell
cd ocs_exporter
py -m venv venv
venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
```

### 2) Run the app

```powershell
python main.py
```

Fill in the **Connection** section (OCS URL, username, password), the **Loop** interval, and the **Output** folder, then press **Avvia**. Settings are saved automatically (with the password encrypted) so the next launch — including an unattended `--autostart` — can reuse them.

### 3) (Optional) Test the export engine from the command line

```powershell
python run_export.py --base-url http://your-ocs-server/ocsreports --username your_user --output-dir C:\OCS\export
```

Add `--show-browser` to watch the browser while it works — useful the first time, to visually confirm login and column selection succeed.

## ⚙️ Configuration

All settings are managed from the GUI and persisted to `%APPDATA%\OCSExporter\config.json`:

- **Connection**: OCS base URL, username, password (encrypted with DPAPI before being written to disk)
- **Loop**: extraction interval (minutes or hours)
- **Output**: destination folder for CSV files, plus two independent cleanup rules:
  - *Keep at most N files* — deletes the oldest exports beyond the configured count
  - *Delete files older than* — deletes exports older than a configured number of days/weeks/months/years
  - If both are enabled, a file is deleted as soon as it matches **either** condition

## 🧠 How it works (technical flow)

1. Validates the configuration and the output folder
2. Logs into OCS Inventory using the standard fields (`LOGIN`, `PASSWD`, `Valid_CNX`)
3. Opens the advanced search page and iterates every option in `#select_colaffich_multi_crit` to enable all available columns
4. Triggers the CSV export (`function=export_csv`, `tablename=affich_multi_crit`, `nolimit=true`) and saves the file with a timestamped name (`YYYY_MM_DD-HH_mm.csv`)
5. Runs the configured cleanup rule(s) on the output folder
6. Waits for the configured interval, then repeats — until **Stop** is pressed (the current cycle is always allowed to finish first, to avoid orphaned browser processes)

## 🔁 Resuming automatically after a server reboot

The app ships with `--autostart` (starts the loop immediately using the last saved settings, without needing anyone to click **Avvia**) and example `.bat` launchers. Point a shortcut in the Windows **Startup** folder (`shell:startup`), or a **Task Scheduler** action, at the launcher for your setup:

```bat
start "" "OCSExporter.exe" --autostart
```

The built-in single-instance guard makes it safe to have more than one autostart method configured at once while you figure out which fits your server best.
