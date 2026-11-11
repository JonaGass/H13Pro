# H13 Pro – Übergabe an eine lokale Codex-Instanz

Stand: 11. November 2026. Dieses Verzeichnis enthält den gesamten verfügbaren Forschungsstand einschließlich heruntergeladener Referenzfirmware, extrahierter Dateien und Disassemblierungen. Es ist kein fertiges Flashpaket.

## Direkt weiterarbeiten

Öffne dieses entpackte Verzeichnis als Arbeitsverzeichnis in der lokalen Codex-Instanz. Übergib folgenden Auftrag:

> Lies zuerst AGENTS.md und HANDOFF.md, danach Ohne-Verkaeufer.md. Setze die Untersuchung meines Imagebon H13 Pro fort. Ziel ist ein eigenes Bootlogo ohne Hilfe des Verkäufers. Die HTTP-API auf 192.168.10.1:8082 wurde auf dem echten H13 bereits erfolgreich angesprochen. Prüfe zunächst die lokale Verbindung und den aktuellen Gerätestand mit Leseoperationen. Die Antwort auf cmd=2002 steht noch aus. Nutze die vorhandene Referenzanalyse, lies nach Möglichkeit die tatsächliche H13-App/Firmware aus und prüfe den Logo-Import am Zielbuild. Die mitgelieferte R33-Firmware gehört zum H70 und darf nicht auf mein H13 geflasht werden. Das Gehäuse soll geschlossen bleiben, solange ein Zugang ohne Öffnen möglich ist.

**Zum Einstieg sind keine Python-Pakete nötig**, außer Python selbst für `h13_probe.py` und `inspect_firmware.py`. Die Analyseabhängigkeiten sind erst für erneutes Disassemblieren oder UBI-Entpacken erforderlich.

## Zuerst lesen

1. [HANDOFF.md](HANDOFF.md): aktueller Stand, Nutzerwünsche, bestätigte Befunde und nächste Schritte.
2. [Ohne-Verkaeufer.md](Ohne-Verkaeufer.md): vertiefte USB-/HTTP-/Logo-Analyse.
3. [Recherche-H13-Pro.md](Recherche-H13-Pro.md): erste Recherche und Format-/Firmwarebefunde. Die Verkäuferanfrage darin ist überholt.
4. [SOURCES.md](SOURCES.md): Herkunft der Downloads und Primärquellen.

## Arbeitsdateien

| Pfad | Inhalt |
|---|---|
| `device-evidence/` | Vom Nutzer am echten H13 beobachtete API-Antwort und Stand offener Abfragen. |
| `h13_probe.py` | Lokal ausführbare Diagnose: HTTP-GET, USB-Auflistung unter Windows, vorhandenes ADB; optional `cvr_app` auslesen. |
| `inspect_firmware.py` | RKFW-/RKAF-Paket oder BMP rein lesend untersuchen. |
| `disassemble_reference.py` | ARM-Code mit Literal-/Symbolkommentaren disassemblieren. |
| `sources/` | Originaldownloads, einschließlich H70-R33-Referenzfirmware und SD-Werkzeug. |
| `reference-extracted/` | Firmwarekomponenten und entpackte Recovery-Ramdisk. |
| `reference-rootfs/1305731643/rootfs/` | Extrahiertes normales H70-R33-Dateisystem; enthält `usr/bin/cvr_app`. |
| `reference-oem/350262819/oem/` | OEM-Startskripte und Konfiguration. |
| `reference-userdata/1611133048/userdata/` | Extrahierte Referenz-Userdata. |
| `*-disassembly.txt`, `logo-import-details.txt`, `cvr-app-strings.txt` | Bisherige Codeanalyse; direkt lesbar ohne Zusatzsoftware. |
| `SHA256SUMS.txt` | Integrität aller enthaltenen regulären Dateien. |
| `verify_bundle.py` | Prüfsummen lokal mit Python prüfen; benötigt keine Zusatzpakete. |
| `FIRMWARE_SYMLINKS.json` | Ursprüngliche Symlinks als Metadaten für portables Entpacken unter Windows. |

## Windows: Diagnose

Optional nach dem Entpacken die Vollständigkeit prüfen:

```powershell
py .\verify_bundle.py
```

Die Prüfliste erfasst die Originaldateien dieser Übergabe, ausgenommen die Prüfliste selbst. Neue lokale Arbeitsdateien werden nicht beanstandet; nachträglich veränderte Originaldateien werden gemeldet.

Wenn der PC mit dem WLAN des Displays verbunden ist:

```powershell
py .\h13_probe.py --host 192.168.10.1
```

Wenn außerdem die offiziellen Android Platform-Tools vorliegen und das Display per USB verbunden ist:

```powershell
py .\h13_probe.py --host 192.168.10.1 --adb .\platform-tools\adb.exe --pull-app
```

Der Ordner `h13-diagnose-...` enthält das Ergebnis. Kein aktiver ADB-Zugang wurde bisher nachgewiesen. Fehlende USB-Erkennung ist deshalb zunächst ein Diagnosebefund.

## Optionale Analyseumgebung

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-analysis.txt
.\.venv\Scripts\python.exe .\disassemble_reference.py .\reference-rootfs\1305731643\rootfs\usr\bin\cvr_app _Z11Start_initdv
```

Unter Linux entsprechen die Interpreterpfade `.venv/bin/python`. Die Cloud-venv wird absichtlich nicht mitgeliefert, da sie betriebssystemspezifisch ist. `requirements-cloud-lock.txt` dokumentiert die tatsächlich verwendeten Versionen.

## Portabilität und Grenzen

Die Firmware-Dateien sind Untersuchungsmaterial, nicht ausführbare Desktop-Programme. Symlinks und Geräteknoten aus dem Linux-Firmwaredateisystem werden im ZIP nicht als aktive Verknüpfungen/Geräte angelegt. Alle regulären extrahierten Dateien sowie die originalen UBI-Abbilder liegen bei; bei Bedarf unter Linux erneut mit ubi-reader entpacken.

Einige historische Berichte/JSON-Dateien enthalten `/workspace/h13-research/...` als Herkunftspfad. Das bezeichnet den Cloud-Arbeitsort. Für lokale Befehle den tatsächlichen Pfad dieses entpackten Verzeichnisses verwenden.

Dies ist eine inhaltliche Arbeitsübergabe, kein vollständiger ChatGPT-Chat-Export. Nutzerauftrag, Entscheidungen, Gerätebeobachtungen und Untersuchungsergebnisse sind in HANDOFF.md zusammengeführt. Zugangsdaten oder eine Verbindung zum Rechner des Nutzers werden nicht mitübertragen.
