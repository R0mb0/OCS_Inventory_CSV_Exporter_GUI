"""Sezione 2 della finestra: pulsanti Avvia/Stop e stato corrente."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from core.i18n import t

GREEN_STYLE = """
QPushButton {
    background-color: #2e8b3d;
    color: white;
    font-weight: bold;
    padding: 10px 24px;
    border-radius: 4px;
    border: none;
}
QPushButton:hover:!disabled { background-color: #379246; }
QPushButton:disabled { background-color: #7fae86; color: #e8e8e8; }
"""

RED_STYLE = """
QPushButton {
    background-color: #c0392b;
    color: white;
    font-weight: bold;
    padding: 10px 24px;
    border-radius: 4px;
    border: none;
}
QPushButton:hover:!disabled { background-color: #d14435; }
QPushButton:disabled { background-color: #d69a93; color: #e8e8e8; }
"""


class ControlPanel(QWidget):
    start_requested = Signal()
    stop_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        # Testo "interno" (gia' tradotto) mostrato dopo il prefisso "Stato:",
        # tenuto a parte cosi' retranslate_ui() puo' ricomporre l'etichetta
        # completa quando cambia solo la lingua del prefisso (il testo vero
        # e proprio viene comunque ricalcolato e re-impostato dalla
        # MainWindow subito dopo un cambio lingua).
        self._status_text = t("status.stopped")

        layout = QHBoxLayout(self)

        self.start_btn = QPushButton()
        self.start_btn.setStyleSheet(GREEN_STYLE)
        self.start_btn.clicked.connect(self.start_requested.emit)
        layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton()
        self.stop_btn.setStyleSheet(RED_STYLE)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_requested.emit)
        layout.addWidget(self.stop_btn)

        layout.addSpacing(20)

        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        layout.addStretch(1)

        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        self.start_btn.setText(t("control.start"))
        self.stop_btn.setText(t("control.stop"))
        self.status_label.setText(t("control.status_prefix", text=self._status_text))

    def set_running(self, running: bool) -> None:
        self.start_btn.setEnabled(not running)
        self.stop_btn.setEnabled(running)

    def set_status_text(self, text: str) -> None:
        self._status_text = text
        self.status_label.setText(t("control.status_prefix", text=text))
