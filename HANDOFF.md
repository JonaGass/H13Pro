# Aktueller Arbeitsstand

**HTTP 2002 beantwortet, 16.11.2026:** Das echte H13 antwortet mit `device_id: RV1126`, `device_name: R8`, `software: V1.0` und einer `info`-Liste. Vollständig unter `device-evidence/http-cmd-2002-2026-11-16.json`. Der frühere Status „2002 ausstehend“ in historischen Abschnitten ist damit überholt. API-Identität, kein physischer Chip-/Binärgleichheitsnachweis; R13-Menüversion bleibt maßgeblich. Keine in `info` genannten Cmd-Werte blind erproben. Als Nächstes gezielte Portdiagnose.

**Zweiter SD-Versuch ebenfalls ohne Ergebnis, 16.11.2026:** Laut Nutzer weiterhin keine neuen Dateien; v2-Marker und `H13-READOUT` fehlen. Damit kein belegter externer SD-Skriptstart. Keine weiteren Flag-/Namensvarianten versuchen; die Erstdiagnose wechselt zur bestätigten HTTP-Schnittstelle. Anleitung: `research-2026-11-16/NETZWERK.md`, neues einzelnes Standardbibliothek-Skript `h13_network_probe.py`. Die Antwort auf `cmd=2002` und Ziel-Portbefunde stehen noch aus. Kein Root-/Flash-/App-Ausleseerfolg.

**Ergebnis des ersten SD-Versuchs, 16.11.2026:** Kein `H13-READOUT`, nur leere Videoordner. Alle drei Testdateien blieben laut Nutzer unter den exakten Namen vorhanden. Skriptstart/Root/Flashdump sind damit weiterhin unbestätigt. Das v1-Skript konnte vor der ersten Ausgabe bei anderen Argumenten als `128m 1` aussteigen und nahm `/mnt/sdcard` fest an. Ein begrenzter v2-Versuch entfernt diese Annahmen und schreibt zuerst `rk_pcba_test_res/H13-PROBE-STARTED.txt`; siehe `research-2026-11-16/sd-probe-v2/README.md`. Noch kein v2-Test am H13. Bei erneut fehlendem Marker den externen SD-Programmpfad nicht als funktionierend behandeln und keine beliebigen weiteren Flags versuchen.

**Zielgerätebefund vom 16.11.2026:** Nutzerfoto bestätigt den SD-ausgelösten Fertigungstest am echten H13. Sichtbar ist der breite Test mit GPS `testing` (Modul fehlt), DDR-Anzeige `1024MB`, `norflash: 128MB`. Das ist noch kein Beleg, dass `memtester_smd` lief oder die tatsächliche Flashart feststeht. Der breite Test weicht vom emulierten H70-DDR-Sonderzweig ab. Als Nächstes nach Ausschalten die Karte auf `H13-READOUT` prüfen; keine zusätzlichen Testtasten/Flags versuchen. Details: `device-evidence/sd-factory-screen-2026-11-16.json`.

**Fortsetzung vom 15.11.2026:** Zuerst [research-2026-11-15/ERGEBNISSE.md](research-2026-11-15/ERGEBNISSE.md) lesen. USB-C zeigte laut Nutzer kein neues Windows-Gerät. Neuer, isoliert ARM-emulierter SD-Fertigungstestpfad und ein vorbereitetes App-Auslesepaket liegen in `research-2026-11-15/sd-readout/`. Noch kein H13-Test, keine Root-/Flash-Erfolgsmeldung. Der Referenz-Aufrufer remountet `/` schreibbar. Die nachfolgenden Abschnitte dokumentieren den ursprünglichen Stand vom 11.11.; offene H13-HTTP-Abfrage und fehlender Zieldump sind weiterhin aktuell.

## Nutzerauftrag

Der Nutzer besitzt ein portables CarPlay-/Android-Auto-Display **Imagebon H13 Pro**, vor längerer Zeit auf AliExpress gekauft. Er möchte das Bootlogo durch ein eigenes Bild ersetzen und wünscht eine gründliche Untersuchung einschließlich Reverse Engineering, Firmwaremodifikation und Auslesen/Flashing, soweit erforderlich.

Vom Nutzer genannte Firmware, unverändert inklusive abschließender Punkte:

`R13.10.01.22_1.1.1026.0_2.77.3f_20231013.1841..`

Es gibt noch kein vom Nutzer geliefertes Wunschbild, keine genaue Platinenrevision und keine bestätigte Speicher-/Chipidentifikation am Gerät. Die exakte USB-/FM-Gerätevariante wurde ebenfalls noch nicht beantwortet.

Der Verkäufer wurde bereits mehrfach erfolglos kontaktiert. **Nicht erneut als nächsten Schritt zum Verkäufer schicken.** Der Nutzer will direkten USB-/Netzwerkzugriff, ein eigenes Auslesen oder ein tatsächlich passendes öffentliches Paket. Ein solches R13-Komplettimage wurde nicht gefunden.

Der Nutzer kann Windows verwenden, Linux wäre möglich. Während der Untersuchung hatte er zunächst keinen Rechner zur Hand, anschließend öffnete er ChatGPT am Rechner. Ein lokales Terminal/USB-/Browser-Steuerwerkzeug war dadurch in der Cloud-Sitzung nicht verfügbar. Er möchte nun dieses Verzeichnis in einer lokalen Codex-Instanz öffnen. Das Gehäuse würde er nur öffnen, wenn es zwingend notwendig ist.

## Was auf dem H13 wirklich beobachtet wurde

Der Nutzer verband sein Handy mit dem WLAN des Displays und öffnete:

`http://192.168.10.1:8082/api/getdeviceinfo?cmd=2001`

Gemeldete Antwort (MAC hier weggelassen):

```json
{"Version":"v1.0","product":"R8-V2.0","sp":"qckj"}
```

**Das ist die zentrale neue Zielgeräte-Evidenz.** Die API funktioniert. Produkt-/Protokollfelder stimmen mit der Referenz überein. Die Werte sind im Referenzprogramm teilweise Konstanten; das ist kein Hashvergleich und kein Nachweis identischer Binärdateien.

Als nächste Leseabfrage wurde bereits angefordert:

`http://192.168.10.1:8082/api/getdeviceinfo?cmd=2002`

**Die Antwort ist noch ausstehend.** Nicht behaupten, diese Abfrage sei fehlgeschlagen oder erfolgreich gewesen. `device-evidence/http-cmd-2001.json` enthält die bestätigten Daten ohne MAC.

Nicht erfolgt: USB-Hardware-ID-Messung, ADB-Shell, Rootzugang, BootROM-/Loader-Zugang, Öffnen, UART-Messung, Auslesen von H13-Partitionen, Änderung von Zugangsdaten, HTTP-POST/Setter-Test, Logo-Flash oder Firmware-Flash. Es gab keine Fernverbindung der Cloud mit dem Gerät; die Information stammt vom Nutzer.

## Untersuchungsergebnisse in Kürze

### 1. Dokumentierter H10-Logo-Wechsel

Ein Besitzerbericht von 19.08.2023 beschreibt einen erfolgreichen Logo-Austausch beim Imagebon H10 Pro mittels Rockchip-Updatekarte und Datei `logo`. Vorgaben dort: 24-Bit-BMP, höchstens 1600×600, unter 4 MB, Datei ohne Endung. Screenshot zeigt getrennte Dateien `logo`, `boot`, `uboot`, `rootfs`, `recovery` usw. Bericht: https://isulnara.com/archives/2794

Übertragbarkeit auf den konkreten R13-Build unbestätigt. Sekundärseiten setzen H10/A9/H13 gleich; das wurde ausdrücklich nicht als Crossflash-Freigabe gewertet.

### 2. Öffentliches H70-R33-Referenzpaket tatsächlich analysiert

Datei: `sources/H70-R33-reference-only.img`, ursprünglicher Name:

`update_R33.10.03.22_1.2.1025.4_V3.08151.50_20250702.1543.img`

Größe 91.910.616 Bytes, SHA-256:

`3f462bcce6370157050f07d362bba576d19e790283094d7cefcb304bc9b933f3`

RKFW-Container mit RKAF bei Byte 283060; Loader benennt RV1126; Rootfs/OEM/Userdata als UBI. Eine separate Logo-Partition hat in dieser Referenz 4 MiB Kapazität. Ihr Inhalt ist eine direkte BMP-Datei, 48.180 Bytes, 720×112, 8 Bit RLE8, „Welcome“. Das ist kein H13-Original-Logo.

Ein altes Protokoll im ebenfalls heruntergeladenen SDDiskTool erwähnt einen **fehlgeschlagenen Dateiöffnungsversuch** für `update_R13.10.03.22_1.1.90.0_V2.00.3f.debug_20240123.1531.img`. Hinweis auf verwandte Werkzeugfamilie, kein Firmwaredownload und kein erfolgreicher Flash.

### 3. Normales System und Recovery wurden weiter entpackt

`reference-rootfs/1305731643/rootfs/usr/bin/cvr_app` ist die Referenz-Anwendung (ARM32, dynamisch verlinkt, viele Funktionsnamen in `.dynsym`). Größe 2596408 Bytes, SHA-256:

`9a719fc17bc404c3f640c9aa117fbb973bf0edb4adc4c8d899500c1ebc874c79`

Mit Capstone und pyelftools wurden tatsächliche Kontrollflüsse, Literaladressen und PLT-Aufrufe untersucht. Die Ausgaben liegen als Textdateien bei; Details/Adressen in Ohne-Verkaeufer.md.

### 4. USB/ADB: aktivierbarer Mechanismus, aber Normalbetrieb ist Host

Referenz-Recovery: `.usb_config` enthält `usb_adb_en`; Gadget VID/PID 2207:0006.

Normale Referenz-App: `Start_initd()` prüft `debug_mode_enable()` und schaltet ansonsten den OTG-Port ausdrücklich auf Host. Der Rückgabewert 2 aktiviert ADB über `/tmp/.usb_config` und `S50usbdevice`.

- `/oem/qckj_isptunner_file` -> Wert 2.
- `/mnt/sdcard/qckj_debug_all_file` -> Wert 1; **aktiviert diesen ADB-Zweig nicht**.
- OEM-Skript `adb.sh` und `usr/bin/start_usb.sh` sind vorhanden. Kein extern erreichbarer Aufruf auf H13 bestätigt.

Die Textdatei `debug-disassembly.txt` dokumentiert dies. Nicht einen simplen SD-Flag-Trick zum Freischalten behaupten.

### 5. Eingebauter Logo-Import: möglicherweise ohne ganzes Firmwareimage

Referenzfunktionen: `sd_upgrade_start()` -> `ChangeEmmcLogo()` / `ChangeSpinandLogo()`. Quelle ist `/mnt/sdcard/userdata/logo.bin`.

SPI-NAND-Funktion verwendet `flashcp`; eMMC hat einen eigenen Kopierpfad. Fest hinterlegte Referenzziele `/dev/mtd8` und `/dev/mmcblk0p8` **nicht ungeprüft auf H13 anwenden**.

Die Aufrufe kommen unter anderem aus `LylinkSettingWindow::SetSDUpgradeEvent` und `MotoSettingWindow::SetSDUpgradeEvent`. Der Stringkatalog nennt „Personalized upgrade“ / „Personalisiertes Upgrade“, getrennt vom Firmware-Upgrade. Ob dieses Menü auf H13 vorhanden/erreichbar ist, ist offen.

`sd_upgrade_start` verarbeitet vorher auch Personalisierungsdaten; `userdataCover` liest `/oem/etc/version` und kann Konfigurationsdateien kopieren. Kein fertiges Logo-only-Paket erstellt, keine leere Testkarte ausprobiert. Aufruf und Seiteneffekte für den Zielbuild prüfen.

### 6. Lokale HTTP-API und Shell-Kandidat

Referenz-Webserver: Port 8082, document_root `/tmp`. Registriert GET `/api/getdeviceinfo`, POST `/api/setdeviceinfo`, Downloadhandler für SD-/SQLite-Dateien. GET liest die Kommandonummer nach dem letzten `=`. Dispatcher: 2001 Version/Produkt; 2002 Geräteinfo.

Der POST-Setter verarbeitet Query-Strings; nicht einfach von einem JSON-Body ausgehen. In der Referenz wird unter anderem mit festem Substring-Start 13, dem letzten `&` und letzten `=` geparst. Die genaue Zielsyntax ist nicht am H13 getestet.

Referenz-Setter für Namen/Passwort bauen über `sprintf` Shellkommandos für `sed` zusammen und gelangen über `qc_system` zu `popen`. Die Namensprüfung protokolliert ungültige Zeichen, erreicht danach aber trotzdem den Setter. Damit besteht ein konkreter Command-Injection-Kandidat. Eine **lokale Nachstellung der Shell-Befehlskonstruktion** erzeugte einen harmlosen Marker bei unveränderter Testkonfiguration. Das war keine ARM-Emulation, kein Test des HTTP-Pfads und kein Rootnachweis auf H13.

Die Setter speichern Gerätekonfiguration und rebooten in der Referenz. Keine experimentellen Setter am Nutzergerät gesendet. Ein unpassender Probeaufruf könnte WLAN-Einstellungen ändern. Die echte H13-App auslesen oder weitere rein lesende Identifikation hat Vorrang; einen kontrollierten, wiederherstellbaren Versuch erst nach Prüfung der Details ausarbeiten.

## Konkreter Einstieg für die lokale Instanz

1. Prüfen, ob Rechner mit dem Display-WLAN verbunden ist. Nicht die Cloud-IP/LAN-Reichweite voraussetzen. HTTP-GET 2001 erneut dokumentieren und 2002 erheben.
2. Nutzer kann prüfen, ob „Personalisiertes Upgrade“ im Menü existiert; noch nicht auslösen.
3. USB-Geräte/Hardware-IDs unter Windows erfassen; bekannte ADB-Geräte auflisten. ADB wird nicht automatisch durch USB-Stromversorgung oder eine neu installierte App aktiv.
4. Falls vorhandenes ADB erreichbar: `id`, Kernel, `/proc/mtd`, Partitionslinks lesen; tatsächliches `/usr/bin/cvr_app` mit `adb pull` sichern und separat als **H13-Zielartefakt** aufbewahren.
5. Gibt es kein ADB, den bestätigten HTTP-Zugang vertiefen. Verifizierten API-Lesepfad und tatsächliche Zielcode-Evidenz von Referenzhypothesen trennen.
6. Original-Logo und notwendige Wiederherstellungsdaten sichern, bevor geschrieben wird. NAND-Dumps brauchen Beachtung von ECC/Bad Blocks; ein beliebiger Rohdump ist nicht automatisch ein brauchbares Flashimage.
7. Erst danach den geringsten nötigen Eingriff für das eigene Logo entwickeln. Der Nutzer hat noch kein Wunschbild geliefert.

Nicht erledigt: exaktes R13-Komplettimage gefunden, H13-Firmware ausgelesen, Root/Shell verifiziert, eigenes Bootlogo erstellt/geflasht. Das Ziel ist noch offen. Den bisherigen Stand nicht als fertige getestete Anleitung präsentieren.

## Hilfsmittel und bekannte Grenzen

- `h13_probe.py`: Standardbibliothek; HTTP 2001/2002, Windows-PnP-Infos, bestehendes ADB, optional App-Pull. Keine POST-/Flash-/Root-/Reboot-Befehle. Bisher nur Syntax/CLI geprüft, nicht am H13.
- `inspect_firmware.py`: RKFW/RKAF extrahieren/BMP anzeigen; Containergrenzen und Hashes, **keine** Signatur-/Checksumme-/Hardwarekompatibilitätsprüfung. Am echten Referenzdownload ausgeführt.
- `disassemble_reference.py`: ARM-Modus; PLT-Zuordnung nimmt die in der Referenz beobachtete GNU-ARM-PLT-Struktur an (20 Byte Kopf, 12 Byte Einträge). Bei anderer Zielbinärdatei diese Annahmen prüfen. Literalpools werden teils als Instruktionen angezeigt; daraus keine Codewirkung ableiten. Strings unter 3 Zeichen werden nicht kommentiert.
- `.venv` aus der Cloud ist nicht portabel und wird durch Requirements ersetzt.
- Alte JSON-Ergebnisse enthalten absolute Cloud-Pfade; sie sind Herkunftsinformationen, keine lokal existierenden Pfade.
- Die Dokumente sind kumulative Ergebnisse, kein Wortprotokoll des gesamten Chats. Quellenmaterial, Code und alle regulären extrahierten Dateien sind enthalten.
