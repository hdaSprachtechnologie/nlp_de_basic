from morphy_mapping import find_lemma_dict


#textin = open('lemma_test.txt', 'r',encoding='utf-8')
#out  = open('out.txt','w',encoding='utf-8')

#lines = textin.readlines()


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
        return find_lemma_dict(word)
    else:
        return find_lemma_dict(word)
        


def lemmatize_sentence(sentence):
    wlist = sentence.split()
    for w in wlist:
        w_new = lemmatize_word(w)
        sentence = sentence.replace(w,w_new)
    return(sentence)

#print(lemmatize_sentence(testsatz))

#for line in lines:
#    out.write(lemmatize_sentence(line))

#textin.close()
#out.close()
