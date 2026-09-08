#!/usr/bin/env python3


from __future__ import annotations

import argparse
import getpass
import os
import sys
from pathlib import Path

from core.exporter import OcsExportError, run_export

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Estrazione CSV da OCS Inventory NG")
    parser.add_argument(
        "--base-url",
        required=True,
        help="URL base di OCS Inventory, es. http://your-ocs-server/ocsreports",
    )
    parser.add_argument("--username", default=os.environ.get("OCS_USER"))
    parser.add_argument("--password", default=os.environ.get("OCS_PASS"))
    parser.add_argument(
        "--output-dir",
        default=str(Path.cwd()),
        help="Cartella dove salvare il CSV (default: cartella corrente)",
    )
    parser.add_argument(
        "--show-browser",
        action="store_true",
        help="Mostra il browser invece di girare headless (solo per debug/verifica manuale)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    username = args.username or input("Utente OCS: ")
    password = args.password or getpass.getpass("Password OCS: ")

    try:
        result = run_export(
            base_url=args.base_url,
            username=username,
            password=password,
            output_dir=args.output_dir,
            headless=not args.show_browser,
        )
    except OcsExportError as exc:
        print(f"ERRORE: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 - vogliamo comunque un messaggio chiaro
        print(f"ERRORE IMPREVISTO: {exc}", file=sys.stderr)
        return 1

    print(f"\nFile creato: {result.csv_path} ({result.columns_count} colonne)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
