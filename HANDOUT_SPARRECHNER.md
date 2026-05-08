# Handout: Sparpotenzial Rechner

## Ziel

Der Sparpotenzial Rechner soll aus persoenlichen Fahrdaten und historischen Tankzeit-Daten eine konkrete Tankplanung erstellen. Nutzer sollen nicht nur sehen, wann Tanken allgemein guenstig ist, sondern wann sie persoenlich am besten tanken sollten.

Die zentrale Frage lautet:

> Wann sollte ich mit meinem Verbrauch, meinem Tankstand und meiner Fahrleistung tanken, damit ich moeglichst guenstig unterwegs bin?

## Was wurde gemacht?

### Neue Seite: `sparrechner.html`

Es wurde eine eigene Seite fuer den Sparpotenzial Rechner erstellt. Die Seite ist ueber den Tab **Sparen** erreichbar.

Der Nutzer kann eingeben:

- Kraftstoffart: Diesel, E10 oder E5
- Verbrauch in Liter pro 100 km
- Kilometer pro Wochentag
- Tankvolumen in Liter
- aktueller Tankinhalt in Liter

### Tankplanung statt einzelner Empfehlung

Der Rechner gibt nicht nur eine einzelne Empfehlung aus, sondern plant die **naechsten 4 Tankstopps**.

In der Ergebnis-Tabelle werden angezeigt:

- Tankstelle
- Datum
- empfohlene Uhrzeit
- geplante Liter
- geschaetzter Preis
- geschaetzte Ersparnis

### App-Benachrichtigung

Zusaetzlich gibt es eine Option fuer eine App-Benachrichtigung.

Wenn der Nutzer den Button **Benachrichtigung aktivieren** anklickt, merkt sich die App den naechsten geplanten Tankstopp. Die Erinnerung soll am Vortag um 18:00 Uhr erscheinen und enthaelt:

- den Tanktag
- die empfohlene Uhrzeit
- die Tankstelle
- die geplante Liter-Menge
- den ungefaehren Preis

Wichtig: Der Nutzer muss Benachrichtigungen im Browser erlauben. Auf dem Handy funktioniert das am besten, wenn die Webseite als App/PWA installiert ist.

## Wie wird berechnet?

### 1. Startpunkt

Der Rechner startet immer beim aktuellen Moment. Dadurch wird nicht mit einem festen Datum gerechnet, sondern mit der aktuellen Situation des Nutzers.

### 2. Verbrauch pro Tag

Aus den Tageskilometern und dem Verbrauch wird berechnet, wie viele Liter pro Tag benoetigt werden.

Formel:

```text
Tagesverbrauch = Kilometer am Tag * Verbrauch / 100
```

Beispiel:

```text
40 km * 6,5 l / 100 km = 2,6 l pro Tag
```

### 3. Reichweite des aktuellen Tanks

Mit dem aktuellen Tankinhalt wird berechnet, bis zu welchem Tag der Kraftstoff reicht.

Der Rechner zieht fuer jeden Tag den berechneten Tagesverbrauch vom aktuellen Tankstand ab. Sobald der Tank fuer den naechsten Tag nicht mehr reicht, entsteht ein spaetester Tanktermin.

### 4. Guenstige Tankmoeglichkeiten suchen

Bis zu diesem spaetesten Tanktermin sucht der Rechner passende Tankmoeglichkeiten bei nahegelegenen Tankstellen.

Dafuer werden historische Daten genutzt:

- durchschnittliche Preise je Wochentag
- typische guenstige Uhrzeiten
- Preisprofile der Tankstellen

### 5. Beste Option waehlen

Die moeglichen Tankstopps werden verglichen. Bevorzugt wird:

1. der niedrigere Preis
2. bei gleichem Preis der fruehere Tag
3. bei gleichem Tag die naehere Tankstelle

### 6. Tank wieder auffuellen

Nach einem geplanten Tankstopp wird angenommen, dass der Tank wieder bis zum angegebenen Tankvolumen gefuellt ist.

Danach beginnt die Berechnung erneut, bis die naechsten 4 Tankstopps geplant sind.

## Was ist die Ersparnis?

Die Ersparnis wird pro Liter aus dem Unterschied zwischen einem typischen Referenzpreis und dem guenstigeren geplanten Preis berechnet.

Formel:

```text
Ersparnis = geplante Liter * Ersparnis pro Liter
```

Beispiel:

```text
40 l * 0,08 EUR = 3,20 EUR Ersparnis
```

## Wichtige Dateien

- `sparrechner.html`  
  Enthaelt die Seite, Eingaben, Tankplanung, Berechnung und App-Benachrichtigung.

- `styles.css`  
  Enthaelt das Design fuer Formular, Ergebnisbereich, Tabellen und Benachrichtigungs-Karte.

- `station-catalog.js`  
  Laedt Tankstellen und findet nahe Stationen anhand des Standorts.

- `app-stats.js`  
  Hilft bei der Auswertung der Preisprofile und guenstigen Zeitfenster.

- `serve-local.ps1`  
  Startet die Webseite lokal im Browser.

## Kurze Anleitung

PowerShell:

```powershell
cd C:\Users\G8\Documents\GitHub\tankzeit.de
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\serve-local.ps1
```

Browser:

```text
http://127.0.0.1:4173/sparrechner.html
```

## Vorfuehrung

1. Sparrechner im Browser oeffnen.
2. Standort erlauben, damit nahe Tankstellen geladen werden.
3. Verbrauch eintragen, z. B. `6.5`.
4. Kilometer pro Wochentag eintragen.
5. Tankvolumen in Liter eintragen, z. B. `55`.
6. Aktuellen Tankinhalt eintragen, z. B. `25`.
7. Auf **Berechnen** klicken.
8. Die naechsten 4 Tankstopps ansehen.
9. Optional **Benachrichtigung aktivieren**, damit die App am Vortag an den naechsten Tankstopp erinnert.

## Kurz erklaert

Ich habe einen persoenlichen Sparpotenzial Rechner gebaut. Er kombiniert Verbrauch, Tageskilometer, Tankvolumen, aktuellen Tankstand, Standortdaten und historische Preisprofile. Daraus entsteht eine konkrete Planung fuer die naechsten 4 Tankstopps inklusive Preis, Uhrzeit, Liter-Menge, Ersparnis und optionaler App-Benachrichtigung.
