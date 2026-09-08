"""
Internationalization (i18n) for the OCS Exporter GUI.

Supported languages: it, en, de, fr, es, nl. The active language defaults to
the operating system's language (detected via QLocale.system()) and falls
back to English if the system language isn't one of the six supported ones.
The user can override it manually from the Edit > Language menu; the choice
is persisted in config.json (key "language": "auto" | "it" | "en" | ... )
exactly like the "theme" setting.

Usage:
    from core.i18n import t, set_language, current_language

    label.setText(t("settings.connection"))
    set_language("de")                  # switch, returns the effective code
    t("engine.columns_found", count=12) # supports .format(**kwargs)

All widgets that display translated text should implement a
`retranslate_ui()` method that re-applies t(...) to every label/button/etc.,
so the whole GUI updates immediately when the language changes, without
needing to restart the app.
"""

from __future__ import annotations

SUPPORTED_LANGUAGES = ["it", "en", "de", "fr", "es", "nl"]
DEFAULT_LANGUAGE = "en"

# Native display names, shown as-is in the language menu regardless of the
# currently active UI language (same convention used by browsers and OSes).
LANGUAGE_NAMES = {
    "it": "Italiano",
    "en": "English",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
    "nl": "Nederlands",
}

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "menu.file": "File",
        "menu.exit": "Exit",
        "menu.edit": "Edit",
        "menu.theme": "Theme",
        "menu.theme_auto": "Automatic",
        "menu.theme_light": "Light",
        "menu.theme_dark": "Dark",
        "menu.language": "Language",
        "menu.language_auto": "Automatic (system)",

        "status_bar.config_path": "Configuration: {path}",

        "log.gui_ready": "GUI ready. Fill in the settings (if not already saved) and press START.",
        "log.theme_set": "Theme set to '{mode}' (effective: {effective}).",
        "log.language_set": "Language set to '{lang}'.",
        "log.settings_saved": "Settings saved (URL, username, password, loop, output folder).",
        "log.cannot_start": "Cannot start: {msg}.",
        "log.invalid_output_dir": "Invalid output folder: {exc}",

        "missing.ocs_url": "OCS URL",
        "missing.username": "Username",
        "missing.password": "Password",
        "missing.output_folder": "CSV folder",
        "missing.prefix": "Please fill in first: {fields}",

        "dialog.ok": "OK",
        "dialog.yes": "Yes",
        "dialog.no": "No",
        "dialog.incomplete_settings_title": "Incomplete settings",
        "dialog.invalid_folder_title": "Invalid folder",
        "dialog.already_running_title": "OCS Exporter",
        "dialog.already_running_text": "OCS Exporter is already running on this machine.\nCheck the already-open window (or the taskbar icon).",
        "dialog.close_confirm_title": "Export in progress",
        "dialog.close_confirm_text": "The extraction loop is running. Stop it and quit?\n(a running extraction is always allowed to finish first)",

        "control.start": "START",
        "control.stop": "STOP",
        "control.status_prefix": "Status: {text}",

        "status.running": "running",
        "status.stopped": "stopped",
        "status.stopping": "stopping, waiting for the current cycle to finish...",
        "status.next_run": "next extraction at {time}",
        "status.last_success": "last extraction OK at {time} ({filename})",
        "status.last_error": "last error at {time}: {message}",

        "settings.connection": "Connection",
        "settings.url_label": "OCS URL:",
        "settings.url_placeholder": "http://your-ocs-server/ocsreports",
        "settings.username_label": "Username:",
        "settings.password_label": "Password:",
        "settings.show_password": "Show",
        "settings.loop": "Extraction loop",
        "settings.every": "Every",
        "settings.interval_label": "Interval:",
        "settings.output": "Output",
        "settings.csv_folder_label": "CSV folder:",
        "settings.csv_folder_placeholder": "C:\\OCS\\export",
        "settings.browse": "Browse...",
        "settings.browse_dialog_title": "Choose output folder",
        "settings.keep_at_most": "Keep at most",
        "settings.keep_at_most_suffix": "CSV files (deletes the oldest ones beyond this number)",
        "settings.delete_older_than": "Delete if older than",
        "settings.save_button": "Save settings",
        "settings.saved_at": "Saved at {time}",

        "unit.minutes": "minutes",
        "unit.hours": "hours",
        "unit.days": "days",
        "unit.weeks": "weeks",
        "unit.months": "months",
        "unit.years": "years",

        "log_panel.placeholder": "The extraction log will appear here (last {n} lines; older ones are discarded).",
        "log_panel.clear_button": "Clear log",

        "engine.starting": "Starting automation...",
        "engine.opening_login": "Opening login page",
        "engine.filling_credentials": "Filling in credentials",
        "engine.submitting_login": "Submitting login",
        "engine.opening_search": "Opening search page",
        "engine.columns_found": "Columns found: {count}",
        "engine.toggle_column": "Toggling column {i}/{total}: {value}",
        "engine.stabilizing": "Waiting for the page to stabilize...",
        "engine.starting_download": "Starting CSV download",
        "engine.download_complete": "Download complete",
        "engine.cleaning_browser": "Cleaning up browser context",
        "engine.success": "SUCCESS: {path}",
        "engine.error_timeout": "Timeout during extraction: {exc}",
        "engine.error_csv_not_found": "CSV not found.",
        "engine.error_html_not_csv": "The file is HTML, not CSV (likely a failed login or an expired session).",

        "scheduler.error": "ERROR: {exc}",
        "scheduler.unexpected_error": "UNEXPECTED ERROR: {exc}",
        "scheduler.cleanup_error": "Error during old CSV cleanup: {exc}",
        "scheduler.loop_stopped": "Loop stopped.",

        "cleanup.deleted": "CSV cleanup: deleted {name}",
        "cleanup.delete_failed": "CSV cleanup: could not delete {name}: {exc}",
    },

    "it": {
        "menu.file": "File",
        "menu.exit": "Esci",
        "menu.edit": "Modifica",
        "menu.theme": "Tema",
        "menu.theme_auto": "Automatico",
        "menu.theme_light": "Chiaro",
        "menu.theme_dark": "Scuro",
        "menu.language": "Lingua",
        "menu.language_auto": "Automatica (sistema)",

        "status_bar.config_path": "Configurazione: {path}",

        "log.gui_ready": "GUI pronta. Compila le impostazioni (se non gia' salvate) e premi AVVIA.",
        "log.theme_set": "Tema impostato su '{mode}' (effettivo: {effective}).",
        "log.language_set": "Lingua impostata su '{lang}'.",
        "log.settings_saved": "Impostazioni salvate (URL, utente, password, loop, cartella output).",
        "log.cannot_start": "Impossibile avviare: {msg}.",
        "log.invalid_output_dir": "Cartella di output non valida: {exc}",

        "missing.ocs_url": "URL OCS",
        "missing.username": "Utente",
        "missing.password": "Password",
        "missing.output_folder": "Cartella CSV",
        "missing.prefix": "Compila prima: {fields}",

        "dialog.ok": "OK",
        "dialog.yes": "Sì",
        "dialog.no": "No",
        "dialog.incomplete_settings_title": "Impostazioni incomplete",
        "dialog.invalid_folder_title": "Cartella non valida",
        "dialog.already_running_title": "OCS Exporter",
        "dialog.already_running_text": "OCS Exporter e' gia' in esecuzione su questa macchina.\nControlla la finestra gia' aperta (o l'icona nella barra delle applicazioni).",
        "dialog.close_confirm_title": "Estrazione in corso",
        "dialog.close_confirm_text": "Il loop di estrazione e' attivo. Fermarlo e uscire?\n(se un'estrazione e' in corso viene sempre lasciata terminare)",

        "control.start": "AVVIA",
        "control.stop": "STOP",
        "control.status_prefix": "Stato: {text}",

        "status.running": "in esecuzione",
        "status.stopped": "fermo",
        "status.stopping": "arresto in corso, attendo la fine del ciclo...",
        "status.next_run": "prossima estrazione alle {time}",
        "status.last_success": "ultima estrazione OK alle {time} ({filename})",
        "status.last_error": "ultimo errore alle {time}: {message}",

        "settings.connection": "Connessione",
        "settings.url_label": "URL OCS:",
        "settings.url_placeholder": "http://your-ocs-server/ocsreports",
        "settings.username_label": "Utente:",
        "settings.password_label": "Password:",
        "settings.show_password": "Mostra",
        "settings.loop": "Loop di estrazione",
        "settings.every": "Ogni",
        "settings.interval_label": "Intervallo:",
        "settings.output": "Output",
        "settings.csv_folder_label": "Cartella CSV:",
        "settings.csv_folder_placeholder": "C:\\OCS\\export",
        "settings.browse": "Sfoglia...",
        "settings.browse_dialog_title": "Scegli cartella di output",
        "settings.keep_at_most": "Mantieni al massimo",
        "settings.keep_at_most_suffix": "file CSV (elimina i piu' vecchi oltre questo numero)",
        "settings.delete_older_than": "Elimina se piu' vecchi di",
        "settings.save_button": "Salva impostazioni",
        "settings.saved_at": "Salvato alle {time}",

        "unit.minutes": "minuti",
        "unit.hours": "ore",
        "unit.days": "giorni",
        "unit.weeks": "settimane",
        "unit.months": "mesi",
        "unit.years": "anni",

        "log_panel.placeholder": "Il log dell'estrazione comparira' qui (ultime {n} righe; quelle piu' vecchie vengono scartate).",
        "log_panel.clear_button": "Pulisci log",

        "engine.starting": "Avvio automazione...",
        "engine.opening_login": "Apro login page",
        "engine.filling_credentials": "Compilo credenziali",
        "engine.submitting_login": "Invio login",
        "engine.opening_search": "Apro pagina ricerca",
        "engine.columns_found": "Colonne trovate: {count}",
        "engine.toggle_column": "Toggle colonna {i}/{total}: {value}",
        "engine.stabilizing": "Attendo stabilizzazione...",
        "engine.starting_download": "Avvio download CSV",
        "engine.download_complete": "Download completato",
        "engine.cleaning_browser": "Pulizia browser context",
        "engine.success": "SUCCESSO: {path}",
        "engine.error_timeout": "Timeout durante l'estrazione: {exc}",
        "engine.error_csv_not_found": "CSV non trovato.",
        "engine.error_html_not_csv": "Il file e' HTML, non CSV (probabile login fallito o sessione scaduta).",

        "scheduler.error": "ERRORE: {exc}",
        "scheduler.unexpected_error": "ERRORE IMPREVISTO: {exc}",
        "scheduler.cleanup_error": "Errore durante la pulizia dei CSV vecchi: {exc}",
        "scheduler.loop_stopped": "Loop fermato.",

        "cleanup.deleted": "Pulizia CSV: eliminato {name}",
        "cleanup.delete_failed": "Pulizia CSV: impossibile eliminare {name}: {exc}",
    },

    "de": {
        "menu.file": "Datei",
        "menu.exit": "Beenden",
        "menu.edit": "Bearbeiten",
        "menu.theme": "Design",
        "menu.theme_auto": "Automatisch",
        "menu.theme_light": "Hell",
        "menu.theme_dark": "Dunkel",
        "menu.language": "Sprache",
        "menu.language_auto": "Automatisch (System)",

        "status_bar.config_path": "Konfiguration: {path}",

        "log.gui_ready": "GUI bereit. Einstellungen ausfüllen (falls noch nicht gespeichert) und START drücken.",
        "log.theme_set": "Design auf '{mode}' gesetzt (aktiv: {effective}).",
        "log.language_set": "Sprache auf '{lang}' gesetzt.",
        "log.settings_saved": "Einstellungen gespeichert (URL, Benutzer, Passwort, Intervall, Ausgabeordner).",
        "log.cannot_start": "Start nicht möglich: {msg}.",
        "log.invalid_output_dir": "Ungültiger Ausgabeordner: {exc}",

        "missing.ocs_url": "OCS-URL",
        "missing.username": "Benutzername",
        "missing.password": "Passwort",
        "missing.output_folder": "CSV-Ordner",
        "missing.prefix": "Bitte zuerst ausfüllen: {fields}",

        "dialog.ok": "OK",
        "dialog.yes": "Ja",
        "dialog.no": "Nein",
        "dialog.incomplete_settings_title": "Einstellungen unvollständig",
        "dialog.invalid_folder_title": "Ungültiger Ordner",
        "dialog.already_running_title": "OCS Exporter",
        "dialog.already_running_text": "OCS Exporter läuft bereits auf diesem Rechner.\nPrüfe das bereits geöffnete Fenster (oder das Symbol in der Taskleiste).",
        "dialog.close_confirm_title": "Export läuft",
        "dialog.close_confirm_text": "Die Extraktionsschleife läuft. Anhalten und beenden?\n(ein laufender Export wird immer zuerst zu Ende geführt)",

        "control.start": "START",
        "control.stop": "STOP",
        "control.status_prefix": "Status: {text}",

        "status.running": "läuft",
        "status.stopped": "gestoppt",
        "status.stopping": "wird angehalten, warte auf das Ende des aktuellen Zyklus...",
        "status.next_run": "nächster Export um {time}",
        "status.last_success": "letzter Export OK um {time} ({filename})",
        "status.last_error": "letzter Fehler um {time}: {message}",

        "settings.connection": "Verbindung",
        "settings.url_label": "OCS-URL:",
        "settings.url_placeholder": "http://your-ocs-server/ocsreports",
        "settings.username_label": "Benutzername:",
        "settings.password_label": "Passwort:",
        "settings.show_password": "Anzeigen",
        "settings.loop": "Export-Intervall",
        "settings.every": "Alle",
        "settings.interval_label": "Intervall:",
        "settings.output": "Ausgabe",
        "settings.csv_folder_label": "CSV-Ordner:",
        "settings.csv_folder_placeholder": "C:\\OCS\\export",
        "settings.browse": "Durchsuchen...",
        "settings.browse_dialog_title": "Ausgabeordner wählen",
        "settings.keep_at_most": "Höchstens behalten",
        "settings.keep_at_most_suffix": "CSV-Dateien (löscht die ältesten über dieser Anzahl)",
        "settings.delete_older_than": "Löschen, wenn älter als",
        "settings.save_button": "Einstellungen speichern",
        "settings.saved_at": "Gespeichert um {time}",

        "unit.minutes": "Minuten",
        "unit.hours": "Stunden",
        "unit.days": "Tage",
        "unit.weeks": "Wochen",
        "unit.months": "Monate",
        "unit.years": "Jahre",

        "log_panel.placeholder": "Das Extraktionsprotokoll erscheint hier (letzte {n} Zeilen; ältere werden verworfen).",
        "log_panel.clear_button": "Protokoll leeren",

        "engine.starting": "Automatisierung wird gestartet...",
        "engine.opening_login": "Öffne Login-Seite",
        "engine.filling_credentials": "Trage Zugangsdaten ein",
        "engine.submitting_login": "Sende Login",
        "engine.opening_search": "Öffne Suchseite",
        "engine.columns_found": "Gefundene Spalten: {count}",
        "engine.toggle_column": "Schalte Spalte {i}/{total} um: {value}",
        "engine.stabilizing": "Warte auf Stabilisierung...",
        "engine.starting_download": "Starte CSV-Download",
        "engine.download_complete": "Download abgeschlossen",
        "engine.cleaning_browser": "Räume Browser-Kontext auf",
        "engine.success": "ERFOLG: {path}",
        "engine.error_timeout": "Zeitüberschreitung während der Extraktion: {exc}",
        "engine.error_csv_not_found": "CSV nicht gefunden.",
        "engine.error_html_not_csv": "Die Datei ist HTML, keine CSV (vermutlich fehlgeschlagener Login oder abgelaufene Sitzung).",

        "scheduler.error": "FEHLER: {exc}",
        "scheduler.unexpected_error": "UNERWARTETER FEHLER: {exc}",
        "scheduler.cleanup_error": "Fehler beim Aufräumen alter CSV-Dateien: {exc}",
        "scheduler.loop_stopped": "Schleife gestoppt.",

        "cleanup.deleted": "CSV-Aufräumung: {name} gelöscht",
        "cleanup.delete_failed": "CSV-Aufräumung: {name} konnte nicht gelöscht werden: {exc}",
    },

    "fr": {
        "menu.file": "Fichier",
        "menu.exit": "Quitter",
        "menu.edit": "Édition",
        "menu.theme": "Thème",
        "menu.theme_auto": "Automatique",
        "menu.theme_light": "Clair",
        "menu.theme_dark": "Sombre",
        "menu.language": "Langue",
        "menu.language_auto": "Automatique (système)",

        "status_bar.config_path": "Configuration : {path}",

        "log.gui_ready": "Interface prête. Complétez les paramètres (si pas déjà enregistrés) puis appuyez sur DÉMARRER.",
        "log.theme_set": "Thème réglé sur « {mode} » (effectif : {effective}).",
        "log.language_set": "Langue réglée sur « {lang} ».",
        "log.settings_saved": "Paramètres enregistrés (URL, utilisateur, mot de passe, intervalle, dossier de sortie).",
        "log.cannot_start": "Démarrage impossible : {msg}.",
        "log.invalid_output_dir": "Dossier de sortie invalide : {exc}",

        "missing.ocs_url": "URL OCS",
        "missing.username": "Utilisateur",
        "missing.password": "Mot de passe",
        "missing.output_folder": "Dossier CSV",
        "missing.prefix": "Veuillez d'abord compléter : {fields}",

        "dialog.ok": "OK",
        "dialog.yes": "Oui",
        "dialog.no": "Non",
        "dialog.incomplete_settings_title": "Paramètres incomplets",
        "dialog.invalid_folder_title": "Dossier invalide",
        "dialog.already_running_title": "OCS Exporter",
        "dialog.already_running_text": "OCS Exporter est déjà en cours d'exécution sur cette machine.\nVérifiez la fenêtre déjà ouverte (ou l'icône dans la barre des tâches).",
        "dialog.close_confirm_title": "Export en cours",
        "dialog.close_confirm_text": "La boucle d'extraction est active. L'arrêter et quitter ?\n(un export en cours a toujours le temps de se terminer)",

        "control.start": "DÉMARRER",
        "control.stop": "STOP",
        "control.status_prefix": "État : {text}",

        "status.running": "en cours",
        "status.stopped": "arrêté",
        "status.stopping": "arrêt en cours, attente de la fin du cycle actuel...",
        "status.next_run": "prochain export à {time}",
        "status.last_success": "dernier export réussi à {time} ({filename})",
        "status.last_error": "dernière erreur à {time} : {message}",

        "settings.connection": "Connexion",
        "settings.url_label": "URL OCS :",
        "settings.url_placeholder": "http://your-ocs-server/ocsreports",
        "settings.username_label": "Utilisateur :",
        "settings.password_label": "Mot de passe :",
        "settings.show_password": "Afficher",
        "settings.loop": "Boucle d'extraction",
        "settings.every": "Toutes les",
        "settings.interval_label": "Intervalle :",
        "settings.output": "Sortie",
        "settings.csv_folder_label": "Dossier CSV :",
        "settings.csv_folder_placeholder": "C:\\OCS\\export",
        "settings.browse": "Parcourir...",
        "settings.browse_dialog_title": "Choisir le dossier de sortie",
        "settings.keep_at_most": "Conserver au maximum",
        "settings.keep_at_most_suffix": "fichiers CSV (supprime les plus anciens au-delà de ce nombre)",
        "settings.delete_older_than": "Supprimer si plus vieux que",
        "settings.save_button": "Enregistrer les paramètres",
        "settings.saved_at": "Enregistré à {time}",

        "unit.minutes": "minutes",
        "unit.hours": "heures",
        "unit.days": "jours",
        "unit.weeks": "semaines",
        "unit.months": "mois",
        "unit.years": "ans",

        "log_panel.placeholder": "Le journal d'extraction apparaîtra ici (les {n} dernières lignes ; les plus anciennes sont supprimées).",
        "log_panel.clear_button": "Effacer le journal",

        "engine.starting": "Démarrage de l'automatisation...",
        "engine.opening_login": "Ouverture de la page de connexion",
        "engine.filling_credentials": "Saisie des identifiants",
        "engine.submitting_login": "Envoi de la connexion",
        "engine.opening_search": "Ouverture de la page de recherche",
        "engine.columns_found": "Colonnes trouvées : {count}",
        "engine.toggle_column": "Activation colonne {i}/{total} : {value}",
        "engine.stabilizing": "Attente de la stabilisation...",
        "engine.starting_download": "Démarrage du téléchargement CSV",
        "engine.download_complete": "Téléchargement terminé",
        "engine.cleaning_browser": "Nettoyage du contexte du navigateur",
        "engine.success": "SUCCÈS : {path}",
        "engine.error_timeout": "Délai dépassé pendant l'extraction : {exc}",
        "engine.error_csv_not_found": "CSV introuvable.",
        "engine.error_html_not_csv": "Le fichier est en HTML, pas en CSV (échec de connexion probable ou session expirée).",

        "scheduler.error": "ERREUR : {exc}",
        "scheduler.unexpected_error": "ERREUR INATTENDUE : {exc}",
        "scheduler.cleanup_error": "Erreur lors du nettoyage des anciens CSV : {exc}",
        "scheduler.loop_stopped": "Boucle arrêtée.",

        "cleanup.deleted": "Nettoyage CSV : {name} supprimé",
        "cleanup.delete_failed": "Nettoyage CSV : impossible de supprimer {name} : {exc}",
    },

    "es": {
        "menu.file": "Archivo",
        "menu.exit": "Salir",
        "menu.edit": "Editar",
        "menu.theme": "Tema",
        "menu.theme_auto": "Automático",
        "menu.theme_light": "Claro",
        "menu.theme_dark": "Oscuro",
        "menu.language": "Idioma",
        "menu.language_auto": "Automático (sistema)",

        "status_bar.config_path": "Configuración: {path}",

        "log.gui_ready": "Interfaz lista. Completa los ajustes (si aún no están guardados) y pulsa INICIAR.",
        "log.theme_set": "Tema establecido en '{mode}' (efectivo: {effective}).",
        "log.language_set": "Idioma establecido en '{lang}'.",
        "log.settings_saved": "Ajustes guardados (URL, usuario, contraseña, intervalo, carpeta de salida).",
        "log.cannot_start": "No se puede iniciar: {msg}.",
        "log.invalid_output_dir": "Carpeta de salida no válida: {exc}",

        "missing.ocs_url": "URL de OCS",
        "missing.username": "Usuario",
        "missing.password": "Contraseña",
        "missing.output_folder": "Carpeta CSV",
        "missing.prefix": "Completa primero: {fields}",

        "dialog.ok": "OK",
        "dialog.yes": "Sí",
        "dialog.no": "No",
        "dialog.incomplete_settings_title": "Ajustes incompletos",
        "dialog.invalid_folder_title": "Carpeta no válida",
        "dialog.already_running_title": "OCS Exporter",
        "dialog.already_running_text": "OCS Exporter ya se está ejecutando en esta máquina.\nRevisa la ventana ya abierta (o el icono en la barra de tareas).",
        "dialog.close_confirm_title": "Exportación en curso",
        "dialog.close_confirm_text": "El bucle de extracción está activo. ¿Detenerlo y salir?\n(una extracción en curso siempre puede terminar primero)",

        "control.start": "INICIAR",
        "control.stop": "STOP",
        "control.status_prefix": "Estado: {text}",

        "status.running": "en ejecución",
        "status.stopped": "detenido",
        "status.stopping": "deteniendo, esperando a que termine el ciclo actual...",
        "status.next_run": "próxima extracción a las {time}",
        "status.last_success": "última extracción correcta a las {time} ({filename})",
        "status.last_error": "último error a las {time}: {message}",

        "settings.connection": "Conexión",
        "settings.url_label": "URL de OCS:",
        "settings.url_placeholder": "http://your-ocs-server/ocsreports",
        "settings.username_label": "Usuario:",
        "settings.password_label": "Contraseña:",
        "settings.show_password": "Mostrar",
        "settings.loop": "Bucle de extracción",
        "settings.every": "Cada",
        "settings.interval_label": "Intervalo:",
        "settings.output": "Salida",
        "settings.csv_folder_label": "Carpeta CSV:",
        "settings.csv_folder_placeholder": "C:\\OCS\\export",
        "settings.browse": "Examinar...",
        "settings.browse_dialog_title": "Elegir carpeta de salida",
        "settings.keep_at_most": "Mantener como máximo",
        "settings.keep_at_most_suffix": "archivos CSV (elimina los más antiguos por encima de este número)",
        "settings.delete_older_than": "Eliminar si es más antiguo que",
        "settings.save_button": "Guardar ajustes",
        "settings.saved_at": "Guardado a las {time}",

        "unit.minutes": "minutos",
        "unit.hours": "horas",
        "unit.days": "días",
        "unit.weeks": "semanas",
        "unit.months": "meses",
        "unit.years": "años",

        "log_panel.placeholder": "El registro de extracción aparecerá aquí (últimas {n} líneas; las más antiguas se descartan).",
        "log_panel.clear_button": "Borrar registro",

        "engine.starting": "Iniciando automatización...",
        "engine.opening_login": "Abriendo página de acceso",
        "engine.filling_credentials": "Rellenando credenciales",
        "engine.submitting_login": "Enviando acceso",
        "engine.opening_search": "Abriendo página de búsqueda",
        "engine.columns_found": "Columnas encontradas: {count}",
        "engine.toggle_column": "Activando columna {i}/{total}: {value}",
        "engine.stabilizing": "Esperando estabilización...",
        "engine.starting_download": "Iniciando descarga del CSV",
        "engine.download_complete": "Descarga completada",
        "engine.cleaning_browser": "Limpiando contexto del navegador",
        "engine.success": "ÉXITO: {path}",
        "engine.error_timeout": "Tiempo de espera agotado durante la extracción: {exc}",
        "engine.error_csv_not_found": "CSV no encontrado.",
        "engine.error_html_not_csv": "El archivo es HTML, no CSV (probable fallo de acceso o sesión caducada).",

        "scheduler.error": "ERROR: {exc}",
        "scheduler.unexpected_error": "ERROR INESPERADO: {exc}",
        "scheduler.cleanup_error": "Error durante la limpieza de CSV antiguos: {exc}",
        "scheduler.loop_stopped": "Bucle detenido.",

        "cleanup.deleted": "Limpieza CSV: {name} eliminado",
        "cleanup.delete_failed": "Limpieza CSV: no se pudo eliminar {name}: {exc}",
    },

    "nl": {
        "menu.file": "Bestand",
        "menu.exit": "Afsluiten",
        "menu.edit": "Bewerken",
        "menu.theme": "Thema",
        "menu.theme_auto": "Automatisch",
        "menu.theme_light": "Licht",
        "menu.theme_dark": "Donker",
        "menu.language": "Taal",
        "menu.language_auto": "Automatisch (systeem)",

        "status_bar.config_path": "Configuratie: {path}",

        "log.gui_ready": "GUI klaar. Vul de instellingen in (indien nog niet opgeslagen) en druk op START.",
        "log.theme_set": "Thema ingesteld op '{mode}' (effectief: {effective}).",
        "log.language_set": "Taal ingesteld op '{lang}'.",
        "log.settings_saved": "Instellingen opgeslagen (URL, gebruiker, wachtwoord, interval, uitvoermap).",
        "log.cannot_start": "Kan niet starten: {msg}.",
        "log.invalid_output_dir": "Ongeldige uitvoermap: {exc}",

        "missing.ocs_url": "OCS-URL",
        "missing.username": "Gebruikersnaam",
        "missing.password": "Wachtwoord",
        "missing.output_folder": "CSV-map",
        "missing.prefix": "Vul eerst in: {fields}",

        "dialog.ok": "OK",
        "dialog.yes": "Ja",
        "dialog.no": "Nee",
        "dialog.incomplete_settings_title": "Instellingen onvolledig",
        "dialog.invalid_folder_title": "Ongeldige map",
        "dialog.already_running_title": "OCS Exporter",
        "dialog.already_running_text": "OCS Exporter draait al op deze computer.\nControleer het reeds geopende venster (of het pictogram in de taakbalk).",
        "dialog.close_confirm_title": "Export bezig",
        "dialog.close_confirm_text": "De extractielus is actief. Stoppen en afsluiten?\n(een lopende extractie mag altijd eerst worden afgerond)",

        "control.start": "START",
        "control.stop": "STOP",
        "control.status_prefix": "Status: {text}",

        "status.running": "actief",
        "status.stopped": "gestopt",
        "status.stopping": "wordt gestopt, wacht op het einde van de huidige cyclus...",
        "status.next_run": "volgende extractie om {time}",
        "status.last_success": "laatste extractie OK om {time} ({filename})",
        "status.last_error": "laatste fout om {time}: {message}",

        "settings.connection": "Verbinding",
        "settings.url_label": "OCS-URL:",
        "settings.username_label": "Gebruikersnaam:",
        "settings.password_label": "Wachtwoord:",
        "settings.show_password": "Tonen",
        "settings.loop": "Extractielus",
        "settings.every": "Elke",
        "settings.interval_label": "Interval:",
        "settings.output": "Uitvoer",
        "settings.csv_folder_label": "CSV-map:",
        "settings.csv_folder_placeholder": "C:\\OCS\\export",
        "settings.browse": "Bladeren...",
        "settings.browse_dialog_title": "Kies uitvoermap",
        "settings.keep_at_most": "Maximaal bewaren",
        "settings.keep_at_most_suffix": "CSV-bestanden (verwijdert de oudste boven dit aantal)",
        "settings.delete_older_than": "Verwijderen als ouder dan",
        "settings.save_button": "Instellingen opslaan",
        "settings.saved_at": "Opgeslagen om {time}",
        "settings.url_placeholder": "http://your-ocs-server/ocsreports",

        "unit.minutes": "minuten",
        "unit.hours": "uur",
        "unit.days": "dagen",
        "unit.weeks": "weken",
        "unit.months": "maanden",
        "unit.years": "jaar",

        "log_panel.placeholder": "Het extractielogboek verschijnt hier (laatste {n} regels; oudere worden verwijderd).",
        "log_panel.clear_button": "Logboek wissen",

        "engine.starting": "Automatisering wordt gestart...",
        "engine.opening_login": "Inlogpagina wordt geopend",
        "engine.filling_credentials": "Inloggegevens invullen",
        "engine.submitting_login": "Login verzenden",
        "engine.opening_search": "Zoekpagina wordt geopend",
        "engine.columns_found": "Gevonden kolommen: {count}",
        "engine.toggle_column": "Kolom {i}/{total} wordt geschakeld: {value}",
        "engine.stabilizing": "Wachten op stabilisatie...",
        "engine.starting_download": "CSV-download wordt gestart",
        "engine.download_complete": "Download voltooid",
        "engine.cleaning_browser": "Browsercontext wordt opgeruimd",
        "engine.success": "GESLAAGD: {path}",
        "engine.error_timeout": "Time-out tijdens de extractie: {exc}",
        "engine.error_csv_not_found": "CSV niet gevonden.",
        "engine.error_html_not_csv": "Het bestand is HTML, geen CSV (waarschijnlijk mislukte login of verlopen sessie).",

        "scheduler.error": "FOUT: {exc}",
        "scheduler.unexpected_error": "ONVERWACHTE FOUT: {exc}",
        "scheduler.cleanup_error": "Fout tijdens het opruimen van oude CSV-bestanden: {exc}",
        "scheduler.loop_stopped": "Lus gestopt.",

        "cleanup.deleted": "CSV-opruiming: {name} verwijderd",
        "cleanup.delete_failed": "CSV-opruiming: kon {name} niet verwijderen: {exc}",
    },
}

_current_language = DEFAULT_LANGUAGE


def detect_system_language() -> str:
    """Detects the OS UI language via Qt, mapped to a supported code.

    Falls back to English if PySide6/Qt isn't available yet, or if the
    system language isn't one of the six supported ones.
    """
    try:
        from PySide6.QtCore import QLocale

        name = QLocale.system().name()  # e.g. "it_IT", "de_DE", "en_US"
        code = name.split("_")[0].lower()
        if code in TRANSLATIONS:
            return code
    except Exception:  # noqa: BLE001 - detection must never crash startup
        pass
    return DEFAULT_LANGUAGE


def set_language(code: str) -> str:
    """Sets the active language. Returns the effective code actually applied."""
    global _current_language
    if code not in TRANSLATIONS:
        code = DEFAULT_LANGUAGE
    _current_language = code
    return _current_language


def current_language() -> str:
    return _current_language


def t(key: str, **kwargs) -> str:
    """Translates `key` in the current language, formatting with kwargs.

    Falls back to English if the key is missing in the current language,
    and to the raw key itself if it's missing everywhere (so a typo or a
    not-yet-translated string never crashes the app).
    """
    dict_current = TRANSLATIONS.get(_current_language, {})
    dict_fallback = TRANSLATIONS[DEFAULT_LANGUAGE]
    template = dict_current.get(key) or dict_fallback.get(key) or key
    if kwargs:
        try:
            return template.format(**kwargs)
        except (KeyError, IndexError):
            return template
    return template
