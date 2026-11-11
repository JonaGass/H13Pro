# Imagebon H13 Pro: eigenes Bootlogo

**Fortsetzung:** Der Verkäufer antwortet nicht. Die weitere Untersuchung erfolgt ohne ihn; inzwischen wurde die lokale HTTP-Schnittstelle am echten H13 bestätigt. Siehe [Zugriff ohne Verkäufer](Ohne-Verkaeufer.md). Die unten vorgeschlagene Verkäuferanfrage gehört zum ersten Recherchestand und ist nicht mehr der vorgesehene nächste Schritt.

Recherche vom 11. November 2026. Ausgangsversion laut Nutzer:

`R13.10.01.22_1.1.1026.0_2.77.3f_20231013.1841..`

## Ergebnis und Reichweite

Es gibt einen dokumentierten erfolgreichen Logo-Austausch beim Imagebon H10 Pro. Eine eigene Offline-Analyse einer öffentlich verlinkten H70-Pro-Firmware bestätigt unabhängig davon, dass Imagebon auf einer verwandten Rockchip-Plattform eine separate Logo-Partition mit einer gewöhnlichen BMP-Datei verwendet. Damit ist ein konkreter technischer Weg gefunden.

**Für die exakte H13-Pro-Hardware und den oben genannten Build ist der Weg noch nicht validiert.** Kein passendes R13-Firmwarepaket, kein Flash-Dump und kein angeschlossenes Gerät lagen zur Untersuchung vor. Ein modifiziertes H13-Image wurde deshalb weder erstellt noch getestet. Die Recherche ersetzt diese fehlende Prüfung nicht.

Die beste nächste Handlung ist: vom ursprünglichen Verkäufer ein zur vollständigen Versionsnummer passendes Wiederherstellungspaket einschließlich SD-Werkzeug und möglichst ein reines Logo-Update anfordern. Das Paket lässt sich vor jedem Geräteeingriff offline untersuchen. Ein Firmware-Upgrade auf einen neueren Softwarestand ist für das Ziel nicht grundsätzlich erforderlich.

## Was die Quellen tatsächlich belegen

| Befund | Beleg | Aussagegrenze |
|---|---|---|
| Ein Besitzer hat beim H10 Pro das Bootbild erfolgreich ersetzt. | [Eigener Erfahrungsbericht von isul, 19.08.2023](https://isulnara.com/archives/2794) | H10 Pro; keine identische H13-Firmwareversion angegeben. |
| Die dortige SD-Karte führt `logo` getrennt von den Systemabbildern. | [Original-Screenshot](https://isulnara.com/wp-content/uploads/2023/08/h10pro-sd-1.png) | Zeigt Dateien; kein Beweis, dass ausschließlich die Logo-Partition geflasht wird. |
| H13 Pro wird in Produktunterlagen zusammen mit H10 Pro und A9 Pro genannt. | [Zusammenstellung zum AliExpress-Artikel 1005005666024981](https://manuals.plus/ae/1005005666024981) | Sekundärquelle mit generierten Abschnitten; kein Beleg für austauschbare Firmware. |
| Das H13-Originalhandbuch beschreibt Themes und Systemoptionen, aber dort kein Logo-Importmenü. | [Konvertiertes Originalhandbuch mit PDF](https://manuals.plus/m/25242b46d2845b4d4c115be1acb5fd0ced5d162dcdac69e2977ca4e6aba1b247) | Ein verborgenes Menü ist damit weder nachgewiesen noch ausgeschlossen. |
| Rockchip bietet einen offenen RockUSB-Lese-/Schreibclient. | [rockchip-linux/rkdeveloptool](https://github.com/rockchip-linux/rkdeveloptool) | Kein gerätespezifischer Nachweis für den Zugang zum H13. |
| Die untersuchte Imagebon-R33-Datei enthält RV1126, Linux-Bestandteile und ein separates BMP-Logo. | Eigene Binäranalyse; Details und Hashes unten. | Referenz H70 Pro, nicht das Zielgerät. |

Die teils widersprüchlichen Daten auf automatisierten Handbuchseiten wurden nicht als Hardware-Nachweis behandelt. Insbesondere ist die Behauptung „H10/H13 sind gleich“ keine Freigabe zum Crossflash. Der Präfix `R13` belegt auch keine Android-Version. Der Zeitanteil der Nutzer-Version lässt sich plausibel als 13.10.2023, 18:41 lesen; die übrigen Felder sind nicht verlässlich entschlüsselt.

## Nachgewiesene Methode und Übertragung auf das H13

Der [H10-Erfolgsbericht](https://isulnara.com/archives/2794) beschreibt: passende Firmware mit **Rockchip Create Upgrade Disk Tool** auf SD schreiben und einmal aktualisieren; nach dem Herunterfahren auf der Karte `logo` ersetzen. Das Ersatzbild ist eine **24-Bit-BMP**, höchstens **1600 × 600**, unter **4 MB**, mit dem Dateinamen **`logo` ohne Endung**. Anschließend wird erneut über diese Karte aktualisiert. Der Autor nennt Originalfirmware als Rückweg bei einem nicht dargestellten Bild und weist auf Brick-Risiko hin.

Für dein H13 ist diese Methode erst dann ausführbar begründet, wenn das passende Paket denselben Mechanismus zeigt. Zu prüfen sind insbesondere:

1. **Hardware-Zuordnung:** Verkäufer bestätigt den vollständigen Build und die bestellte Gerätevariante; wenn nötig auch Kamerasensor, Panel und Platinenrevision.
2. **Logo-Container:** Beginnt die extrahierte Logo-Datei wirklich mit `BM`? Oder liegt das Bild in einem anderen Container? Im zweiten Fall gilt der einfache Austausch nicht automatisch.
3. **Grenzen:** Partitionsgröße aus dem eigenen Paket lesen. 1600 × 600 × 3 Pixelbytes ergeben mit klassischem BMP-Header 2.880.054 Bytes und passen in 4 MiB; daraus folgt keine universelle Grenze für andere Geräte.
4. **Update-Ablauf:** Ermitteln, ob die SD-Recovery die sichtbaren Einzeldateien oder das eingebettete Gesamtpaket verwendet, welche Partitionen sie überschreibt und ob sie Einstellungen löscht.
5. **Rückweg:** Originalpaket unverändert behalten. Eine vorbereitete Original-Updatekarte ist sinnvoll; sie ersetzt keine garantierte Maskrom-Wiederherstellung bei beschädigtem Bootloader.

Die erste Originalaktualisierung aus dem Erfahrungsbericht sollte nicht vorschnell durchgeführt werden: Das Paket und eine am PC erstellte Karte lassen sich zunächst ohne Gerät untersuchen. Wenn ein Logo-only-Update verfügbar ist, lässt sich ein unnötiger Vollflash vermeiden. Ob der erste Flash im beschriebenen Verfahren technisch notwendig ist, konnte ohne das damalige Paket nicht geklärt werden.

## Eigene Offline-Analyse: öffentliches H70-Pro-Referenzpaket

Ausgangspunkt war ein [öffentliches Produktangebot mit Firmwarelink](https://hfg3d.com/produto/imagebon-h70-plus-114%E2%80%B2%E2%80%B2-4k-adas-dash-cam-60fps-carro-sem-fio-play-e-android-auto-gravacao-dupla-visao-noturna-dvr/). Die referenzierte [Drive-Freigabe](https://drive.google.com/drive/folders/1AYti2WEuObgKGuRzH-U1W1F-JGd6YXVm) enthält einen [H70Pro-Unterordner](https://drive.google.com/drive/folders/1UpUSbFUOF8zsZCvRLihPBZMB3rE__ISG) mit Werkzeug, Anleitung, Video und Firmware. Die Verkäufer-/Herstellerherkunft wurde nicht kryptografisch authentifiziert.

**Diese Firmware nicht auf das H13 schreiben.** Sie ist nur Vergleichsmaterial:

```text
update_R33.10.03.22_1.2.1025.4_V3.08151.50_20250702.1543.img
Dateigröße: 91.910.616 Bytes
SHA-256:
3f462bcce6370157050f07d362bba576d19e790283094d7cefcb304bc9b933f3
```

Der Download wurde anhand der tatsächlichen Dateistruktur geprüft, nicht allein anhand der Endung. Das Paket beginnt mit `RKFW`; bei Byte 283.060 folgt `RKAF`. Der eingebettete Loader benennt `rv1126_ddr` und `rv1126_usbplug`. Die Partitionsbeschreibung nennt `RV1126`, GPT und NAND. `rootfs`, `oem` und `userdata` sind UBI-Abbilder. Das passt zu einem eingebetteten Linux-System.

| Bestandteil | Extrahierte Größe | Relevanz |
|---|---:|---|
| `uboot` | 4.194.304 B | Bootloader, für einen Bildaustausch möglichst unberührt lassen. |
| `boot` | 7.606.272 B | FIT-Container mit Kernel und Ressourcen. |
| `recovery` | 15.474.176 B | FIT-Container einschließlich Recovery-Ramdisk. |
| `rootfs` | 60.030.976 B | UBI-Dateisystem. |
| `logo` | 48.180 B | **Direkte BMP-Datei**, kein ext4-Dateisystem und kein Android-Bootanimations-ZIP. |

Für `logo` lautet der Eintrag in dieser Referenz `0x00002000@0x0003BC00(logo)`: 8192 Sektoren zu 512 Bytes, also **4.194.304 Bytes Kapazität**. Der Startsektor ist ausschließlich eine Eigenschaft dieser Referenz. Er ist ausdrücklich kein H13-Flashparameter.

Der BMP-Header meldet **720 × 112, 8 Bit, RLE8-Kompression**, DIB-Header mit 124 Bytes. Die dekodierte Ansicht zeigt einen „Welcome“-Schriftzug. SHA-256 der extrahierten Datei:

`711d014fa3048b48b1c9645ccfc4d0286354f60572b118d44e1de8c3e3c17717`

Das beweist zugleich, dass man aus dem Format eines neueren Originalbildes nicht blind die Vorgaben für ein älteres H13 ableiten darf. Für das H10-Verfahren ist die berichtete 24-Bit-Variante der bessere Ausgangspunkt; die H13-Datei muss dennoch zuerst geprüft werden.

Weitere technische Befunde:

- Die Recovery-Ramdisk wurde als gzip-komprimiertes CPIO extrahiert, ohne ihre Programme auszuführen.
- Darin liegen ARM-Programme `recovery`, `updateEngine`, `update` und auch `adbd`. Ein enthaltenes `adbd` beweist keinen aktivierten oder erreichbaren ADB-Zugang auf einem H13.
- `recovery` enthält Referenzen auf `sd_boot_config.config`, `fw_update`, `sdupdate.img` und `sh /mnt/sdcard/cmd4recovery`.
- `updateEngine` enthält ebenfalls den Pfad `cmd4recovery` sowie Partitionsnamen einschließlich `logo` und Schreibpfade unter `/dev/block/by-name/`.
- Daraus ergibt sich ein **Ansatz zur Prüfung eines Updates nur der Logo-Partition**. Zeichenketten allein beweisen weder die Ausführungsbedingungen noch die sichere Unterstützung eines solchen Updates auf R13. Ein modifiziertes Recovery-Skript wurde deshalb nicht angeboten.
- Die FIT-Strukturen enthalten Signatur-Konfigurationen. Daraus lässt sich ohne weitere Analyse keine Aussage über erzwungenes Secure Boot oder die Akzeptanz neu gepackter Images ableiten.

Die [Rockchip-Headerdefinition](https://github.com/rockchip-linux/rkdeveloptool/blob/master/RKImage.h) wurde zum Abgleich des äußeren Containers herangezogen. Das beigefügte Skript `inspect_firmware.py` liest RKFW/RKAF, extrahiert optional Einzeldateien, protokolliert SHA-256 und erkennt BMP-Header. Es schreibt weder auf USB-Geräte noch auf Flashspeicher und packt keine Firmware neu. Es prüft **keine** Signaturen, Containerprüfsummen oder Gerätekompatibilität.

Reproduktion:

```bash
python inspect_firmware.py ORIGINAL.img > analyse.json
python inspect_firmware.py ORIGINAL.img --extract neues-verzeichnis
python inspect_firmware.py --bmp neues-verzeichnis/logo
```

`reference-analysis.json` enthält das mit dem echten Referenzdownload erzeugte Ergebnis. Das Skript wurde gegen dieses Paket ausgeführt; eine Ausführung gegen dein R13-Paket steht aus.

## Das SD-Werkzeug und der R13-Hinweis

Das heruntergeladene `SDDiskTool_v1.73.zip` enthält `SD_Firmware_Tool.exe`, `SDBoot.bin`, Konfiguration und alte Laufprotokolle. Die EXE wurde nicht ausgeführt.

In `Log/AppLog2024-01-23.txt` steht ein fehlgeschlagener Öffnungsversuch für:

`update_R13.10.03.22_1.1.90.0_V2.00.3f.debug_20240123.1531.img`

Das verbindet den R13-Namenszweig mit dieser Werkzeugfamilie. Es belegt weder, dass jenes Image tatsächlich ein H13 unterstützt, noch einen erfolgreichen Flash. Der relevante Ausschnitt liegt in `sources/tool-log-R13-excerpt.txt`.

Die begleitende H70-Anleitung verwendet den Modus **Upgrade Firmware**; „SD Boot“ und „PCBA Test“ sollen dort nicht gewählt werden. Sie empfiehlt eine 32-GB-Karte. Auch hier gilt: Die mit dem exakten H13-Paket gelieferten Anweisungen haben Vorrang. Werkzeugmodus und Version können beeinflussen, wie die Updatekarte aufgebaut wird.

## Bewertung der Alternativen

| Weg | Einschätzung für dieses Ziel |
|---|---|
| Verkäufer liefert passendes Logo-only-Paket | Beste Option, sofern eindeutig für den vollständigen Build und die Hardware bestätigt; Original zur Rückkehr mit anfordern. |
| Passende Rockchip-Updatekarte, separate Logo-Datei tauschen | Durch H10-Erfolg und eigene Referenzanalyse gut begründet; konkrete R13-Karte noch zu prüfen. Ein Vollflash kann dabei weitere Partitionen überschreiben. |
| Firmware entpacken, Logo ersetzen, neu packen | Technisch untersuchbar, aber erst erforderlich, wenn der direkte Dateiaustausch nicht funktioniert; Längen, Prüfsummen und mögliche Signaturprüfung beachten. |
| Vorhandener ADB-/UART-Zugang, Logo-Partition gezielt schreiben | Möglicher Fallback nach Identifikation und Backup. Keine bestätigte H13-Shell, kein bestätigtes Pinout oder Spannungsniveau gefunden. |
| RockUSB-/Loader-/Maskrom-Zugang | Für Backup oder Recovery relevant. Korrekte DDR-/Flash-Initialisierung und die unterstützte Speicherschnittstelle sind Voraussetzung. Kein bestätigter H13-Testpunkt gefunden. |
| Flashchip extern auslesen | Letzter Weg. Chip identifizieren; bei SPI-NAND sind ECC, OOB und Bad-Block-Behandlung relevant. Ein einfacher NOR-Programmer-Workflow ist nicht automatisch geeignet. |

Bei bestätigtem RockUSB-Loader sind `rkdeveloptool ld` und `rkdeveloptool rfi` erste lesende Identifikationsschritte. Kein `ef`, kein fremder Loader, kein pauschaler Schreibbefehl und keine übernommenen Sektoradressen aus diesem Bericht. Ein logischer Flash-Dump und ein physischer NAND-Dump sind nicht dasselbe.

Wenn Shellzugang vorhanden ist, liefern `cat /proc/mtd`, `cat /proc/partitions` und `ls -l /dev/block/by-name` zunächst Informationen über die tatsächliche Speicheraufteilung. Erst daraus und aus dem passenden Update-Code lässt sich ein korrekter Schreibweg ableiten. Besonders herstellerspezifische Speicherbereiche, Seriennummern und Aktivierungsdaten müssen erhalten bleiben.

Android-`bootanimation.zip`, Allwinner-FEL-Verfahren, UNISOC-PAC-Dateien neuerer Imagebon-Android-Geräte und generische Factory-Codes sind kein belegter Weg für dieses H13. Beispiele auf [Allwinner F133](https://github.com/dan-os/B5300-reverse-engineering) oder [Imagebon W60N/UNISOC](https://www.hovatek.com/forum/thread-49095.html) gehören zu anderen Plattformen. Auch verbreitete `boot_logo.jpg`-Rezepte wurden nicht als H13-Anleitung übernommen.

## Konkrete Anfrage an den Verkäufer

Am besten im ursprünglichen AliExpress-Bestellchat senden; alternativ ist `Imagebons@outlook.com` in einem [reproduzierten Imagebon-Handbuch](https://manuals.plus/imagebon/9-3-inch-portable-car-stereo-with-adjustable-4k-dash-cam-manual) dokumentiert. Die aktuelle Erreichbarkeit wurde nicht überprüft. Es wurde keine Nachricht versendet.

```text
Hello, I own an Imagebon H13 Pro and want to replace only the startup logo.
My full current firmware version is:
R13.10.01.22_1.1.1026.0_2.77.3f_20231013.1841..

Please provide the original recovery firmware compatible with my exact unit,
the matching Rockchip SD upgrade tool and instructions, and preferably a
logo-only update method/package.

Does this version accept a 24-bit BMP named "logo" without an extension on
the prepared upgrade SD card? What dimensions and maximum file size apply?
Does the procedure update only the logo or rewrite the entire firmware?
How can I restore the original logo if the new image is not displayed?

Please confirm compatibility with my hardware revision before providing any
newer firmware. I can provide my order number and a photo of the version page.
```

Für die nächste Untersuchung werden die unveränderte ZIP-/IMG-Datei oder der Downloadlink sowie die konkrete Gerätevariante benötigt. Damit können Logoformat, Partitionierung, SD-Recovery und eine möglichst kleine Änderung gezielt geprüft werden. Bis dahin ist die Aussage „belegter Weg auf verwandtem Imagebon-Gerät, technisch bestätigt an Referenzfirmware“ belastbar; „für diesen H13-Build erfolgreich getestet“ wäre es nicht.
