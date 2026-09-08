"""
Gestione del file di configurazione persistente dell'app.

Percorso: %APPDATA%\\OCSExporter\\config.json (su Windows). Se APPDATA non
e' definita (es. durante lo sviluppo su un altro sistema operativo), si usa
una cartella nella home dell'utente.

Sicurezza password: il file su disco non contiene MAI la password in
chiaro. load_config()/save_config() gestiscono la cifratura in modo
trasparente:
  - save_config(cfg): se cfg contiene "password" (stringa non vuota), la
    cifra con Windows DPAPI (vedi core/crypto.py) e salva solo il blob
    cifrato nella chiave "password_enc"; la chiave "password" non viene
    mai scritta su disco.
  - load_config(): decifra "password_enc" (se presente) e la espone come
    cfg["password"] pronta all'uso, solo in memoria.

Chi usa questo modulo (GUI, worker) puo' quindi trattare cfg["password"]
come un campo normale: la cifratura/decifratura avviene sempre qui.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from core.crypto import decrypt_password, encrypt_password

APP_DIR_NAME = "OCSExporter"
CONFIG_FILE_NAME = "config.json"

DEFAULT_CONFIG: dict[str, Any] = {
    "base_url": "",
    "username": "",
    "password_enc": "",  # blob cifrato DPAPI, mai la password in chiaro
    "output_dir": "",
    "interval_value": 60,
    "interval_unit": "minutes",  # "minutes" | "hours" (valore canonico interno, indipendente dalla lingua)
    "cleanup_max_files_enabled": False,
    "cleanup_max_files_value": 3,
    "cleanup_max_age_enabled": False,
    "cleanup_max_age_value": 1,
    "cleanup_max_age_unit": "months",  # "days" | "weeks" | "months" | "years" (canonico)
    "theme": "auto",  # "auto" | "light" | "dark"
    "language": "auto",  # "auto" | "it" | "en" | "de" | "fr" | "es" | "nl"
    "window_geometry": None,  # base64 di QMainWindow.saveGeometry(), impostato dalla GUI
    "splitter_sizes": None,  # lista di interi (pixel) delle 3 sezioni
}

# Migrazione dei valori delle unita' salvati in italiano dalle versioni
# precedenti (prima dell'introduzione della i18n), verso i nuovi valori
# canonici in inglese usati internamente indipendentemente dalla lingua
# dell'interfaccia.
_LEGACY_INTERVAL_UNIT_MAP = {
    "minuti": "minutes",
    "ore": "hours",
}
_LEGACY_AGE_UNIT_MAP = {
    "giorni": "days",
    "settimane": "weeks",
    "mesi": "months",
    "anni": "years",
}


def _config_dir() -> Path:
    appdata = os.environ.get("APPDATA")
    base = Path(appdata) if appdata else Path.home() / ".config"
    return base / APP_DIR_NAME


def config_path() -> Path:
    return _config_dir() / CONFIG_FILE_NAME


def load_config() -> dict[str, Any]:
    """Carica la configurazione, applicando i default per le chiavi mancanti.

    Tollera file assente o corrotto (torna ai default senza sollevare
    eccezioni: un config.json rovinato non deve impedire l'avvio dell'app).
    La password viene decifrata ed esposta come cfg["password"] (stringa
    vuota se assente o non decifrabile, es. file copiato da un'altra
    macchina: DPAPI e' legato a utente+macchina, com'e' corretto che sia).
    """
    cfg = dict(DEFAULT_CONFIG)
    path = config_path()
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                saved = json.load(f)
            if isinstance(saved, dict):
                cfg.update(saved)
        except (json.JSONDecodeError, OSError):
            pass

    # Migra eventuali valori legacy in italiano (config salvato da una
    # versione precedente alla i18n) verso i valori canonici in inglese.
    cfg["interval_unit"] = _LEGACY_INTERVAL_UNIT_MAP.get(cfg.get("interval_unit"), cfg.get("interval_unit"))
    cfg["cleanup_max_age_unit"] = _LEGACY_AGE_UNIT_MAP.get(cfg.get("cleanup_max_age_unit"), cfg.get("cleanup_max_age_unit"))

    cfg["password"] = decrypt_password(cfg.get("password_enc", ""))
    return cfg


def save_config(cfg: dict[str, Any]) -> None:
    """Salva la configurazione in modo atomico (scrive su file temporaneo poi rinomina).

    Non scrive mai "password" in chiaro su disco: la cifra in "password_enc"
    (lasciando invariato il blob esistente se la password passata e' vuota,
    cosi' un salvataggio delle sole altre impostazioni non cancella quella
    gia' salvata).
    """
    to_write = dict(cfg)
    plain_password = to_write.pop("password", None)
    if plain_password:
        to_write["password_enc"] = encrypt_password(plain_password)

    directory = _config_dir()
    directory.mkdir(parents=True, exist_ok=True)
    path = config_path()

    fd, tmp_path = tempfile.mkstemp(prefix="config_", suffix=".tmp", dir=str(directory))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(to_write, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
        raise
