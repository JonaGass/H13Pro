# Nach zwei erfolglosen SD-Ausleseversuchen: Netzwerk identifizieren

Aktueller Zielbefund vom 16.11.2026: Der Fertigungsmodus ist erreichbar; weder v1 noch v2 erzeugten neue Auslesedateien. Auch der frühe v2-Marker fehlt nach Nutzerbericht. Damit ist die Ausführung unseres SD-Programms nicht belegt. Kein weiterer Flag-/Dateinamen-/GPS-Versuch ist vorgesehen. Die genauen Ursachen lassen sich ohne Zielcode nicht unterscheiden.

**Die unten beschriebene erste HTTP-Abfrage ist inzwischen beantwortet:** Das H13 meldet `device_id: RV1126`, `device_name: R8`, `software: V1.0`. Vollständige Antwort: `device-evidence/http-cmd-2002-2026-11-16.json`. Diese API-Identität stützt die Plattformzuordnung, ist wegen teilweise fester Felder im Referenzcode kein physischer Chipnachweis. Die `info`-Liste nicht als Befehlsliste zum Experimentieren verwenden. Als Nächstes den PC-Test durchführen; er wiederholt 2001/2002 als Verbindungskontrolle und ergänzt Portbefunde.

## Zuerst eine Geräteinfo, auch mit dem Handy möglich

Testkarte bei ausgeschaltetem Gerät entfernen. Display normal starten und Handy mit dessen WLAN verbinden, wie beim früher erfolgreichen 2001-GET. Öffnen:

```text
http://192.168.10.1:8082/api/getdeviceinfo?cmd=2002
```

Exakte Antwort oder Fehlermeldung dokumentieren. Ist der Dienst nicht erreichbar, zunächst den schon bestätigten Kontrollaufruf mit `cmd=2001` wiederholen. Fehlendes Internet im Display-WLAN ist zu erwarten und belegt keinen Fehler dieser lokalen Verbindung.

## Gezielte Diagnose am Windows-PC

Das neue Skript zuerst bei bestehender Internetverbindung herunterladen bzw. den Checkout mit `git pull --ff-only` aktualisieren. Danach den PC mit dem Display-WLAN verbinden; dort ist normalerweise kein Internet vorhanden. Es ist keine USB-Verbindung erforderlich. Im Verzeichnis mit dem Skript:

```powershell
py .\h13_network_probe.py
```

Python 3 ist erforderlich; Zusatzpakete und Administratorrechte sind nicht nötig. Das kleine `H13-Netzwerkdiagnose.zip` enthält das einzelne Skript und eine Kurzbeschreibung; es ist kein SD-Paket.

Das Skript fragt nur `GET /api/getdeviceinfo?cmd=2001` und `cmd=2002` an Port 8082 ab. Danach prüft es einmalig zehn TCP-Ports derselben Geräte-IP: 22, 23, 80, 443, 554, 5555, 8080, 8081, 8082 und 9999. Es sendet dabei keine Anwendungsdaten, meldet sich nirgends an und aktiviert keine Dienste. Die IP ist standardmäßig `192.168.10.1`; ein anderer tatsächlich angezeigter lokaler Gerätewert kann über `--host` angegeben werden. Kein Subnetzscan.

Die Ports sind Suchhinweise für mögliche Shell-, Web-, Streaming- oder Diagnosezugänge. Ein offener Port beweist noch nicht, welches Protokoll dort läuft oder dass Root-/Firmwarezugriff möglich ist. Eine Ablehnung und ein Timeout werden getrennt aufgezeichnet; ein Timeout beweist nicht sicher, dass ein Dienst geschlossen ist.

HTTP-Anfragen umgehen Internet-Proxys und folgen keinen Weiterleitungen. Es werden keine POST-Anfragen, Uploads, WLAN-Setter, ADB-Verbindungen, Neustarts oder Flashbefehle gesendet. Der Diagnosecode nimmt keine Konfigurationsänderung vor; bestehende Server können Verbindungsvorgänge protokollieren oder ihren Verbindungszustand ändern.

Ergebnis ist eine einzelne lokale Datei `h13-network-<Zeit>.json`. Diese im Chat zur Analyse bereitstellen; nicht automatisch ins öffentliche Repository übertragen. MAC-Adressen im üblichen Doppelpunkt-/Bindestrichformat werden im HTTP-Text redigiert; andere Gerätekennungen können enthalten sein. Vorhandene Ergebnisdateien werden nicht überschrieben.

Mit Antwort und Portbefund wird der nächste Zugriff am tatsächlichen H13 ausgewählt. Es gibt weiterhin keinen bestätigten Rootzugang, keine Ziel-App und keinen Zieldump. Ein Gehäuseöffnen oder erneutes Nachrüsten des GPS-Moduls ist für diese Diagnose nicht notwendig.
