import nltk
from nltk.tokenize import word_tokenize

from textblob_de import TextBlobDE
import nlp_melanie
from nlp_melanie import *
import nltk.data
import re


#### Termextraktion: Alle Nomen und Namen aus einem Text ####


#erst mache ich eine Terminologie-Liste auf

terms = []

#dann frage ich, aus welchem Text ich extrahieren soll

#textfile = input("Aus welchem Text soll ich extrahieren?\n")

#text = open(textfile,'r', encoding='utf-8')

#lines = text.readlines()

#jetzt eine Stoppwortliste

stoppwortliste = ("&", "Das","Ihrem","Ihres", "Ihr", "Sie","\ufeff3",'fürs','http','https','–','•','3','~','03erfolgte','1a','%','\$\/€',
                  "%-igen","\'",'*','+',"\'%3E%3C\/script%3E","\'\/ebanzwww\/","\'\/ebanzwww\/contentloader",
                  "\'\/ebanzwww\/wexsservlet", "\'Hair", "\'https", "\'ISIN", "\'s", "\'session\.sessionid=0c20b7b2f963372e84459686a04d3c05",
                  "\'text\/javascript", "\+", "\/\/publikations-plattform.de\/sp\/wexsservlet", "\/\/www\.bundesanzeiger\.de\/", "\/css", "\images", "\=", "\[", "\]")



#dann extrahiere ich alle Wörter mit einem POS-Tag, der mit "N" anfängt

def termex_nouns(txt):
    myblob = TextBlobDE(txt)
    pos = myblob.tags
    for item in pos:
        if item[1].startswith('N'):
            terms.append(item)
    return(terms)
   
    
''' ein anderer Ansatz, für Deutsch gültig:
Ich extrahiere alle Wörter, die mit einem Großbuchstaben beginnen, außer denen am Satzanfang.
Dazu nehme ich alle Nomen am Satzanfang. 
Wenn mehrere Wörter mit Großbuchstaben hintereinander stehen, nehme ich sie als Mehrwortlexem auf.
'''

def termex_capital(sentence):
    pos = TextBlobDE(sentence).tags
    if len(pos) > 0:
        first_word = pos[0]
        if first_word[1].startswith('N'):
            term = first_word[0]
    for word in pos[1:]:
        if word[0][0].isupper() and word[0] not in stoppwortliste:
            term = word[0]
            try:
                next_word = pos[pos.index(word) +1]
                if next_word[0][0].isupper() and next_word[0] not in stoppwortliste:
                    term = term + ' ' + next_word[0]
                    try:
                        nextnext_word = pos[pos.index(word) +2]
                        if nextnext_word[0][0].isupper()and nextnext_word[0] not in stoppwortliste:
                            term = term + ' ' + nextnext_word[0]
                    except IndexError:
                        term = term
            except IndexError:
                    term = term
            terms.append(term)
    return(terms)



# Terme in der Stoppwortliste werden rausgeworfen

def delete_stopwords(sorted_terms): 
    for term in sorted_terms:
        if term[0] in stoppwortliste:
            sorted_terms.remove(term)
    return(sorted_terms)

# Ab hier die Aufrufe:
# Zuerst die Termextraktion mit Nomen:

def termex_n():
    terms = []
    textfile = input("Aus welchem Text soll ich extrahieren?\n")
    text = open(textfile,'r', encoding='utf-8')
    lines = text.readlines()
    for line in lines:
        terms = termex_nouns(line)
    terms = delete_stopwords(terms)
#die Liste mit Tuples wird auch noch sortiert (unabhängig von Groß- und Kleinschreibung
#und dann Duplikate rausgeworfen
    sorted_terms = sorted(set(terms), key=lambda terms:(terms[0].lower()))
#    sorted_terms = delete_stopwords(sorted_terms)
    print("TERMEXTRAKTION NOMEN:")
    for term in sorted_terms:
        print(term[0])
#jetzt schreibe ich das Ganze in eine Datei
    terms_out = open('terms_out','w', encoding='utf-8')
    for term in sorted_terms:
        terms_out.write(term[0])
        terms_out.write(':\tPOS: ')
        terms_out.write(term[1])
        terms_out.write('\n')
    terms_out.close()
    text.close()


#Hier die Termextraktion auf Basis von Großbuchstaben

def termex_cap():
    terms = []
    textfile = input("Aus welchem Text soll ich extrahieren?\n")
    text = open(textfile,'r', encoding='utf-8')
    lines = text.readlines()
    for line in lines:
        sents = TextBlobDE(line).sentences
        for sent in sents:
             if len(sent)>0:
#                print(sent)
                terms = termex_capital(str(sent))
    terms = delete_stopwords(terms)
    sorted_terms = sorted(set(terms), key=lambda terms:(terms[0].lower()))
#    print("SORTED TERMS: " + str(sorted_terms))
#    sorted_terms = delete_stopwords(sorted_terms)
    print("TERMEXTRAKTION GROSS:")
    for t in sorted_terms:
        print(t)
#jetzt schreibe ich das Ganze in eine Datei
    terms_out = open('terms_out','w', encoding='utf-8')
    for term in sorted_terms:
        terms_out.write(str(term))
        terms_out.write('\t' + lemmatize_sentence(term))
        terms_out.write('\n')
    terms_out.close()
    text.close()



#Hier die Termextraktion auf Basis von Differenzanalyse

#hier sind die 1.000 häufigsten Wörter aus dem Wortschatz Leipzig

haeufige_deutsche_Woerter = ['.', ',', '50', '20', '100', 'der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich', 'des', 'auf', 'für', 'ist', 'im', 'dem', 'nicht', 'ein', 'Die', 'eine', 'als', 'auch', 'es', 'an', 'werden', 'aus', 'er', 'hat', 'daß', 'sie', 'nach', 'wird', 'bei', 'einer', 'Der', 'um', 'am', 'sind', 'noch', 'wie', 'einem', 'über', 'einen', 'Das', 'so', 'Sie', 'zum', 'war', 'haben', 'nur', 'oder', 'aber', 'vor', 'zur', 'bis', 'mehr', 'durch', 'man', 'sein', 'wurde', 'sei', 'In', 'Prozent', 'hatte', 'kann', 'gegen', 'vom', 'können', 'schon', 'wenn', 'habe', 'seine', 'Mark', 'ihre', 'dann', 'unter', 'wir', 'soll', 'ich', 'eines', 'Es', 'Jahr', 'zwei', 'Jahren', 'diese', 'dieser', 'wieder', 'keine', 'Uhr', 'seiner', 'worden', 'Und', 'will', 'zwischen', 'Im', 'immer', 'Millionen', 'Ein', 'was', 'sagte', 'Er', 'gibt', 'alle', 'DM', 'diesem', 'seit', 'muß', 'wurden', 'beim', 'doch', 'jetzt', 'waren', 'drei', 'Jahre', 'Mit', 'neue', 'neuen', 'damit', 'bereits', 'da', 'Auch', 'ihr', 'seinen', 'müssen', 'ab', 'ihrer', 'Nach', 'ohne', 'sondern', 'selbst', 'ersten', 'nun', 'etwa', 'Bei', 'heute', 'ihren', 'weil', 'ihm', 'seien', 'Menschen', 'Deutschland', 'anderen', 'werde', 'Ich', 'sagt', 'Wir', 'Eine', 'rund', 'Für', 'Aber', 'ihn', 'Ende', 'jedoch', 'Zeit', 'sollen', 'ins', 'Wenn', 'So', 'seinem', 'uns', 'Stadt', 'geht', 'Doch', 'sehr', 'hier', 'ganz', 'erst', 'wollen', 'Berlin', 'vor allem', 'sowie', 'hatten', 'kein', 'deutschen', 'machen', 'lassen', 'Als', 'Unternehmen', 'andere', 'ob', 'dieses', 'steht', 'dabei', 'wegen', 'weiter', 'denn', 'beiden', 'einmal', 'etwas', 'Wie', 'nichts', 'allerdings', 'vier', 'gut', 'viele', 'wo', 'viel', 'dort', 'alles', 'Auf', 'wäre', 'SPD', 'kommt', 'vergangenen', 'denen', 'fast', 'fünf', 'könnte', 'nicht nur', 'hätten', 'Frau', 'Am', 'dafür', 'kommen', 'diesen', 'letzten', 'zwar', 'Diese', 'großen', 'dazu', 'Von', 'Mann', 'Da', 'sollte', 'würde', 'also', 'bisher', 'Leben', 'Milliarden', 'Welt', 'Regierung', 'konnte', 'ihrem', 'Frauen', 'während', 'Land', 'zehn', 'würden', 'stehen', 'ja', 'USA', 'heißt', 'dies', 'zurück', 'Kinder', 'dessen', 'ihnen', 'deren', 'sogar', 'Frage', 'gewesen', 'erste', 'gab', 'liegt', 'gar', 'davon', 'gestern', 'geben', 'Teil', 'Polizei', 'dass', 'hätte', 'eigenen', 'kaum', 'sieht', 'große', 'Denn', 'weitere', 'Was', 'sehen', 'macht', 'Angaben', 'weniger', 'gerade', 'läßt', 'Geld', 'München', 'deutsche', 'allen', 'darauf', 'wohl', 'später', 'könne', 'deshalb', 'aller', 'kam', 'Arbeit', 'mich', 'gegenüber', 'nächsten', 'bleibt', 'wenig', 'lange', 'gemacht', 'Wer', 'Dies', 'Fall', 'mir', 'gehen', 'Berliner', 'mal', 'Weg', 'CDU', 'wollte', 'sechs', 'keinen', 'Woche', 'dagegen', 'alten', 'möglich', 'gilt', 'erklärte', 'müsse', 'Dabei', 'könnten', 'Geschichte', 'zusammen', 'finden', 'Tag', 'Art', 'erhalten', 'Man', 'Dollar', 'Wochen', 'jeder', 'nie', 'bleiben', 'besonders', 'Jahres', 'Deutschen', 'Den', 'Zu', 'zunächst', 'derzeit', 'allein', 'deutlich', 'Entwicklung', 'weiß', 'einige', 'sollten', 'Präsident', 'geworden', 'statt', 'Bonn', 'Platz', 'inzwischen', 'Nur', 'Freitag', 'Um', 'pro', 'seines', 'Damit', 'Montag', 'Europa', 'schließlich', 'Sonntag', 'einfach', 'gehört', 'eher', 'oft', 'Zahl', 'neben', 'hält', 'weit', 'Partei', 'meisten', 'Thema', 'zeigt', 'Politik', 'Aus', 'zweiten', 'Januar', 'insgesamt', 'je', 'mußte', 'Anfang', 'hinter', 'ebenfalls', 'ging', 'Mitarbeiter', 'darüber', 'vielen', 'Ziel', 'darf', 'Seite', 'fest', 'hin', 'erklärt', 'Namen', 'Haus', 'An', 'Frankfurt', 'Gesellschaft', 'Mittwoch', 'damals', 'Dienstag', 'Hilfe', 'Mai', 'Markt', 'Seit', 'Tage', 'Donnerstag', 'halten', 'gleich', 'nehmen', 'solche', 'Entscheidung', 'besser', 'alte', 'Leute', 'Ergebnis', 'Samstag', 'Daß', 'sagen', 'System', 'März', 'tun', 'Monaten', 'kleinen', 'lang', 'Nicht', 'knapp', 'bringen', 'wissen', 'Kosten', 'Erfolg', 'bekannt', 'findet', 'daran', 'künftig', 'wer', 'acht', 'Grünen', 'schnell', 'Grund', 'scheint', 'Zukunft', 'Stuttgart', 'bin', 'liegen', 'politischen', 'Gruppe', 'Rolle', 'stellt', 'Juni', 'sieben', 'September', 'nämlich', 'Männer', 'Oktober', 'Mrd', 'überhaupt', 'eigene', 'Dann', 'gegeben', 'Außerdem', 'Stunden', 'eigentlich', 'Meter', 'ließ', 'Probleme', 'vielleicht', 'ebenso', 'Bereich', 'zum Beispiel', 'Bis', 'Höhe', 'Familie', 'Während', 'Bild', 'Ländern', 'Informationen', 'Frankreich', 'Tagen', 'schwer', 'zuvor', 'Vor', 'genau', 'April', 'stellen', 'neu', 'erwartet', 'Hamburg', 'sicher', 'führen', 'Mal', 'Über', 'mehrere', 'Wirtschaft', 'Mio', 'Programm', 'offenbar', 'Hier', 'weiteren', 'natürlich', 'konnten', 'stark', 'Dezember', 'Juli', 'ganze', 'kommenden', 'Kunden', 'bekommen', 'eben', 'kleine', 'trotz', 'wirklich', 'Lage', 'Länder', 'leicht', 'gekommen', 'Spiel', 'laut', 'November', 'kurz', 'politische', 'führt', 'innerhalb', 'unsere', 'meint', 'immer wieder', 'Form', 'Münchner', 'AG', 'anders', 'ihres', 'völlig', 'beispielsweise', 'gute', 'bislang', 'August', 'Hand', 'jede', 'GmbH', 'Film', 'Minuten', 'erreicht', 'beide', 'Musik', 'Kritik', 'Mitte', 'Verfügung', 'Buch', 'dürfen', 'Unter', 'jeweils', 'einigen', 'Zum', 'Umsatz', 'spielen', 'Daten', 'welche', 'müßten', 'hieß', 'paar', 'nachdem', 'Kunst', 'Euro', 'gebracht', 'Problem', 'Noch', 'jeden', 'Ihre', 'Sprecher', 'recht', 'erneut', 'längst', 'europäischen', 'Sein', 'Eltern', 'Beginn', 'besteht', 'Seine', 'mindestens', 'machte', 'Jetzt', 'bietet', 'außerdem', 'Bürger', 'Trainer', 'bald', 'Deutsche', 'Schon', 'Fragen', 'klar', 'Durch', 'Seiten', 'gehören', 'Dort', 'erstmals', 'Februar', 'zeigen', 'Titel', 'Stück', 'größten', 'FDP', 'setzt', 'Wert', 'Frankfurter', 'Staat', 'möchte', 'daher', 'wolle', 'Bundesregierung', 'lediglich', 'Nacht', 'Krieg', 'Opfer', 'Tod', 'nimmt', 'Firma', 'zuletzt', 'Werk', 'hohen', 'leben', 'unter anderem', 'Dieser', 'Kirche', 'weiterhin', 'gebe', 'gestellt', 'Mitglieder', 'Rahmen', 'zweite', 'Paris', 'Situation', 'gefunden', 'Wochenende', 'internationalen', 'Wasser', 'Recht', 'sonst', 'stand', 'Hälfte', 'Möglichkeit', 'versucht', 'blieb', 'junge', 'Mehrheit', 'Straße', 'Sache', 'arbeiten', 'Monate', 'Mutter', 'berichtet', 'letzte', 'Gericht', 'wollten', 'Ihr', 'zwölf', 'zumindest', 'Wahl', 'genug', 'Weise', 'Vater', 'Bericht', 'amerikanischen', 'hoch', 'beginnt', 'Wort', 'obwohl', 'Kopf', 'spielt', 'Interesse', 'Westen', 'verloren', 'Preis', 'Erst', 'jedem', 'erreichen', 'setzen', 'spricht', 'früher', 'teilte', 'Landes', 'zudem', 'einzelnen', 'bereit', 'Blick', 'Druck', 'Bayern', 'Kilometer', 'gemeinsam', 'Bedeutung', 'Chance', 'Politiker', 'Dazu', 'Zwei', 'besten', 'Ansicht', 'endlich', 'Stelle', 'direkt', 'Beim', 'Bevölkerung', 'Viele', 'solchen', 'Alle', 'solle', 'jungen', 'Einsatz', 'richtig', 'größte', 'sofort', 'neuer', 'ehemaligen', 'unserer', 'dürfte', 'schaffen', 'Augen', 'Rußland', 'Internet', 'Allerdings', 'Raum', 'Mannschaft', 'neun', 'kamen', 'Ausstellung', 'Zeiten', 'Dem', 'einzige', 'meine', 'Nun', 'Verfahren', 'Angebot', 'Richtung', 'Projekt', 'niemand', 'Kampf', 'weder', 'tatsächlich', 'Personen', 'dpa', 'Heute', 'geführt', 'Gespräch', 'Kreis', 'Hamburger', 'Schule', 'guten', 'Hauptstadt', 'durchaus', 'Zusammenarbeit', 'darin', 'Amt', 'Schritt', 'meist', 'groß', 'zufolge', 'Sprache', 'Region', 'Punkte', 'Vergleich', 'genommen', 'gleichen', 'du', 'Ob', 'Soldaten', 'Universität', 'verschiedenen', 'Kollegen', 'neues', 'Bürgermeister', 'Angst', 'stellte', 'Sommer', 'danach', 'anderer', 'gesagt', 'Sicherheit', 'Macht', 'Bau', 'handelt', 'Folge', 'Bilder', 'lag', 'Osten', 'Handel', 'sprach', 'Aufgabe', 'Chef', 'frei', 'dennoch', 'DDR', 'hohe', 'Firmen', 'bzw', 'Koalition', 'Mädchen', 'Zur', 'entwickelt', 'fand', 'Diskussion', 'bringt', 'Deshalb', 'Hause', 'Gefahr', 'per', 'zugleich', 'früheren', 'dadurch', 'ganzen', 'abend', 'erzählt', 'Streit', 'Vergangenheit', 'Parteien', 'Verhandlungen', 'jedenfalls', 'gesehen', 'französischen', 'Trotz', 'darunter', 'Spieler', 'forderte', 'Beispiel', 'Meinung', 'wenigen', 'Publikum', 'sowohl', 'meinte', 'mag', 'Auto', 'Lösung', 'Boden', 'Einen', 'Präsidenten', 'hinaus', 'Zwar', 'verletzt', 'weltweit', 'Sohn', 'bevor', 'Peter', 'mußten', 'keiner', 'Produktion', 'Ort', 'braucht', 'Zusammenhang', 'Kind', 'Verein', 'sprechen', 'Aktien', 'gleichzeitig', 'London', 'sogenannten', 'Richter', 'geplant', 'Italien', 'Mittel', 'her', 'freilich', 'Mensch', 'großer', 'Bonner', 'wenige', 'öffentlichen', 'Unterstützung', 'dritten', 'nahm', 'Bundesrepublik', 'Arbeitsplätze', 'bedeutet', 'Feld', 'Dr.', 'Bank', 'oben', 'gesetzt', 'Ausland', 'Ministerpräsident', 'Vertreter', 'z.B.', 'jedes', 'ziehen', 'Parlament', 'berichtete', 'Dieses', 'China', 'aufgrund', 'Stellen', 'warum', 'Kindern', 'heraus', 'heutigen', 'Anteil', 'Herr', 'Öffentlichkeit', 'Abend', 'Selbst', 'Liebe', 'Neben', 'rechnen', 'fällt', 'New York', 'Industrie', 'WELT', 'Stuttgarter', 'wären', 'Vorjahr', 'Sicht', 'Idee', 'Banken', 'verlassen', 'Leiter', 'Bühne', 'insbesondere', 'offen', 'stets', 'Theater', 'ändern', 'entschieden', 'Staaten', 'Experten', 'Gesetz', 'Geschäft', 'Tochter', 'angesichts', 'gelten', 'Mehr', 'erwarten', 'läuft', 'fordert', 'Japan', 'Sieg', 'Ist', 'Stimmen', 'wählen', 'russischen', 'gewinnen', 'CSU', 'bieten', 'Nähe', 'jährlich', 'Bremen', 'Schüler', 'Rede', 'Funktion', 'Zuschauer', 'hingegen', 'anderes', 'Führung', 'Besucher', 'Drittel', 'Moskau', 'immerhin', 'Vorsitzende', 'Urteil', 'Schließlich', 'Kultur', 'betonte', 'mittlerweile', 'Saison', 'Konzept', 'suchen', 'Zahlen', 'Roman', 'Gewalt', 'Köln', 'gesamte', 'indem', 'EU', 'Stunde', 'ehemalige', 'Auftrag', 'entscheiden', 'genannt', 'tragen', 'Börse', 'langen', 'häufig', 'Chancen', 'Vor allem', 'Position', 'alt', 'Luft', 'Studenten', 'übernehmen', 'stärker', 'ohnehin', 'zeigte', 'geplanten', 'Reihe', 'darum', 'verhindern', 'begann', 'Medien', 'verkauft', 'Minister', 'wichtig', 'amerikanische', 'sah', 'gesamten', 'einst', 'verwendet', 'vorbei', 'Behörden', 'helfen', 'Folgen', 'bezeichnet']
sorted_stopwords = sorted(set(haeufige_deutsche_Woerter), key=lambda haeufige_deutsche_Woerter:(haeufige_deutsche_Woerter.lower()))

def termex_diff():
    terms = []
    textfile = input("Aus welchem Text soll ich extrahieren?\n")
    text = open(textfile,'r', encoding='utf-8')
    lines = text.readlines()
    for line in lines:
        line_terms = word_tokenize(line)
        terms = terms + line_terms
    sorted_terms = sorted(set(terms))
    terms = list(set(sorted_terms) - set(sorted_stopwords))
    terms = delete_stopwords(terms)
    terms = sorted(set(terms))
    print("TERMEXTRAKTION DIFFERENZANALYSE:")
    for t in terms:
        print(t)
    terms_out = open('terms_out','w', encoding='utf-8')
    for term in terms:
        terms_out.write(term + '\n')
    terms_out.close()
    text.close()
