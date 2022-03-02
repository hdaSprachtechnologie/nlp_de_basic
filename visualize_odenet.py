import networkx as nx
import matplotlib.pyplot as plt
G=nx.Graph()
import access_open_de_wn
from access_open_de_wn import *

'''
word = input("Welches Wort? ")

lemma, pos, senses = check_word_lemma(word)

print("Ich habe diese Senses dafür: ")

for sense in senses:
    print("SYNSET: " + sense[1])
    print(check_synset(sense[1]))

sense = input("Welcher Sense? ")
'''
seen = set()

def recurse_hyper(s,word):
    if not s in seen:
        seen.add(s)
        G.add_node(word)
        hypers = hypernyms(s)
        print(str(hypers))
#        if len(hypers) > 0:
        for h in hypers:
            G.add_node(h[1][0])
            G.add_edge(word,h[1][0])
            recurse_hyper(h[0],h[1][0])

def recurse_hypo(s,word):
    if not s in seen:
        seen.add(s)
        G.add_node(word)
        hypos = hyponyms(s)
        for h in hypos:
            G.add_node(h[1][0])
            G.add_edge(word,h[1][0])
            recurse_hypo(h[0],h[1][0])


#recurse_hyper(sense,word)

#recurse_hypo(sense,word)

def visualize_hypernyms():
    word = input("Welches Wort? ")
    lemma, pos, senses = check_word_lemma(word)
    print("Ich habe diese Senses dafür: ")
    for s in senses:
        print("SYNSET: " + s[1])
        print(check_synset(s[1]))
    sense = input("Welcher Sense? ")      
    recurse_hyper(sense,word)
    print (G.nodes(data=True))
    nx.draw_networkx(G, width=2, with_labels=True)
    plt.show()

def visualize_hyponyms():
    word = input("Welches Wort? ")
    lemma, pos, senses = check_word_lemma(word)
    print("Ich habe diese Senses dafür: ")
    for s in senses:
        print("SYNSET: " + s[1])
        print(check_synset(s[1]))
    sense = input("Welcher Sense? ")
    recurse_hypo(sense,word)
    print (G.nodes(data=True))
    nx.draw_networkx(G, width=2, with_labels=True)
    plt.show()


'''
G.add_node(word)

hyper_list = hypernyms(word)

for h in hyper_list:
    G.add_node(h[2][0])
    G.add_edge(word,h[2][0])


hypo_list = hyponyms(word)

for h in hypo_list:
    G.add_node(h[2][0])
    G.add_edge(word,h[2][0])

print (G.nodes(data=True))

nx.draw_networkx(G, width=2, with_labels=True)
plt.show()
'''

