# Zweiter, begrenzter SD-Versuch: Aufruf sichtbar machen

Am 16.11.2026 erreichte das H13 mit Paket v1 den breiten Fertigungstest. Es entstand **kein** `H13-READOUT`; nur leere Dashcam-Verzeichnisse wurden angelegt. Der Nutzer bestätigte anschließend, dass alle drei ursprünglichen Dateien mit korrekten Namen unverändert vorhanden waren.

Damit ist der Fertigungsmodus bestätigt, der externe Programmaustausch jedoch **nicht**. Der ältere Build zeigt außerdem den breiten Test statt des H70-DDR-Sonderzweigs. Das fehlende GPS-Modul belegt keine Ursache für das fehlende Ausleseergebnis.

## Was an v1 zu eng war

Das erste Skript beendete sich vor seiner ersten Ausgabe, wenn die Argumente nicht exakt `128m 1` waren. Es schrieb außerdem nur unter dem fest angenommenen `/mnt/sdcard`. Beides war lediglich aus der H70-Referenz übernommen. Ohne Zielcode konnte ein abweichender Aufruf daher unsichtbar bleiben. **Es gibt noch keinen Nachweis, dass dies beim H13 passiert ist.**

Version 2 entfernt die Argumentprüfung und leitet den Kartenpfad aus dem Speicherort des Skripts ab. Die erste Ausgabe ist jetzt `rk_pcba_test_res/H13-PROBE-STARTED.txt`, noch vor dem Anlegen von `H13-READOUT`. Darin stehen die echten Argumente und die Rechte. Ein Kopierfehler kann dadurch von einem fehlenden Einstieg unterschieden werden.

Keine neuen Steuerflags, kein echtes Memtest-Programm, keine zusätzlichen Executable-Namen, keine Update-/Logo-Datei und keine Aktivierungsdateien. Die Funktionen und möglichen Nebenwirkungen des vom Gerät gestarteten Fertigungsmodus bleiben dieselben wie beim ersten Versuch; der H70-Aufrufer remountet `/` schreibbar. Unser Skript enthält keine Flash-/Formatierungs-/Einstellungsänderungen und schreibt nur auf die Karte.

## Vorgehen

1. SD-Karte am Rechner öffnen und vorhandene Ergebnisse sichern, falls inzwischen welche vorhanden sind.
2. Den Inhalt des neuen ZIPs auf die oberste Kartenebene entpacken. Nur `rk_pcba_test_res/memtester_smd` ist inhaltlich geändert; die beiden leeren Flags bleiben gleich. Die alte Skriptdatei ausdrücklich überschreiben. Keine weitere Ebene `card-root` oder `H13-SD-Probe-v2` dazwischen anlegen.
3. Zur Kontrolle: In der Datei `memtester_smd` steht ganz oben **Version 2**; die alte Prüfung auf `128m` darf nicht mehr enthalten sein. Zeilenenden nicht durch erneutes Speichern ändern.
4. Karte bei ausgeschaltetem Display einlegen, normal versorgen, 60–90 Sekunden warten. Keine Testfelder antippen und nicht auf GPS-Abschluss warten.
5. Ausschalten, Karte entnehmen und am Rechner zuerst **im Testordner** nach `H13-PROBE-STARTED.txt` suchen; danach im Kartenhauptverzeichnis nach `H13-READOUT`.

Ergebnisbewertung:

- **Marker und Readout vorhanden:** Skriptstart bestätigt. `identity.txt`, App-Kopie und Fehlerdateien auswerten.
- **Nur Marker vorhanden:** Start ist belegt; Marker enthält gegebenenfalls den Fehler beim Ordneranlegen. Auch auf einen bereits vorhandenen `H13-READOUT` achten.
- **Wieder weder Marker noch Readout:** Dieser Shellskript-Einstieg bleibt unbestätigt. Mögliche Ursachen sind ein fehlender oder anders benannter externer DDR-Aufruf, Exec-/Mountbeschränkungen oder ein anderer früher Aufrufkontext. Keine weiteren Variationen von Flags/Programmnamen ausprobieren; dann Netzwerkidentifikation fortsetzen.

Das Skript überschreibt einen vorhandenen Ergebnisordner nicht. Es protokolliert einen solchen Fall im Marker. Für einen bewussten weiteren Versuch vorhandene Auslesedaten zuerst am Rechner sichern/umbenennen.

Die Codeprüfung und lokalen Tests verwenden temporäre Kartennachbildungen sowie eine künstliche Appdatei. Auf dem echten H13 ist v2 noch nicht getestet. Die tatsächliche H13-Anwendung liegt weiterhin nicht vor.
