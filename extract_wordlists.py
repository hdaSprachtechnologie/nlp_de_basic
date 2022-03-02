import textblob_de
from textblob_de import *

# z.B.: extract_wordlist('other_tweets.txt','offense_tweets.txt')


# Das hier brauchen wir für Emojis und andere komische Buchstaben

def bmp(s):
    return "".join((i if ord(i) < 10000 else '\ufffd' for i in s))



# Task: extract word lists from annotated data
# words that are only in file_a and words that are only in file_b

def extract_wordlist(file_a, file_b):
    file_a_data = open(file_a, 'r', encoding="utf-8", errors = 'ignore')
    file_b_data = open(file_b, 'r', encoding="utf-8", errors = 'ignore')
    out = open('out.txt','w', encoding="utf-8")
    file_a_lines = file_a_data.readlines()
    file_b_lines = file_b_data.readlines()
    file_a_wordlist = []
    file_b_wordlist = []
    for file_a_line in file_a_lines:
        file_a_line = bmp(file_a_line)
        file_a_words = TextBlobDE(file_a_line).words
        for word in file_a_words:
            file_a_wordlist.append(word)
    file_a_wordlist = sorted(set(file_a_wordlist))
    for file_b_line in file_b_lines:
        file_b_line = bmp(file_b_line)
        file_b_words = TextBlobDE(file_b_line).words
        for word in file_b_words:
            file_b_wordlist.append(word)
    file_b_wordlist = sorted(set(file_b_wordlist))
    only_in_file_a = list(set(file_a_wordlist) - set(file_b_wordlist))
    only_in_file_b = list(set(file_b_wordlist) - set(file_a_wordlist))
    out.write("ONLY IN FILE A: " + str(only_in_file_a) + '\n')
    out.write("ONLY IN FILE B: " + str(only_in_file_b) + '\n')
    file_a_data.close()
    file_b_data.close()
    out.close()
    
