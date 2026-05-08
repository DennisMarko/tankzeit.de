# Handout: Ketten und freie Tankstellen

## Ziel

Die Uebersicht soll zeigen, ob sich grosse Tankstellenketten und freie bzw. private Tankstellen preislich unterscheiden.

Die zentrale Frage lautet:

> Sind freie Tankstellen oder grosse Ketten beim Tanken guenstiger?

Dabei wird zuerst der aktuelle Datenstand betrachtet. Danach kann man im Detail sehen, wie sich die Preise ueber die Woche und um 12:00 Uhr unterscheiden.

## Was wurde gemacht?

### Vergleich in der Statistik

In `management.html` wurde ein neuer Vergleichsbereich eingebaut:

```text
Freie vs. Ketten - 12:00-Referenz
```

Dieser Bereich zeigt direkt in der Statistik:

- welche Gruppe guenstiger ist
- die Median-Differenz in Cent pro Liter
- wie viele Stationen verglichen wurden
- Median, Durchschnitt und Preisspanne fuer beide Gruppen

Oben rechts im Vergleichsfeld gibt es den Button **Mehr Details**.

### Detailseite: `kettenvergleich.html`

Die Detailseite zeigt genauer, welche Tankstellen als Ketten und welche als freie/private Tankstellen gelten.

Zusaetzlich enthaelt sie mehrere Diagramme:

- Preisverlauf Montag bis Sonntag
- 12:00-Referenzpreis nach Gruppe
- Preisaenderung zu 12:00
- Zeitpunkt der 12:00-Referenz

### Einordnung der Tankstellen

Als Ketten werden grosse bekannte Marken gezaehlt, zum Beispiel:

- ARAL
- Shell
- ESSO
- TotalEnergies
- JET
- STAR
- HEM
- ORLEN
- OIL!
- Q1

Alle anderen Marken, lokale Betreiber oder Tankstellen ohne klare Markenangabe werden als **freie/private Tankstellen** eingeordnet.

## Wie wird berechnet?

### 1. Stationsdaten laden

Die Seite laedt zuerst die Datei:

```text
data/stations.json
```

Darin stehen die Tankstellen mit Name, Marke, Standort und eindeutiger Stations-ID.

### 2. Stationen gruppieren

Jede Station wird anhand ihrer Marke einer Gruppe zugeordnet:

```text
Kette
```

oder

```text
freie/private Tankstelle
```

Wenn die Marke in der Liste der grossen Ketten steht, kommt sie in die Gruppe Ketten. Sonst kommt sie in die Gruppe freie/private Tankstellen.

### 3. 12:00-Preisdaten laden

Fuer den ausgewaehlten Tag wird die Datei mit den 12:00-Referenzpreisen geladen:

```text
data2/<jahr>/<monat>/<tag>/noon.csv
```

Diese Datei enthaelt pro Tankstelle die Preise fuer Diesel, E10 und E5 zur 12:00-Referenz.

### 4. Preise nach Gruppe sammeln

Fuer den gewaehlten Kraftstoff werden die Preise getrennt gesammelt:

- Preise aller Ketten
- Preise aller freien/private Tankstellen

Danach werden Kennzahlen berechnet.

## Welche Kennzahlen werden angezeigt?

### Median

Der Median ist der typische Preis einer Gruppe. Er ist robuster als der Durchschnitt, weil einzelne extreme Preise weniger Einfluss haben.

Beispiel:

```text
Ketten Median: 2,269 EUR/l
Freie Median: 2,249 EUR/l
```

Dann waeren freie Tankstellen im typischen Preis guenstiger.

### Durchschnitt

Der Durchschnitt zeigt den Mittelwert aller Preise einer Gruppe.

### Preisspanne

Die Preisspanne zeigt:

```text
Minimum bis Maximum
```

Also den guenstigsten und teuersten Preis innerhalb der Gruppe.

### Median-Differenz

Die Median-Differenz zeigt, wie weit die beiden Gruppen auseinanderliegen.

Beispiel:

```text
2,269 EUR/l - 2,249 EUR/l = 0,020 EUR/l
```

Das entspricht:

```text
2,0 ct/l
```

## Diagramme auf der Detailseite

### Preisverlauf Montag bis Sonntag

Dieses Liniendiagramm zeigt den Median der 12:00-Referenzpreise fuer Ketten und freie Tankstellen ueber die Woche.

Darstellung:

- Linie Ketten
- Linie freie/private Tankstellen
- gestrichelter Teil = Prognose fuer fehlende Folgetage

### 12:00-Referenzpreis nach Gruppe

Dieses Diagramm vergleicht die Preisverteilung am gewaehlten Tag.

Es zeigt fuer beide Gruppen:

- Minimum
- erstes Quartil
- Median
- drittes Quartil
- Maximum

Damit sieht man nicht nur einen einzelnen Wert, sondern die gesamte Streuung der Preise.

### Preisaenderung zu 12:00

Dieses Diagramm zeigt, wie sich der 12:00-Median gegenueber dem Vortag veraendert hat.

Auch hier werden Ketten und freie Tankstellen getrennt betrachtet.

Wenn fuer Folgetage noch Daten fehlen, wird eine gestrichelte Prognose gezeichnet.

### Zeitpunkt der 12:00-Referenz

Dieses Diagramm zeigt, wann der verwendete Referenzpreis laut Datenstand feststand.

Dadurch kann man sehen, ob die Referenzpreise eher genau um 12:00 Uhr oder leicht versetzt in den Daten auftauchen.

## Was sieht man im Ergebnis?

Die Uebersicht beantwortet:

- Wie viele Tankstellen gehoeren zu Ketten?
- Wie viele Tankstellen sind frei/private Betreiber?
- Welche Gruppe ist beim 12:00-Referenzpreis guenstiger?
- Wie stark unterscheidet sich der typische Preis?
- Wie entwickeln sich beide Gruppen ueber die Woche?
- Gibt es Unterschiede beim Zeitpunkt der 12:00-Referenz?

## Wichtige Dateien

- `management.html`  
  Enthaelt den kompakten Vergleich direkt in der Statistik.

- `kettenvergleich.html`  
  Enthaelt die Detailseite mit Einordnung, Tabellen und Diagrammen.

- `styles.css`  
  Enthaelt das Layout fuer Vergleichskarten, Tabellen und Diagramme.

- `data/stations.json`  
  Enthaelt die Stationsdaten und Marken.

- `data2/<jahr>/<monat>/<tag>/noon.csv`  
  Enthaelt die 12:00-Referenzpreise pro Station und Kraftstoff.

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

Detailseite:

```text
http://127.0.0.1:4173/kettenvergleich.html
```

## Vorfuehrung

1. Statistikseite oeffnen.
2. Den Bereich **Freie vs. Ketten - 12:00-Referenz** zeigen.
3. Erklaeren, welche Gruppe guenstiger ist.
4. Den Button **Mehr Details** anklicken.
5. Auf der Detailseite die Einordnung zeigen:
   - Ketten
   - freie/private Tankstellen
6. Die Diagramme zeigen:
   - Wochenverlauf
   - 12:00-Referenzpreis nach Gruppe
   - Preisaenderung zu 12:00
   - Zeitpunkt der 12:00-Referenz
7. Optional zwischen Diesel, E10 und E5 wechseln.

## Kurz erklaert

Ich habe eine Uebersicht gebaut, die grosse Tankstellenketten mit freien und privaten Tankstellen vergleicht. Dafuer werden die Tankstellen anhand ihrer Marke gruppiert und die 12:00-Referenzpreise getrennt ausgewertet. So sieht man, welche Gruppe typischerweise guenstiger ist und wie sich die Preise im Wochenverlauf unterscheiden.
