import pandas as pd


df_lemma = pd.read_csv("morphy_mapping.tsv", sep="\t")
lemma = df_lemma.set_index("word")["lemma"].to_dict()


'''
Verallgemeinerungen (z.B. ung, heit, keit) dienen dazu, die Mapping-Datei etwas kleiner machen zu können.
Evtl. würde es Sinn machen, noch mehr Verallgemeinerungen zu definieren?
'''

def lemmatize_word(word):
    if word.endswith("ungen"):
        word = word.replace("ungen","ung")
        return(word)
    elif word.endswith("heiten"):
        word = word.replace("heiten","heit")
        return(word)
    elif word.endswith("keiten"):
        word = word.replace("keiten","keit")
        return(word)
    elif word.endswith("erlöse"):
        word = word.replace("erlöse","erlös")
        return(word)
    elif word.isupper():
        word = word.capitalize()
        if word in lemma.keys():
            return(lemma[word])
    elif word in lemma.keys():
        return(lemma[word])
    else:
        return(word)
        


def lemmatize_sentence(sentence):
    wlist = sentence.split()
    for w in wlist:
        w_new = lemmatize_word(w)
        sentence = sentence.replace(w,w_new)
    return(sentence)


