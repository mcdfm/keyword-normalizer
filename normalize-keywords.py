import pandas as pd
import re
import sys

def normalize_keyword(keyword):
    """
    Normalisiert einen Keyword-String, indem Bindestriche entfernt,
    Kleinbuchstaben verwendet, Leerzeichen entfernt, Singular/Plural normalisiert 
    und Wörter alphabetisch sortiert werden.
    """
    # Sicherstellen, dass das Keyword ein String ist
    if not isinstance(keyword, str):
        return ""
    
    # 1. In Kleinbuchstaben umwandeln
    keyword = keyword.lower()
    
    # 2. Punkte und andere Satzzeichen entfernen
    keyword = keyword.replace('.', '').replace(',', '').replace('!', '').replace('?', '').replace(':', '').replace(';', '')
    
    # 3. Bindestriche durch Leerzeichen ersetzen
    keyword = keyword.replace('-', ' ')
    
    # 4. Mehrere Leerzeichen durch ein einzelnes Leerzeichen ersetzen
    keyword = re.sub(' +', ' ', keyword).strip()
    
    # 5. Wörter in einer Liste aufteilen
    words = keyword.split(' ')
    
    # 6. Leerzeichen in der Mitte entfernen (für Zusammenschreibungen)
    normalized_words = []
    for word in words:
        # Leerzeichen entfernen für Zusammenschreibungen
        # "auto flotte" -> "autoflotte"
        word = word.replace(' ', '')
        normalized_words.append(word)
    
    # 7. Singular/Plural normalisieren
    final_words = []
    for word in normalized_words:
        # Deutsche Plural-Regeln
        if word.endswith('en'):
            # "autos" -> "auto", "versicherungen" -> "versicherung"
            singular = word[:-2]
            if len(singular) > 2:  # Mindestens 3 Buchstaben
                final_words.append(singular)
            else:
                final_words.append(word)
        elif word.endswith('er'):
            # "kinder" -> "kind", "häuser" -> "haus"
            singular = word[:-2]
            if len(singular) > 2:
                final_words.append(singular)
            else:
                final_words.append(word)
        elif word.endswith('e'):
            # "tage" -> "tag", "jahre" -> "jahr"
            singular = word[:-1]
            if len(singular) > 2:
                final_words.append(singular)
            else:
                final_words.append(word)
        elif word.endswith('s'):
            # "autos" -> "auto", "hotels" -> "hotel"
            singular = word[:-1]
            if len(singular) > 2:
                final_words.append(singular)
            else:
                final_words.append(word)
        else:
            final_words.append(word)
    
    # 7. Wörter alphabetisch sortieren
    final_words.sort()
    
    # 9. Wörter wieder zu einem String zusammenfügen
    return ' '.join(final_words)

def display_duplicate_groups(df, keyword_column_name='Keyword'):
    """
    Zeigt Near-Duplicates gruppiert an, um die manuelle Überprüfung zu erleichtern.
    """
    # Nur Zeilen mit Duplikaten filtern
    duplicates_df = df[df['Is_Near_Duplicate'] == True].copy()
    
    if len(duplicates_df) == 0:
        print("Keine Near-Duplicates gefunden!")
        return
    
    # Gruppiere nach normalisierten Keywords
    grouped = duplicates_df.groupby('Normalized_Keyword')
    
    print(f"\n=== NEAR-DUPLICATE GRUPPEN ({len(grouped)} Gruppen) ===")
    print("=" * 80)
    
    for i, (normalized_keyword, group) in enumerate(grouped, 1):
        print(f"\n📋 GRUPPE {i}: '{normalized_keyword}'")
        print("-" * 60)
        
        for idx, row in group.iterrows():
            original_keyword = row[keyword_column_name]
            print(f"  • {original_keyword}")
        
        print(f"  → {len(group)} Varianten gefunden")
    
    print(f"\n💡 TIPP: Du kannst jetzt für jede Gruppe entscheiden, welche Variante du behalten möchtest.")
    print(f"   Die anderen Varianten kannst du dann aus der Excel-Datei entfernen.")

def process_keywords(excel_file_path, worksheet_name=None, keyword_column_name='Keyword'):
    """
    Verarbeitet Keywords aus einer Excel-Datei.
    
    Args:
        excel_file_path (str): Pfad zur Excel-Datei
        worksheet_name (str): Name des Worksheets (optional, verwendet das erste Sheet wenn None)
        keyword_column_name (str): Name der Spalte mit den Keywords
    """
    try:
        # Debug: Pfad ausgeben
        print(f"Versuche Datei zu laden: '{excel_file_path}'")
        
        # Excel-Datei laden
        if worksheet_name:
            df = pd.read_excel(excel_file_path, sheet_name=worksheet_name)
        else:
            df = pd.read_excel(excel_file_path)
        
        print(f"Excel-Datei erfolgreich geladen: {excel_file_path}")
        if worksheet_name:
            print(f"Worksheet: {worksheet_name}")
        else:
            print("Verwende erstes Worksheet")
        
        # Verfügbare Spalten anzeigen
        print(f"Verfügbare Spalten: {list(df.columns)}")
        
        # Prüfen ob die Keyword-Spalte existiert
        if keyword_column_name not in df.columns:
            print(f"Fehler: Spalte '{keyword_column_name}' nicht gefunden!")
            print("Verfügbare Spalten:")
            for i, col in enumerate(df.columns):
                print(f"  {i+1}. {col}")
            return
        
        print(f"Verwende Spalte: {keyword_column_name}")
        print(f"Anzahl Zeilen: {len(df)}")
        
        # Eine neue Spalte mit den normalisierten Keywords erstellen
        df['Normalized_Keyword'] = df[keyword_column_name].apply(normalize_keyword)
        
        # Die Near-Duplicates identifizieren
        # Wir zählen die Häufigkeit der normalisierten Keywords
        duplicate_counts = df['Normalized_Keyword'].value_counts()
        
        # Eine neue Spalte 'Duplicate_Group' erstellen, die den kanonischen Begriff zeigt
        # Wenn es ein Duplikat ist, zeige das normalisierte Keyword, sonst leer
        df['Duplicate_Group'] = ''
        df.loc[df['Normalized_Keyword'].map(duplicate_counts) > 1, 'Duplicate_Group'] = df['Normalized_Keyword']
        
        # Anzahl der Duplicates anzeigen
        duplicate_count = (df['Duplicate_Group'] != '').sum()
        print(f"Gefundene Near-Duplicates: {duplicate_count}")
        
        # Das Ergebnis in eine neue Excel-Datei speichern
        if excel_file_path.endswith('.xlsx'):
            output_file_path = excel_file_path.replace('.xlsx', '_normalized.xlsx')
        elif excel_file_path.endswith('.xls'):
            output_file_path = excel_file_path.replace('.xls', '_normalized.xlsx')
        else:
            output_file_path = excel_file_path + '_normalized.xlsx'
        
        print(f"Speichere Ergebnis in: {output_file_path}")
        df.to_excel(output_file_path, index=False, engine='openpyxl')
        
        print(f"Die Near-Duplicates wurden identifiziert und in der Datei '{output_file_path}' gespeichert.")
        print("\nDie ersten 5 Zeilen mit den neuen Spalten:")
        print(df[[keyword_column_name, 'Normalized_Keyword', 'Duplicate_Group']].head())
        
        return df
        
    except FileNotFoundError:
        print(f"Fehler: Datei '{excel_file_path}' nicht gefunden!")
    except Exception as e:
        print(f"Fehler beim Verarbeiten der Datei: {e}")

def main():
    """
    Hauptfunktion mit Benutzerinteraktion
    """
    print("=== Keyword Normalizer ===")
    
    # Excel-Datei abfragen
    print("Tippe den Pfad ein oder ziehe die Datei aus dem Finder hierher:")
    excel_file_path = input("Pfad zur Excel-Datei eingeben: ")
    # Entferne nur Anführungszeichen am Anfang und Ende, aber nicht Leerzeichen in der Mitte
    excel_file_path = excel_file_path.strip('"').strip("'")
    print(f"Eingegebener Pfad: '{excel_file_path}'")
    
    # Worksheet abfragen
    worksheet_name = input("Worksheet-Name (Enter für erstes Sheet): ").strip()
    if not worksheet_name:
        worksheet_name = None
    
    # Keyword-Spalte abfragen
    keyword_column_name = input("Name der Keyword-Spalte (Standard: 'Keyword'): ").strip()
    if not keyword_column_name:
        keyword_column_name = 'Keyword'
    
    # Verarbeitung starten
    process_keywords(excel_file_path, worksheet_name, keyword_column_name)

if __name__ == "__main__":
    # Wenn Kommandozeilenargumente übergeben werden
    if len(sys.argv) > 1:
        excel_file_path = sys.argv[1]
        worksheet_name = sys.argv[2] if len(sys.argv) > 2 else None
        keyword_column_name = sys.argv[3] if len(sys.argv) > 3 else 'Keyword'
        process_keywords(excel_file_path, worksheet_name, keyword_column_name)
    else:
        # Interaktiver Modus
        main()