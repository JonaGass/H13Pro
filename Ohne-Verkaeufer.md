# H13 Pro: Zugriff ohne Verkäufer

Fortsetzung der Untersuchung vom 11.11.2026. Zielversion:
`R13.10.01.22_1.1.1026.0_2.77.3f_20231013.1841..`

## Am echten H13 bestätigt

Der Nutzer hat das Handy mit dem WLAN des Displays verbunden und aufgerufen:

`http://192.168.10.1:8082/api/getdeviceinfo?cmd=2001`

Die Antwort enthält:

```json
{
  "Version": "v1.0",
  "product": "R8-V2.0",
  "sp": "qckj"
}
```

Die ebenfalls zurückgegebene MAC-Adresse wird hier nicht wiederholt. Damit sind IP, HTTP-Port, Endpunkt und dieses Lese-Kommando **am Zielgerät bestätigt**. Diese API-Antwort ist ein Protokoll-/Produktkennzeichen, keine vollständige Firmwarekennung. Sie ersetzt nicht die längere R13-Versionsnummer aus dem Einstellungsmenü.

Die Antwort stimmt in ihren charakteristischen Feldern mit der untersuchten H70-R33-Referenz überein. Das ist starke Evidenz für gemeinsame Softwareherkunft (QCKJ/QICHENG), aber keine Binäridentität und keine Freigabe für R33-Firmware auf R13-Hardware.

Nächste reine Leseabfrage:

`http://192.168.10.1:8082/api/getdeviceinfo?cmd=2002`

Im Referenzprogramm führt Kommando 2002 in den Geräteinformationszweig. Die Rückmeldung des H13 dazu war beim Erstellen dieses Dokuments noch ausstehend.

## Neu untersuchtes Material

Die bereits heruntergeladene H70-R33-Firmware wurde weiter zerlegt. Die UBI-Abbilder `rootfs`, `oem` und `userdata` wurden mit ubi-reader extrahiert; Geräteknoten konnten im lokalen Sandbox-Dateisystem nicht angelegt werden. Reguläre Dateien, Startskripte und das Programm `cvr_app` waren zugänglich. Kein ARM-Programm wurde ausgeführt.

`cvr_app` der Referenz:

```text
Größe: 2.596.408 Bytes
SHA-256:
9a719fc17bc404c3f640c9aa117fbb973bf0edb4adc4c8d899500c1ebc874c79
```

ARM-Code wurde mit Capstone disassembliert, ELF-Informationen mit pyelftools gelesen. Die Programme enthalten exportierte Funktionsnamen, wodurch sich Aufrufketten erheblich zuverlässiger bestimmen lassen als mit einer reinen Zeichenkettensuche.

## Konkrete Erkenntnisse

### HTTP-Schnittstelle

Im Referenzprogramm richtet `WebServer` den Port **8082** und das Dokumentverzeichnis **`/tmp`** ein. `httpServer::init` registriert unter anderem:

- `GET /api/getdeviceinfo`
- `POST /api/setdeviceinfo`
- Dateidownloadhandler unter `/mnt/sdcard/` und `/tmp/sqlite/`

Der GET-Handler interpretiert den Zahlenwert nach dem letzten Gleichheitszeichen der Query. Der Dispatcher ordnet **2001** dem Versions-/Produktinformationszweig und **2002** dem Geräteinformationszweig zu. Darauf beruhen die obigen Leseabfragen. Andere Kommandonummern wurden am H13 nicht getestet. Keine zufälligen Kommandonummern ausprobieren: Es gibt auch Setter für Formatieren und Zurücksetzen.

### USB/ADB

Die Referenz-Recovery enthält eine `.usb_config` mit `usb_adb_en`. Ihr Startskript legt einen USB-Gadget mit VID **2207**, PID **0006** und `adbd` an.

Das normale Referenzsystem ist komplizierter: `cvr_app::Start_initd` schaltet USB normalerweise ausdrücklich auf **Host**. Ein PC erkennt deshalb unter Umständen überhaupt kein Debug-Gerät. Ein Datenkabel allein garantiert keinen Zugriff.

Eine konkrete interne Diagnoseverzweigung ist vorhanden:

```text
debug_mode_enable() == 2
    -> udev und Netzwerk starten
    -> USB-Konfiguration auf ADB setzen
    -> S50usbdevice starten
```

In der Referenz erreicht die Existenz von `/oem/qckj_isptunner_file` diesen Rückgabewert. Dagegen ergibt `/mnt/sdcard/qckj_debug_all_file` nur den Wert **1**. **Diese SD-Datei aktiviert in der untersuchten Version nicht den ADB-Zweig.** Das ist durch die Verzweigungen belegt und sollte nicht zu einem vermeintlichen „ADB-Freischalttrick“ verkürzt werden.

Das OEM-Verzeichnis enthält außerdem `adb.sh`, und das Dateisystem enthält `start_usb.sh`. Sie beweisen vorhandene Mechanismen, aber noch keinen Weg, diese auf dem H13 von außen aufzurufen. Die ADB-Konfiguration wurde nicht auf dem Zielgerät geändert.

### Eingebauter Logo-Import ohne komplettes Firmwareimage

Ein wichtiger zusätzlicher Weg steckt bereits im Referenzprogramm:

```text
Personalisierter SD-Upgrade-Dialog
  -> sd_upgrade_start()
  -> ChangeEmmcLogo()
  -> ChangeSpinandLogo()
```

Die Logoquelle ist:

`/mnt/sdcard/userdata/logo.bin`

Für SPI-NAND ruft die Referenz `flashcp` auf die dortige Logo-Partition auf; für eMMC gibt es einen eigenen Kopierpfad. Ein vollständiges `update.img` ist in dieser Funktionskette nicht grundsätzlich Voraussetzung. Das spricht für einen Logo-Import über eine gewöhnliche SD-Karte, sofern die Zielversion dieselbe Funktion und einen erreichbaren Menüpunkt besitzt.

**Noch nicht am R13 bestätigt.** Insbesondere nicht allein aufgrund dieses Befunds die SD-Datei auf ein H13 loslassen. Die Funktion bearbeitet auch Personalisierungsdateien, und die aufrufenden Dialoge können weitere Einstellungen zurücksetzen oder neu starten. `/dev/mtd8` beziehungsweise `/dev/mmcblk0p8` sind im Referenzcode fest einprogrammiert. Ihre Zuordnung muss am H13 überprüft werden. Der Name `.bin` beschreibt hier nicht automatisch ein neues Dateiformat; der tatsächliche Inhalt ist am Ziel zu prüfen.

Im Referenz-Stringkatalog heißt der einschlägige Eintrag **„Personalized upgrade“ / „Personalisiertes Upgrade“**. Er ist vom normalen **„Firmware Upgrade“** getrennt.

### Ansatz für Shellzugriff über die lokale API

Die Referenz enthält einen weiteren untersuchenswerten Zugang: Die HTTP-Setter für WLAN-/Bluetooth-Namen und -Passwort gelangen zu Funktionen, die Eingaben mit `sprintf` in einen Shellbefehl einbauen. `qc_system` führt diesen über `popen` aus. In der untersuchten Aufrufkette ist keine verlässliche Shell-Escapierung erkennbar. Bei der Namensprüfung führt selbst der protokollierte ungültige-Zeichen-Fall anschließend zum Setter.

Das ist ein konkreter **Command-Injection-Kandidat** für den lokalen Gerätezugriff. Ein solcher Zugang könnte USB umschalten oder Dateien zum Auslesen bereitstellen, ohne ein fremdes Betriebssystem zu flashen. Er ist aber **nicht am H13 getestet**. Gleiche Lese-API bedeutet nicht zwangsläufig gleichen verwundbaren Setter.

Die reine Shell-Befehlskonstruktion wurde in einem lokalen temporären Verzeichnis nachgestellt. Eine harmlose Markerdatei konnte durch Command Substitution erzeugt werden, während die Test-Konfiguration ihren ursprünglichen Wert behielt. Das bestätigt ausschließlich das Verhalten dieser Shell-Grenze; weder den Netzwerkpfad noch Root-Rechte oder die Ausnutzbarkeit des H13. Das Ergebnis steht in `local-shell-boundary-proof.json`.

Die Setter ändern Geräte-Konfiguration und lösen in der Referenz anschließend einen Neustart aus. Deshalb ist ein experimenteller Probeaufruf kein read-only-Test. Vor einem Versuch sind Länge der Eingabe, Erhalt der Zugangsdaten, tatsächlicher Zielcode und ein Rückweg zu prüfen. Ein fertiger blind auszuführender Payload ist hier nicht beigefügt.

## Praktische Reihenfolge für dieses Gerät

1. **HTTP-Identifikation fertigstellen.** Der Nutzer kann dies jetzt mit dem Handy tun; 2001 ist bereits erfolgreich.
2. **Menübestand prüfen.** Existiert „Personalisiertes Upgrade“? Nur feststellen, nicht auslösen. Das kann der kürzeste Weg zum späteren Logo-Import sein.
3. **Windows-USB prüfen, wenn ein Rechner verfügbar ist.** Datenkabel verwenden, das Display allein vom PC versorgen, soweit die normale Leistungsversorgung ausreicht. Nicht versuchsweise zwei Stromquellen über ungeprüfte Adapter verbinden. Im Geräte-Manager die Hardware-IDs auslesen.
4. **Vorhandenes ADB nutzen, wenn es sich meldet.** Mit den offiziellen [Google Platform-Tools](https://developer.android.com/tools/releases/platform-tools) `adb devices -l`, anschließend `adb shell id`, `adb shell cat /proc/mtd` und `adb shell ls -l /dev/block/by-name`. Das sind Leseoperationen.
5. **Eigene Software auslesen.** Bei erreichbarem ADB kann `adb pull /usr/bin/cvr_app` die exakte H13-App sichern. Dann lassen sich Logo-Import und USB-/HTTP-Diagnosepfade an der echten R13-Binärdatei überprüfen. Ein Rootzugang ist für eine lesbare Appdatei möglicherweise nicht nötig; für rohe Flashpartitionen kann er erforderlich sein.
6. **Original-Logo und Speicherplan sichern**, bevor irgendein Schreibweg ausgewählt wird. Ein Firmwaredownload vom Verkäufer ist dafür nicht erforderlich. Bei MTD müssen ECC und Bad Blocks für einen wiederherstellbaren Dump berücksichtigt werden; ein beliebiger `dd`-Dump ist keine pauschale Komplettsicherung.
7. **Nur die bestätigte Logo-Partition ändern.** Der endgültige Schreibweg hängt von Speicherart und vorhandenen Werkzeuge ab. Keine feste H70-Partitionsnummer übernehmen.

Wenn USB keinen Zugang bietet, ist die bestätigte Netzwerkschnittstelle der nächste Untersuchungspunkt. Ein Öffnen des Gehäuses ist erst ein späterer Fallback für UART oder einen identifizierten Download-Taster. Es wurde kein verifiziertes H13-Pinout gefunden. Die [Firefly-Dokumentation für RV1109/RV1126](https://wiki.t-firefly.com/en/Core-1109-JD4/upgrade_firmware.html) erklärt Loader- und Maskrom-Zugänge auf Entwicklerboards, liefert aber keine H13-Tastenkombination oder H13-Platinenbelegung.

## Vorbereitetes Diagnosewerkzeug

`h13_probe.py` sammelt ausschließlich:

- USB-Geräteinformationen unter Windows;
- optional die beiden HTTP-GET-Antworten;
- vorhandene ADB-Verbindungen und lesende Systeminformationen;
- optional eine lokale Kopie von `cvr_app`.

Es installiert keine Treiber, aktiviert kein Debugging, sendet keine POST-Anfragen, startet das Gerät nicht neu und schreibt nicht auf Flash.

```powershell
py h13_probe.py --host 192.168.10.1 --adb .\platform-tools\adb.exe --pull-app
```

Es entsteht ein lokaler Diagnoseordner. Nur bei genau einem bereits verbundenen ADB-Gerät wird dessen Shell verwendet. Die Diagnose enthält Seriennummern/MAC-Adressen; vor dem Weitergeben ansehen. Das Skript wurde syntaktisch und über seinen CLI-Einstieg geprüft, nicht gegen das physische H13 ausgeführt.

## Fundstellen für die technische Nachprüfung

Alle Adressen beziehen sich ausschließlich auf die oben gehashte Referenz-App:

| Funktion | Adresse |
|---|---:|
| `debug_mode_enable` | `0x8b914` |
| `Start_initd` | `0x8bab4` |
| `qc_system` | `0x9f9c4` |
| `SetdevWifiBtName` | `0xa02ac` |
| `SetdevWifiBtPassword` | `0xa0420` |
| `ChangeEmmcLogo` | `0xa1254` |
| `ChangeSpinandLogo` | `0xa13c8` |
| `sd_upgrade_start` | `0xa1e34` |
| `GetDeviceInfoHandler::handleGet` | `0x218694` |
| `HandleSetIotCtrlCmd` | `0x218ee4` |
| `SetDeviceInfoHandler::handlePost` | `0x21950c` |
| `WebServer`-Konstruktor | `0x21a294` |

Ein passendes öffentliches R13-Komplettimage wurde auch in der erweiterten Recherche nicht identifiziert. Der Fortschritt besteht jetzt im **am H13 bestätigten HTTP-Zugang**, einem konkreten eingebauten Logo-Importpfad in der verwandten Software und einem untersuchbaren Weg zu eigenem Gerätezugriff. Für den nächsten Schritt ist keine weitere Verkäuferanfrage vorgesehen.
