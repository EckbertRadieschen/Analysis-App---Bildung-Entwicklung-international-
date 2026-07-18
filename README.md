# Projekt Abhängigkeit der CO2-Emission der G20 - Staaten vom Bildungssystem der jeweiligen Länder

## Die G20 ...
- repräsentierten im Jahr 2024 fast 79 % der Weltbevölkerung 
- erwirtschafteten mehr als 85 % der weltweiten Wirtschaftsleistung
- waren dabei für nahezu 83 % aller CO2-Emissionen verantwortlich

## Zielfrage:
Besteht ein Zusammenhang zwischen:
    - den erhobenen Kompetenzen von SchülerInnen 
    - der Entwicklung ihres Landes nach einem Versatz von einer bestimmten Zeitperiode (10, 15, 20 Jahre)

- Analyse der Umweltdaten der Länder
- Analyse der Bildungsdaten der Länder 


## Daten:
- data/raw/EdStatsData.csv
- Datenquelle: https://datacatalog.worldbank.org/ (Stand: Mittwoch, 15.07.2026 - 14:45)

- Struktur: 886.930 Einträge auf (69+1) Spalten (1 Dummy-Spalte)
- Spalten: 
    - Country Name, Country Code, Indicator Name, Indicator Code
    - Jahre: 1970 - 2017 (2020 - 2100 in 5er Schritten vorangelegt)

    - Country Name und - Code: 242 verschiedene Länder (vereinzelt zusammengefasst oder Länderregionen)
    - Indicator Name und - Code: 3665 verschiedene Indikatoren (oft mit vielen Unter-Indikatoren)
        - Bildungsindikatoren (z.B. PISA, TIMSS, Bildungsinvestionen, Schulabbrecherquote, usw)
        - Entwicklungsvariablen des jeweiligen Landes (z.B. BIP, Arbeitslosenquote, usw)
    - Jahresspalten: Messen die jeweiligen Werte bzgl Land und Indikator

### Datenvorbereitungen
- die Daten liegen im Wide-Format vor
- es wird eine Liste mit analyse-relevanten Bildungsindikatoren und Entwicklungsvariablen erstellt
- es werden aus der Datenstruktur zwei neue Daten-Strukturen erzeugt
    - die Daten werden nach Bildungsindikatoren und Entwicklungsvariablen aufgetrennt
    - es werden Jahresspalten entfernt, die keinen Inhalt haben
    - es werden nur tatsächliche Länder angezeigt, keine gruppierten Regionen
    - es werden 

### Neue Datenstruktur
- data/processed/education_indicators.csv
    - 6029 Einträge auf 51 Spalten
    - 209 Länder, 46 Indikatoren

- data/processed/development_indicators.csv
    - 4974 Einträge auf 69 Spalten
    - 214 Länder, 26 Indikatoren

### Datenqualität
- nicht für jedes Land werden Werte für jeden Indikator in jedem Jahr erhoben
    - es kann über die Vollständigkeit der Daten deshalb keine Aussage getroffen werden
- die Länder- und Indikator-Spalten sind einheitlich und fehlerfrei (es liegen keine fehlenden Werte vor)
- es existieren keine Duplikate

## Tool:
Entwicklung einer Streamlit-App zur spezifischen Analyse:

User-Eingabe-Daten:
- Bildungs-Indikator (z.B. TIMSS, PISA, usw.)
- Entwicklungs-Variable des Landes (z.B. BIP, Arbeitslosenquote, usw.)
- Zeitversatz (SchülerInnen-Bildung macht sich erst nach 10-20 Jahren im Land bemerkbar)

Speicherung:
- Einstellungskombinationen, die eine erhöhte Korrelation liefern, werden in einer Datei abgelegt.

Ausgabe:
- Visualisierung der Top-/Bottom-Länder nach Bildungs-Indikator
- Visualisierung der Top-/Bottom-Länder nach Entwicklungs-Variable
- Visualisierung der Abhängigkeit zwischen Bildungs-Indikator und Entwicklungs-Variable länderübergreifend
- Visualisierung des Zusammenhangs von Bildung und Länderentwicklung aus den gespeicherten Daten

## Das Programm

- erzeugt mit Hilfe von klar definierten Funktionen die benötigen pandas-DataFrames
- filtert diese anhand der vom User ausgewählten Variablen-Einstellungen
- erzeugt im Hintergrund die nötigen plotly-Charts
- implementiert die plotly-Charts als Visualisierungen in die Streamlit-App

