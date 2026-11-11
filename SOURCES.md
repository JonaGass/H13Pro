# Quellen und Downloadherkunft

Recherche-/Downloadstand: 11.11.2026. Firmware nur als Referenz; keine H13-Kompatibilitätsfreigabe.

## Entscheidende Quellen

- Eigener H10-Pro-Erfolgsbericht vom 19.08.2023: https://isulnara.com/archives/2794
  - Gespeichert: `sources/isulnara-2794.html`
  - Original-Screenshot: https://isulnara.com/wp-content/uploads/2023/08/h10pro-sd-1.png
  - Gespeichert: `sources/h10pro-sd-1.png`
- Öffentliches Produktangebot, über das die Firmwarefreigabe gefunden wurde: https://hfg3d.com/produto/imagebon-h70-plus-114%E2%80%B2%E2%80%B2-4k-adas-dash-cam-60fps-carro-sem-fio-play-e-android-auto-gravacao-dupla-visao-noturna-dvr/
- Öffentliche Drive-Freigabe: https://drive.google.com/drive/folders/1AYti2WEuObgKGuRzH-U1W1F-JGd6YXVm
  - HTML-Liste: `sources/imagebon-drive.html`
- Unterordner mit tatsächlich untersuchtem H70Pro-Paket: https://drive.google.com/drive/folders/1UpUSbFUOF8zsZCvRLihPBZMB3rE__ISG
  - HTML-Liste: `sources/drive-1UpUSbFUOF8zsZCvRLihPBZMB3rE__ISG.html`

## Originale Drive-Dateien

| Datei | Öffentliche Referenz | Lokale Datei |
|---|---|---|
| `update_R33.10.03.22_1.2.1025.4_V3.08151.50_20250702.1543.img` | https://drive.google.com/file/d/1eo_0rJKW9GaNF7TeRtGfy9nFrwssQvPl/view | `sources/H70-R33-reference-only.img` |
| `SDDiskTool_v1.73.zip` | https://drive.google.com/file/d/17Klu1IpmS5H_qyYctU5Pft94h8VOAltN/view | `sources/SDDiskTool_v1.73.zip` |
| `SD card Upgrade Instruction.docx` | https://drive.google.com/file/d/1efW15UkbNOWGAQb-5CeLH1eW4h95nOqi/view | `sources/H70-SD-instructions.docx` |

Zusätzliche untersuchte Ordnerlisten liegen bei. Der H70K-Ordner enthielt weitere Werkzeuge/Anleitungsvideo; diese wurden nicht als Ziel-Firmware für H13 genutzt. Der Download der R33-Datei wurde zunächst von einer Google-Zwischenseite beantwortet; anschließend wurde die tatsächliche Binärdatei geladen und ihre Struktur geprüft. Die beiliegende IMG ist der bestätigte Binärdownload, keine HTML-Seite. Hashes: `download-hashes.json` und `SHA256SUMS.txt`.

Die Freigabe ist öffentlich verlinkt; Herstellerherkunft und Authentizität wurden nicht kryptografisch verifiziert. Keine enthaltene EXE wurde ausgeführt.

## Technische Primärquellen und Werkzeuge

- Rockchip rkdeveloptool: https://github.com/rockchip-linux/rkdeveloptool
- RKFW-Header: https://github.com/rockchip-linux/rkdeveloptool/blob/master/RKImage.h
- Werkzeugbefehle im Quellcode: https://github.com/rockchip-linux/rkdeveloptool/blob/master/main.cpp
- Rockchip-Recovery-Beispielquelle: https://github.com/rockchip-android/bootable-recovery/blob/rk3399-box-7.1/sdboot.cpp (andere Plattform/Version, kein exakter H13-Quellcode)
- Firefly RV1109/RV1126 USB-/Loader-/Maskrom-Dokumentation: https://wiki.t-firefly.com/en/Core-1109-JD4/upgrade_firmware.html (Entwicklerboard, keine H13-Belegung)
- Offizielle ADB-Downloads: https://developer.android.com/tools/releases/platform-tools
- ubi-reader: https://github.com/onekey-sec/ubi_reader
- Capstone: https://www.capstone-engine.org/
- pyelftools: https://github.com/eliben/pyelftools

`sources/RKImage.h` und `sources/DefineHeader.h` wurden von den Raw-Dateien des Rockchip-rkdeveloptool-Repositories geladen. Die eigentlichen Aussagen über den Imagebon-Code stammen aus eigener statischer Binäranalyse, nicht aus öffentlich zugänglichem Imagebon-Quellcode.

## Handbücher/Plattformabgrenzung

- H13-Originalhandbuch als Konvertierung mit PDF: https://manuals.plus/m/25242b46d2845b4d4c115be1acb5fd0ced5d162dcdac69e2977ca4e6aba1b247
- AliExpress-Artikel-Zusammenstellung: https://manuals.plus/ae/1005005666024981 — Sekundärquelle; teils generierte Inhalte, nicht als Crossflash-Beleg behandeln.
- Imagebon W60N/UNISOC, **andere Plattform**: https://www.hovatek.com/forum/thread-49095.html
- B5300/Allwinner F133, **andere Plattform**: https://github.com/dan-os/B5300-reverse-engineering

Es wurden englische, koreanische, russische, japanische und chinesische Suchbegriffe sowie die vollständige Firmwarekennung und Teilkennungen verwendet. Kein passendes öffentliches H13-R13-Komplettimage wurde gefunden. Es gibt kein gespeichertes vollständiges Suchprotokoll; konkrete verwertete Quellen stehen hier und in den beiden Berichten.
