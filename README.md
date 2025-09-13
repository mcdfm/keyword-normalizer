# Keyword Normalizer

Ein Python-Tool zur Erkennung und Gruppierung von Near-Duplicate Keywords in Excel-Dateien.

## 🎯 Features

- **Automatische Near-Duplicate-Erkennung** in Keyword-Listen
- **Leerzeichen-Entfernung** für Zusammenschreibungen (versicherung police → versicherungpolice)
- **Satzzeichen-Entfernung** für saubere Keywords (dr. mickeler → dr mickeler)
- **ß-Normalisierung** für deutsche Texte (schrank nach maß → schrank nach mass)
- **Deutsche Plural-Formen-Erkennung** (en, er, e, s)
- **Bindestrich-Normalisierung** (e-mobility → e mobility)
- **Alphabetische Sortierung** der Wörter
- **Excel-Integration** mit flexiblen Worksheet- und Spaltennamen
- **Gruppierte Duplikat-Anzeige** für einfache manuelle Überprüfung

## 🚀 Installation

### Voraussetzungen
- Python 3.7+
- pip

### Setup
```bash
# Repository klonen
git clone https://github.com/yourusername/keyword-normalizer.git
cd keyword-normalizer

# Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# oder: venv\Scripts\activate  # Windows

# Dependencies installieren
pip install pandas openpyxl
```

## 📖 Verwendung

### Interaktiver Modus
```bash
python3 normalize-keywords.py
```

Das Tool fragt dich nach:
1. **Pfad zur Excel-Datei**
2. **Worksheet-Name** (optional, als Standard wird das erste Sheet genommen)
3. **Name der Keyword-Spalte** (Standard: 'Keyword')

### Kommandozeilen-Modus
```bash
python3 normalize-keywords.py "pfad/zur/datei.xlsx" "Sheet1" "Keywords"
```

## 📊 Output

Das Tool erstellt eine neue Excel-Datei mit folgenden Spalten:

- **Original Keyword**: Das ursprüngliche Keyword
- **Normalized_Keyword**: Das normalisierte Keyword (für technische Details)
- **Duplicate_Group**: Der kanonische Begriff (nur bei Duplikaten gefüllt)

### Beispiel Output
```
Keyword              | Normalized_Keyword | Duplicate_Group
versicherung police  | versicherungpolice | versicherungpolice
versicherungpolice   | versicherungpolice | versicherungpolice
e-mobility           | e mobility         | e mobility
e mobility           | e mobility         | e mobility
schrank nach maß     | schrank nach mass  | schrank nach mass
schrank nach mass    | schrank nach mass  | schrank nach mass
versicherungen       | versicherung       | versicherung
versicherung         | versicherung       | versicherung
```

## 🔧 Normalisierungs-Regeln

### 1. Leerzeichen-Entfernung (für Zusammenschreibungen)
- `versicherung police` → `versicherungpolice`
- `schaden meldung` → `schadenmeldung`
- `unfall protokoll` → `unfallprotokoll`

### 2. Satzzeichen-Entfernung
- `dr. mickeler` → `dr mickeler`
- `schaden.meldung!` → `schadenmeldung`
- `unfall,protokoll?` → `unfallprotokoll`

### 3. ß-Normalisierung
- `schrank nach maß` → `schrank nach mass`
- `straße` → `strasse`
- `groß` → `gross`

### 4. Bindestrich-Normalisierung
- `e-mobility` → `e mobility`
- `auto-versicherung` → `auto versicherung`

### 5. Deutsche Plural-Formen
- `autos` → `auto`
- `kinder` → `kind`
- `tage` → `tag`
- `hotels` → `hotel`
- `versicherungen` → `versicherung`

### 6. Alphabetische Sortierung
- `versicherung auto` → `auto versicherung`
- `schweiz auto` → `auto schweiz`

## 📝 Verwendung in Excel

1. **Nach `Duplicate_Group` sortieren** - alle Duplikate sind gruppiert
2. **Gruppen durchgehen** - entscheide welche Variante du behältst
3. **Redundante Keywords entfernen** - lösche die ungewünschten Varianten

## 🤝 Beitragen

Beiträge sind willkommen! Bitte erstelle einen Pull Request oder öffne ein Issue.

### Geplante Features
- [ ] Umlaut-Normalisierung
- [ ] Stop-Wort-Entfernung
- [ ] Abkürzungs-Erkennung
- [ ] Zahlen-Normalisierung

## 📄 Lizenz

MIT License - siehe [LICENSE](LICENSE) Datei für Details.

## 🙏 Danksagung

Entwickelt für SEO-Keyword-Optimierung und Content-Management. 