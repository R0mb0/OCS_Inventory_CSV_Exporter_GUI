"""Sezione 3 della finestra: visualizzatore log limitato alle ultime 1000 righe.

Usiamo QPlainTextEdit.setMaximumBlockCount(1000): e' la funzione nativa di
Qt per scartare automaticamente le righe piu' vecchie quando se ne
aggiungono di nuove, evitando che il consumo di memoria cresca
indefinitamente su un'applicazione pensata per restare accesa a lungo
(tipicamente su un server).
"""

from __future__ import annotations

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QPlainTextEdit, QPushButton, QVBoxLayout, QWidget

from core.i18n import t

MAX_LOG_LINES = 1000


class LogPanel(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.text_edit = QPlainTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setMaximumBlockCount(MAX_LOG_LINES)
        mono = QFont("Consolas")
        mono.setStyleHint(QFont.Monospace)
        mono.setPointSize(9)
        self.text_edit.setFont(mono)
        layout.addWidget(self.text_edit)

        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        self.clear_btn = QPushButton()
        self.clear_btn.clicked.connect(self.text_edit.clear)
        btn_row.addWidget(self.clear_btn)
        layout.addLayout(btn_row)

        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        self.text_edit.setPlaceholderText(t("log_panel.placeholder", n=MAX_LOG_LINES))
        self.clear_btn.setText(t("log_panel.clear_button"))

    def append_line(self, line: str) -> None:
        self.text_edit.appendPlainText(line)
