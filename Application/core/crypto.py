"""
Cifratura della password OCS con Windows DPAPI.

DPAPI (Data Protection API) cifra i dati legandoli all'utente/macchina
Windows corrente: solo lo stesso utente, sulla stessa macchina, puo'
decifrarli. E' l'approccio standard di Windows per credenziali salvate su
disco da applicazioni desktop (lo stesso meccanismo usato per esempio dal
Credential Manager).

Su sistemi non Windows (durante lo sviluppo/test di questo modulo, dove
pywin32 non e' disponibile) usiamo un offuscamento base64 reversibile:
NON e' sicuro, serve solo a non far crashare l'app fuori da Windows. In
produzione questa app gira solo su Windows, dove viene sempre usata la
vera cifratura DPAPI.
"""

from __future__ import annotations

import base64

_DEV_FALLBACK_PREFIX = "DEV:"


def _has_dpapi() -> bool:
    try:
        import win32crypt  # noqa: F401

        return True
    except ImportError:
        return False


def encrypt_password(plain: str) -> str:
    """Cifra la password e la restituisce come stringa (da salvare in JSON)."""
    if not plain:
        return ""
    if _has_dpapi():
        import win32crypt

        blob = win32crypt.CryptProtectData(
            plain.encode("utf-8"),
            "OCS Exporter",  # descrizione, solo informativa
            None,  # entropia opzionale aggiuntiva, non necessaria qui
            None,
            None,
            0,
        )
        return base64.b64encode(blob).decode("ascii")

    # Fallback non sicuro, solo per sviluppo su sistemi non Windows.
    return _DEV_FALLBACK_PREFIX + base64.b64encode(plain.encode("utf-8")).decode("ascii")


def decrypt_password(token: str) -> str:
    """Decifra una password salvata con encrypt_password. Ritorna '' se non decifrabile."""
    if not token:
        return ""

    if token.startswith(_DEV_FALLBACK_PREFIX):
        try:
            return base64.b64decode(token[len(_DEV_FALLBACK_PREFIX):]).decode("utf-8")
        except Exception:
            return ""

    if not _has_dpapi():
        # Un blob cifrato con DPAPI su un'altra macchina non e' decifrabile
        # qui (ne' dovrebbe esserlo, e' il comportamento corretto di DPAPI).
        return ""

    import win32crypt

    try:
        raw = base64.b64decode(token)
        _descr, data = win32crypt.CryptUnprotectData(raw, None, None, None, 0)
        return data.decode("utf-8")
    except Exception:
        return ""
