# Vertiefung vom 15. November 2026

## Ergebnis

Ein passendes öffentliches H13-R13-Komplettimage wurde auch in dieser Runde **nicht** gefunden. Der relevante neue Fortschritt ist ein konkreter SD-Ausführungspfad in der bereits vorhandenen H70-R33-Referenz, der keinen USB-Device-Modus und kein Updateimage voraussetzt. Dazu liegt ein kleines, lokal vorbereitetes Auslesepaket vor. Seine Übertragbarkeit auf das H13 vom Oktober 2023 ist offen.

**Direkt zum Versuch: [sd-readout/README.md](sd-readout/README.md).** Noch kein Erfolg auf dem H13; keine Flash-Schreiboperation ausgeführt. Ziel ist zunächst die originale H13-Anwendung plus Speicherplan, nicht ein sofortiger Logo-Wechsel.

## Neue Zielgeräte-Evidenz

Der Nutzer berichtete am 15.11.2026: Beim Anschluss per USB-C an den Windows-Rechner erschien im Geräte-Manager kein neues Gerät. Das ist ein Beobachtungsbefund, kein Nachweis eines stromseitig defekten Ports, einer falschen Platine oder eines ausschließlich zur Versorgung verdrahteten Anschlusses. Der bereits analysierte normale Referenzbetrieb schaltet OTG auf Host; ein USB-Device-Modus wäre ein anderer Zustand.

Auf GitHub wurden ausschließlich `main` und der ursprüngliche Übergabecommit `592a44895a02029aebcd0c5a5c7baeed0f445bf9` vorgefunden. Neue lokale Codex-Diagnosen waren dort nicht abgelegt. HTTP `cmd=2002` bleibt unbeantwortet; USB-VID/PID, Root, ADB, H13-Firmwaredump und Ziel-App liegen weiterhin nicht vor.

## Neuer SD-Pfad: echte Instruktionen statt nur Dateinamen

Alle folgenden Adressen gehören ausschließlich zur Referenz-App mit SHA-256 `9a719fc17bc404c3f640c9aa117fbb973bf0edb4adc4c8d899500c1ebc874c79`.

1. `main` ruft bei `0x897c4` die Funktion `pcba_test()` auf.
2. `pcba_test` (`0x225530`) prüft tatsächlich den **Ordner** `/mnt/sdcard/rk_pcba_test_res` mit `access`. Der anschließende Fehlertext behauptet stattdessen `pcba_test_flag_file`; hier ist der Code maßgeblich. Eine solche zusätzliche Datei ist für den Referenz-Einstieg nicht erforderlich.
3. Die Datei `rk_pcba_test_res/pcba_factory_flag_file` führt bei `0x225808` zu `CreateBigWindow()` (`0x222a4c`).
4. Dort wählt die Datei `rk_pcba_test_res/pcba_ddr_special_flag_file` ab `0x222e04` einen Sonderzweig. Der überspringt den breiten Fertigungstest und startet bei vorhandener Datei `memtester_smd` über `pthread_create` den Thread `ddr_Thread` (`0x220448`).
5. Der Thread verwendet `system` für `mount -o remount,rw /`, anschließend `chmod 777 /mnt/sdcard/rk_pcba_test_res/memtester_smd` und schließlich `/mnt/sdcard/rk_pcba_test_res/memtester_smd 128m 1`.
6. Der Thread prüft danach SD-Ergebnisdateien des erwarteten RAM-Tests; deren Fehlen verhindert die vorherige Ausführung nicht. Ein Testfehler im Bildschirm ist kein Beleg, dass das Skript nicht gelaufen ist.

Ein Shellskript mit `#!/bin/sh` kann die Stelle des erwarteten Programms einnehmen, sofern der Zielbuild diese Aufrufkette besitzt, die Karte frühzeitig gemountet wird und ihre Mountoptionen Ausführung erlauben. Der genaue frühe Kartenerkennungszeitpunkt, der vollständige H13-Boot und dessen Rechte wurden nicht emuliert.

### Zusätzliche Prüfung in Unicorn

`emulate_sd_path.py` lädt die echten ELF-Segmente in einen ARM-Emulator und führt drei isolierte Referenzfunktionen aus. Dateiexistenz, LVGL, Bibliotheksaufrufe und Threadstart werden gezielt nachgebildet; **es wird kein Host-Shellbefehl ausgeführt**. Unbekannte Aufrufe brechen die Emulation ab. Die Appdatei muss den oben genannten Hash besitzen.

Vier Fälle wurden geprüft:

- Ohne Testordner kehrt `pcba_test` zurück.
- Mit den Paketdateien wählt `pcba_test` `CreateBigWindow`.
- Mit dem DDR-Sonderflag meldet `CreateBigWindow` genau DDR- und Touch-Thread; keine Aktivierungs-/Bluetooth-/WLAN-Testthreads dieses Fensters.
- Der echte Code von `ddr_Thread` erreicht genau die drei oben genannten Systemaufrufe.

Die Einzelfunktionen werden separat gestartet, nicht als vollständiges Betriebssystem. Die Größenabfrage und echte Hardware-/GUI-Funktionen sind Stubs. Das beweist die referenzseitige Kontrollflusskette unter den dokumentierten Annahmen; weder einen echten H70-Boot noch einen H13-Test. Rohbefund: `sd-path-emulation.json`.

```bash
python -m pip install unicorn==2.1.4 pyelftools==0.33
python research-2026-11-15/emulate_sd_path.py
```

### Auslesepaket und Nebenwirkungen

`sd-readout/H13-SD-Readout-Versuch.zip` enthält nur drei Dateien. Das beigefügte Shellskript kopiert eine lesbare `/usr/bin/cvr_app` und `/oem/etc/version` auf SD und liest Rechte, Kernel, `/proc/mtd`, Partitionen, Mounts und MTD-Metadaten. Es liest keine rohen Flashpartitionen, ändert keine WLAN-Einstellung und startet keinen Netzwerkserver. Ein vorhandener Ergebnisordner wird nicht überschrieben. Tests auf dem Host mit künstlicher Appdatei: `sd-script-test.json`.

**Nicht als insgesamt rein lesend oder risikofrei bezeichnen:** Schon der Referenz-Aufrufer schaltet `/` auf schreibbar. Der Fertigungsmodus verändert die laufende Oberfläche und initialisiert weitere Diagnosefunktionen. Bei Auswahl des beabsichtigten Sonderzweigs wurden keine Firmware-Flash-/Formatierungsbefehle gefunden; Verhalten eines unbekannten älteren H13-Builds bleibt offen. Eine separate leere Karte ohne IMG-, Logo- oder zusätzliche Flags ist wesentlich.

Das Skript ist keine komplette Datensicherung. Auch `COMPLETE.txt` garantiert nicht, dass die App-Kopie gelang; Fehlerdateien, Dateigröße und Hash prüfen. Erst die tatsächlichen Zielartefakte können weitere Schritte absichern.

## HTTP-Pfade weiter geprüft

`http-file-handlers.txt` enthält jetzt den Download- und Uploadhandler der Referenz.

- Der Downloadhandler lässt in der untersuchten Verzweigung nur `.db`, `.jpg`, `.mp4` und `.ts` zu und baut Dateipfade um. Eine bloße Zeichenkettensuche nach `/mnt/sdcard` ist deshalb **kein nachgewiesener allgemeiner Dateileser** für `/usr/bin/cvr_app`. Ein funktionierender Traversalpfad wurde nicht gefunden oder am Gerät getestet.
- Der registrierte Pfad `/mnt/extsd/version` ist in der Referenz an den **Uploadhandler** gebunden; nicht als bestätigten Versions-Download empfehlen.
- Der Uploadhandler löscht beim Eintritt `/mnt/sdcard/*.img`, verarbeitet Multipart-Daten, sucht `RKFWf` und baut am Ende einen unquotierten Shellbefehl zum Umbenennen aus dem Dateinamen. Das ist ein weiterer statischer Command-Injection-Kandidat. Kein H13-Test und kein fertiger Netzwerkpayload: Für eine schon bestätigte SD-Ausführung gibt es keinen Grund, zuerst diesen riskanteren Uploadpfad zu erproben.
- Der frühere WLAN-/Bluetooth-Setter-Kandidat bleibt offen und kann Konfiguration plus Neustart auslösen.

Die Referenz enthält zwar `/mnt/sdcard/thermal.sh` als Variable in `thermal_test.sh`; **das Skript führt sie nicht aus**. Daraus folgt kein Thermal-Autorun-Trick.

## Erneute Firmware- und Quellenrecherche

Es wurden die vollständige Versionskennung, Teilkennungen, R13-Dateinamen aus dem Werkzeuglog, Marken-/Modellvarianten, englischsprachige Begriffe sowie koreanische, russische, japanische und chinesische Suchbegriffe geprüft. GitHub-Suche nach Codebezeichnern ergänzte die Websuche. Ein zurückgegebenes ähnlich benanntes Gerät ist keine kompatible Firmware.

Die öffentliche [Imagebon-Freigabe](https://drive.google.com/drive/folders/1AYti2WEuObgKGuRzH-U1W1F-JGd6YXVm) wurde erneut heruntergeladen. Ihre oberste Ebene enthält dieselben drei Ordner: `H70 Pro-firmware`, `H70K`, `H70Pro`. Es erschien dort kein H13-/R13-Ordner. HTML-Snapshot: `imagebon-drive-current.html`.

Neue hilfreiche Primärquelle: Der öffentliche [Lindenis-V536-HTTP-Quellcode](https://github.com/lindenis-org/lindenis-v536-softwinner/blob/d5d2c4631c829c403a8a7e7047688b555b2b2a32/eyesee-mpp/awcdr/apps/cdr/source/device_model/httpServer/httpServer.cpp) besitzt dieselben Klassennamen und API-Routen. Das erklärt Teile der API-Herkunft, identifiziert aber weder den H13-Chip noch dessen exakten Quellcode. Der untersuchte Imagebon-Code ist eine abweichende Rockchip-Referenz; Portierungen dieser HTTP-Familie existieren auf unterschiedlichen SoCs.

Weitere öffentlich dokumentierte RE-Projekte und Quellen: [QUELLEN.md](QUELLEN.md). Insbesondere Allwinner-F133-/TF790-Anleitungen, Imagebon-W60N-UNISOC-PAC-Dateien und die gleichnamige Roadcam-X3-Kamera wurden nicht als H13-Firmware behandelt.

## Methodischer Fehler gefunden und behoben

Das alte `disassemble_reference.py` bricht einen Funktionsdump beim ersten nicht decodierbaren Datenwort ab. ARM-Funktionen enthalten Literalpools mitten im Adressbereich. Dadurch fehlte in manchen alten Ausgaben späterer Code, zum Beispiel ein großer Teil von `CreateBigWindow`.

`disassemble_complete.py` setzt Capstones `skipdata` und markiert nicht decodierbare Bytes. Damit wird bis zum Ende des ELF-Symbolbereichs ausgegeben. **Auch jetzt sind als Instruktionen dargestellte Literalpools kein ausführbarer Kontrollfluss.** PLT-Struktur und ARM-Modus bleiben referenzspezifische Annahmen. Die relevanten SD-Zweige wurden zusätzlich im Emulator kontrolliert. Die alten Dumps bleiben als historische Artefakte erhalten.

## Nächster Versuch am H13

Den einmaligen SD-Ausleseversuch nach `sd-readout/README.md` durchführen. Wenn er greift, stehen sofort die echte H13-App, Rechte und Speicherzuordnung zur Verfügung. Damit zuerst den personalisierten Logo-Import am **Zielcode** prüfen und anschließend die passende Original-Logo-Partition sichern.

Wenn er nicht greift, keine weiteren beliebigen Fertigungs-/Aktivierungsflags ergänzen. Dann als Nächstes die offene HTTP-Leseabfrage `cmd=2002` und eine begrenzte lokale Portprüfung dokumentieren; danach den zum Zielbuild passenden Netzwerkpfad oder einen konkret identifizierten UART-/Loaderzugang untersuchen. Der Cloud-Rechner ist nicht mit dem Display verbunden und kann diese Zielgeräteprüfungen nicht vorwegnehmen.
