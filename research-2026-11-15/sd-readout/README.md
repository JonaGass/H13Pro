# SD-Ausleseversuch über den Fertigungstest

**Historisches Paket v1:** Am 16.11.2026 wurde damit auf dem echten H13 der Fertigungsbildschirm erreicht, aber kein `H13-READOUT` erzeugt. Für den begrenzten Folgeversuch die [Diagnose v2](../../research-2026-11-16/sd-probe-v2/README.md) verwenden. Der nachfolgende Text dokumentiert den Plan vor dem ersten Zieltest.

**Neuer, im H70-R33-Referenzcode nachgewiesener Einstieg. Auf deinem H13-R13 noch nicht getestet.** Kein H70-Image verwenden. Das enthaltene `memtester_smd` ist ein lesbares Shellskript, kein echtes RAM-Testprogramm.

## Nachweis und Grenzen

Im Referenzprogramm prüft `pcba_test()` beim Start, ob `/mnt/sdcard/rk_pcba_test_res` existiert. `pcba_factory_flag_file` wählt `CreateBigWindow()`. `pcba_ddr_special_flag_file` wählt dort den DDR-Sonderzweig, der bei vorhandenem `memtester_smd` einen Thread startet. Dieser führt aus:

```text
mount -o remount,rw /
chmod 777 /mnt/sdcard/rk_pcba_test_res/memtester_smd
/mnt/sdcard/rk_pcba_test_res/memtester_smd 128m 1
```

Der Sonderzweig überspringt den gewöhnlichen breiten Fertigungstest; zusätzlich werden in der Referenz Speichergrößen gelesen und ein Touch-Test gestartet. Ein vorhandenes Dateiformatierungs-/Aktivierungsflag wird von diesem Paket nicht mitgeliefert.

Die Aufrufkette ist statisch und durch isolierte Emulation der tatsächlichen ARM-Instruktionen mit nachgebildeten Dateisystem-/GUI-/libc-Aufrufen geprüft (`../emulate_sd_path.py`, `../sd-path-emulation.json`). Hardwaretreiber, ein vollständiger Boot und das H13 wurden damit **nicht** getestet. Es ist ein konkret begründeter Versuch, keine bestätigte H13-Anleitung.

**Der Gesamtvorgang ist nicht vollständig read-only:** Bereits der Referenz-Aufrufer remountet `/` schreibbar. Unser Skript selbst schreibt ausschließlich in einen neuen Ergebnisordner auf SD und enthält weder Flash-, Formatierungs-, Installations-, ADB-Umschalt- noch Netzwerkserver-Befehle. Ein älterer Zielbuild kann sich anders verhalten. Die Codekopie läuft mit den Rechten der App; Root wird nicht vorausgesetzt und erst im Ergebnis festgestellt.

## Karte vorbereiten

Eine separate, leere, vom Display bereits unterstützte FAT32-Karte verwenden. Keine Karte mit wichtigen Aufnahmen nehmen. Keine Firmware-IMG-, Logo-, userdata- oder weiteren Testdateien hinzufügen. Nicht das Rockchip-SD-Upgrade-Werkzeug verwenden: Hier genügt normales Kopieren.

Den **Inhalt von `card-root`** auf die oberste Ebene der Karte kopieren. Ergebnis:

```text
Kartenwurzel/
└── rk_pcba_test_res/
    ├── pcba_factory_flag_file        (leer)
    ├── pcba_ddr_special_flag_file    (leer)
    └── memtester_smd                (Shellskript, ohne Endung)
```

Die Dateinamen müssen exakt stimmen; unter Windows Dateiendungen anzeigen. Das Skript hat LF-Zeilenenden. Nicht mit einem Editor als `.txt` oder mit CRLF neu speichern. Der Referenz-Aufrufer setzt die Ausführungsrechte selbst.

## Einmaliger Versuch

1. Display ausschalten, vorbereitete Karte einlegen, mit seiner normalen stabilen Versorgung einschalten.
2. Keinen Firmware-/Logo-Upgrade-Dialog auslösen und in einer eventuell erscheinenden chinesischen Testoberfläche keine Formatierungs-/Aktivierungs-/Reset-Tasten drücken.
3. Mindestens 60 Sekunden warten. Im erwarteten Pfad erfolgt der Skriptstart nach einer zusätzlichen Pause von fünf Sekunden. Es gibt keinen Fortschrittsbalken für dieses Ausleseskript.
4. Ausschalten und Karte entnehmen. Am Rechner nach `H13-READOUT` suchen. Karte vor dem nächsten normalen Gerätestart entnehmen bzw. den gesamten Testordner am Rechner wieder entfernen.

Ergebnisse:

- `STARTED.txt` beweist, dass unser Skript aufgerufen wurde.
- `identity.txt` enthält die tatsächlichen Rechte und Kernelangaben.
- `cvr_app` ist, sofern lesbar, die erstmals aus dem H13 kopierte Anwendung; `app.sha256` ihr Hash.
- `proc-mtd.txt`, `proc-partitions.txt`, `storage-map.txt` und `oem-version.txt` liefern Zielinformationen, ohne Partitionen automatisch auszulesen oder zu schreiben.
- `COMPLETE.txt` bedeutet, dass das Skript sein Ende erreicht hat. **Nicht**, dass jeder einzelne Kopierbefehl erfolgreich war; Fehlerdateien und Appgröße prüfen.
- Kein Ergebnisordner: Dieser Einstieg ist nicht bestätigt. Möglich sind anderer Code, ein anderer SD-Mountpfad, fehlende frühe Kartenerkennung, ein `noexec`-Mount oder abweichende Aufrufargumente. Nicht durch zusätzliche wahllose Flags oder Firmwaredateien erzwingen.

Das Skript überschreibt auch einen unvollständigen Ergebnisordner nicht. Vor einem bewussten zweiten Versuch Ergebnisse sichern und `H13-READOUT` am Rechner umbenennen/entfernen.

Die aufgezeichneten Daten bleiben auf deiner SD-Karte. Vor öffentlichem Hochladen auf Seriennummern, WLAN-Daten und sonstige Kennungen prüfen. Für die Analyse zunächst App-Hash, Rechte, Speicherplan und die Anwendung selbst getrennt sichern. Keine festen H70-Partitionsnummern übernehmen.

## Verifikation in der Cloud

Das Skript wurde syntaktisch und in einem lokalen Test mit temporärem SD-Ersatz und einer künstlichen Appdatei geprüft. Die Emulation prüft die Referenz-Aufrufkette. Keiner dieser Tests behauptet einen erfolgreichen Lauf auf dem H13.
