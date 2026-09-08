/* Translations for the OCS Inventory CSV Exporter GUI project page.
   Supported languages: it, en, de, fr, es, nl. Add a new language by
   copying the "en" block and translating every value. */

const TRANSLATIONS = {
  en: {
    meta: { title: "OCS Inventory CSV Exporter GUI", description: "A Windows desktop app that automates scheduled CSV exports from OCS Inventory NG." },
    nav: { features: "Features", howItWorks: "How it works", requirements: "Requirements", download: "Download" },
    hero: {
      title: "Scheduled OCS Inventory exports, on autopilot.",
      tagline: "A Windows desktop app that logs into OCS Inventory NG, exports a full CSV on a schedule, cleans up old files on its own, and comes back after a reboot — no one needs to be watching.",
      ctaGithub: "View source on GitHub",
      ctaDownload: "Get the latest release"
    },
    features: {
      title: "What it does",
      sub: "Everything the original PowerShell script did, plus a control panel that runs it for you.",
      item1: { title: "Layered, resizable GUI", desc: "Connection, loop interval and output settings stacked in three sections you can resize by dragging the dividers." },
      item2: { title: "Scheduled extraction loop", desc: "Set an interval in minutes or hours; press the green Avvia button and it keeps exporting until you press Stop." },
      item3: { title: "Automatic cleanup", desc: "Keep only the last N CSV files and/or delete files older than a set period — both rules can run together." },
      item4: { title: "Encrypted credentials", desc: "The OCS password is encrypted at rest with Windows DPAPI — never written to disk in plain text." },
      item5: { title: "Follows your OS theme", desc: "Light and dark mode are detected automatically, with a manual override saved for next time." },
      item6: { title: "Survives a reboot", desc: "An --autostart flag and example launcher get the export loop running again on its own after the server restarts." }
    },
    screenshots: {
      title: "Screenshots",
      sub: "Add your own screenshots of the running app here.",
      placeholder1: "Main window screenshot goes here",
      placeholder2: "Settings panel screenshot goes here"
    },
    howItWorks: {
      title: "How it works",
      sub: "The same automation flow as the original ocs_export.ps1 script, now orchestrated by the app.",
      step1: { title: "Log in", desc: "Signs into OCS Inventory NG using the credentials you configured." },
      step2: { title: "Open advanced search", desc: "Navigates to the advanced search page for the inventory table." },
      step3: { title: "Enable every column", desc: "Toggles every available column so the export is always complete." },
      step4: { title: "Export the CSV", desc: "Triggers the export and saves the file with a timestamped name." },
      step5: { title: "Clean up old files", desc: "Applies your cleanup rules to the output folder, if enabled." },
      step6: { title: "Wait and repeat", desc: "Sleeps for the configured interval, then starts the next cycle." }
    },
    requirements: {
      title: "Requirements",
      item1: "Windows 10 or 11",
      item2: "Python 3.10+ (if running from source)",
      item3: "Network access to your OCS Inventory instance",
      item4: "A valid OCS Inventory user account"
    },
    footer: {
      madeWith: "Built by Francesco Rombaldoni.",
      viewSource: "View source on GitHub",
      license: "Released under the MIT License."
    },
    theme: { toggle: "Toggle light/dark theme" },
    lang: { select: "Choose language" }
  },

  it: {
    meta: { title: "OCS Inventory CSV Exporter GUI", description: "Un'applicazione desktop per Windows che automatizza l'esportazione periodica di CSV da OCS Inventory NG." },
    nav: { features: "Funzionalità", howItWorks: "Come funziona", requirements: "Requisiti", download: "Download" },
    hero: {
      title: "Esportazioni programmate da OCS Inventory, in automatico.",
      tagline: "Un'applicazione desktop per Windows che accede a OCS Inventory NG, esporta un CSV completo a intervalli regolari, elimina da sola i file vecchi e riparte da sola dopo un riavvio — senza bisogno di nessuno davanti allo schermo.",
      ctaGithub: "Vedi il codice su GitHub",
      ctaDownload: "Scarica l'ultima versione"
    },
    features: {
      title: "Cosa fa",
      sub: "Tutto quello che faceva lo script PowerShell originale, più un pannello di controllo che lo gestisce al posto tuo.",
      item1: { title: "Interfaccia a sezioni ridimensionabili", desc: "Connessione, intervallo di loop e impostazioni di output impilati in tre sezioni che puoi ridimensionare trascinando i divisori." },
      item2: { title: "Loop di estrazione programmato", desc: "Imposta un intervallo in minuti o ore; premi il pulsante verde Avvia e l'esportazione continua finché non premi Stop." },
      item3: { title: "Pulizia automatica", desc: "Mantieni solo gli ultimi N file CSV e/o elimina i file più vecchi di un periodo impostato — le due regole possono coesistere." },
      item4: { title: "Credenziali cifrate", desc: "La password OCS è cifrata su disco con Windows DPAPI — non viene mai scritta in chiaro." },
      item5: { title: "Segue il tema del sistema", desc: "Il tema chiaro e scuro viene rilevato automaticamente, con un'opzione manuale salvata per la volta successiva." },
      item6: { title: "Sopravvive a un riavvio", desc: "Un flag --autostart e un launcher di esempio rimettono in moto il loop di estrazione da soli dopo il riavvio del server." }
    },
    screenshots: {
      title: "Screenshot",
      sub: "Aggiungi qui i tuoi screenshot dell'app in funzione.",
      placeholder1: "Qui va lo screenshot della finestra principale",
      placeholder2: "Qui va lo screenshot del pannello impostazioni"
    },
    howItWorks: {
      title: "Come funziona",
      sub: "Lo stesso flusso di automazione dello script originale ocs_export.ps1, ora orchestrato dall'app.",
      step1: { title: "Accesso", desc: "Effettua il login a OCS Inventory NG con le credenziali configurate." },
      step2: { title: "Apre la ricerca avanzata", desc: "Naviga alla pagina di ricerca avanzata della tabella inventario." },
      step3: { title: "Attiva tutte le colonne", desc: "Seleziona tutte le colonne disponibili così l'export è sempre completo." },
      step4: { title: "Esporta il CSV", desc: "Avvia l'esportazione e salva il file con un nome basato sulla data e l'ora." },
      step5: { title: "Pulisce i file vecchi", desc: "Applica le regole di pulizia alla cartella di output, se attivate." },
      step6: { title: "Attende e ripete", desc: "Attende l'intervallo configurato, poi avvia il ciclo successivo." }
    },
    requirements: {
      title: "Requisiti",
      item1: "Windows 10 o 11",
      item2: "Python 3.10+ (se eseguito dai sorgenti)",
      item3: "Accesso di rete alla tua istanza OCS Inventory",
      item4: "Un account utente OCS Inventory valido"
    },
    footer: {
      madeWith: "Realizzato da Francesco Rombaldoni.",
      viewSource: "Vedi il codice su GitHub",
      license: "Distribuito con licenza MIT."
    },
    theme: { toggle: "Cambia tema chiaro/scuro" },
    lang: { select: "Scegli la lingua" }
  },

  de: {
    meta: { title: "OCS Inventory CSV Exporter GUI", description: "Eine Windows-Desktopanwendung, die geplante CSV-Exporte aus OCS Inventory NG automatisiert." },
    nav: { features: "Funktionen", howItWorks: "Funktionsweise", requirements: "Voraussetzungen", download: "Download" },
    hero: {
      title: "Geplante OCS-Inventory-Exporte im Autopiloten.",
      tagline: "Eine Windows-Desktopanwendung, die sich bei OCS Inventory NG anmeldet, in festen Zeitabständen einen vollständigen CSV-Export erstellt, alte Dateien selbstständig aufräumt und nach einem Neustart von selbst wieder anläuft.",
      ctaGithub: "Quellcode auf GitHub ansehen",
      ctaDownload: "Neueste Version herunterladen"
    },
    features: {
      title: "Funktionen im Überblick",
      sub: "Alles, was das ursprüngliche PowerShell-Skript konnte, plus eine Oberfläche, die es für dich steuert.",
      item1: { title: "Mehrstufige, anpassbare Oberfläche", desc: "Verbindung, Intervall und Ausgabeeinstellungen in drei Bereichen, deren Größe du per Ziehen anpassen kannst." },
      item2: { title: "Geplanter Export-Loop", desc: "Intervall in Minuten oder Stunden festlegen, den grünen Avvia-Button drücken — der Export läuft bis zum Stop-Klick." },
      item3: { title: "Automatische Bereinigung", desc: "Nur die letzten N CSV-Dateien behalten und/oder ältere Dateien löschen — beide Regeln lassen sich kombinieren." },
      item4: { title: "Verschlüsselte Zugangsdaten", desc: "Das OCS-Passwort wird mit Windows DPAPI verschlüsselt gespeichert — nie im Klartext." },
      item5: { title: "Folgt deinem Systemdesign", desc: "Hell- und Dunkelmodus werden automatisch erkannt, mit manueller Übersteuerung, die gespeichert bleibt." },
      item6: { title: "Übersteht einen Neustart", desc: "Ein --autostart-Flag und ein Beispiel-Launcher starten den Export-Loop nach einem Serverneustart von selbst neu." }
    },
    screenshots: {
      title: "Screenshots",
      sub: "Füge hier eigene Screenshots der laufenden App ein.",
      placeholder1: "Screenshot des Hauptfensters hier einfügen",
      placeholder2: "Screenshot des Einstellungsbereichs hier einfügen"
    },
    howItWorks: {
      title: "Funktionsweise",
      sub: "Derselbe Automatisierungsablauf wie im ursprünglichen Skript ocs_export.ps1, jetzt von der App gesteuert.",
      step1: { title: "Anmeldung", desc: "Meldet sich mit den konfigurierten Zugangsdaten bei OCS Inventory NG an." },
      step2: { title: "Erweiterte Suche öffnen", desc: "Navigiert zur erweiterten Suchseite der Inventartabelle." },
      step3: { title: "Alle Spalten aktivieren", desc: "Aktiviert jede verfügbare Spalte, damit der Export immer vollständig ist." },
      step4: { title: "CSV exportieren", desc: "Startet den Export und speichert die Datei mit einem Zeitstempel im Namen." },
      step5: { title: "Alte Dateien aufräumen", desc: "Wendet die Bereinigungsregeln auf den Ausgabeordner an, falls aktiviert." },
      step6: { title: "Warten und wiederholen", desc: "Wartet das konfigurierte Intervall ab und startet dann den nächsten Zyklus." }
    },
    requirements: {
      title: "Voraussetzungen",
      item1: "Windows 10 oder 11",
      item2: "Python 3.10+ (bei Ausführung aus dem Quellcode)",
      item3: "Netzwerkzugriff auf deine OCS-Inventory-Instanz",
      item4: "Ein gültiges OCS-Inventory-Benutzerkonto"
    },
    footer: {
      madeWith: "Entwickelt von Francesco Rombaldoni.",
      viewSource: "Quellcode auf GitHub ansehen",
      license: "Veröffentlicht unter der MIT-Lizenz."
    },
    theme: { toggle: "Hell-/Dunkelmodus umschalten" },
    lang: { select: "Sprache wählen" }
  },

  fr: {
    meta: { title: "OCS Inventory CSV Exporter GUI", description: "Une application de bureau Windows qui automatise les exports CSV planifiés depuis OCS Inventory NG." },
    nav: { features: "Fonctionnalités", howItWorks: "Fonctionnement", requirements: "Prérequis", download: "Télécharger" },
    hero: {
      title: "Exports OCS Inventory planifiés, en pilote automatique.",
      tagline: "Une application de bureau Windows qui se connecte à OCS Inventory NG, exporte un CSV complet à intervalles réguliers, nettoie seule les anciens fichiers et redémarre d'elle-même après un redémarrage — sans surveillance nécessaire.",
      ctaGithub: "Voir le code sur GitHub",
      ctaDownload: "Télécharger la dernière version"
    },
    features: {
      title: "Ce qu'elle fait",
      sub: "Tout ce que faisait le script PowerShell d'origine, avec en plus un panneau de contrôle qui s'en occupe pour vous.",
      item1: { title: "Interface en sections redimensionnables", desc: "Connexion, intervalle de boucle et paramètres de sortie répartis en trois sections que vous redimensionnez en faisant glisser les séparateurs." },
      item2: { title: "Boucle d'extraction planifiée", desc: "Définissez un intervalle en minutes ou en heures ; appuyez sur le bouton vert Avvia et l'export continue jusqu'à l'arrêt." },
      item3: { title: "Nettoyage automatique", desc: "Conservez uniquement les N derniers fichiers CSV et/ou supprimez les fichiers plus anciens qu'une période donnée — les deux règles peuvent cohabiter." },
      item4: { title: "Identifiants chiffrés", desc: "Le mot de passe OCS est chiffré au repos avec Windows DPAPI — jamais écrit en clair sur le disque." },
      item5: { title: "Suit le thème du système", desc: "Les thèmes clair et sombre sont détectés automatiquement, avec une préférence manuelle mémorisée." },
      item6: { title: "Résiste à un redémarrage", desc: "Un indicateur --autostart et un lanceur d'exemple relancent seuls la boucle d'export après le redémarrage du serveur." }
    },
    screenshots: {
      title: "Captures d'écran",
      sub: "Ajoutez ici vos propres captures d'écran de l'application en fonctionnement.",
      placeholder1: "Capture d'écran de la fenêtre principale à ajouter ici",
      placeholder2: "Capture d'écran du panneau des paramètres à ajouter ici"
    },
    howItWorks: {
      title: "Fonctionnement",
      sub: "Le même flux d'automatisation que le script d'origine ocs_export.ps1, désormais orchestré par l'application.",
      step1: { title: "Connexion", desc: "Se connecte à OCS Inventory NG avec les identifiants configurés." },
      step2: { title: "Ouvre la recherche avancée", desc: "Accède à la page de recherche avancée de la table d'inventaire." },
      step3: { title: "Active toutes les colonnes", desc: "Coche toutes les colonnes disponibles pour un export toujours complet." },
      step4: { title: "Exporte le CSV", desc: "Déclenche l'export et enregistre le fichier avec un nom horodaté." },
      step5: { title: "Nettoie les anciens fichiers", desc: "Applique les règles de nettoyage au dossier de sortie, si elles sont activées." },
      step6: { title: "Attend et recommence", desc: "Attend l'intervalle configuré, puis démarre le cycle suivant." }
    },
    requirements: {
      title: "Prérequis",
      item1: "Windows 10 ou 11",
      item2: "Python 3.10+ (en exécution depuis les sources)",
      item3: "Accès réseau à votre instance OCS Inventory",
      item4: "Un compte utilisateur OCS Inventory valide"
    },
    footer: {
      madeWith: "Créé par Francesco Rombaldoni.",
      viewSource: "Voir le code sur GitHub",
      license: "Distribué sous licence MIT."
    },
    theme: { toggle: "Basculer entre thème clair/sombre" },
    lang: { select: "Choisir la langue" }
  },

  es: {
    meta: { title: "OCS Inventory CSV Exporter GUI", description: "Una aplicación de escritorio para Windows que automatiza las exportaciones programadas de CSV desde OCS Inventory NG." },
    nav: { features: "Funciones", howItWorks: "Cómo funciona", requirements: "Requisitos", download: "Descargar" },
    hero: {
      title: "Exportaciones programadas de OCS Inventory, en piloto automático.",
      tagline: "Una aplicación de escritorio para Windows que inicia sesión en OCS Inventory NG, exporta un CSV completo de forma periódica, limpia los archivos antiguos por sí sola y vuelve a arrancar tras un reinicio, sin que nadie tenga que estar pendiente.",
      ctaGithub: "Ver código en GitHub",
      ctaDownload: "Descargar la última versión"
    },
    features: {
      title: "Qué hace",
      sub: "Todo lo que hacía el script original de PowerShell, además de un panel de control que lo gestiona por ti.",
      item1: { title: "Interfaz en secciones redimensionables", desc: "Conexión, intervalo del bucle y ajustes de salida en tres secciones apiladas que puedes redimensionar arrastrando los separadores." },
      item2: { title: "Bucle de extracción programado", desc: "Define un intervalo en minutos u horas; pulsa el botón verde Avvia y seguirá exportando hasta que pulses Stop." },
      item3: { title: "Limpieza automática", desc: "Conserva solo los últimos N archivos CSV y/o elimina los más antiguos de un periodo definido — ambas reglas pueden combinarse." },
      item4: { title: "Credenciales cifradas", desc: "La contraseña de OCS se cifra en reposo con Windows DPAPI — nunca se guarda en texto plano." },
      item5: { title: "Sigue el tema del sistema", desc: "El modo claro y oscuro se detectan automáticamente, con una opción manual que se recuerda para la próxima vez." },
      item6: { title: "Sobrevive a un reinicio", desc: "Un indicador --autostart y un lanzador de ejemplo hacen que el bucle de exportación se reanude solo tras reiniciar el servidor." }
    },
    screenshots: {
      title: "Capturas de pantalla",
      sub: "Añade aquí tus propias capturas de la aplicación en funcionamiento.",
      placeholder1: "Aquí va la captura de la ventana principal",
      placeholder2: "Aquí va la captura del panel de ajustes"
    },
    howItWorks: {
      title: "Cómo funciona",
      sub: "El mismo flujo de automatización que el script original ocs_export.ps1, ahora orquestado por la aplicación.",
      step1: { title: "Inicio de sesión", desc: "Accede a OCS Inventory NG con las credenciales configuradas." },
      step2: { title: "Abre la búsqueda avanzada", desc: "Navega a la página de búsqueda avanzada de la tabla de inventario." },
      step3: { title: "Activa todas las columnas", desc: "Marca todas las columnas disponibles para que la exportación sea siempre completa." },
      step4: { title: "Exporta el CSV", desc: "Inicia la exportación y guarda el archivo con un nombre basado en la fecha y hora." },
      step5: { title: "Limpia archivos antiguos", desc: "Aplica las reglas de limpieza a la carpeta de salida, si están activadas." },
      step6: { title: "Espera y repite", desc: "Espera el intervalo configurado y luego inicia el siguiente ciclo." }
    },
    requirements: {
      title: "Requisitos",
      item1: "Windows 10 u 11",
      item2: "Python 3.10+ (si se ejecuta desde el código fuente)",
      item3: "Acceso de red a tu instancia de OCS Inventory",
      item4: "Una cuenta de usuario válida de OCS Inventory"
    },
    footer: {
      madeWith: "Creado por Francesco Rombaldoni.",
      viewSource: "Ver código en GitHub",
      license: "Publicado bajo licencia MIT."
    },
    theme: { toggle: "Cambiar tema claro/oscuro" },
    lang: { select: "Elegir idioma" }
  },

  nl: {
    meta: { title: "OCS Inventory CSV Exporter GUI", description: "Een Windows-desktopapplicatie die geplande CSV-exports vanuit OCS Inventory NG automatiseert." },
    nav: { features: "Functies", howItWorks: "Hoe het werkt", requirements: "Vereisten", download: "Download" },
    hero: {
      title: "Geplande OCS Inventory-exports, op de automatische piloot.",
      tagline: "Een Windows-desktopapplicatie die inlogt op OCS Inventory NG, op vaste tijden een volledige CSV exporteert, zelf oude bestanden opruimt en na een herstart zelfstandig weer opstart — zonder dat iemand hoeft toe te kijken.",
      ctaGithub: "Bekijk broncode op GitHub",
      ctaDownload: "Download de laatste versie"
    },
    features: {
      title: "Wat het doet",
      sub: "Alles wat het originele PowerShell-script deed, plus een bedieningspaneel dat het voor je regelt.",
      item1: { title: "Gelaagde, verschaalbare interface", desc: "Verbinding, interval en uitvoerinstellingen in drie secties die je kunt vergroten of verkleinen door de scheidingslijnen te verslepen." },
      item2: { title: "Geplande exportlus", desc: "Stel een interval in minuten of uren in; druk op de groene Avvia-knop en de export blijft doorlopen tot je op Stop drukt." },
      item3: { title: "Automatische opschoning", desc: "Bewaar alleen de laatste N CSV-bestanden en/of verwijder bestanden ouder dan een ingestelde periode — beide regels kunnen samen actief zijn." },
      item4: { title: "Versleutelde inloggegevens", desc: "Het OCS-wachtwoord wordt versleuteld opgeslagen met Windows DPAPI — nooit in platte tekst." },
      item5: { title: "Volgt je systeemthema", desc: "Licht en donker thema worden automatisch herkend, met een handmatige overschrijving die wordt onthouden." },
      item6: { title: "Overleeft een herstart", desc: "Een --autostart-vlag en een voorbeeldlauncher laten de exportlus na een serverherstart vanzelf weer starten." }
    },
    screenshots: {
      title: "Schermafbeeldingen",
      sub: "Voeg hier je eigen schermafbeeldingen van de draaiende app toe.",
      placeholder1: "Schermafbeelding van het hoofdvenster hier toevoegen",
      placeholder2: "Schermafbeelding van het instellingenpaneel hier toevoegen"
    },
    howItWorks: {
      title: "Hoe het werkt",
      sub: "Dezelfde automatiseringsstroom als het originele script ocs_export.ps1, nu georkestreerd door de app.",
      step1: { title: "Inloggen", desc: "Logt in op OCS Inventory NG met de geconfigureerde inloggegevens." },
      step2: { title: "Opent uitgebreid zoeken", desc: "Navigeert naar de uitgebreide zoekpagina van de inventaristabel." },
      step3: { title: "Schakelt alle kolommen in", desc: "Vinkt elke beschikbare kolom aan zodat de export altijd volledig is." },
      step4: { title: "Exporteert de CSV", desc: "Start de export en slaat het bestand op met een naam op basis van datum en tijd." },
      step5: { title: "Ruimt oude bestanden op", desc: "Past de opschoonregels toe op de uitvoermap, indien ingeschakeld." },
      step6: { title: "Wacht en herhaalt", desc: "Wacht het ingestelde interval af en start dan de volgende cyclus." }
    },
    requirements: {
      title: "Vereisten",
      item1: "Windows 10 of 11",
      item2: "Python 3.10+ (bij uitvoeren vanuit de broncode)",
      item3: "Netwerktoegang tot je OCS Inventory-omgeving",
      item4: "Een geldig OCS Inventory-gebruikersaccount"
    },
    footer: {
      madeWith: "Gemaakt door Francesco Rombaldoni.",
      viewSource: "Bekijk broncode op GitHub",
      license: "Uitgebracht onder de MIT-licentie."
    },
    theme: { toggle: "Wissel licht/donker thema" },
    lang: { select: "Kies taal" }
  }
};

const SUPPORTED_LANGS = ["it", "en", "de", "fr", "es", "nl"];
const DEFAULT_LANG = "en";
