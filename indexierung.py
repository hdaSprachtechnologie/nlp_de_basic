import nltk
from nltk.tokenize import word_tokenize
from textblob_de import TextBlobDE
import nlp_melanie
from nlp_melanie import *
import nltk.data
import re
import spacy
nlp = spacy.load('de')

# Automatische Indexierung für Mareike


#erst mache ich eine Terminologie-Liste auf

terms = []

''' Ansatz, für Deutsch gültig:
Ich extrahiere alle Wörter, die mit einem Großbuchstaben beginnen, außer denen am Satzanfang.
Dazu nehme ich alle Nomen am Satzanfang. 
Wenn mehrere Wörter mit Großbuchstaben hintereinander stehen, nehme ich sie als Mehrwortlexem auf.
'''

def termex_capital(sentence):
    terms = []
    pos = TextBlobDE(sentence).tags
    if len(pos) > 0:
        first_word = pos[0]
        if first_word[1].startswith('N'):
            term = lemmatize_word(first_word[0])
            terms.append(term)
    for word in pos[1:]:
          if word[0][0].isupper() or word[0] in ['kein', 'ohne']:
            term = lemmatize_word(word[0])
            try:
                next_word = pos[pos.index(word) +1]
#                print("NEXT_WORD: " + str(next_word))
                if next_word[0] in ['Ihres']:
                    term = term + ' ' + "des"
                    try:
                        nextnext_word = pos[pos.index(word) +2]
#                        if nextnext_word[0][0].isupper()and nextnext_word[0] not in stoppwortliste_strict:
                        if nextnext_word[0][0].isupper():
                            term = term + ' ' + nextnext_word[0]
                    except IndexError:
                        term = lemmatize_word(term)
                elif next_word[0][0].isupper():
                    term = term + ' ' + lemmatize_word(next_word[0])
                    try:
                        nextnext_word = pos[pos.index(word) +2]
#                        if nextnext_word[0][0].isupper()and nextnext_word[0] not in stoppwortliste_strict:
                        if nextnext_word[0][0].isupper():
                            term = term + ' ' + lemmatize_word(nextnext_word[0])
                    except IndexError:
                        term = lemmatize_word(term)
                elif next_word[0] in ['des', 'eines', 'einer', 'der', 'beim']:
                    term = term + ' ' + next_word[0]
                    try:
                        nextnext_word = pos[pos.index(word) +2]
#                        if nextnext_word[0][0].isupper()and nextnext_word[0] not in stoppwortliste_strict:
                        if nextnext_word[0][0].isupper():
                            term = term + ' ' + nextnext_word[0]
                    except IndexError:
                        term = lemmatize_word(term)
            except IndexError:
                    term = lemmatize_word(term)
            terms.append(term)
    return(terms)

'''
nächster Versuch: Information aus spacy nutzen


def termex_entities(txt):
    doc = nlp(txt)
    dep_analysis = []
    termstring = ''
    for token in doc:
        dep_analysis.append((token.lemma_, token.pos_, token.dep_, token.head.text, token.text))
        print(str(dep_analysis))
    for a in dep_analysis:
        if a[1] == 'NOUN':
            termstring = termstring + a[0]
    
'''

'''
Jetzt extrahiere ich alle Verben
'''

def termex_verbs(txt):
    myblob = TextBlobDE(txt)
    pos = myblob.tags
    for item in pos:
        if item[1].startswith('V'):
            terms.append(item[0])
    return(terms)

#jetzt eine Stoppwortliste

stoppwortliste = ["&", "Das","Ihrem","Ihres", "Ihr", "Ihre", "Sie","\ufeff3",'fürs','http','https','–','•','3','~','03erfolgte','1a','%','\$\/€',
                  "%-igen","\'",'*','+',"\'%3E%3C\/script%3E","\'\/ebanzwww\/","\'\/ebanzwww\/contentloader",
                  "\'\/ebanzwww\/wexsservlet", "\'Hair", "\'https", "\'ISIN", "\'s", "\'session\.sessionid=0c20b7b2f963372e84459686a04d3c05",
                  "\'text\/javascript", "\+", "\/\/publikations-plattform.de\/sp\/wexsservlet", "\/\/www\.bundesanzeiger\.de\/", "\/css", "\images", "\=", "\[", "\]",
                  "|", "wollen", "müssen", "Anleitung", "Anzeigefeld", "Anzeigefelder", "Aufruf", "Datev", "DATEV-Hilfe", "DATEV", "Eingaben bestätigen", "Eintrag auswählen", "Erfassung", "Fenster auswählen",
                  "Klick", "Klicken", "Mitarbeiter", "Programm errechnen", "Schlagwörter", "Seite", "Speicher", "Speichern", "Taste", "Taste drücken", "Vorgang", "Wert",
                  "Werte tragen", "Werte eintragen", "zuständig Mitarbeiter", "geben Sie", "Fenster ausauswählen", "Fenster", "Eintrag",
                  'Eingabefeld zuständig', "zuständig", "Anleitung", "Posteingang erfassen", "Erstempfänger übersenden", "Eingangsart öffnen",
                  'Eintrag auswählen', "Datum Eingangsdatum", "Vorgehen", "Datensicht Posteingang", "Anleitung", "Programm", "Programm errechnen"]



# Tuple im Ergebnis in String umwandeln

def tup2str(index_result):
    new_index = []
    for term in index_result:
        if isinstance(term,tuple):
            term_new = ' '.join(term)
            new_index.append(term_new)
        else:
            new_index.append(term)
    return(new_index)



'''
Jetzt versuche ich Verben und ihre Argumente, indem ich den spacy-Dependenzparser verwende
'''

def termex_verb_args(txt):
    dep_analysis = []
    sbj = []
    obj = []
    verb = []
    terms = []
    doc = nlp(txt)
    for token in doc:
        dep_analysis.append((token.lemma_, token.pos_, token.dep_, token.head.text, token.text))
#    print(str(dep_analysis))
    for a in dep_analysis:
#        if a[2] == 'sb' and a[4] not in stoppwortliste and a[1] != 'PRON':
        if a[2] == 'sb' and a[1] != 'PRON':
            vlemma = lemmatize_word(a[3])
            sbj.append((a[4],vlemma))
#        elif a[2] == 'oa' and a[4] not in stoppwortliste:
        elif a[2] == 'oa':
            vlemma = lemmatize_word(a[3])
            obj.append((a[4],vlemma))
#        elif a[2] == 'da' and a[4] not in stoppwortliste:
        elif a[2] == 'da':
            vlemma = lemmatize_word(a[3])
            obj.append((a[4],vlemma))
#        elif a[1] == 'VERB' and a[0] not in stoppwortliste:
        elif a[1] == 'VERB':
                if a[3] in ['werden','wird']:
                    sbj = [tuple(map(lambda i: str.replace(i,'werden',a[0]),tup)) for tup in sbj]
                    obj = [tuple(map(lambda i: str.replace(i,'werden',a[0]),tup)) for tup in obj]
                    verb.append(lemmatize_word(a[0]))
        elif a[1] == 'PART' and a[0] not in ['zu']:
            oldverbterm = lemmatize_word(a[3].lower())
#            print("OLDVERBTERM: " + oldverbterm)
            newverbterm = lemmatize_word(a[4] + a[3].lower())
#            print("NEWVERBTERM: " + newverbterm)
            sbj = [tuple(map(lambda i: str.replace(i,oldverbterm,newverbterm),tup)) for tup in sbj]
            obj = [tuple(map(lambda i: str.replace(i,oldverbterm,newverbterm),tup)) for tup in obj]
            verb.append(newverbterm)
#                else:
#                    verb.append(lemmatize_word(a[0]))
#    lterms = lterms + sbj + obj + verb
#    indexterms = sbj + obj + verb
    indexterms = sbj + obj
    new_index = tup2str(indexterms)
    return(new_index)


# Terme in der Stoppwortliste werden rausgeworfen

def delete_stopwords(sorted_terms):
    sorted_terms_new = []
    for term in sorted_terms:
#        print('ICH SEHE MIR JETZT AN: ' + term)
        if 'Ihres' in term or 'Ihre' in term or 'Ihrem' in term:
            sorted_terms_new = sorted_terms_new
        elif term not in stoppwortliste:
#            print(term + " IN STOPPWORTLISTE")
            sorted_terms_new.append(term)
#            print("REMOVED: " + str(term))
        else:
            sorted_terms_new = sorted_terms_new
    return(sorted_terms_new)

def delete_slashwords(sorted_terms):
    for term in sorted_terms:
        if "/" in term:
#            print("TERM WITH SLASH: " + term)
            terms = term.split("/")
            sorted_terms.remove(term)
            for t in terms:
                sorted_terms.append(t)
    return(sorted_terms)

#Hier die Termextraktion auf Basis von Großbuchstaben und Verb-Argumenten

def indexierung(textfile):
    terms = []
    text = open(textfile,'r', encoding='utf-8')
    lines = text.readlines()
    for line in lines:
        sents = TextBlobDE(line).sentences
        for sent in sents:
             if len(sent)>0:
#                print(sent)
                terms = terms + termex_capital(str(sent)) + termex_verb_args(str(sent))
#                print(str(terms))
    terms = delete_stopwords(terms)
    terms = delete_slashwords(terms)
    sorted_terms = sorted(set(terms), key=lambda terms:(terms[0].lower()))
#    print("SORTED TERMS: " + str(sorted_terms))
#    sorted_terms = delete_stopwords(sorted_terms)
#    print("TERMEXTRAKTION GROSS:")
    for t in sorted_terms:
        print(t)
#jetzt schreibe ich das Ganze in eine Datei
    terms_out = open('terms_out.txt','w', encoding='utf-8')
    for term in sorted_terms:
        if isinstance(term,tuple):
            term = ' '.join(term)
#        terms_out.write(str(term))
        terms_out.write('\t' + lemmatize_sentence(term))
        terms_out.write('\n')
    terms_out.close()
    text.close()
    return(sorted_terms)

# Hier die Indexierung für einen Satz

def index(sent):
    terms = []
#    print(str(terms))
    terms = terms + termex_capital(str(sent)) + termex_verb_args(str(sent))
#    print(str(terms))
    terms = delete_stopwords(terms)
    terms = delete_slashwords(terms)
    sorted_terms = sorted(set(terms), key=lambda terms:(terms[0].lower()))
#    print(str(sorted_terms))
    for term in sorted_terms:
        if isinstance(term,tuple):
            term = ' '.join(term)
        print(term)


# Vergleich mit dem Gold-Standard

gold_index = ["abgleichen", "Bekanntgabedatum", "Bekanntgabedatum errechnen", "berechnen", "Bescheid", "Bescheid abgleichen",
              "Bescheid abgleichen mit Steuererklärung", "Bescheiddaten abgleichen", "Bescheiddaten abgleichen mit Steuererklärung",
              "Daten abgleichen", "Datum eingeben", "Dokumentdatum", "Dokumentdatum abgleichen", "Dokumentdatum abgleichen mit Eingangsdatum",
              "Dokumentdatum eingeben", "Dokument", "eingeben", "Eingangsart", "Eingangsart erfassen", "Eingangsdatum", "Eingangsdatum abgleichen",
              "Empfangsvollmacht", "ohne Empfangsvollmacht", "Empfangsvollmacht des Mandanten", "erfassen", "Erstempfänger",
              "Finanzamt", "Frist-Ende", "Frist-Ende berechnen", "Fristendedatum", "Fristendedatum berechnen",
              "Institution", "Mandant", "Posteingang", "Posteingang bei Mandant", "Posteingang beim Erstempfänger", "Steuererklärung",
              "Steuererklärung abgleichen", "Steuererklärung abgleichen mit Bescheid", "Vorfrist", "Vorfrist berechnen", "Wiedereinsetzung", "Wiedereinsetzungsende",
              "Wiedereinsetzungsende berechnen", "Fristerfassung", "Nummer des Mitarbeiters", 'Bescheid erteilen', "Eingabe", 'Finanzamt auswählen',
              "Steuerart", "Bescheidabgleich", "Veranlagungsjahr", "Post", "Frist", "Fristen", "Nummer des Finanzamts", 'Bescheide übersenden', 'Mitarbeiter auswählen',
              'Erfassung abschließen', 'Vorgang bearbeiten']


def evaluate_index():
    my_terms = indexierung("Dokument_9216772.txt")
    for term in my_terms:
        if isinstance(term,tuple):
            term = ' '.join(term)
    not_found = list(set(gold_index) - set(my_terms))
    print("Nicht gefundene Terme: " + str(not_found))
    add_found = list(set(my_terms) - set(gold_index))
    print("Zusätzlich gefundene Terme: " + str(add_found))


'''
Wie geht's weiter?

Verben ohne Argumente rausnehmen
DONE

abgleichen mit:
wenn Sie anschließend auf der Registerkarte Bescheidabgleich die Daten des Bescheids mit den Daten der Steuererklärung abgleichen wollen
-> Daten der Steuererklärung abgleichen, Daten des Bescheids abgleichen


Falls Sie keine Empfangsvollmacht Ihres Mandanten besitzen, werden die Bescheide von den Institutionen zunächst dem Erstempfänger, Ihrem Mandanten, übersendet.
-> Empfangsvollmacht des Mandanten
DONE
-> Erstempfänger Mandant

Daher müssen Sie das Dialogfenster Posteingang beim Erstempfänger (Mandant) erfassen.
-> Erstempfänger Mandant

Partikelverben:
DONE

komplexe Argumente:
Geben Sie in das Eingabefeld Dokumentdatum das Datum des Dokuments ein
-> Datum des Dokuments eingeben
Das Programm errechnet das Bekanntgabedatum, Wiedereinsetzungsende, die Vorfrist und das Fristendedatum und trägt die Werte in die entsprechenden Anzeigefelder ein.
-> Fristendedatum errechnen

Negationen:
Frist-Ende berechnen - ohne Empfangsvollmacht
-> Empfangsvollmacht, ohne
DONE

Verben nicht ohne Argumente extrahieren, bis auf Ausnahmen?
DONE

Nominalisierungen von Verben ins Indexat aufnehmen

Stoppwörter (am Ende filtern):
DONE

Ändern:
Empfangsvollmacht Ihres Mandanten -> Empfangsvollmacht des Mandanten
DONE
Ihre Eingabe -> Eingabe
DONE
Mandant/Steuerart/Veranlagungsjahr -> Mandant, Steuerart, Veranlagungsjahr
DONE

'''
