"""Finestra principale: menu, le 3 sezioni ridimensionabili, persistenza e
collegamento reale al motore di estrazione (worker in thread separato)."""

from __future__ import annotations

import base64
import datetime as _dt
from pathlib import Path
from typing import Any, Optional

from PySide6.QtCore import QByteArray, Qt
from PySide6.QtGui import QAction, QActionGroup, QCloseEvent, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QSplitter

from core.cleanup import CleanupSettings
from core.config import config_path, load_config, save_config
from core.i18n import (
    LANGUAGE_NAMES,
    SUPPORTED_LANGUAGES,
    detect_system_language,
    set_language,
    t,
)
from core.scheduler import ExportParams, ExportWorker
from gui.control_panel import ControlPanel
from gui.log_panel import LogPanel
from gui.settings_panel import SettingsPanel
from gui.theme import apply_theme

WINDOW_TITLE = "OCS Exporter"
THEME_MODES = ["auto", "light", "dark"]

# icon.ico sta nella cartella del progetto (un livello sopra gui/).
ICON_PATH = Path(__file__).resolve().parent.parent / "icon.ico"


class MainWindow(QMainWindow):
    def __init__(self, app: QApplication, autostart: bool = False) -> None:
        super().__init__()
        self._app = app
        self.setWindowTitle(WINDOW_TITLE)
        if ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(ICON_PATH)))
        self.resize(760, 640)

        self.config: dict[str, Any] = load_config()

        # Applica subito la lingua configurata (o quella di sistema se
        # "auto"), PRIMA di costruire qualunque widget: cosi' tutto il testo
        # iniziale (pannelli, menu) nasce gia' nella lingua giusta.
        language_mode = self.config.get("language", "auto")
        if language_mode != "auto" and language_mode not in SUPPORTED_LANGUAGES:
            language_mode = "auto"
        set_language(detect_system_language() if language_mode == "auto" else language_mode)

        self.worker: Optional[ExportWorker] = None
        self._next_run_at: Optional[_dt.datetime] = None
        self._last_cycle_success: Optional[bool] = None
        self._last_cycle_stamp: Optional[str] = None
        self._last_cycle_detail: str = ""
        self._stopping: bool = False

        # --- 3 sezioni in uno splitter verticale, ridimensionabili -------
        self.settings_panel = SettingsPanel()
        self.control_panel = ControlPanel()
        self.log_panel = LogPanel()

        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.setHandleWidth(6)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.addWidget(self.settings_panel)
        self.splitter.addWidget(self.control_panel)
        self.splitter.addWidget(self.log_panel)
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 0)
        self.splitter.setStretchFactor(2, 1)
        self.setCentralWidget(self.splitter)

        self._build_menu()
        self._restore_settings()
        self.statusBar().showMessage(t("status_bar.config_path", path=config_path()))

        self.settings_panel.save_requested.connect(self._on_save_settings)
        self.control_panel.start_requested.connect(self._on_start)
        self.control_panel.stop_requested.connect(self._on_stop)

        self._log(t("log.gui_ready"))

        if autostart:
            # Rimandato di un istante: la finestra deve prima essere
            # completamente costruita/visibile (usato dal flag --autostart,
            # vedi main.py e la prossima iterazione sull'avvio automatico).
            from PySide6.QtCore import QTimer

            QTimer.singleShot(200, lambda: self._on_start(interactive=False))

    # ------------------------------------------------------------------
    # Menu
    # ------------------------------------------------------------------
    def _build_menu(self) -> None:
        menu_bar = self.menuBar()

        self.file_menu = menu_bar.addMenu(t("menu.file"))
        self.exit_action = QAction(t("menu.exit"), self)
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)

        self.edit_menu = menu_bar.addMenu(t("menu.edit"))
        self.theme_menu = self.edit_menu.addMenu(t("menu.theme"))

        self._theme_group = QActionGroup(self)
        self._theme_group.setExclusive(True)
        self._theme_actions: dict[str, QAction] = {}
        for mode in THEME_MODES:
            action = QAction(t(f"menu.theme_{mode}"), self)
            action.setCheckable(True)
            action.setData(mode)
            action.triggered.connect(lambda checked, m=mode: self._on_theme_selected(m))
            self.theme_menu.addAction(action)
            self._theme_group.addAction(action)
            self._theme_actions[mode] = action

        self.language_menu = self.edit_menu.addMenu(t("menu.language"))
        self._language_group = QActionGroup(self)
        self._language_group.setExclusive(True)
        self._language_actions: dict[str, QAction] = {}

        auto_action = QAction(t("menu.language_auto"), self)
        auto_action.setCheckable(True)
        auto_action.setData("auto")
        auto_action.triggered.connect(lambda checked: self._on_language_selected("auto"))
        self.language_menu.addAction(auto_action)
        self._language_group.addAction(auto_action)
        self._language_actions["auto"] = auto_action

        self.language_menu.addSeparator()

        # I nomi delle lingue sono mostrati nella loro forma nativa
        # (Italiano, English, Deutsch, ...), non tradotti: e' la stessa
        # convenzione usata da browser e sistemi operativi.
        for code in SUPPORTED_LANGUAGES:
            action = QAction(LANGUAGE_NAMES[code], self)
            action.setCheckable(True)
            action.setData(code)
            action.triggered.connect(lambda checked, c=code: self._on_language_selected(c))
            self.language_menu.addAction(action)
            self._language_group.addAction(action)
            self._language_actions[code] = action

    def _on_theme_selected(self, mode: str) -> None:
        effective = apply_theme(self._app, mode)
        self.config["theme"] = mode
        save_config(self.config)
        self._log(t("log.theme_set", mode=t(f"menu.theme_{mode}"), effective=t(f"menu.theme_{effective}")))

    def _on_language_selected(self, mode: str) -> None:
        effective_code = detect_system_language() if mode == "auto" else mode
        set_language(effective_code)
        self.config["language"] = mode
        save_config(self.config)
        self._retranslate_ui()
        self._log(t("log.language_set", lang=LANGUAGE_NAMES.get(effective_code, effective_code)))

    def _retranslate_ui(self) -> None:
        """Riapplica tutte le stringhe statiche (menu, pannelli, stato) nella
        lingua corrente, senza bisogno di riavviare l'app."""
        self.file_menu.setTitle(t("menu.file"))
        self.exit_action.setText(t("menu.exit"))
        self.edit_menu.setTitle(t("menu.edit"))

        self.theme_menu.setTitle(t("menu.theme"))
        for mode, action in self._theme_actions.items():
            action.setText(t(f"menu.theme_{mode}"))

        self.language_menu.setTitle(t("menu.language"))
        self._language_actions["auto"].setText(t("menu.language_auto"))
        # I nomi delle altre lingue restano nella loro forma nativa.

        self.settings_panel.retranslate_ui()
        self.control_panel.retranslate_ui()
        self.log_panel.retranslate_ui()

        self.statusBar().showMessage(t("status_bar.config_path", path=config_path()))
        self._refresh_status(running=self.worker is not None, stopping=self._stopping)

    # ------------------------------------------------------------------
    # Impostazioni
    # ------------------------------------------------------------------
    def _restore_settings(self) -> None:
        self.settings_panel.set_settings(self.config)

        theme_mode = self.config.get("theme", "auto")
        if theme_mode not in self._theme_actions:
            theme_mode = "auto"
        self._theme_actions[theme_mode].setChecked(True)
        apply_theme(self._app, theme_mode)

        language_mode = self.config.get("language", "auto")
        if language_mode not in self._language_actions:
            language_mode = "auto"
        self._language_actions[language_mode].setChecked(True)
        # La lingua effettiva e' gia' stata applicata in __init__, prima di
        # costruire i pannelli: qui serve solo marcare la voce di menu giusta.

        geometry_b64 = self.config.get("window_geometry")
        if geometry_b64:
            try:
                self.restoreGeometry(QByteArray(base64.b64decode(geometry_b64)))
            except Exception:
                pass

        splitter_sizes = self.config.get("splitter_sizes")
        if splitter_sizes and isinstance(splitter_sizes, list) and len(splitter_sizes) == 3:
            self.splitter.setSizes(splitter_sizes)
        else:
            self.splitter.setSizes([320, 90, 260])

    def _collect_settings_into_config(self) -> None:
        values = self.settings_panel.get_settings()
        self.config.update(values)

    def _on_save_settings(self) -> None:
        self._collect_settings_into_config()
        save_config(self.config)
        self.settings_panel.mark_saved()
        self._log(t("log.settings_saved"))

    # ------------------------------------------------------------------
    # Dialoghi (bottoni tradotti manualmente: i bottoni standard di Qt non
    # si traducono da soli senza caricare i .qm ufficiali di Qt)
    # ------------------------------------------------------------------
    def _show_warning(self, title: str, text: str) -> None:
        box = QMessageBox(QMessageBox.Warning, title, text, parent=self)
        box.addButton(t("dialog.ok"), QMessageBox.AcceptRole)
        box.exec()

    def _confirm_close_while_running(self) -> bool:
        box = QMessageBox(
            QMessageBox.Question,
            t("dialog.close_confirm_title"),
            t("dialog.close_confirm_text"),
            parent=self,
        )
        yes_btn = box.addButton(t("dialog.yes"), QMessageBox.YesRole)
        no_btn = box.addButton(t("dialog.no"), QMessageBox.NoRole)
        box.setDefaultButton(no_btn)
        box.exec()
        return box.clickedButton() is yes_btn

    # ------------------------------------------------------------------
    # Controlli Avvia/Stop, collegati al vero motore di estrazione
    # ------------------------------------------------------------------
    def _on_start(self, interactive: bool = True) -> None:
        if self.worker is not None:
            return  # gia' in esecuzione

        self._collect_settings_into_config()

        missing = []
        if not self.config.get("base_url"):
            missing.append(t("missing.ocs_url"))
        if not self.config.get("username"):
            missing.append(t("missing.username"))
        if not self.config.get("password"):
            missing.append(t("missing.password"))
        if not self.config.get("output_dir"):
            missing.append(t("missing.output_folder"))
        if missing:
            msg = t("missing.prefix", fields=", ".join(missing))
            self._log(t("log.cannot_start", msg=msg))
            if interactive:
                self._show_warning(t("dialog.incomplete_settings_title"), msg)
            return

        try:
            Path(self.config["output_dir"]).mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            msg = t("log.invalid_output_dir", exc=exc)
            self._log(t("log.cannot_start", msg=msg))
            if interactive:
                self._show_warning(t("dialog.invalid_folder_title"), msg)
            return

        # Salva (con password cifrata) cosi' l'ultima configurazione usata
        # per avviare il loop resta disponibile anche dopo un riavvio.
        save_config(self.config)
        self.settings_panel.mark_saved()

        unit = self.config.get("interval_unit", "minutes")
        value = int(self.config.get("interval_value", 60) or 60)
        interval_seconds = value * 60 if unit == "minutes" else value * 3600

        cleanup_settings = CleanupSettings(
            max_files_enabled=bool(self.config.get("cleanup_max_files_enabled", False)),
            max_files_value=int(self.config.get("cleanup_max_files_value", 3) or 3),
            max_age_enabled=bool(self.config.get("cleanup_max_age_enabled", False)),
            max_age_value=int(self.config.get("cleanup_max_age_value", 1) or 1),
            max_age_unit=self.config.get("cleanup_max_age_unit", "months"),
        )

        params = ExportParams(
            base_url=self.config["base_url"],
            username=self.config["username"],
            password=self.config["password"],
            output_dir=self.config["output_dir"],
            interval_seconds=max(interval_seconds, 1),
            cleanup_settings=cleanup_settings,
        )

        self.worker = ExportWorker(params)
        self.worker.log_message.connect(self.log_panel.append_line)
        self.worker.cycle_finished.connect(self._on_cycle_finished)
        self.worker.next_run_at_changed.connect(self._on_next_run_changed)
        self.worker.finished.connect(self._on_worker_thread_finished)

        self._last_cycle_success = None
        self._last_cycle_stamp = None
        self._last_cycle_detail = ""
        self._next_run_at = None
        self._stopping = False
        self.control_panel.set_running(True)
        self.settings_panel.set_editable(False)
        self._refresh_status(running=True)

        self.worker.start()

    def _on_stop(self) -> None:
        if self.worker is None:
            return
        self.control_panel.stop_btn.setEnabled(False)
        self._stopping = True
        self._refresh_status(running=True, stopping=True)
        self.worker.request_stop()

    def _on_worker_thread_finished(self) -> None:
        self.worker = None
        self._next_run_at = None
        self._stopping = False
        self.control_panel.set_running(False)
        self.settings_panel.set_editable(True)
        self._refresh_status(running=False)

    def _on_cycle_finished(self, success: bool, message: str) -> None:
        self._last_cycle_success = success
        self._last_cycle_stamp = _dt.datetime.now().strftime("%H:%M:%S")
        self._last_cycle_detail = Path(message).name if success else message
        self._refresh_status(running=self.worker is not None)

    def _on_next_run_changed(self, next_run: object) -> None:
        self._next_run_at = next_run if isinstance(next_run, _dt.datetime) else None
        self._refresh_status(running=self.worker is not None)

    def _refresh_status(self, running: bool, stopping: bool = False) -> None:
        parts = [t("status.running") if running else t("status.stopped")]
        if stopping:
            parts.append(t("status.stopping"))
        elif running and self._next_run_at:
            parts.append(t("status.next_run", time=self._next_run_at.strftime("%H:%M:%S")))
        if self._last_cycle_stamp:
            if self._last_cycle_success:
                parts.append(
                    t("status.last_success", time=self._last_cycle_stamp, filename=self._last_cycle_detail)
                )
            else:
                parts.append(t("status.last_error", time=self._last_cycle_stamp, message=self._last_cycle_detail))
        self.control_panel.set_status_text(" — ".join(parts))

    # ------------------------------------------------------------------
    def _log(self, message: str) -> None:
        stamp = _dt.datetime.now().strftime("%H:%M:%S")
        self.log_panel.append_line(f"[{stamp}] {message}")

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.worker is not None and self.worker.isRunning():
            if not self._confirm_close_while_running():
                event.ignore()
                return
            self.worker.request_stop()
            self.worker.wait()

        self.config["window_geometry"] = base64.b64encode(bytes(self.saveGeometry())).decode("ascii")
        self.config["splitter_sizes"] = self.splitter.sizes()
        try:
            save_config(self.config)
        except OSError:
            pass
        super().closeEvent(event)
