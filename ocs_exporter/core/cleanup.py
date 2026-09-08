"""
Pulizia dei CSV vecchi prodotti dall'app.

Due criteri configurabili in modo indipendente (vedi la sezione Output
delle impostazioni nella GUI):

  - numero massimo di file: se in cartella ce ne sono di piu', si
    eliminano i piu' vecchi finche' non ne restano al massimo tanti
    quanti impostati ("tengo solo gli ultimi N").
  - eta' massima: si eliminano tutti i file piu' vecchi di un certo
    periodo (giorni / settimane / mesi / anni). "Mesi" e "anni" sono
    approssimati rispettivamente a 30 e 365 giorni: per una pulizia di
    questo tipo non serve la precisione del calendario civile.

Se sono attivi entrambi i criteri sono "in OR", come richiesto: un file
viene eliminato se soddisfa ALMENO UNO dei due, non serve che li
soddisfi entrambi.

Per sicurezza vengono presi in considerazione SOLO i file il cui nome
corrisponde esattamente al formato generato da questa app
(AAAA_MM_GG-HH_MM.csv, vedi core/exporter.py): cosi' non si rischia di
cancellare per errore altri CSV che l'utente tenesse nella stessa
cartella di output.
"""

from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from core.i18n import t

# Stesso formato di stampa usato in core/exporter.py per il nome del CSV.
OUR_CSV_PATTERN = re.compile(r"^\d{4}_\d{2}_\d{2}-\d{2}_\d{2}\.csv$", re.IGNORECASE)

# Valori canonici (in inglese, indipendenti dalla lingua dell'interfaccia).
UNIT_TO_DAYS = {
    "days": 1,
    "weeks": 7,
    "months": 30,
    "years": 365,
}

LogCallback = Callable[[str], None]


@dataclass
class CleanupSettings:
    max_files_enabled: bool = False
    max_files_value: int = 3
    max_age_enabled: bool = False
    max_age_value: int = 1
    max_age_unit: str = "months"  # "days" | "weeks" | "months" | "years" (canonico)

    @property
    def active(self) -> bool:
        return self.max_files_enabled or self.max_age_enabled


def _our_csv_files(output_dir: Path) -> list[Path]:
    if not output_dir.exists():
        return []
    return [p for p in output_dir.iterdir() if p.is_file() and OUR_CSV_PATTERN.match(p.name)]


def cleanup_old_csv(
    output_dir: str | Path,
    settings: CleanupSettings,
    log_callback: Optional[LogCallback] = None,
) -> int:
    """Applica le regole di pulizia attive. Ritorna quanti file sono stati eliminati."""
    if not settings.active:
        return 0

    log = log_callback or (lambda _msg: None)
    files = _our_csv_files(Path(output_dir))
    if not files:
        return 0

    # Il formato AAAA_MM_GG-HH_MM e' ordinabile alfabeticamente esattamente
    # come nel tempo: non serve leggere la data di modifica del file per
    # sapere qual e' il piu' recente.
    files.sort(key=lambda p: p.name, reverse=True)  # piu' recenti prima

    to_delete: set[Path] = set()

    if settings.max_files_enabled and settings.max_files_value > 0:
        to_delete.update(files[settings.max_files_value:])

    if settings.max_age_enabled and settings.max_age_value > 0:
        days = UNIT_TO_DAYS.get(settings.max_age_unit, 30) * settings.max_age_value
        cutoff = _dt.datetime.now() - _dt.timedelta(days=days)
        for p in files:
            try:
                mtime = _dt.datetime.fromtimestamp(p.stat().st_mtime)
            except OSError:
                continue
            if mtime < cutoff:
                to_delete.add(p)

    if not to_delete:
        return 0

    deleted = 0
    for p in sorted(to_delete, key=lambda p: p.name):
        try:
            p.unlink()
            deleted += 1
            log(t("cleanup.deleted", name=p.name))
        except OSError as exc:
            log(t("cleanup.delete_failed", name=p.name, exc=exc))

    return deleted
