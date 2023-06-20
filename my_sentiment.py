import re
#from sentiment_words import sentiments
import spacy
nlp = spacy.load('de_core_news_sm')
import pandas as pd


#df_sentiment = pd.read_csv("202306012_sentiment_wordlist.tsv", sep="\t")
df_sentiment = pd.read_csv("sentiment_words.tsv", sep="\t")
sentiments = df_sentiment.set_index("word")["sentiment"].to_dict()


negations = ("NIE", 'nicht', 'nich', 'kein', 'keine', "Keine", "ohne", "nie", "nein", "keiner", "nichts", "weder", "Weder", 'garnicht',
             'statt', 'Nix', 'nix', 'wäre','Wäre', ":-)", "Gegensatz", "kaum", "Niemand", "nullen", "null")

verstaerker = ('sehr', 'total', 'enorm', 'häufig', 'wirklich', 'völlig','voellig',
               'absolut', 'rein', 'endlich', 'vollstes', 'viel', 'hoffen', 'genug', 'Ziemlich',
               'scharf', 'ziemlich', 'kolossalen', 'kolossale', 'kolossales', 'stark', 'hohes',
               'hohe', "zusätzlichen", 'lupenreinen', 'absolut', 'schleichend', 'definitiv', 'besonders', 'Besonders')

ironie = ('NICHT', 'Nicht','Ironie', 'ironie','#ironie', 'ManManMan')

# Das hier brauchen wir für Emojis und andere komische Buchstaben

def bmp(s):
    return "".join((i if ord(i) < 10000 else '\ufffd' for i in s))



sent_score = 0

# Einfache Sentiment-Analyse mit Wortlistenabgleich

def sentiment(testsatz):
    testsatz = bmp(testsatz)
    testsatz = testsatz.replace('|LBR|','')
    scount = 0
    neg_score = 1
    sent_score = 1
    doc=nlp(testsatz)
    if ('?') in testsatz:
        scount = 0
        sent_score = 0
    elif("Wenn") in testsatz:
        scount = 0
        sent_score = 0
    else:
        for token in doc:
            wcount=0
            word_lemma = token.lemma_
            if token.text in ironie:
                return -1.0
            elif token.text in negations:
                neg_score = -1.0
#                print("WORD: " + word + " NEGATION")
                wcount = '0'
            elif token.text in verstaerker:
                neg_score = 1.5
 #               print("WORD: " + word + " VERSTÄRKER")
                wcount = '0'
            elif word_lemma in sentiments.keys():
                wcount = float(sentiments[word_lemma]) * neg_score
  #              print("WORD: " + word + ': ' + str(wcount))
                neg_score = 1
                sent_score = 1
            else:
                wcount = '0'
            scount = scount + float(wcount)
    return(scount)

def detect_irony(testsatz):
    doc=nlp(testsatz)
    for token in doc:
        if token.text in ironie:
            return "IRONIC"
        


'''
Negation mit der Dependenzanalyse von Spacy. Wo es nicht funktioniert:
"Hatte noch bei keiner Lesung und keinem Vortrag ein Problem."
Wir haben die Ausnahmen für "?" und "Wenn" rausgenommen, weil die Twitter-Daten da wohl speziell sind.

'''

def sentiment_spacy(testsatz):
    testsatz = bmp(testsatz)
    testsatz = testsatz.replace('|LBR|','')
#    print(testsatz)
    dep_analysis = []
    scount = 0
    sent_analysis = []
    doc=nlp(testsatz)
    for token in doc:
        dep_analysis.append((token.lemma_, token.pos_, token.dep_, token.head.text, token.text))
        if token.text in ironie:
            return -1.0
        elif token.lemma_ in sentiments.keys():
            wcount = float(sentiments[token.lemma_])
            sent_analysis.append((token.text,wcount))
#            print("SENTIMENT-WORT: " + str(token.text) + "(" + str(wcount) + ")")
        elif token.lemma_ in negations:
            sent_analysis.append((token.head.text, 'NEG'))
#            print("NEGIERT: " + str(token.head.text))
        elif token.lemma_ in verstaerker:
            sent_analysis.append((token.head.text, 'EMP'))
 #           print("VERSTÄRKT: " + str(token.head.text))
        else:
            wcount = '0'
#           scount = scount + float(wcount)
 #   print(dep_analysis)
 #       print(str(sent_analysis))
    first_vals = [x[0] for x in sent_analysis]
# erste Schleife: Negationen und Emphasis
    for wresult in sent_analysis:
        if wresult[1] == 'NEG':
            for rresult in sent_analysis:
                if wresult[0] == rresult[0] and type(rresult[1]) != str:
                    wcount = -1.0 * float(rresult[1])
                    sent_analysis.remove(rresult)
                    sent_analysis.append((rresult[0],wcount))
                    if wresult in sent_analysis:
                        sent_analysis.remove(wresult)
        elif wresult[1] == 'EMP':
            for rresult in sent_analysis:
                if wresult[0] == rresult[0] and type(rresult[1]) != str:
                    wcount = 1.5 * float(rresult[1])
                    sent_analysis.remove(rresult)
                    sent_analysis.append((rresult[0],wcount))
                    if wresult in sent_analysis:
                        sent_analysis.remove(wresult)
#        print(str(sent_analysis))
# 2. Schleife: jetzt alle Werte addieren
    for wresult in sent_analysis:
        if type(wresult[1]) != str:
            scount = scount + float(wresult[1])
    return(scount)
                           
    

def sentiment_line(testsatz):
    scount = sentiment_spacy(testsatz)
    if scount > 1:
        print('Dieser Satz enthält eine sehr positive Meinungsäußerung. (' + str(scount) + ')')
    elif scount < -1:
        print('Dieser Satz enthält eine sehr negative Meinungsäußerung. (' + str(scount) + ')')
    elif scount > 0:
        print('Dieser Satz enthält eine positive Meinungsäußerung. (' + str(scount) + ')')
    elif scount < 0:
        print('Dieser Satz enthält eine negative Meinungsäußerung. (' + str(scount) + ')')
    elif scount == 0:
        if sent_score == 1:
            print('Dieser Satz enthält eine Meinungsäußerung. (' + str(scount) + ')')
        else:
            print('Dieser Satz enthält keine Meinungsäußerung. (' + str(scount) + ')')

def sentiment_file(infile):
    pos_count = 0
    neg_count = 0
    neut_count = 0
#    infile = input("Welche Datei soll ich analysieren?\n")
    text = open(infile,'r', encoding='utf-8', errors='ignore')
    lines = text.readlines()
    positive_tweets = open('out/positive_tweets.txt','w', encoding='utf-8', errors='ignore')
    negative_tweets = open('out/negative_tweets.txt','w', encoding='utf-8', errors='ignore')
    neutrale_tweets = open('out/neutrale_tweets.txt','w', encoding='utf-8', errors='ignore')
    stats = open('out/statistics.txt','w', encoding='utf-8', errors='ignore')
    for line in lines:
        scount = sentiment_spacy(line)
#    print(str(line) + ': ' + str(scount))
        if scount > 0:
            positive_tweets.write(str(line).strip() + '\t' + str(scount) + '\n')
            pos_count = pos_count+1
        elif scount < 0:
            negative_tweets.write(str(line).strip() + '\t' + str(scount) + '\n')
            neg_count = neg_count+1
        elif scount == 0:
            neutrale_tweets.write(str(line).strip() + '\t' + str(scount) + '\n')
            neut_count = neut_count+1
    all_tweets = pos_count + neg_count + neut_count
    stats.write("Anzahl Tweets: " + str(all_tweets) +  '\n')
    stats.write("Positive Tweets: " + str(pos_count) + " (" + str(pos_count*100/all_tweets) + '%)\n')
    stats.write("Negative Tweets: " + str(neg_count) + " (" + str(neg_count*100/all_tweets) + '%)\n')
    stats.write("Neutrale Tweets: " + str(neut_count) + " (" + str(neut_count*100/all_tweets) + '%)\n')
    text.close()
    positive_tweets.close()
    negative_tweets.close()
    neutrale_tweets.close()
    stats.close()



