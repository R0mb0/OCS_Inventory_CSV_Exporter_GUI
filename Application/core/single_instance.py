"""
Blocco "singola istanza": impedisce che due copie dell'app girino insieme
sulla stessa macchina (puo' succedere facilmente in un contesto di
autostart: es. sia la cartella Esecuzione automatica sia un'Attivita'
pianificata configurate per errore, oppure un utente che apre l'app a
mano mentre quella di autostart e' gia' partita). Due istanze in
esecuzione insieme farebbero doppio login su OCS e doppie scritture di
CSV nella stessa cartella.

Implementazione: un mutex di sistema con nome fisso ("named mutex" di
Windows). E' l'approccio standard per le app desktop Windows: a
differenza di un file di lock, viene rilasciato automaticamente dal
sistema operativo anche se il processo precedente e' terminato in modo
anomalo (crash, kill da Task Manager), quindi non rischia di restare
"bloccato" per sempre come puo' succedere con un file di lock orfano.

Su sistemi non Windows (sviluppo) la funzione non fa nulla e dichiara
sempre che non c'e' un'altra istanza, dato che il meccanismo e' specifico
di Windows.
"""

from __future__ import annotations

MUTEX_NAME = "Global\\OCSExporterSingleInstanceMutex"

# Riferimento tenuto vivo per tutta la durata del processo: se venisse
# raccolto dal garbage collector, il mutex si libererebbe subito.
_mutex_handle = None


def acquire_single_instance() -> bool:
    """Ritorna True se questa e' l'unica istanza in esecuzione (lock preso).

    Ritorna False se un'altra istanza ha gia' il lock: chi chiama dovrebbe
    avvisare l'utente e uscire subito, senza fare nient'altro (in
    particolare senza toccare config.json o avviare un secondo loop).
    """
    global _mutex_handle
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32  # esiste solo su Windows
    except (ImportError, AttributeError):
        return True  # piattaforma non Windows: nessun controllo, sempre "libero"

    ERROR_ALREADY_EXISTS = 183
    handle = kernel32.CreateMutexW(None, False, MUTEX_NAME)
    if not handle:
        # Impossibile creare il mutex per qualche motivo: non blocchiamo
        # l'avvio dell'app solo per questo.
        return True

    already_running = kernel32.GetLastError() == ERROR_ALREADY_EXISTS
    _mutex_handle = handle  # tenuto vivo finche' il processo e' in esecuzione
    return not already_running
