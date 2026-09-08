#!/usr/bin/env python3
"""Punto di ingresso della GUI.

Uso:
    python main.py                # apre la GUI normalmente
    python main.py --autostart    # apre la GUI e avvia subito il loop
                                   # (usato dopo il riavvio del server,
                                   # vedi autostart.bat / Task Scheduler)

Se un'altra istanza dell'app e' gia' in esecuzione sulla stessa macchina,
questa seconda copia mostra un avviso e si chiude subito, senza toccare
config.json ne' avviare un secondo loop (vedi core/single_instance.py).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox

from core.config import load_config
from core.i18n import SUPPORTED_LANGUAGES, detect_system_language, set_language, t
from core.single_instance import acquire_single_instance
from gui.main_window import MainWindow

# icon.ico sta nella cartella del progetto, accanto a questo file.
ICON_PATH = Path(__file__).resolve().parent / "icon.ico"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OCS Exporter")
    parser.add_argument(
        "--autostart",
        action="store_true",
        help="Avvia subito il loop di estrazione con le ultime impostazioni salvate",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    app = QApplication(sys.argv)
    app.setApplicationName("OCS Exporter")
    if ICON_PATH.exists():
        # Applicata a livello di app: vale anche per finestre di dialogo
        # mostrate prima che la MainWindow esista (es. avviso "gia' in
        # esecuzione") e per l'icona nella taskbar/alt-tab di Windows.
        app.setWindowIcon(QIcon(str(ICON_PATH)))

    # Applica la lingua configurata (o quella di sistema) anche per questo
    # eventuale avviso iniziale, prima ancora di creare la MainWindow (che
    # rilegge comunque la stessa configurazione per il resto della GUI).
    language_mode = load_config().get("language", "auto")
    if language_mode != "auto" and language_mode not in SUPPORTED_LANGUAGES:
        language_mode = "auto"
    set_language(detect_system_language() if language_mode == "auto" else language_mode)

    if not acquire_single_instance():
        box = QMessageBox(
            QMessageBox.Warning,
            t("dialog.already_running_title"),
            t("dialog.already_running_text"),
        )
        box.addButton(t("dialog.ok"), QMessageBox.AcceptRole)
        box.exec()
        return 1

    window = MainWindow(app, autostart=args.autostart)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
