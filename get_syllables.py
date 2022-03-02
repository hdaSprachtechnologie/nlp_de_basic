import pyphen



def get_syls(word):
    dic = pyphen.Pyphen(lang='de_DE')
    hyphenized = dic.inserted(word)
    syls = hyphenized.split("-")
    return(syls)
