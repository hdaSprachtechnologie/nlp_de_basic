import access_open_de_wn
from access_open_de_wn import *
import textblob_de
from textblob_de import TextBlobDE
from nlp_melanie import *

de_wn = open(r"C:\Users\melaniesiegel\Documents\05_Projekte\WordNet\OdeNet\odenet.git\trunk\deWordNet.xml","r",encoding="utf-8")
lines = de_wn.readlines()


def find_word_status(word):
      try:
        lemma_id, lemma, pos, senses = check_word_lemma(word)
        for line in lines:
            if 'id="' + lemma_id + '" dc:type="Grundwortschatz"' in line:
                return(True)
            else:
                  return(False)
      except:
         print(word + " NOT IN ODENET")
  

def find_easy_syn(word, syns):
    if find_word_status(word) == True:
        print('Leichtes Wort: ' + word)
    else:
        for w in syns:
            try:
                lemma_id, lemma, pos, senses = check_word_lemma(w)
                for line in lines:
                    if 'id="' + lemma_id + '" dc:type="Grundwortschatz"' in line:
                        print(word + " hat eine leichte Alternative: " + str(lemma))
            except:
                print(w + " NOT IN ODENET")
    




def lex_vereinfache(satz):
      lemmata = TextBlobDE(satz).words.lemmatize()
      for lemma in lemmata:
        syns = synonyms(lemma)
        print(str(syns))
        if syns != None:
            find_easy_syn(lemma, syns)
      de_wn.close()
        
