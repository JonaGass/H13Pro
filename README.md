# Imagebon H13 Pro – Bootlogo-Recherche und Codex-Übergabe

Dieses Repository enthält den vollständigen verfügbaren Arbeitsstand zur Untersuchung eines nutzereigenen Imagebon H13 Pro. Ziel ist ein eigenes Bootlogo ohne Unterstützung des AliExpress-Verkäufers.

## Lokal fortsetzen

```powershell
git clone https://github.com/JonaGass/H13Pro.git
cd H13Pro
```

Alternativ oben über **Code → Download ZIP** herunterladen und entpacken. Alle regulären Dateien sind direkt im Repository enthalten; Git LFS und Submodule sind nicht erforderlich. Der entpackte Arbeitsstand umfasst rund 306 MB.

Dieses Verzeichnis mit der lokalen Codex-Instanz öffnen und folgenden Auftrag übergeben:

> Lies AGENTS.md, START_HERE.md und HANDOFF.md, danach Ohne-Verkaeufer.md. Setze die Untersuchung meines H13 Pro für ein eigenes Bootlogo ohne Verkäuferhilfe am dokumentierten Stand fort. Prüfe zunächst mit Leseoperationen die lokale Geräteverbindung. Die Antwort auf HTTP cmd=2002 steht noch aus.

## Aktueller Stand

- Zielgerät: Imagebon H13 Pro, Firmware `R13.10.01.22_1.1.1026.0_2.77.3f_20231013.1841..`.
- Vom Nutzer am echten Gerät bestätigt: `GET http://192.168.10.1:8082/api/getdeviceinfo?cmd=2001` antwortet mit `Version: v1.0`, `product: R8-V2.0`, `sp: qckj`.
- Öffentliches H70-R33-Referenzimage wurde heruntergeladen, entpackt und statisch analysiert. Hinweise auf Logo-Import, USB-/ADB-Umschaltung und eine HTTP-Shell-Hypothese sind dokumentiert.
- Kein H13-Firmwaredump, Root-/ADB-Zugang oder funktionierender Logo-Wechsel wurde bisher bestätigt.

**Die enthaltene H70-R33-Firmware ist ausschließlich Referenzmaterial und darf nicht auf das H13 geflasht werden.** Befunde aus der Referenz sind in der Übergabe ausdrücklich von tatsächlichen H13-Beobachtungen getrennt.

## Einstieg und Dateien

- [START_HERE.md](START_HERE.md): Bedienung der Diagnose, Python-Umgebung und Dateizuordnung.
- [HANDOFF.md](HANDOFF.md): Nutzerwünsche, belegte Ergebnisse, Grenzen und konkrete nächste Schritte.
- [Ohne-Verkaeufer.md](Ohne-Verkaeufer.md): vertiefte technische Untersuchung.
- [SOURCES.md](SOURCES.md): Quellen und Herkunft der Originaldownloads.
- `sources/`, `reference-extracted/`, `reference-rootfs/`, `reference-oem/`, `reference-userdata/`: Originale und Analyseartefakte.
- `device-evidence/`: bestätigte Gerätebeobachtungen; die MAC-Adresse wurde weggelassen.

Zur Integritätsprüfung der übergebenen Originaldateien:

```powershell
py .\verify_bundle.py
```

Symlinks aus der Linux-Referenzfirmware sind zur Windows-Portabilität als Metadaten in `FIRMWARE_SYMLINKS.json` enthalten. Die ursprünglichen UBI-Abbilder liegen ebenfalls bei. Betriebssystemspezifische Cloud-venvs und Caches wurden durch Requirements-Dateien ersetzt.

Das Repository ist eine inhaltliche Arbeitsübergabe mit Quellen und Analyseartefakten, kein vollständiger Chat-Export. Die Untersuchung und der Bootlogo-Wechsel sind noch nicht abgeschlossen.
