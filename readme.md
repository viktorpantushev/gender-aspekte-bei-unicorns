# 🦄 Gender-Aspekte bei Unicorns

Dieses Projekt untersucht, wie häufig Frauen und Männer unter den Gründerinnen und Gründern von Unicorn-Startups vertreten sind. Dazu werden öffentlich verfügbare Daten aus Wikipedia gesammelt, Gründerinnen und Gründer über Namen und zusätzliche Web-Quellen klassifiziert und die Ergebnisse anschließend ausgewertet.

## Ziel

Die Analyse beantwortet die Frage, wie die Geschlechterverteilung bei Unicorn-Gründerinnen und -Gründern aussieht und wie sie sich nach Land, Branche, Sektor oder Bewertung unterscheidet.

## Überblick über den Workflow

1. Daten von Wikipedia sammeln
2. Rohdaten in Tabellenstruktur bringen
3. Gründerinnen und Gründer nach Geschlecht klassifizieren
4. Unsichere oder unbekannte Einträge nachverarbeiten
5. Ergebnisse als CSV-Dateien speichern und weiter analysieren

## Datenquellen

Die Basisdaten kommen aus der Wikipedia-Liste zu Unicorn-Startups:

- https://en.wikipedia.org/wiki/List_of_unicorn_startup_companies

Die Scraping-Logik liegt in [src/scrape_wiki.py](src/scrape_wiki.py).

## Hauptablauf

### 1. Abhängigkeiten installieren

Klonen
```bash
git clone https://github.com/viktorpantushev/gender-aspekte-bei-unicorns.git
```

Und installieren
```bash
pip install -r requirements.txt
```

### 2. Daten sammeln

Die eigentliche Datenbeschaffung läuft im Notebook [gender_aspekte_bei_unicorns.ipynb](gender_aspekte_bei_unicorns.ipynb). Dort werden die Wikipedia-Tabellen gelesen und als CSV-Dateien gespeichert.

### 3. Geschlechterklassifikation

Die eigentliche Geschlechtsvorhersage geschieht über [src/get_gender_data.py](src/get_gender_data.py). Dabei wird zunächst ein Name-basierter Ansatz verwendet, ergänzt durch:

- gender-guesser
- eine spezielle Modellierung für indische Namen
- zusätzliche Web-Suchen über Wikidata, Wikipedia und Google-Snippets

### 4. Nachverarbeitung unsicherer Einträge

Mit [src/rescue_unknowns.py](src/rescue_unknowns.py) können Einträge, bei denen das Geschlecht nicht sicher bestimmt werden konnte, gezielt erneut verarbeitet werden.

## Ausgabeprodukte

Das Projekt erzeugt unter anderem:

- Rohdaten zu aktuellen und vergangenen Unicorns
- Daten mit Geschlechterklassifikation
- aggregierte CSV-Dateien für Länder, Branchen und Sektoren
- Zwischenstände in [data](data) und [processed_data](processed_data)

## Hinweise

- Die Geschlechterzuordnung basiert auf Namen und öffentlich verfügbaren Informationen. Daher sind die Ergebnisse als Schätzung zu verstehen.
- Unsichere Fälle werden bewusst als "unknown" behandelt, um Fehlklassifikationen zu vermeiden.
- Web-basierte Nachschlagevorgänge können je nach Netzwerk und Rate-Limits langsamer sein.
