# B1: Drohnennetzwerk einlesen


import os
import glob


def find_json_files():
    # Findet alle JSON-Dateien im aktuellen Verzeichnis
    return sorted(glob.glob('*.json'))


def select_json_file():
    # JSON-Dateien finden
    json_files = find_json_files()
    
    # falls keine Dateien gefunden wurden
    if not json_files:
        print("Keine JSON-Dateien gefunden!")
        return ""
    
    print("\nVerfügbare Dateien:")
    print("="*50)
    
    # Dateien mit Index und Größe auflisten
    for i, filename in enumerate(json_files, 1):
        size = os.path.getsize(filename)
        # wenn Größe < 1024 B, in B anzeigen, sonst in KB mit 1 Nachkommastelle
        size_str = f"{size} B" if size < 1024 else f"{size/1024:.1f} KB"
        # Dateinamen kürzen auf 30 Zeichen
        print(f"  [{i}] {filename:<30} ({size_str})")
    
    print(f"  [0] Abbrechen")
    print("="*50)
    

    # manuelle Dateiauswahl
    while True:
        try:
            choice = int(input("\nDatei wählen: ").strip())
            
            if choice == 0:
                return ""
            
            if 1 <= choice <= len(json_files):
                return json_files[choice - 1]
            else:
                print(f"Bitte Zahl zwischen 0 und {len(json_files)} eingeben!")
                
        except ValueError:
            print("Bitte gültige Zahl eingeben!")


"""
Beispiel Eingabe:
find_json_files()
Beispiel Ausgabe:
['drone_testdata_1.json', 'drone_testdata_2.json']

Beispiel Eingabe:
select_json_file()
Beispiel Ausgabe:
'drone_testdata_1.json'
"""