"""
Rilevamento del tema chiaro/scuro di Windows e applicazione alla GUI.

Tre modalita' possibili (salvate in config.json, chiave "theme"):
  - "auto"  -> segue il tema di sistema di Windows (rilevato dal registro)
  - "light" -> forza il tema chiaro indipendentemente dal sistema
  - "dark"  -> forza il tema scuro indipendentemente dal sistema

Usiamo lo stile Qt "Fusion" perche', a differenza dello stile nativo
Windows, rispetta fedelmente la QPalette che gli passiamo: e' l'unico modo
per poter forzare "chiaro" anche quando Windows e' in modalita' scura (e
viceversa).
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

VALID_MODES = ("auto", "light", "dark")


def detect_windows_theme() -> str:
    """Legge la chiave di registro di Windows che indica il tema chiaro/scuro.

    AppsUseLightTheme = 1 -> chiaro, 0 -> scuro. Su sistemi non Windows (es.
    durante lo sviluppo) o se la chiave non esiste, torna "light" come
    default ragionevole.
    """
    try:
        import winreg  # disponibile solo su Windows

        key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return "light" if value else "dark"
    except (ImportError, FileNotFoundError, OSError):
        return "light"


def _light_palette() -> QPalette:
    # Palette chiara "di sistema" standard, esplicita per coerenza con Fusion.
    p = QPalette()
    p.setColor(QPalette.Window, QColor(240, 240, 240))
    p.setColor(QPalette.WindowText, QColor(0, 0, 0))
    p.setColor(QPalette.Base, QColor(255, 255, 255))
    p.setColor(QPalette.AlternateBase, QColor(233, 233, 233))
    p.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
    p.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    p.setColor(QPalette.Text, QColor(0, 0, 0))
    p.setColor(QPalette.Button, QColor(240, 240, 240))
    p.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    p.setColor(QPalette.BrightText, QColor(255, 0, 0))
    p.setColor(QPalette.Highlight, QColor(0, 120, 215))
    p.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    p.setColor(QPalette.PlaceholderText, QColor(120, 120, 120))
    p.setColor(QPalette.Disabled, QPalette.Text, QColor(150, 150, 150))
    p.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(150, 150, 150))
    return p


def _dark_palette() -> QPalette:
    # Ricetta "Fusion dark" ben nota, ampiamente usata per app Qt.
    p = QPalette()
    p.setColor(QPalette.Window, QColor(45, 45, 45))
    p.setColor(QPalette.WindowText, QColor(220, 220, 220))
    p.setColor(QPalette.Base, QColor(30, 30, 30))
    p.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
    p.setColor(QPalette.ToolTipBase, QColor(220, 220, 220))
    p.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    p.setColor(QPalette.Text, QColor(220, 220, 220))
    p.setColor(QPalette.Button, QColor(60, 60, 60))
    p.setColor(QPalette.ButtonText, QColor(220, 220, 220))
    p.setColor(QPalette.BrightText, QColor(255, 80, 80))
    p.setColor(QPalette.Highlight, QColor(42, 130, 218))
    p.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    p.setColor(QPalette.PlaceholderText, QColor(150, 150, 150))
    p.setColor(QPalette.Disabled, QPalette.Text, QColor(110, 110, 110))
    p.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(110, 110, 110))
    return p


def resolve_effective_theme(mode: str) -> str:
    """Da 'auto'/'light'/'dark' restituisce sempre 'light' o 'dark'."""
    if mode not in VALID_MODES:
        mode = "auto"
    return detect_windows_theme() if mode == "auto" else mode


def apply_theme(app: QApplication, mode: str) -> str:
    """Applica il tema all'intera applicazione. Ritorna il tema effettivo applicato."""
    effective = resolve_effective_theme(mode)
    app.setStyle("Fusion")
    app.setPalette(_light_palette() if effective == "light" else _dark_palette())
    return effective
