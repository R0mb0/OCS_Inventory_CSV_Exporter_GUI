"""
Motore di estrazione OCS Inventory NG.

Porting in Python (Playwright) della logica originariamente scritta in
PowerShell + Node.js/Playwright (ocs_export.ps1). Il comportamento e'
identico passo per passo:

  1. Login sulla pagina OCS Inventory NG.
  2. Apertura della pagina di ricerca multi-criterio.
  3. Selezione (toggle) di TUTTE le colonne disponibili nel menu a tendina
     #select_colaffich_multi_crit, una alla volta.
  4. Attesa di stabilizzazione della tabella.
  5. Click sul link di export CSV e salvataggio del file scaricato.
  6. Verifica che il file scaricato sia davvero un CSV (e non una pagina
     di errore HTML).

Il modulo espone la funzione `run_export(...)` pensata per essere
riutilizzata sia da riga di comando (vedi run_export.py) sia, nelle
prossime iterazioni, dal worker thread della GUI: non stampa nulla da
solo, ma invia ogni riga di log a un `log_callback(msg: str)` fornito da
chi lo chiama, cosi' la GUI potra' incanalare le righe nel proprio
pannello di log senza modificare questo file.
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

from core.i18n import t

# Stesso selettore/URL dello script PowerShell originale.
SEARCH_PATH_TEMPLATE = (
    "{base_url}/index.php?function=visu_search&fields=HARDWARE-LASTCOME"
    "&comp=tall&values=&values2=all&type_field="
)
LOGIN_PATH_TEMPLATE = "{base_url}/index.php"

COLUMN_SELECT_SELECTOR = "#select_colaffich_multi_crit"
LOGIN_SELECTOR = 'input[name="LOGIN"]'
PASSWORD_SELECTOR = 'input[name="PASSWD"]'
LOGIN_BUTTON_SELECTOR = 'input[name="Valid_CNX"], #btn-logon'
EXPORT_LINK_SELECTOR = (
    'a[href*="function=export_csv"]'
    '[href*="tablename=affich_multi_crit"]'
    '[href*="nolimit=true"]'
)

DEFAULT_TIMEOUT_MS = 30_000
DOWNLOAD_TIMEOUT_MS = 60_000
COLUMN_TOGGLE_DELAY_MS = 400
STABILIZE_DELAY_MS = 1_500


class OcsExportError(RuntimeError):
    """Errore applicativo durante l'estrazione (login fallito, CSV non valido, ...)."""


LogCallback = Callable[[str], None]


@dataclass
class ExportResult:
    csv_path: Path
    columns_count: int


def _default_log(msg: str) -> None:
    print(msg)


def _timestamped(log_callback: LogCallback, msg: str) -> None:
    now = _dt.datetime.now().strftime("%H:%M:%S")
    log_callback(f"[{now}] {msg}")


def run_export(
    base_url: str,
    username: str,
    password: str,
    output_dir: Path | str,
    headless: bool = True,
    log_callback: Optional[LogCallback] = None,
) -> ExportResult:
    """Esegue un ciclo completo di estrazione e restituisce il percorso del CSV.

    Solleva OcsExportError (o le eccezioni di Playwright) in caso di problemi;
    chi chiama decide se loggare e continuare al giro successivo del loop.
    """
    log = log_callback or _default_log
    base_url = base_url.rstrip("/")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    stamp = _dt.datetime.now().strftime("%Y_%m_%d-%H_%M")
    out_csv = output_dir / f"{stamp}.csv"

    login_url = LOGIN_PATH_TEMPLATE.format(base_url=base_url)
    search_url = SEARCH_PATH_TEMPLATE.format(base_url=base_url)

    _timestamped(log, t("engine.starting"))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT_MS)

        try:
            _timestamped(log, t("engine.opening_login"))
            page.goto(login_url, wait_until="domcontentloaded")

            _timestamped(log, t("engine.filling_credentials"))
            page.fill(LOGIN_SELECTOR, username)
            page.fill(PASSWORD_SELECTOR, password)

            _timestamped(log, t("engine.submitting_login"))
            # Fedele all'originale: click e attesa di networkidle, senza
            # forzare un evento di navigazione "classico" (alcune pagine
            # OCS gestiscono il submit via redirect non sempre rilevato
            # come nuova navigazione da Playwright).
            page.click(LOGIN_BUTTON_SELECTOR)
            page.wait_for_load_state("networkidle")

            _timestamped(log, t("engine.opening_search"))
            page.goto(search_url, wait_until="networkidle")

            page.wait_for_selector(COLUMN_SELECT_SELECTOR, timeout=DEFAULT_TIMEOUT_MS)

            values = page.eval_on_selector_all(
                f"{COLUMN_SELECT_SELECTOR} option",
                "opts => opts.map(o => o.value).filter(v => v && v !== 'default')",
            )

            _timestamped(log, t("engine.columns_found", count=len(values)))

            for i, value in enumerate(values, start=1):
                _timestamped(log, t("engine.toggle_column", i=i, total=len(values), value=value))
                page.select_option(COLUMN_SELECT_SELECTOR, value)
                page.wait_for_timeout(COLUMN_TOGGLE_DELAY_MS)

            _timestamped(log, t("engine.stabilizing"))
            page.wait_for_timeout(STABILIZE_DELAY_MS)

            page.wait_for_selector(EXPORT_LINK_SELECTOR, timeout=DEFAULT_TIMEOUT_MS)

            _timestamped(log, t("engine.starting_download"))
            with page.expect_download(timeout=DOWNLOAD_TIMEOUT_MS) as download_info:
                page.click(EXPORT_LINK_SELECTOR)
            download = download_info.value
            download.save_as(str(out_csv))

            _timestamped(log, t("engine.download_complete"))

        except PlaywrightTimeoutError as exc:
            raise OcsExportError(t("engine.error_timeout", exc=exc)) from exc
        finally:
            _timestamped(log, t("engine.cleaning_browser"))
            context.close()
            browser.close()

    if not out_csv.exists():
        raise OcsExportError(t("engine.error_csv_not_found"))

    with open(out_csv, "r", encoding="utf-8", errors="ignore") as f:
        head = f.read(2048)
    if "<html" in head.lower() or "<!doctype" in head.lower():
        raise OcsExportError(t("engine.error_html_not_csv"))

    _timestamped(log, t("engine.success", path=out_csv))
    return ExportResult(csv_path=out_csv, columns_count=len(values))
