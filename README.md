# [Untertägige Preisveränderungen für Treibstoffe](https://tankzeit.de)

[Finden Sie die beste Zeit zum Tanken](https://tankzeit.de)

Dieses Repository beobachtet die Preisveränderungen innerhalb eines Tages für Diesel, E10 und E5 an allen deutschen Tankstellen.

Datenquelle: MTS-K via [Tankerkönig](https://www.tankerkoenig.de/).

![Marktübersicht](img/marketview.png)

Die berechneten Preisunterschiede und stündlichen Mittelwerte der Preise für *jede Tankstelle* werden per GitHub Actions erzeugt und in diesem Repository gespeichert.

## Erfahrungsberichte zur Projektarbeit

In diesem Abschnitt werden die persönlichen Erfahrungen aus der Projektarbeit mit GitHub, Codex und der Weiterentwicklung von tankzeit.de gesammelt. Die Berichte zeigen, wie die einzelnen Teammitglieder mit Prompts, Branches, Tests, Datenanalyse und der schrittweisen Umsetzung neuer Funktionen gearbeitet haben.

<details>
<summary><strong>Dennis Marko</strong></summary>

Die Arbeit mit GitHub und Codex war für mich am Anfang eine neue und ungewohnte Erfahrung. Meine zentrale Aufgabe war der Sparpotenzial-Rechner. Ziel war es, nicht nur allgemein zu zeigen, wann Tanken günstig ist, sondern eine persönliche Planung für den Nutzer zu erstellen. Dafür sollten persönliche Fahrdaten mit historischen Tankzeit-Daten verbunden werden. Nutzer können zum Beispiel Kraftstoffart, Verbrauch, Kilometer pro Wochentag, Tankvolumen und den aktuellen Tankinhalt eingeben. Daraus berechnet der Rechner, wann die nächsten Tankstopps sinnvoll sind und welche Uhrzeit beziehungsweise Tankstelle besonders günstig ist.

Bei der Umsetzung habe ich gemerkt, dass es einen Unterschied macht, ob man nur eine einzelne Empfehlung anzeigen lässt oder wirklich eine Tankplanung erstellt. Der Rechner plant die nächsten vier Tankstopps und berücksichtigt dabei, wie weit der aktuelle Tankstand noch reicht. Aus den Tageskilometern und dem Verbrauch wird berechnet, wie viele Liter pro Tag benötigt werden. Sobald der Tank für den nächsten Tag nicht mehr ausreichen würde, entsteht ein spätester Tanktermin. Bis zu diesem Zeitpunkt sucht der Rechner nach günstigen Möglichkeiten und nutzt dafür unter anderem typische Preisprofile, durchschnittliche Preise je Wochentag und günstige Uhrzeiten.

Besonders wichtig war es, erst einmal zu verstehen, wie man seine Aufgaben so beschreibt, dass Codex genau das umsetzt, was man sich vorstellt. Dabei habe ich gemerkt, dass die Eingrenzung der Prompts eine große Rolle spielt. Wenn ein Prompt zu allgemein formuliert war, musste das Ergebnis oft noch einmal angepasst werden. Je klarer das Ziel beschrieben war und je genauer ich erklärt habe, was verändert werden soll, desto besser hat die Umsetzung funktioniert. Bei größeren Änderungen, wie der Planung der nächsten vier Tankstopps, war mehr Kontext hilfreich. Bei kleineren Anpassungen reichten dagegen kurze und genaue Anweisungen aus.

Nicht alle Änderungen haben direkt beim ersten Versuch perfekt funktioniert. Einige Funktionen oder Darstellungen mussten mehrfach überarbeitet werden, bis sie so waren, wie ich sie mir vorgestellt habe. Gerade beim Sparrechner war es wichtig, die Berechnung zu testen: Der aktuelle Tankinhalt wird mit dem täglichen Verbrauch verrechnet, anschließend sucht der Rechner bis zum spätesten Tanktermin nach günstigen Möglichkeiten und plant danach weiter. Insgesamt fand ich es spannend zu sehen, wie aus einzelnen Prompts Schritt für Schritt ein nutzbares Ergebnis auf der Website entstanden ist. Besonders motivierend war, dass man die eigenen Änderungen direkt testen und verbessern konnte.

Außerdem habe ich gelernt, dass Codex zwar sehr schnell Funktionen erstellen kann, man die Ergebnisse aber trotzdem kritisch prüfen muss. Teilweise sah eine Änderung auf den ersten Blick richtig aus, musste aber in der Bedienung oder im Design noch angepasst werden. Beim Sparrechner war mir wichtig, dass die Eingaben verständlich sind und das Ergebnis nicht nur technisch funktioniert, sondern auch für Nutzer nachvollziehbar bleibt. Dadurch habe ich besser verstanden, wie wichtig Testen, Nachfragen und schrittweises Verbessern bei der Arbeit mit KI sind.

</details>

<details>
<summary><strong>Helena Schmidt</strong></summary>

Die Arbeit mit GitHub und Codex war eine komplett neue Erfahrung für mich. Dementsprechend dauerte es zu Beginn, bis man sich eingefunden und den Umgang verstanden hatte. Es war spannend, neue Erfahrungen in einem für mich völlig neuen Gebiet zu sammeln und nach etwas Zeit auch Zusammenhänge zu verstehen. Für mich hat die Arbeit mit Codex gut funktioniert. Ich bin mit der Aufgabe schrittweise vorgegangen, so konnte ich die Vorgehensweise von Codex immer wieder überprüfen und gegebenenfalls korrigieren. Wie in der Vorlesung gelernt, hat Codex manchmal Dinge geändert, die nicht gewünscht waren. Diese konnten meiner Erfahrung nach jedoch schnell korrigiert werden und mithilfe der iterativen Vorgehensweise früh erkannt werden.

Zur Erklärung der Tankstellenauszeichnungen: Besonders kundenfreundliche Tankstellen wurden mit Auszeichnungen ausgezeichnet. Kriterien für die Kundenfreundlichkeit sind das Preisniveau, die Preisstabilität und wie schnell die Tankstelle ihre Preise nach 12 Uhr senkt. Die Top 10 Prozent der kundenfreundlichsten Tankstellen sind mit Bronze, die Top 5 Prozent mit Silber und die Top 2 Prozent mit Gold ausgezeichnet. Diese Struktur habe ich zuerst selbst überlegt und anschließend Codex gefragt. Da Codex die Sinnhaftigkeit dieser Struktur bestätigte, wurde diese übernommen. Sie stellt sicher, dass die Auszeichnung der Tankstellen etwas Besonderes bleibt, aber dennoch ausreichend oft von Kunden gesehen wird.

Die Aufgabe hat mir nicht nur das Programmieren mithilfe von KI beigebracht, sondern auch die Arbeit mit Daten. Wir haben uns im Team viele Gedanken über mögliche Auswertungen und Erweiterungen der Webseite gemacht und gemeinschaftlich spannende Möglichkeiten gefunden.

Insgesamt war der Kurs für mich sehr lehrreich bezüglich neuer Erfahrungen in der Softwareentwicklung und Datenanalyse. Ich habe gelernt, wie man sinnvoll mit KI umgeht und sie für sich nutzen kann. Darüber hinaus habe ich meine erste Erfahrung in der Entwicklung einer Webseite gesammelt und mich intensiv mit der Analyse von Daten beschäftigt. Hinzu kommt, dass ich mich nebenbei auch im Umgang im Team weiterentwickeln konnte.

</details>

<details>
<summary><strong>Sandra-Silvia Grec</strong></summary>

Während der Arbeit an der Heatmap und dem Standortfilter habe ich gemerkt, dass es nicht nur darum geht, eine Funktion irgendwie einzubauen, sondern wirklich zu verstehen, wie sie sich später auf der Website verhält. Bei der Heatmap war zum Beispiel wichtig, dass die Darstellung übersichtlich bleibt und nicht einfach nur viele Informationen gleichzeitig angezeigt werden. Beim Standortfilter ging es eher darum, dass die Nutzer schnell und logisch eingrenzen können, welche Tankstellen oder Orte für sie relevant sind.

Eine wichtige Erfahrung war für mich, dass Codex sehr hilfreich sein kann, aber trotzdem klare Anweisungen braucht. Am Anfang habe ich oft längere Prompts geschrieben, weil ich möglichst genau erklären wollte, was ich mir vorstelle. Später habe ich gelernt, dass kurze Prompts manchmal besser funktionieren, wenn es nur um einzelne Änderungen geht. Wenn etwas nicht richtig umgesetzt wurde, war es hilfreicher, direkt zu sagen: „Ändere nur diesen Teil“ oder „Passe nur diese Funktion an“, anstatt wieder alles neu zu erklären.

Auch die Arbeit mit GitHub und Branches war eine neue Erfahrung. Ich habe verstanden, warum es sinnvoll ist, nicht direkt am Hauptstand der Website zu arbeiten, sondern neue Funktionen zuerst in einem eigenen Branch zu entwickeln. Dadurch konnte man Änderungen ausprobieren, Fehler finden und Verbesserungen machen, ohne direkt das ganze Projekt zu beeinflussen. Gleichzeitig musste ich lernen, sorgfältig zu arbeiten, damit ich nicht durcheinanderkomme, auf welchem Branch ich gerade bin oder welche Änderungen schon gespeichert wurden.

Zusätzlich habe ich gemerkt, wie wichtig Testen ist. Nur weil Codex eine Funktion eingebaut hat, heißt das nicht automatisch, dass sie genau so funktioniert, wie man es sich vorgestellt hat. Gerade beim Standortfilter musste man prüfen, ob die Auswahl wirklich die richtigen Ergebnisse anzeigt. Bei der Heatmap musste man schauen, ob die Darstellung verständlich ist und ob sie auf der Website optisch gut passt.

Insgesamt habe ich durch die Arbeit gelernt, technischer und genauer zu denken. Ich musste meine eigenen Vorstellungen klarer formulieren, Ergebnisse kritisch überprüfen und bei Fehlern gezielt nachbessern. Dadurch wurde die Zusammenarbeit mit Codex mit der Zeit einfacher und ich habe besser verstanden, wie man KI sinnvoll für die Entwicklung einer Website einsetzen kann.

</details>

<details>
<summary><strong>Michael Kriegl</strong></summary>

Obwohl ich durch meine Tätigkeit bei Bosch bereits praktische Vorerfahrungen im Bereich von Datenbanken und Agentic AI mitbrachte, stellte die Arbeit mit GitHub und das Coding in diesem Modul eine neue Erfahrung für mich dar. Nachdem wir uns nach dem theoretischen Input als Gruppe zusammensetzten und das Vorgehen diskutierten, wurde das Konzept jedoch schnell greifbarer.

Das anfängliche technische Problem lag für mich darin, dass sich GitHub Desktop aufgrund von mangelndem Arbeitsspeicher auf meinem Laptop nicht installieren ließ. Als Lösung arbeitete ich letztendlich zusammen mit Sandra an mehreren Use Cases. Diese Zusammenarbeit funktionierte hervorragend, da wir uns gegenseitig optimal ergänzten und dennoch beide das Gesamtkonzept verstanden. Das Arbeiten mit Branches im gesamten Team verlief ebenfalls positiv, obwohl wir während des Projektes Sorge hatten, dadurch Komplikationen zu bekommen. Das spätere Zusammenführen der Branches verlief dann positiv. Es mussten lediglich kleine Details angepasst werden, sodass das Gesamtkonzept am Ende erfolgreich realisiert wurde. Dadurch, dass meine Gruppe einen BWL-Fokus hat und weniger IT-affin ist, fühlten wir uns durch separate Kopien sicherer.

Besonders fasziniert hat mich die Leistungsfähigkeit der KI. Ich war erstaunt, wie präzise die KI die Anforderungen grundsätzlich aus den Prompts umsetzte. Wenn ein Befehl verstanden wurde, war das Ergebnis sehr nah an den Anforderungen. Dennoch musste ich teilweise iterativ vorgehen, da die KI bei bestimmten spezifischen Wünschen einfach keine Umsetzung vornahm. Dies war vor allem dann der Fall, wenn mehrere Umsetzungen in einem Prompt geschildert wurden. Folglich sehe ich zukünftig kleinere Prompts als vorteilhafter, um auch besser kontrollieren zu können.

So weigerte sich die KI beispielsweise trotz mehrfacher Aufforderung, die Informationen unter einer Heatmap als Tabelle zu formatieren. Teilweise wurde es sogar schlimmer, da die Formatierung dann plötzlich überlappte, obwohl es davor eigentlich passte. Eine weitere Herausforderung war, dass eine Anforderung, die eigentlich funktionierte, durch weitere Prompts bei einer zusätzlichen Funktion plötzlich wieder negativ verändert wurde. Hier brauchte es ein genaues Auge.

Positiv überrascht hat mich wiederum das „Mitdenken“ der KI. Bei Unklarheiten oder mehreren Optionen wurde ich noch einmal gefragt, wie eine Anforderung konkret umgesetzt werden soll. Dadurch entstand während der Arbeit das Gefühl, inhaltlich besser verstanden zu werden, was den Entwicklungsprozess enorm unterstützt hat.

Schlussfolgernd konnte ich mein anwendungsorientiertes Wissen mit GitHub und Codex verbessern und gleichzeitig kritisches Hinterfragen stärken. Mir gefiel es ebenfalls, dass es mehrere Lösungsansätze gab und wir kreativen Freiraum hatten. Dadurch, dass die meisten Module sehr theorielastig sind, war das eine positive Abwechslung.

</details>

<details>
<summary><strong>Katharina Marie-Therese Schmidt</strong></summary>

Anfangs war die Arbeit mit GitHub und Codex eine völlig neue Erfahrung für mich, da ich zuvor noch nie damit gearbeitet hatte. Deshalb musste man sich einfach auf die neue Aufgabe einlassen und sich durch Learning by Doing die Programme aneignen.

Erschwerend kam hinzu, dass ich Probleme mit dem Herunterladen des Repositorys auf meinen Laptop hatte, weshalb ich mich Dennis angeschlossen habe. Unsere Teamarbeit lief super: Durch eine gute Mischung aus persönlichen Treffen und Teams-Meetings konnten wir gut zusammenarbeiten.

Nachdem man sich erst einmal eingearbeitet und die passende Vorgehensweise für sich selbst gefunden hatte, zum Beispiel wie man gute Prompts stellt, damit genau das in der Website gebaut wird, was man sich vorstellt, wurde die Arbeit deutlich einfacher. Besonders die Zusammenarbeit im Team hat dabei sehr geholfen, sodass das Arbeiten am Ende insgesamt gut funktioniert hat. Man muss sich einfach darauf einlassen, dann findet man sich mit der Zeit gut zurecht. Schön war außerdem, dass man am Ende auch das eigene und gemeinsame Ergebnis sehen konnte und dadurch direkt gemerkt hat, wofür man gearbeitet hat.

Rückblickend war der Kurs für mich eine ganz neue und wertvolle Erfahrung. Ich habe gelernt, dass man manchmal einfach Vertrauen in den Ablauf haben muss, denn am Ende fügt sich doch immer alles zusammen. Besonders spannend war für mich zu sehen, was KI eigentlich alles kann, wie man sie clever nutzt und wie wichtig es gleichzeitig ist, ihre Ergebnisse zu hinterfragen. Dass das Ganze kein rein theoretischer Kurs war, sondern wir direkt praktisch gearbeitet haben, war eine wirklich gelungene Abwechslung.

</details>

## Datenpipeline (Python)

Die tägliche Aktualisierung läuft via GitHub Actions und schreibt die Ergebnisse in dieses Repository.

Erforderlich:
- GitHub Secrets `TK_USER` und `TK_PASS` (Zugang zum Tankerkönig Data Repository)

Abbildung der MTS-K Tankstellen ID auf Ordnerstrukur aus

Beispiel OMV Bad Herrenalb (ID b4ed695f-2cfc-4688-8ecf-268b10cdb93e)

wird

[/b4ed695f/2cfc/4688/8ecf/268b10cdb93e/](https://huggingface.co/datasets/loffenauer/fuel-prices-germany/tree/main/data2/b4ed695f/2cfc/4688/8ecf/268b10cdb93e/) 

mit Daten der jeweiligen Tankstelle


* [Diesel](https://huggingface.co/datasets/loffenauer/fuel-prices-germany/resolve/main/data2/b4ed695f/2cfc/4688/8ecf/268b10cdb93e/diesel.csv)
* [E10](https://huggingface.co/datasets/loffenauer/fuel-prices-germany/resolve/main/data2/b4ed695f/2cfc/4688/8ecf/268b10cdb93e/e10.csv)
* [E5](https://huggingface.co/datasets/loffenauer/fuel-prices-germany/resolve/main/data2/b4ed695f/2cfc/4688/8ecf/268b10cdb93e/e5.csv)

In jedem Ordner finden sich auch JSON Dateien für 

* [Diesel](https://huggingface.co/datasets/loffenauer/fuel-prices-germany/resolve/main/data2/b4ed695f/2cfc/4688/8ecf/268b10cdb93e/diesel.json)
* [E10](https://huggingface.co/datasets/loffenauer/fuel-prices-germany/resolve/main/data2/b4ed695f/2cfc/4688/8ecf/268b10cdb93e/e10.json)
* [E5](https://huggingface.co/datasets/loffenauer/fuel-prices-germany/resolve/main/data2/b4ed695f/2cfc/4688/8ecf/268b10cdb93e/e5.json)
CSV und JSON sind inhaltlich gleich, aber unterschiedlich formatiert.

Jeweils gleichartiger Aufbau dieser Dateien für alle Tankstellen

* 2 Spalten: Uhrzeit, Preisdifferenz in Euro
* 25 Zeilen, Header, dann Stunde, Preisdifferenz

Die Dateien `diesel.csv`, `e10.csv` und `e5.csv` bleiben die untertägigen Preisdifferenzen.

Für die Mittags-Historie seit dem 1. April 2026 gibt es zusätzlich pro Tankstelle und Kraftstoff:

* `data2/<station>/<fuel>/history.csv`

Aufbau von `history.csv`:

* 3 Spalten: `date`, `price`, `last_update`
* eine Zeile pro lokalem Tag mit dem in `noon.csv` etablierten Mittagspreis

## Website Build

SEO-Landingpages pro Tankstelle sowie `sitemap.xml` werden mit folgendem Skript erzeugt:

```bash
python scripts/build_site.py
```

Das Skript aktualisiert:

- `station/*.html`
- `sitemap.xml`
- `robots.txt`

## Android Play Store Assets

Metadaten und Basisgrafiken für den bestehenden Google-Play-Draft lassen sich so erzeugen:

```bash
python scripts/generate_android_play_store_assets.py
```

# Frequently Asked Questions (FAQ)

## Wozu? Weshalb? Warum?

Wer sparen will tankt zum richtigen Zeitpunkt. Siehe [Untertägige Preisveränderungen für Treibstoffe](https://tankzeit.de).

## Wie funktioniert das ?

Tankstellen sind gesetzlich verpflichtet ihre Preise an das Bundeskartellamt zu melden. Dieses Amt publiziert den Datensatz MTS-K auf umständlicher Weise. Tankerkönig veröffentlicht und archiviert diese Preise. Die Preise des letzten Tages werden von uns aufbereitet, um die Preisveränderungen nach Stunde darzustellen. Das macht das Script `scripts/generate_data.py`, welches Sie mit Python auf einem System Ihrer Wahl selbst ausführen und den eigenen Bedürfnissen anpassen können.

## Wer hat das gemacht ?

Bei Fragen kontaktieren Sie bitte Raphael Volz (raphael.volz@hs-pforzheim.de). Alle Anregungen sind willkommen.

## Welche Tankstellen gibt es denn in Deutschland und was ist deren MTS-K ID ?

[Eine Liste der Tankstellen und deren ID im Format JSON finden Sie hier](https://huggingface.co/datasets/loffenauer/fuel-prices-germany/resolve/main/data/stations.json), diese Liste entspricht meist der letzten [CSV Datei, die Tankerkönig in ihrem Repository publizieren](https://dev.azure.com/tankerkoenig/_git/tankerkoenig-data). [Sie können die Tankstellen auch alle auf einer Karte betrachten (ACHTUNG: Rechner wird schwitzen...)](https://rpubs.com/loffenauer/mts-k)
