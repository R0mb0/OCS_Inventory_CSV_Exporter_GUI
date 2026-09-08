"""Sezione 1 della finestra: impostazioni di connessione, loop e output."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from core.i18n import t

# Valori canonici (in inglese, indipendenti dalla lingua dell'interfaccia)
# usati come userData delle combo, cosi' il valore salvato in config.json e
# usato dalla logica interna non cambia mai al cambio di lingua: cambia solo
# l'etichetta mostrata all'utente.
INTERVAL_UNITS = ["minutes", "hours"]
AGE_UNITS = ["days", "weeks", "months", "years"]


class SettingsPanel(QWidget):
    """Emette save_requested quando l'utente clicca "Salva impostazioni".

    Non scrive da sola il file di configurazione: e' la MainWindow a
    occuparsi della persistenza (questo pannello si limita a raccogliere e
    mostrare i valori), cosi' la logica di salvataggio resta in un unico
    posto (core/config.py).
    """

    save_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        root = QVBoxLayout(self)

        # --- Connessione -----------------------------------------------
        self.conn_group = QGroupBox()
        conn_form = QFormLayout(self.conn_group)

        self.base_url_edit = QLineEdit()
        self.url_label = QLabel()
        conn_form.addRow(self.url_label, self.base_url_edit)

        self.username_edit = QLineEdit()
        self.username_label = QLabel()
        conn_form.addRow(self.username_label, self.username_edit)

        pw_row = QHBoxLayout()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        pw_row.addWidget(self.password_edit)
        self.show_password_checkbox = QCheckBox()
        self.show_password_checkbox.toggled.connect(self._toggle_password_visibility)
        pw_row.addWidget(self.show_password_checkbox)
        self.password_label = QLabel()
        conn_form.addRow(self.password_label, pw_row)

        root.addWidget(self.conn_group)

        # --- Loop --------------------------------------------------------
        self.loop_group = QGroupBox()
        loop_form = QFormLayout(self.loop_group)

        interval_row = QHBoxLayout()
        self.every_label = QLabel()
        interval_row.addWidget(self.every_label)
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 1440)
        self.interval_spin.setValue(60)
        interval_row.addWidget(self.interval_spin)
        self.interval_unit_combo = QComboBox()
        for unit in INTERVAL_UNITS:
            self.interval_unit_combo.addItem(t(f"unit.{unit}"), unit)
        interval_row.addWidget(self.interval_unit_combo)
        interval_row.addStretch(1)
        self.interval_label = QLabel()
        loop_form.addRow(self.interval_label, interval_row)

        root.addWidget(self.loop_group)

        # --- Output --------------------------------------------------------
        self.out_group = QGroupBox()
        out_form = QFormLayout(self.out_group)

        out_row = QHBoxLayout()
        self.output_dir_edit = QLineEdit()
        out_row.addWidget(self.output_dir_edit)
        self.browse_btn = QPushButton()
        self.browse_btn.clicked.connect(self._browse_output_dir)
        out_row.addWidget(self.browse_btn)
        self.csv_folder_label = QLabel()
        out_form.addRow(self.csv_folder_label, out_row)

        # --- Pulizia CSV vecchi (due criteri indipendenti, attivabili
        # singolarmente; se attivi entrambi basta che se ne avveri UNO
        # perche' il file venga eliminato) -----------------------------
        self.max_files_checkbox = QCheckBox()
        max_files_row = QHBoxLayout()
        self.max_files_spin = QSpinBox()
        self.max_files_spin.setRange(1, 100000)
        self.max_files_spin.setValue(3)
        self.max_files_spin.setEnabled(False)
        max_files_row.addWidget(self.max_files_spin)
        self.max_files_suffix_label = QLabel()
        max_files_row.addWidget(self.max_files_suffix_label)
        max_files_row.addStretch(1)
        self.max_files_checkbox.toggled.connect(self.max_files_spin.setEnabled)
        out_form.addRow(self.max_files_checkbox, self._wrap_layout(max_files_row))

        self.max_age_checkbox = QCheckBox()
        max_age_row = QHBoxLayout()
        self.max_age_spin = QSpinBox()
        self.max_age_spin.setRange(1, 1000)
        self.max_age_spin.setValue(1)
        self.max_age_spin.setEnabled(False)
        max_age_row.addWidget(self.max_age_spin)
        self.max_age_unit_combo = QComboBox()
        for unit in AGE_UNITS:
            self.max_age_unit_combo.addItem(t(f"unit.{unit}"), unit)
        idx = self.max_age_unit_combo.findData("months")
        if idx >= 0:
            self.max_age_unit_combo.setCurrentIndex(idx)
        self.max_age_unit_combo.setEnabled(False)
        max_age_row.addWidget(self.max_age_unit_combo)
        max_age_row.addStretch(1)
        self.max_age_checkbox.toggled.connect(self.max_age_spin.setEnabled)
        self.max_age_checkbox.toggled.connect(self.max_age_unit_combo.setEnabled)
        out_form.addRow(self.max_age_checkbox, self._wrap_layout(max_age_row))

        root.addWidget(self.out_group)

        # --- Salva ---------------------------------------------------------
        save_row = QHBoxLayout()
        save_row.addStretch(1)
        self.save_status_label = QLabel("")
        save_row.addWidget(self.save_status_label)
        self.save_btn = QPushButton()
        self.save_btn.clicked.connect(self.save_requested.emit)
        save_row.addWidget(self.save_btn)
        root.addLayout(save_row)

        root.addStretch(1)

        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        """Riapplica tutte le stringhe statiche nella lingua corrente.

        Le combo box vengono ripopolate mantenendo la selezione corrente
        (il valore canonico salvato in userData non cambia mai, cambia solo
        l'etichetta mostrata).
        """
        self.conn_group.setTitle(t("settings.connection"))
        self.url_label.setText(t("settings.url_label"))
        self.base_url_edit.setPlaceholderText(t("settings.url_placeholder"))
        self.username_label.setText(t("settings.username_label"))
        self.password_label.setText(t("settings.password_label"))
        self.show_password_checkbox.setText(t("settings.show_password"))

        self.loop_group.setTitle(t("settings.loop"))
        self.every_label.setText(t("settings.every"))
        self.interval_label.setText(t("settings.interval_label"))
        self._repopulate_combo(self.interval_unit_combo, INTERVAL_UNITS)

        self.out_group.setTitle(t("settings.output"))
        self.csv_folder_label.setText(t("settings.csv_folder_label"))
        self.output_dir_edit.setPlaceholderText(t("settings.csv_folder_placeholder"))
        self.browse_btn.setText(t("settings.browse"))
        self.max_files_checkbox.setText(t("settings.keep_at_most"))
        self.max_files_suffix_label.setText(t("settings.keep_at_most_suffix"))
        self.max_age_checkbox.setText(t("settings.delete_older_than"))
        self._repopulate_combo(self.max_age_unit_combo, AGE_UNITS)

        self.save_btn.setText(t("settings.save_button"))

    @staticmethod
    def _repopulate_combo(combo: QComboBox, canonical_values: list[str]) -> None:
        current = combo.currentData()
        combo.blockSignals(True)
        combo.clear()
        for unit in canonical_values:
            combo.addItem(t(f"unit.{unit}"), unit)
        if current is not None:
            idx = combo.findData(current)
            if idx >= 0:
                combo.setCurrentIndex(idx)
        combo.blockSignals(False)

    def _toggle_password_visibility(self, checked: bool) -> None:
        self.password_edit.setEchoMode(QLineEdit.Normal if checked else QLineEdit.Password)

    def _browse_output_dir(self) -> None:
        start_dir = self.output_dir_edit.text() or str(self._default_dir())
        chosen = QFileDialog.getExistingDirectory(self, t("settings.browse_dialog_title"), start_dir)
        if chosen:
            self.output_dir_edit.setText(chosen)

    @staticmethod
    def _default_dir() -> str:
        from pathlib import Path

        return str(Path.home())

    @staticmethod
    def _wrap_layout(layout) -> QWidget:
        """Racchiude un QLayout in un QWidget, per usarlo come campo di una QFormLayout.addRow."""
        w = QWidget()
        w.setLayout(layout)
        return w

    def get_settings(self) -> dict[str, Any]:
        return {
            "base_url": self.base_url_edit.text().strip(),
            "username": self.username_edit.text().strip(),
            "password": self.password_edit.text(),
            "output_dir": self.output_dir_edit.text().strip(),
            "interval_value": self.interval_spin.value(),
            "interval_unit": self.interval_unit_combo.currentData(),
            "cleanup_max_files_enabled": self.max_files_checkbox.isChecked(),
            "cleanup_max_files_value": self.max_files_spin.value(),
            "cleanup_max_age_enabled": self.max_age_checkbox.isChecked(),
            "cleanup_max_age_value": self.max_age_spin.value(),
            "cleanup_max_age_unit": self.max_age_unit_combo.currentData(),
        }

    def set_settings(self, cfg: dict[str, Any]) -> None:
        self.base_url_edit.setText(cfg.get("base_url", "") or "")
        self.username_edit.setText(cfg.get("username", "") or "")
        self.output_dir_edit.setText(cfg.get("output_dir", "") or "")
        self.interval_spin.setValue(int(cfg.get("interval_value", 60) or 60))
        unit = cfg.get("interval_unit", "minutes")
        idx = self.interval_unit_combo.findData(unit)
        if idx >= 0:
            self.interval_unit_combo.setCurrentIndex(idx)
        # La password arriva gia' decifrata da core.config.load_config().
        self.password_edit.setText(cfg.get("password", "") or "")

        self.max_files_checkbox.setChecked(bool(cfg.get("cleanup_max_files_enabled", False)))
        self.max_files_spin.setValue(int(cfg.get("cleanup_max_files_value", 3) or 3))
        self.max_age_checkbox.setChecked(bool(cfg.get("cleanup_max_age_enabled", False)))
        self.max_age_spin.setValue(int(cfg.get("cleanup_max_age_value", 1) or 1))
        age_unit = cfg.get("cleanup_max_age_unit", "months")
        age_idx = self.max_age_unit_combo.findData(age_unit)
        if age_idx >= 0:
            self.max_age_unit_combo.setCurrentIndex(age_idx)

    def set_editable(self, editable: bool) -> None:
        """Disabilita l'intero pannello mentre il loop e' in esecuzione."""
        self.setEnabled(editable)

    def mark_saved(self) -> None:
        from PySide6.QtCore import QTime

        self.save_status_label.setText(t("settings.saved_at", time=QTime.currentTime().toString("HH:mm:ss")))
