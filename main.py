#!/usr/bin/env python3
"""
Spotify Album Cover Collage Generator
====================================

Main script that orchestrates the entire workflow:
1. Analyze playlist and extract album information
2. Download album covers from Spotify
3. Create a beautiful collage from the covers

Author: Generated with Claude Code
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header():
    """Print a nice header for the application"""
    print("=" * 60)
    print("🎵 SPOTIFY ALBUM COVER COLLAGE GENERATOR 🎨")
    print("=" * 60)
    print()

def print_step(step_num, title, description):
    """Print a formatted step header"""
    print(f"\n📍 SCHRITT {step_num}: {title}")
    print("-" * 50)
    print(f"   {description}")
    print()

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    try:
        print(f"▶️  Starte {script_name}...")
        
        # Run the script in the same virtual environment
        result = subprocess.run([
            sys.executable, script_name
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"✅ {description} erfolgreich abgeschlossen!")
            if result.stdout:
                print("Ausgabe:")
                print(result.stdout)
        else:
            print(f"❌ Fehler beim Ausführen von {script_name}:")
            if result.stderr:
                print("Fehlermeldung:")
                print(result.stderr)
            if result.stdout:
                print("Ausgabe:")
                print(result.stdout)
            return False
            
    except Exception as e:
        print(f"❌ Unerwarteter Fehler beim Ausführen von {script_name}: {e}")
        return False
    
    return True

def check_dependencies():
    """Check if all required files exist"""
    required_files = [
        "playlist_analyzer.py",
        "cover_downloader.py", 
        "collage_maker.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Fehlende Dateien:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    return True

def check_spotify_token():
    """Check if Spotify token is configured"""
    print("🔑 Überprüfe Spotify-Konfiguration...")
    
    # Check if .env file exists
    if Path(".env").exists():
        print("✅ .env Datei gefunden")
        return True
    
    # Check if token is directly in the files (for backward compatibility)
    try:
        with open("playlist_analyzer.py", "r") as f:
            content = f.read()
            if "token = 'BQA" in content and len(content.split("token = '")[1].split("'")[0]) > 50:
                print("⚠️  Token direkt im Code gefunden (empfohlen: .env verwenden)")
                return True
    except:
        pass
    
    print("❌ Kein gültiger Spotify-Token gefunden!")
    print("   Bitte konfiguriere deinen Spotify-Token:")
    print("   1. Erstelle eine .env Datei")
    print("   2. Füge hinzu: SPOTIFY_TOKEN=dein_token_hier")
    print("   3. Oder bearbeite playlist_analyzer.py direkt")
    return False

def main():
    """Main function that runs the complete workflow"""
    print_header()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Abhängigkeiten nicht erfüllt. Beende Programm.")
        sys.exit(1)
    
    # Check Spotify configuration
    if not check_spotify_token():
        print("\n⚠️  Warnung: Spotify-Token nicht konfiguriert.")
        print("   Das Programm wird möglicherweise fehlschlagen.")
        
        response = input("\nTrotzdem fortfahren? (j/n): ").lower().strip()
        if response not in ['j', 'ja', 'y', 'yes']:
            print("Programm beendet.")
            sys.exit(1)
    
    print("\n🚀 Starte Workflow...")
    
    # Step 1: Analyze playlist and extract albums
    print_step(1, "PLAYLIST ANALYSE", 
               "Analysiere Spotify-Playlist und extrahiere Album-Informationen")
    
    if not run_script("playlist_analyzer.py", "Playlist-Analyse"):
        print("\n❌ Workflow abgebrochen.")
        sys.exit(1)
    
    # Check if musik.txt was created
    if not Path("musik.txt").exists():
        print("\n❌ musik.txt wurde nicht erstellt. Workflow abgebrochen.")
        sys.exit(1)
    
    # Step 2: Download album covers
    print_step(2, "COVER DOWNLOAD", 
               "Lade Album-Cover von Spotify herunter")
    
    if not run_script("cover_downloader.py", "Cover-Download"):
        print("\n❌ Workflow abgebrochen.")
        sys.exit(1)
    
    # Check if photos directory has files
    photos_dir = Path("photos")
    if not photos_dir.exists() or not any(photos_dir.glob("*.jpg")):
        print("\n❌ Keine Album-Cover heruntergeladen. Workflow abgebrochen.")
        sys.exit(1)
    
    # Step 3: Create collage
    print_step(3, "COLLAGE ERSTELLEN", 
               "Erstelle eine künstlerische Collage aus allen Album-Covern")
    
    if not run_script("collage_maker.py", "Collage-Erstellung"):
        print("\n❌ Workflow abgebrochen.")
        sys.exit(1)
    
    # Success!
    print("\n" + "=" * 60)
    print("🎉 WORKFLOW ERFOLGREICH ABGESCHLOSSEN! 🎉")
    print("=" * 60)
    
    # Show results
    if Path("album_collage.jpg").exists():
        print("✅ Collage erstellt: album_collage.jpg")
    
    if Path("musik.txt").exists():
        # Count albums in musik.txt
        with open("musik.txt", "r") as f:
            lines = f.readlines()
            album_count = len([line for line in lines if line.strip().startswith("- ")])
        print(f"✅ Album-Liste: musik.txt ({album_count} Alben)")
    
    if photos_dir.exists():
        cover_count = len(list(photos_dir.glob("*.jpg")))
        print(f"✅ Album-Cover: photos/ ({cover_count} Bilder)")
    
    print("\n📂 Alle Dateien befinden sich im aktuellen Verzeichnis.")
    print("🖼️  Öffne 'album_collage.jpg' um deine Collage zu sehen!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programm wurde unterbrochen.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unerwarteter Fehler: {e}")
        sys.exit(1)