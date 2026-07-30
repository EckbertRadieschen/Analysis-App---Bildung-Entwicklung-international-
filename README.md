# 📊 Bildung und Entwicklung
> **Interaktive Analyse globaler Zusammenhänge zwischen Bildungs- und Entwicklungsindikatoren**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Inhaltsverzeichnis

- Projektübersicht
- Motivation
- Features
- Datenquellen
- Technologien
- Projektstruktur
- Analyseablauf
- Screenshots
- Installation
- Hinweise
- Autor

---

# Projektübersicht

Dieses Projekt analysiert statistische Zusammenhänge zwischen Bildungsindikatoren und Entwicklungsindikatoren verschiedener Länder auf Basis von Datensätzen der World Bank.

Mithilfe einer interaktiven Streamlit-Anwendung können berechnete Korrelationen gefiltert, visualisiert und statistisch ausgewertet werden.

## Motivation

Bildung beeinflusst viele Bereiche gesellschaftlicher Entwicklung. Ziel des Projekts ist es, mögliche Zusammenhänge zwischen Bildung und Bereichen wie Wirtschaft, Gesundheit, Innovation, Umwelt oder Governance sichtbar zu machen.

**Hinweis:** Korrelation bedeutet keine Kausalität.

## Features

- 📈 Interaktive Streamlit-Oberfläche
- 🌍 Analyse internationaler Daten
- 📊 Pearson- und Spearman-Korrelationen
- ⏳ Analyse verschiedener Zeitverzögerungen (Lag)
- 🗂️ Auswertung nach Bildungs- und Entwicklungskategorien
- 📉 Statistische Übersichten und Diagramme

## Datenquellen

Alle verwendeten Daten stammen aus dem World Bank Data Catalog.

- Länderinformationen
- Bildungsindikatoren
- Entwicklungsindikatoren

## Technologien

- Python
- Pandas
- NumPy
- Plotly
- Streamlit

## Projektstruktur

```text
.
├── app/
│   ├── app.py                          (Kern der Streamlit-Anwendung)
│   └── ...
├── config/                             (Konfiguration der...)
│   ├── development_indicators.json     (Entwicklungsindikatoren)    
│   └── education_indicators.json       (Bildungsindikatoren)
├── data/
│   ├── raw/                            (enthält die originalen csv-Dateien der World Bank)
│   └── processed/                      (enthält die für die Analyse verwendeten, aufbereiteten Versionen der raw-Dateien)
├── notebooks/
├── src/
│   ├── all_calcs.py                    (Programm, das aus den processed-csv-Dateien und Config die corrleation_results.json erzeugt)
│   ├── analysis.py                     (alle für die Analyse relevanten Funktionen)
│   ├── visuals.py                      (alle für die plotly.Figures relevanten Funktionen)
│   ├── paths.py                        (enthält die pathlib-Pfade des Projekts)
│   └── preparations.py                 (Programm, dass raw -> processed überführt)
├── utils/
│   └── hilfsfunktionen.py              (kleinere im Projekt verwendete Hilfsfunktionen)
├── correlation_results.json            (Ergebnisse der umfassenden Korrelationsanalyse aller Indikatorkombinationen)
├── requirements.txt
└── README.md
```

## Analyseablauf

1. Daten importieren
2. Daten bereinigen
3. Länder filtern
4. Kategorien zuordnen
5. Zeitverzögerungen berücksichtigen
6. Pearson- und Spearman-Korrelation berechnen
7. Ergebnisse speichern
8. Interaktive Analyse


## Installation

```bash
git clone https://github.com/EckbertRadieschen/Analysis-App---Bildung-Entwicklung-international-.git bildungsanalyse
cd bildungsanalyse
pip install -r requirements.txt
streamlit run app.py
```

## Geplante Erweiterungen

- Weitere Visualisierungen
- Exportfunktionen
- Zusätzliche statistische Verfahren
- Verbesserte Filtermöglichkeiten

## Autor

**Marcel Kramer**

DSP - Data Analysis Bootcamp
