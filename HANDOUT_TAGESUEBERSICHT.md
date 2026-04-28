# Handout: Tagesübersicht in der Statistik

## Ziel der Änderung

Die Statistikseite wurde um eine Tagesübersicht erweitert. Sie zeigt, wie sich der Kraftstoffpreis innerhalb einer Woche von Montag bis Sonntag entwickelt.

Damit kann man besser erkennen, an welchem Tag der Woche Tanken günstiger ist.

## Was wurde verändert?

### 1. Diagramm in `management.html`

Die Tagesübersicht wurde direkt in die bestehende Statistikseite eingebaut.

Die separate Seite `tagesuebersicht.html` wurde wieder entfernt, damit die Funktion nicht als eigene Seite, sondern als Teil der Statistik erscheint.

### 2. Neues Diagramm: Montag bis Sonntag

In der Statistik gibt es jetzt ein neues Liniendiagramm:

`Preisverlauf Montag bis Sonntag`

Das Diagramm zeigt für die Woche des ausgewählten Datums den Preisverlauf von Montag bis Sonntag.

### 3. Kraftstoffauswahl bleibt erhalten

Das Diagramm reagiert auf die vorhandenen Kraftstoff-Buttons:

- Diesel
- E10
- E5

Wenn man den Kraftstoff wechselt, aktualisiert sich auch die Tagesübersicht.

### 4. Prognose für fehlende Tage

Wenn für den Rest der Woche noch keine echten Daten vorhanden sind, wird eine Prognose angezeigt.

Darstellung:

- echte Daten: durchgezogene Linie
- Prognose: gestrichelte Linie

Die Prognose basiert auf dem bisherigen Trend der vorhandenen Wochenwerte.

### 5. Datenstand sichtbar gemacht

Da lokal nicht immer Daten bis zum aktuellen Datum vorhanden sind, zeigt die Statistikseite jetzt einen Datenstand an.

Beispiel:

`Datenstand: 2026-04-23`

So ist klar, warum die Statistik eventuell nicht den heutigen Tag zeigt.

## Warum war der aktuelle Tag nicht sichtbar?

Der Browser hatte zwar das richtige Datum, aber im lokalen Projekt lagen Management-Daten nur bis zu einem bestimmten Tag vor.

Wenn eine Datei wie diese fehlt:

```text
data2/2026/04/27/management_boxplots.json
```

kann die Statistik diesen Tag nicht anzeigen.

Deshalb sucht die Seite jetzt automatisch den neuesten lokal verfügbaren Datensatz.

## Wichtige Dateien

- `management.html`  
  Enthält die Statistikseite, das neue Wochen-Diagramm und die Prognose-Logik.

- `styles.css`  
  Enthält kleine Layout-Anpassungen für Hinweise und bestehende Statistik-Elemente.

- `data2/<jahr>/<monat>/<tag>/management_boxplots.json`  
  Enthält die Daten, aus denen die Statistik-Diagramme berechnet werden.

## Kurze Anleitung zum Starten

PowerShell öffnen und diese Befehle ausführen:

```powershell
cd C:\Users\G8\Documents\GitHub\tankzeit.de
powershell -ExecutionPolicy Bypass -File .\serve-local.ps1
```

Danach im Browser öffnen:

```text
http://127.0.0.1:4173/management.html
```

Zum Beenden des lokalen Servers:

```text
Strg + C
```

## Kurze Anleitung zur Vorführung

1. Website lokal starten.
2. Statistikseite öffnen.
3. Oben den Datenstand erklären.
4. Kraftstoff auswählen, z. B. Diesel.
5. Das Diagramm `Preisverlauf Montag bis Sonntag` zeigen.
6. Erklären:
   - durchgezogene Linie = echte vorhandene Daten
   - gestrichelte Linie = Prognose für fehlende/restliche Tage
7. Optional zwischen Diesel, E10 und E5 wechseln.

## Kurzer Erklärungssatz

Ich habe die Statistikseite um eine Tagesübersicht erweitert, die den Preisverlauf von Montag bis Sonntag zeigt und fehlende Tage der aktuellen Woche als gestrichelte Prognose ergänzt.
