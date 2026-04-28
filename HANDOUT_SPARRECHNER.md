# Handout: Sparpotenzial Rechner

## Ziel der Änderung

Der bestehende Tankzeit-Webauftritt wurde um einen Sparpotenzial Rechner erweitert. Statt nur günstige Tankzeiten anzuzeigen, kann die Seite jetzt auf Basis persönlicher Fahrdaten eine konkrete Tankplanung erstellen.

## Was wurde verändert?

### 1. Neue Seite: `sparrechner.html`

Es wurde eine neue Seite für den Sparrechner erstellt.

Der Nutzer kann dort eingeben:

- Kraftstoffart: Diesel, E10 oder E5
- Verbrauch in Liter pro 100 km
- Kilometer pro Wochentag
- Tankvolumen des Autos
- aktueller Tankinhalt in Litern

Aus diesen Angaben berechnet die Seite eine Tankplanung.

### 2. Navigation erweitert

In der unteren Navigation wurde ein neuer Tab `Sparen` ergänzt.

Dadurch ist der Sparrechner direkt über die Hauptnavigation erreichbar.

Der Tab wurde unter anderem ergänzt in:

- `index.html`
- `e10.html`
- `favoriten.html`
- `management.html`
- `info.html`
- `chart.html`
- `price.html`

### 3. Startseite erweitert

Auf der Hauptseite wurde zusätzlich ein Hinweisbereich eingebaut:

`Sparpotenzial Rechner`

Über diesen Bereich kann man direkt zum Rechner wechseln.

### 4. Eingaben verbessert

Die erste Version hatte nur eine einfache Angabe wie `Kilometer pro Woche` und `Tankmenge pro Stopp`.

Das wurde verbessert:

- Kilometer können jetzt pro Wochentag eingetragen werden.
- Statt einer festen Tankmenge wird das echte Tankvolumen des Autos angegeben.
- Zusätzlich wird der aktuelle Tankstand in Litern berücksichtigt.

### 5. Ergebnis verbessert

Vorher gab es nur eine einzelne Empfehlung.

Jetzt erstellt der Rechner eine Tankplanung für die nächsten 4 Tankstopps.

Die Planung zeigt:

- Datum
- Uhrzeit
- Tankstelle
- geplante Liter
- geschätzter Preis
- geschätzte Ersparnis

## Wie funktioniert die Berechnung grob?

1. Der Rechner nimmt den aktuellen Moment als Startpunkt.
2. Er berechnet anhand von Verbrauch, Tageskilometern und aktuellem Tankstand, wie lange der Tank ungefähr reicht.
3. Innerhalb dieses Zeitraums sucht er günstige Tankmöglichkeiten.
4. Danach wird angenommen, dass der Tank wieder voll ist.
5. Dieser Ablauf wird wiederholt, bis 4 Tankstopps geplant sind.

Die Preise werden aus den vorhandenen historischen Daten und Tankzeit-Profilen berechnet.

## Wichtige Dateien

- `sparrechner.html`  
  Enthält die neue Rechner-Seite und die Berechnungslogik.

- `styles.css`  
  Enthält das Styling für Formular, Tageskilometer und Ergebnisanzeige.

- `serve-local.ps1`  
  Kleiner lokaler Server, um die Website im Browser testen zu können.

- `index.html`  
  Enthält den Einstieg zum Sparrechner auf der Hauptseite.

## Kurze Anleitung zum Starten

PowerShell öffnen und diese Befehle ausführen:

```powershell
cd C:\Users\G8\Documents\GitHub\tankzeit.de
powershell -ExecutionPolicy Bypass -File .\serve-local.ps1
```

Danach im Browser öffnen:

```text
http://127.0.0.1:4173/sparrechner.html
```

Zum Beenden des lokalen Servers:

```text
Strg + C
```

## Kurze Anleitung zur Vorführung

1. Website lokal starten.
2. Im Browser die Seite `sparrechner.html` öffnen.
3. Standortzugriff erlauben, damit nahe Tankstellen gefunden werden.
4. Beispielwerte eingeben:
   - Verbrauch: `6.5`
   - Kilometer pro Tag: z. B. Montag bis Freitag `40`
   - Tankvolumen: `55`
   - Aktuell im Tank: `25`
5. Auf `Berechnen` klicken.
6. Die Seite zeigt die nächsten 4 geplanten Tankstopps.

## Kurzer Erklärungssatz

Ich habe die Tankzeit-Seite um einen persönlichen Sparrechner erweitert, der aus Verbrauch, Fahrstrecke, Tankvolumen, aktuellem Tankstand und historischen Preisdaten eine konkrete Tankplanung für die nächsten 4 Tankstopps berechnet.
