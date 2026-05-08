# Handout: Tagesuebersicht in der Statistik

## Ziel

Die Tagesuebersicht soll zeigen, an welchem Tag einer Woche Tanken eher guenstig oder teuer ist. Statt nur einzelne Uhrzeiten zu betrachten, wird der Preisverlauf von **Montag bis Sonntag** sichtbar gemacht.

Die zentrale Frage lautet:

> An welchem Tag der aktuellen Woche ist Tanken voraussichtlich am guenstigsten?

## Was wurde gemacht?

### Wochen-Diagramm in der Statistik

Die Tagesuebersicht wurde direkt in die Statistikseite `management.html` eingebaut.

Das Diagramm heisst:

```text
Preisverlauf Montag bis Sonntag
```

Es zeigt fuer die Woche des ausgewaehlten Datums den Preisverlauf von Montag bis Sonntag.

### Keine extra Tagesseite mehr

Eine separate Seite fuer die Tagesuebersicht wurde wieder entfernt. Die Funktion ist jetzt Teil der bestehenden Statistikseite.

Das ist uebersichtlicher, weil alle Statistikfunktionen an einem Ort liegen.

### Datum und Kraftstoff bleiben steuerbar

Oben auf der Statistikseite gibt es weiterhin:

- Datumsauswahl
- Kraftstoffauswahl: Diesel, E10, E5

Wenn der Kraftstoff gewechselt wird, aktualisiert sich auch die Tagesuebersicht.

### Prognose fuer fehlende Tage

Wenn fuer den Rest der Woche noch keine echten Daten vorhanden sind, wird eine Prognose angezeigt.

Darstellung:

- durchgezogene Linie = echte vorhandene Daten
- gestrichelte Linie = Prognose

Die Prognose hilft, die Woche trotzdem vollstaendig von Montag bis Sonntag zu zeigen.

### Datenstand sichtbar gemacht

Die Statistik zeigt den neuesten lokal verfuegbaren Datenstand an.

Beispiel:

```text
Datenstand: 2026-04-23
```

Das ist wichtig, weil lokal nicht immer Daten bis zum echten heutigen Tag vorhanden sind.

## Wie wird berechnet?

### 1. Woche bestimmen

Aus dem ausgewaehlten Datum wird zuerst der Montag der passenden Woche berechnet.

Danach werden die sieben Tage der Woche aufgebaut:

```text
Montag, Dienstag, Mittwoch, Donnerstag, Freitag, Samstag, Sonntag
```

### 2. Tagesdaten laden

Fuer jeden dieser Tage versucht die Seite, die lokalen Management-Daten zu laden.

Beispielpfad:

```text
data2/2026/04/23/management_boxplots.json
```

Wenn fuer einen Tag keine Datei vorhanden ist, bleibt dieser Tag zunaechst leer.

### 3. 12:00-Referenzpreis verwenden

Fuer jeden vorhandenen Tag wird der Median des 12:00-Referenzpreises genutzt.

Der Median ist sinnvoll, weil einzelne extreme Preise die Darstellung weniger stark verzerren als ein einfacher Durchschnitt.

### 4. Diagramm zeichnen

Die vorhandenen Tageswerte werden als Linie dargestellt.

Auf der X-Achse stehen die Wochentage mit Datum.  
Auf der Y-Achse steht der Preis in Euro pro Liter.

### 5. Prognose berechnen

Wenn Tage fehlen, wird der bisherige Trend der Woche genutzt.

Vereinfacht:

1. vorhandene echte Tageswerte sammeln
2. Preisunterschiede zwischen den vorhandenen Tagen berechnen
3. daraus einen durchschnittlichen Tagestrend ableiten
4. fehlende Folgetage mit diesem Trend fortschreiben

Beispiel:

```text
Montag: 2,20 EUR
Dienstag: 2,22 EUR
Trend: +0,02 EUR pro Tag
Mittwoch Prognose: 2,24 EUR
```

Die prognostizierten Werte werden gestrichelt angezeigt.

## Was sieht man im Ergebnis?

Die Tagesuebersicht zeigt:

- welcher Tag bisher am guenstigsten war
- wie sich der Preis ueber die Woche entwickelt
- ob der Preis eher steigt oder faellt
- welche Tage nur Prognose sind

## Erweiterung im Kettenvergleich

Auf `kettenvergleich.html` wurde das Prinzip ebenfalls genutzt.

Dort wird der Wochenverlauf getrennt nach Gruppen dargestellt:

- Ketten
- freie/private Tankstellen

Auch dort werden fehlende Folgetage als gestrichelte Prognose angezeigt.

## Wichtige Dateien

- `management.html`  
  Enthaelt die Statistikseite, das Wochen-Diagramm und die Prognose-Logik.

- `kettenvergleich.html`  
  Enthaelt den Wochenvergleich zwischen Ketten und freien Tankstellen.

- `styles.css`  
  Enthaelt Layout und Darstellung der Statistikbereiche.

- `data2/<jahr>/<monat>/<tag>/management_boxplots.json`  
  Enthaelt die Tagesdaten fuer die Statistikseite.

- `data2/<jahr>/<monat>/<tag>/noon.csv`  
  Wird im Kettenvergleich fuer die 12:00-Referenzpreise genutzt.

## Kurze Anleitung

PowerShell:

```powershell
cd C:\Users\G8\Documents\GitHub\tankzeit.de
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\serve-local.ps1
```

Browser:

```text
http://127.0.0.1:4173/management.html
```

Optional fuer den Vergleich Ketten gegen freie Tankstellen:

```text
http://127.0.0.1:4173/kettenvergleich.html
```

## Vorfuehrung

1. Website lokal starten.
2. Statistikseite oeffnen.
3. Oben den Datenstand zeigen.
4. Kraftstoff auswaehlen, z. B. Diesel.
5. Diagramm **Preisverlauf Montag bis Sonntag** zeigen.
6. Erklaeren:
   - durchgezogene Linie = echte Daten
   - gestrichelte Linie = Prognose
7. Optional zu E10 oder E5 wechseln.
8. Optional im Kettenvergleich zeigen, wie sich Ketten und freie Tankstellen unterscheiden.

## Kurz erklaert

Ich habe die Statistik um eine Tagesuebersicht erweitert. Sie zeigt den 12:00-Referenzpreis von Montag bis Sonntag und ergaenzt fehlende Tage mit einer gestrichelten Prognose. So kann man besser erkennen, an welchem Wochentag Tanken eher guenstig ist.
