"""
Worker che esegue l'estrazione OCS in loop, in un thread separato dalla GUI.

Comportamento:
  - Alla partenza esegue subito un primo ciclo di estrazione, poi ripete
    ogni `interval_seconds`.
  - Se un ciclo fallisce (errore di rete, login, ecc.) l'errore viene
    loggato e il worker continua al giro successivo, senza fermarsi da
    solo: si ferma solo se l'utente preme STOP (o chiude l'app).
  - STOP e' "gentile": se un'estrazione e' in corso viene lasciata
    terminare (per chiudere correttamente il browser Playwright ed evitare
    processi orfani); il worker si ferma prima del ciclo successivo o
    durante l'attesa tra un ciclo e l'altro.

Comunica con la GUI solo tramite segnali Qt (mai toccando direttamente i
widget da questo thread).
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass

from PySide6.QtCore import QThread, Signal

from core.cleanup import CleanupSettings, cleanup_old_csv
from core.exporter import OcsExportError, run_export
from core.i18n import t

POLL_INTERVAL_S = 1.0  # granularita' con cui controlliamo se e' stato premuto STOP


@dataclass
class ExportParams:
    base_url: str
    username: str
    password: str
    output_dir: str
    interval_seconds: int
    cleanup_settings: CleanupSettings = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.cleanup_settings is None:
            self.cleanup_settings = CleanupSettings()


class ExportWorker(QThread):
    log_message = Signal(str)
    cycle_finished = Signal(bool, str)  # (successo, path_csv_o_messaggio_errore)
    next_run_at_changed = Signal(object)  # datetime.datetime | None

    def __init__(self, params: ExportParams, parent=None) -> None:
        super().__init__(parent)
        self._params = params
        self._stop_requested = False

    def request_stop(self) -> None:
        self._stop_requested = True

    def _log(self, message: str) -> None:
        stamp = _dt.datetime.now().strftime("%H:%M:%S")
        self.log_message.emit(f"[{stamp}] {message}")

    def run(self) -> None:  # noqa: C901 - loop lineare, va bene cosi'
        p = self._params
        while not self._stop_requested:
            self.next_run_at_changed.emit(None)
            try:
                result = run_export(
                    base_url=p.base_url,
                    username=p.username,
                    password=p.password,
                    output_dir=p.output_dir,
                    headless=True,
                    log_callback=self.log_message.emit,
                )
                self.cycle_finished.emit(True, str(result.csv_path))
            except OcsExportError as exc:
                self._log(t("scheduler.error", exc=exc))
                self.cycle_finished.emit(False, str(exc))
            except Exception as exc:  # noqa: BLE001
                self._log(t("scheduler.unexpected_error", exc=exc))
                self.cycle_finished.emit(False, str(exc))

            if p.cleanup_settings.active:
                try:
                    cleanup_old_csv(p.output_dir, p.cleanup_settings, log_callback=self.log_message.emit)
                except Exception as exc:  # noqa: BLE001
                    self._log(t("scheduler.cleanup_error", exc=exc))

            if self._stop_requested:
                break

            next_run = _dt.datetime.now() + _dt.timedelta(seconds=p.interval_seconds)
            self.next_run_at_changed.emit(next_run)

            waited = 0.0
            while waited < p.interval_seconds and not self._stop_requested:
                self.msleep(int(POLL_INTERVAL_S * 1000))
                waited += POLL_INTERVAL_S

        self.next_run_at_changed.emit(None)
        self._log(t("scheduler.loop_stopped"))
