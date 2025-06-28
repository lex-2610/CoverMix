# 🎵 Spotify Album Cover Collage Generator

Ein Python-Projekt, das automatisch eine künstlerische Collage aus den Album-Covern deiner Spotify-Playlists erstellt.

## ✨ Features

- 🎶 **Playlist-Analyse**: Liest deine Spotify-Playlists und extrahiert Album-Informationen
- 🖼️ **Cover-Download**: Lädt hochaufgelöste Album-Cover direkt von Spotify
- 🎨 **Collage-Erstellung**: Erstellt eine künstlerische Collage mit intelligenter Platzierung
- 📱 **Hochformat-Optimiert**: Perfekt für mobile Hintergründe (9:16 Format)
- 🔄 **Automatischer Workflow**: Ein Befehl führt den gesamten Prozess aus

## 🖼️ Beispiel-Ergebnis

Das Programm erstellt eine vollflächige Collage wie diese:

```
┌─────────────────────────────┐
│  🎵 Album Cover Collage 🎨  │
│                             │
│  [Cover1]    [Cover2]       │
│     [Cover3] [Cover4]       │
│  [Cover5]       [Cover6]    │
│     [Cover7] [Cover8]       │
│  [Cover9]    [Cover10]      │
│                             │
└─────────────────────────────┘
```

## 🚀 Installation

### 1. Repository klonen
```bash
git clone <repository-url>
cd spotify-album-collage
```

### 2. Virtual Environment erstellen
```bash
python3 -m venv .venv
source .venv/bin/activate  # Auf macOS/Linux
# oder
.venv\Scripts\activate     # Auf Windows
```

### 3. Abhängigkeiten installieren
```bash
pip install requests pillow python-dotenv
```

### 4. Spotify-Token konfigurieren

1. Gehe zu [Spotify Web API](https://developer.spotify.com)
2. Bearbeite die `.env` Datei:

```env
SPOTIFY_TOKEN=dein_echter_token_hier
PLAYLIST_NAME=Lieblingssongs
```

## 🎯 Verwendung

### Einfacher Start
```bash
# Virtual Environment aktivieren
source .venv/bin/activate

# Gesamten Workflow ausführen
python main.py
```

### Einzelne Schritte (optional)
```bash
# 1. Playlist analysieren
python playlist_analyzer.py

# 2. Album-Cover herunterladen
python cover_downloader.py

# 3. Collage erstellen
python collage_maker.py
```

## 📁 Projektstruktur

```
spotify-album-collage/
├── main.py                 # Hauptskript (orchestriert alles)
├── playlist_analyzer.py    # Analysiert Spotify-Playlists
├── cover_downloader.py     # Lädt Album-Cover herunter
├── collage_maker.py        # Erstellt die Collage
├── .env                    # Konfigurationsdatei
├── requirements.txt        # Python-Abhängigkeiten
├── README.md              # Diese Datei
├── photos/                # Heruntergeladene Album-Cover
├── musik.txt              # Liste der gefundenen Alben
└── album_collage.jpg      # Finale Collage
```

## ⚙️ Konfiguration

Alle Einstellungen können in der `.env` Datei angepasst werden:

```env
# Spotify-Konfiguration
SPOTIFY_TOKEN=dein_token_hier
PLAYLIST_NAME=Lieblingssongs

# Collage-Einstellungen
COLLAGE_WIDTH=1080
COLLAGE_HEIGHT=1920
COLLAGE_FORMAT=9:16
```

## 🔧 Funktionsweise

### 1. Playlist-Analyse (`playlist_analyzer.py`)
- Verbindet sich mit der Spotify Web API
- Liest die angegebene Playlist
- Extrahiert Album-Namen und Künstler
- Speichert die Liste in `musik.txt`

### 2. Cover-Download (`cover_downloader.py`)
- Liest die Album-Liste aus `musik.txt`
- Sucht jedes Album in der Spotify-Datenbank
- Lädt die Cover in höchster Auflösung herunter
- Speichert sie im `photos/` Ordner

### 3. Collage-Erstellung (`collage_maker.py`)
- Lädt alle Bilder aus dem `photos/` Ordner
- Berechnet optimale Platzierung mit intelligentem Grid-System
- Fügt künstlerische Überlappung und Rotation hinzu
- Stellt sicher, dass alle Bilder sichtbar bleiben
- Erstellt `album_collage.jpg` im 9:16 Format

## 🎨 Collage-Features

- **Intelligente Platzierung**: Jedes Album-Cover ist sichtbar
- **Organische Verteilung**: Leichte Überlappung und Rotation für natürlichen Look
- **Vollflächige Abdeckung**: Keine Leerräume im finalen Bild
- **Zentren-Schutz**: Die Mitte jedes Covers bleibt erkennbar
- **Multi-Layer-System**: Zusätzliche Schichten für bessere Raumausnutzung

## 🛠️ Technische Details

### Abhängigkeiten
- **requests**: Für Spotify API-Aufrufe
- **Pillow (PIL)**: Für Bildverarbeitung
- **python-dotenv**: Für Umgebungsvariablen

### Unterstützte Formate
- **Input**: Spotify-Playlists, JPG/JPEG Album-Cover
- **Output**: JPEG-Collage in 1080x1920 (9:16)

### Performance
- Verarbeitet 50-100 Album-Cover in unter 2 Minuten
- Automatische Größenanpassung je nach Anzahl der Bilder
- Intelligente Speicherverwaltung

## 🔒 Datenschutz

- Token werden nur lokal in der `.env` Datei gespeichert
- Keine Daten werden an externe Server gesendet
- Album-Cover werden temporär heruntergeladen und können gelöscht werden

## 🐛 Troubleshooting

### Token-Fehler
```
❌ API Error: 401 Unauthorized
```
**Lösung**: Token in `.env` aktualisieren

### Playlist nicht gefunden
```
❌ Playlist 'Name' nicht gefunden!
```
**Lösung**: Playlist-Name in `.env` korrigieren

### Pillow-Installation fehlgeschlagen
```
❌ ModuleNotFoundError: No module named 'PIL'
```
**Lösung**: 
```bash
pip install Pillow
```

### Leere Collage
```
❌ Keine JPG-Dateien im photos Ordner gefunden!
```
**Lösung**: Überprüfe Internet-Verbindung und Token-Berechtigung


## 🙏 Danksagungen

- Spotify Web API für Album-Cover-Zugang
- Pillow-Community für Bildverarbeitung

---


*Generiere deine eigene Musik-Collage und teile sie mit der Welt!* 🎵✨
