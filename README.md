# Root

docker compose up -d

# Backend folder

pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend folder

npm install
ng serve

Anmerkungen:
Wenn man schon eine Liste bzw. Tabelle mit allen Verträgen darstellt, wäre es natürlich sinnvoll, Infinity-Scroll oder etwas Vergleichbares zu implementieren. Dadurch würden nicht sofort alle Verträge geladen werden, falls es z.B. 100.000 Verträge gibt.

Bei Fehlermeldungen im Frontend ist der Fehlertyp aktuell ebenfalls in der Meldung enthalten (z.B. “Value error, Vertragsende darf nicht vor Vertragsbeginn liegen!” → „Value Error“). Man könnte diesen Teil entfernen, wenn nötig – entweder direkt im Backend oder im Frontend –, damit die Fehlermeldung insgesamt „schöner“ bzw. benutzerfreundlicher wirkt.

Nachdem man auf Hochladen klickt, wäre es logisch, den Namen der ausgewählten Datei wieder zu löschen.

Wenn eine Datei erfolgreich hochgeladen wurde, wäre es sinnvoll, dass die Verträge direkt automatisch angezeigt werden.

Solche Werte wie die Base-URL (requestUrl) im Frontend oder die Origins-URL für CORS im Backend sollte man in einem echten Projekt nicht hardcoden.

Die .env-Datei sollte in einem realen Projekt natürlich nicht ins Git hochgeladen werden.

Aktuell ist das Verhalten so: Wenn in der Datei eine Zeile fehlerhaft ist (z.B. die Vertragsnummer taucht bereits in der Datenbank auf), wird nur diese Zeile nicht gespeichert, während alle anderen validen Zeilen korrekt importiert werden. Man könnte sich überlegen, welches Verhalten besser ist:

Wenn mindestens eine Zeile fehlerhaft ist, wird der komplette Upload abgebrochen.

Nur die fehlerhaften Zeilen werden übersprungen, während alle anderen importiert werden (aktuelles Verhalten). Wenn allerdings der Header einer Spalte fehlt oder falsch geschrieben ist (z.B. „Vertragsnummer“ falsch), wird der gesamte Upload abgebrochen.

Aktuell ist das Verhalten außerdem wie folgt: Wenn der User während des Upload-Prozesses die Seite aktualisiert oder zu einer anderen Seite navigiert, wird der laufende Prozess im Backend nicht abgebrochen. Der Client bricht nur das Warten auf die Antwort ab, aber der Request wurde bereits vollständig übertragen. Das bedeutet: Das Backend verarbeitet die Datei weiterhin vollständig und führt Validierung und Import ganz normal zu Ende. Wenn der User später wieder auf die Seite zurückkehrt und aktualisiert, sieht er die neu importierten Verträge. Aus Backend-Sicht ist dieses Verhalten korrekt, da der Server unabhängig vom Browser des Users weiterarbeitet. Ein Seitenwechsel oder Refresh hat keinen Einfluss auf die Verarbeitung. Da das Anzeigen der Verträge nicht explizit Teil der Aufgabenstellung war, würde ich die folgenden Verbesserungsideen als optional kennzeichnen:

Einen Benutzerhinweis anzeigen wie „Die Verarbeitung läuft noch. Möchten Sie die Seite wirklich verlassen?“

Eine Progressbar anzeigen.

Den Upload abbrechen, wenn der User die Seite verlässt oder aktualisiert – das widerspricht allerdings der Aufgabenstellung, die explizit verlangt, dass der Import robust sein soll.

Die Validierung der Datumsfelder übernimmt vollständig Pydantic. Falsch formatierte Daten werden automatisch erkannt und führen zu Standard-Fehlermeldungen wie „Input should be a valid date or datetime“. Diese Meldungen werden durch mein Error-Handling unverändert an das Frontend weitergegeben. Man könnte überlegen, diese Meldungen für User lesbarer zu gestalten.
