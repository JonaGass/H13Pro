# Zusätzliche Quellen und Abgrenzungen, 15.11.2026

## Primärmaterial und tatsächlich geprüfte Referenzen

- Eigene Analyse der bereits gehashten H70-R33-Referenz-App: `pcba-complete.txt`, `pcba-side-effects.txt`, `http-file-handlers.txt`; Kontrollflussnachstellung mit echten ARM-Instruktionen: `emulate_sd_path.py`, Ergebnis `sd-path-emulation.json`.
- Öffentliche Imagebon-Freigabe erneut abgerufen: https://drive.google.com/drive/folders/1AYti2WEuObgKGuRzH-U1W1F-JGd6YXVm . Gleiche drei H70-Ordner, keine neue R13-Datei. Lokaler Snapshot `imagebon-drive-current.html`.
- Öffentlicher SDK-Quellcode mit ähnlicher HTTP-Implementierung: https://github.com/lindenis-org/lindenis-v536-softwinner/blob/d5d2c4631c829c403a8a7e7047688b555b2b2a32/eyesee-mpp/awcdr/apps/cdr/source/device_model/httpServer/httpServer.cpp . API-Verwandtschaft, **kein** H13-Quellcode und kein Chipnachweis.
- H10-Besitzerbericht erneut geprüft: https://isulnara.com/archives/2794 . Beschreibt Updatekarte plus BMP-Logo; liefert selbst kein Firmwareimage und keinen getesteten H13-Pfad.
- OBDPEAK-Besitzerbericht grenzt seine TF781-/TF790-Anleitung ausdrücklich gegen Imagebon ab: https://studytilldeath.tistory.com/102 . Diese Images nicht für H13 verwenden.

## Interessante, aber nicht übertragbare Spuren

- https://github.com/fuho/moto-display-re/blob/main/WRITEUP.md und https://github.com/fuho/moto-display-re/blob/main/research/motonavi_apk/findings.md : Besitzeranalyse eines **anderen** Motorrad-Displays (M553, Allwinner-F133/Melis). Hinweise auf Roadcam/MotoNavi-OTA-Dienste und App-Protokolle sind nützlich als Suchspuren, kein validierter H13-OTA-Abruf. Der App-Dienst braucht tatsächliche Gerätekennungen. Keine Behauptung, dass eine erfundene `deviceInfo`-Zeichenkette eine passende H13-Firmware liefert. Keine dieser Plattform-Kommandonummern ungeprüft an das H13 senden.
- https://github.com/catplay-labs/catplay : alternative CarPlay-Implementierung für Dongles mit unterschiedlichen SoCs, keine H13-Unterstützung aus dem geprüften README.
- https://www.hovatek.com/forum/thread-49095.html : Imagebon W60N auf UNISOC/Android; andere Speicher-/Bootarchitektur.
- https://github.com/geo-chen/RoadCam : Roadcam-X3-Sicherheitsforschung. Der Markenname einer Kamera ist nicht gleichbedeutend mit jeder von der RoadCam-App unterstützten Hardware. Keine dortigen Default-Passwörter als H13-Zugang behaupten.
- https://fccid.io/2BBHX-1026/Internal-Photos/Internal-Photos-6608595 und https://device.report/m/b950e9fe00ed17f646a6fa3387df46f45f650a686e7d21b68c1e0eaad9819c84 : öffentlich gelistete Innenfotos eines `1026`-Geräts von Shenzhen Yuejia. Ein Zusammenhang mit dem konkreten H13 ist **nicht** nachgewiesen; kein H13-Pinout daraus ableiten. Die Webansicht erkennt ein sechsseitiges Bild-PDF; direkter Shell-Download wurde mit HTTP 403 abgewiesen. Keine belastbare Platinen-/Pinbestimmung vorgenommen.

## Suchgrenzen

Exakte Kennungen und relevante Varianten waren unter anderem `R13.10.01.22`, `R13.10.03.22`, `R13.10.01.22_1.1.1026.0_2.77.3f`, `R13.10.03.22_1.1.90.0`, `R8-V2.0`, `qckj`, `Imagebon H13 Pro firmware`, `Imagebon H13 펌웨어`, `Imagebon H13 прошивка`, `Imagebon H10 H13 固件 下载`, `H13 カープレイ ファームウェア` sowie Suchbegriffe mit Download-/Drive-/GitHub-/Forum-Bezug.

Suchtreffer enthielten viele automatisch erzeugte Handbücher, andere Imagebon-SoCs, Staubsauger/Tablets gleichen Modellnamens und bei R13-Kurzkennungen völlig sachfremde Inhalte. Sie wurden nicht als Firmwarefund gewertet. Ein Fehlen verwertbarer Treffer belegt nicht, dass die Datei nirgends existiert. Es wurde kein Verkäufer, Autor oder Dritter angeschrieben.
