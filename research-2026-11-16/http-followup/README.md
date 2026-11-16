# Auswertung der echten Netzwerkdiagnose und gezielter HTTP-Leseversuch

## Am H13 jetzt bestätigt

Die vom Nutzer hochgeladene Diagnose vom 16.11.2026 zeigt an `192.168.10.1`:

- HTTP GET 2001 und 2002 jeweils Status 200, bereits bekannte R8-/RV1126-Antworten.
- TCP 8082 und 9999 offen.
- TCP 22, 23, 80, 443, 554, 5555, 8080 und 8081: Timeout bei 0,8 Sekunden Verbindungsfrist. Das ist kein sicherer Nachweis eines geschlossenen Ports.
- Kein nachgewiesener SSH-, Telnet-, ADB-, Shell- oder Firmwarezugriff.

Der rohe Nutzerbericht wird nicht im öffentlichen Repository abgelegt. Die zusammengefassten Befunde sind in `device-evidence/network-summary-2026-11-16.json` festgehalten.

## Port 9999

Die Referenzfunktion `httpServer::CreateSocket` bindet TCP an Port 9999. Ihr Empfangspfad liest `cmd_id` aus JSON. `handSocketmassge` erkennt 4016 als Heartbeat; andere Werte können den App-/RTSP-Zustand beenden. Das passt zum erreichbaren Dienst, identifiziert aber den H13-Code nicht binär. Port 9999 ist kein belegter Telnet-/Shellzugang. Keine erfundenen Befehle dorthin senden.

Nachweis: `get-and-control.txt`, Referenz-App SHA-256 `9a719fc17bc404c3f640c9aa117fbb973bf0edb4adc4c8d899500c1ebc874c79`.

## Neuer Versionspfad und Grenze am Ziel

In der Referenz existiert ein GET-Dispatcherzweig für **8567** (`0x2177`), der `GetSystemVersion()` aufruft. Der Getter öffnet `/oem/etc/version` lesend. Der Zweig konstruiert eine neunteilige, durch Semikolon getrennte Kennung nach dem Format `SW;RV1126;QC01;...`, mit der App-Firmwaredienste Modelle unterscheiden können. Es wurden keine Setter-/Flash-/Reboot-Aufrufe in diesem Zweig gefunden.

Der Nutzer öffnete den konkreten GET am H13 und sah eine **leere weiße Seite**. HTTP-Status, Header und tatsächliche Antwortbytes sind davon noch nicht bekannt. Die Referenz bricht die Konstruktion unter anderem ab, wenn sie kein großes `V` in der Versionsdatei findet. Die bisher gemeldete R13-Menüversion enthält dort kein `V`. Das ist eine mögliche Erklärung, kein Beweis für denselben Ablauf auf dem H13. Eine fehlende Unterstützung des Kommandos ist ebenfalls möglich.

Der öffentlich dokumentierte Update-Dienst `http://app.sunninglink.com:9412/iotcam-api-server/firmwareUpgrade/checkUpdate` antwortete bei einer leeren Kennung mit HTTP 200 und `ret:0, data:null`. Drei weitere begrenzte Abfragen mit **abgeleiteten** Referenz-/R13-Kandidaten und ausschließlich Null-MACs lieferten ebenfalls `data:null` (`ota-candidates.json`). Keine echte H13-Updatekennung wurde ermittelt, kein passender Download gefunden. Diese Ergebnisse widerlegen nicht die Existenz einer Firmware oder eines nur mit echten Geräteparametern passenden Eintrags.

Die Feldbedeutungen sind zusätzlich in einem veröffentlichten App-Smali-Artefakt sichtbar: https://github.com/fuho/moto-display-re/blob/main/research/sibling_apks/com.moto.amotocam/artifacts/FirmwareInfo.smali . Der aktive Cloud-Endpunkt wird im dortigen RE-Bericht dokumentiert: https://github.com/fuho/moto-display-re/blob/main/research/sibling_apks/com.moto.amotocam/findings.md . Kein fremdes Firmwarepaket wurde als kompatibel bewertet oder geflasht.

## Nächster Versuch: feste HTTP-Dateipfade lesen

`h13_http_readout.py` prüft zuerst den bestätigten 2001-GET und nur bei erwarteter `R8-V2.0`-Antwort sieben feste Pfade auf Port 8082:

| Pfad | Zweck |
|---|---|
| `/` | Webwurzel bzw. Verzeichnisanzeige erkennen |
| `/api/getdeviceinfo?cmd=8567` | Status/Antwortbytes des weißen Bildschirms erfassen |
| `/mountall.log` | Mögliches Startprotokoll unter der Referenz-Webwurzel `/tmp` |
| `/proc/mtd` | Nur falls der echte Server einen weitergehenden Dateizugriff erlaubt |
| `/oem/etc/version` | Falls direkt zugänglich: tatsächliche Versionsdatei |
| `/usr/bin/cvr_app` | Falls direkt zugänglich: originale Zielanwendung |
| `/cvr_app` | Falls in der Webwurzel bereitgestellt: Anwendungsdatei |

Die Referenz-Webwurzel ist `/tmp`; die absoluten Systempfade müssen daher dort nicht funktionieren. Der ältere H13-Server kann anders konfiguriert sein. **Keiner dieser Dateizugänge ist am H13 bereits bestätigt.** Es werden keine Traversalvarianten ausprobiert, keine Verzeichnisse rekursiv durchsucht und keine Links automatisch verfolgt. Ein HTTP-Downloadhandler kann intern Protokolle oder Cachezustände aktualisieren; der Client sendet ausschließlich GETs und keine Einstellungs-/Updatebefehle.

Eine vollständig empfangene HTTP-200-Datei wird nur an den beiden Anwendungswegen als lokaler Kandidat gespeichert, wenn sie einen 32-Bit-Little-Endian-ARM-ELF-Kopf hat. Die Größe ist auf 8 MiB begrenzt. Das ist eine Formatprüfung, kein Echtheits- oder Kompatibilitätsnachweis. Es wird nichts ausgeführt. Alle übrigen Antworten werden als begrenzter Text im JSON erfasst.

## Durchführung auf dem PC

1. `H13-HTTP-Leseversuch.zip` mit bestehender Internetverbindung herunterladen und entpacken. Es enthält `h13_http_readout.py` und das benötigte `h13_network_probe.py`; kein SD-Paket.
2. Display ohne Testkarte normal starten, PC mit dem Display-WLAN verbinden.
3. Im entpackten Ordner ausführen:

```powershell
py .\h13_http_readout.py
```

4. Den entstandenen Ordner `h13-http-readout-...` lokal sichern. Zunächst `http-report.json` im Chat bereitstellen; wenn zusätzlich eine `cvr_app.*.original` entstand, diese ebenfalls zur Offline-Analyse bereitstellen. Bei Datenanhängen Gerätekennungen beachten. Nicht automatisch ins öffentliche Repository hochladen.

Die Cloud hat keinen direkten Netzwerkpfad zum H13. Dieser lokale Versuch wurde nur mit einem Testserver geprüft. Wenn alle Dateipfade scheitern, ist kein allgemeiner HTTP-Dateileser belegt. Vor einem schreibenden API-Versuch müssen dann dessen Parser, Nebenwirkungen und Wiederherstellung separat konkretisiert werden; der offene Port allein ersetzt das nicht.
