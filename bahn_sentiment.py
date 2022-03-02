import my_sentiment
from my_sentiment import *
import bahn_sentiment_wordlists
from bahn_sentiment_wordlists import *


def bahn_sentiment(testsatz):
    blob = TextBlobDE(testsatz)
    scount = 0
    neg_score = 1
    sent_score = 1
    if ('?') in testsatz:
        scount = 0
        sent_score = 0
    elif("Wenn") in testsatz:
        scount = 0
        sent_score = 0
    else:
        for word in blob.words:
            wcount=0
            word_lemma = lemmatize_word(word)
            if word in negations:
                neg_score = -1.0
                print("NEGATION: " + word)
            elif word in verstaerker:
                neg_score = 1.5
                print("VERSTÄRKER: " + word)
            elif word_lemma in sentiments.keys():
                wcount = float(sentiments[word_lemma]) * neg_score
                neg_score = 1
                print("WORD: " + word + " (" + str(wcount) + ")")
            elif word_lemma in only_negative_words:
                wcount = -0.3 * neg_score
                neg_score = 1
                print("WORD_BAHN_NEG: " + word + " (" + str(wcount) + ")" )
            elif word_lemma in only_positive_words:
                wcount = 0.3 * neg_score
                neg_score = 1
                print("WORD_BAHN_POS: " + word + " (" + str(wcount) + ")")
            else:
                wcount = '0'
            scount = scount + float(wcount)
            print("SCOUNT: " + str(round(scount,3)))
    return(scount)

def bahn_sentiment_file(infile):
    pos_count = 0
    neg_count = 0
    neut_count = 0
    text = open(infile,'r', encoding='utf-8', errors='ignore')
    lines = text.readlines()
    positive_tweets = open('out/positive_tweets.txt','w', encoding='utf-8', errors='ignore')
    negative_tweets = open('out/negative_tweets.txt','w', encoding='utf-8', errors='ignore')
    neutrale_tweets = open('out/neutrale_tweets.txt','w', encoding='utf-8', errors='ignore')
    stats = open('out/statistics.txt','w', encoding='utf-8', errors='ignore')
    for line in lines:
        scount = bahn_sentiment(line)
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

