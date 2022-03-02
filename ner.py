import nltk
from textblob_de import TextBlobDE
from textblob_de.lemmatizers import PatternParserLemmatizer
from textblob_de.packages import pattern_de as pd
from textblob_de import PatternParser
from nltk.tokenize import word_tokenize
import nltk.data
import re
from nltk.util import ngrams
import vornamen
from vornamen import vornamen

#### Named-Entity Recognition ####

#sehr einfache Lösung
'''
print("NER")

ne_grammar = r"""
PERSON: { <NNP><NNP>}
PLACE: {<IN><NNP>}
ORGANIZATION: {<NN><NNP>}
"""

ne_parse = nltk.RegexpParser(ne_grammar)
ne_result = ne_parse.parse(postags)
print(ne_result)
'''



organizations = []
money_expressions = []
products = []
org_divisions = []
markets = []
person_found = 0


org_abbrevs = ["AG", "GmbH", "Konzern",["AG", "&", "Co", "KG"], 'OHG', 'Aktiengesellschaft', 'Corp', 'Corporation', "e.G.", 'eG', "e.G",'Holding', 'GbR', 'gGmbH', ["GmbH", "&", "Co", "KG"], "Regierung"]

money_abbrevs = ['€', 'EUR']

money_multipliers = ["Mrd.", "Mio.", "Tsd"]

product_prefixes = ["Marke", "Marken"]

gaz_organisations = ["adidas", "Adidas", "Reebok", "Reebok-CCM", "TaylorMade-adidas", "Rockport", "Konzerns", "US-Regierung", "US-Auslandsgeheimdienst", "US-Auslandsgeheimdienstes", "Senat"]

gaz_subdivisions = ["Golf", "Hockey"]

gaz_divisions = ["Segmenten", "eCommerce-Geschäft", "Einzelhandelssegment", "Großhandelssegment", "Sportartikelsektors", "Sporteinzelhandels"] 

division_prefixes = ["Segment"]

markets = ["China", "Schwellenländer", "Deutschland", "asiatischen", "Lateinamerikas", "Lateinamerika"]

gaz_titles = ["Frau", "Herr", "Prof.", "Dr.", "Ing.", "jur.", "med.", "phil", "Fr.", "Hr.", "Präsident", "Präsidentin", "Außenminister","Außenministerin", "Nachfolger", "Nachfolgerin", "Stellvertreter", "Stellvertreterin"]

gaz_human_activities = ["erklärte", "sagte", "meinte"]

def ner_products(tags):
    products_string = ""
    products_annotation = ""
    if tags[0][0] in product_prefixes:
        if tags[1][1] in ["NN", "NNP", "JJ"]:
            products_string = tags[0][0] + ' ' + tags[1][0]
            products_annotation = '<PRODUCT>' + products_string + '<\PRODUCT>'
    return(products_string, products_annotation)

def ner_organizations(tags):
    org_string = ""
    org_annotation = ""
    if tags[0][0] in gaz_organisations:
        if tags[1][1] in ["NN", "NNP", "JJ"] and tags[2][1] in ["NN", "NNP", "JJ"]:
            print (tags[1][1] + tags[2][1])
            org_string = tags[0][0] + ' ' + tags[1][0] + ' ' + tags[2][0]
            org_annotation = '<ORG_DIV>' + org_string +'<\ORG_DIV>'
        else:
            org_string = tags[0][0]
            organizations.append(org_string)
            org_annotation = '<ORG>' + org_string + '<\ORG>'
    elif tags[1][0] in org_abbrevs:
        if tags[0][1] in ["NN", "NNP", "JJ"]:
            org_string = tags[0][0] + ' ' + tags[1][0]
            org_annotation = '<ORG_ABB>' + org_string + '<\ORG_ABB>'
    elif tags[2][0] in org_abbrevs:
        if tags[1][1] in ["NN", "NNP", "JJ"]:
            org_string = tags[1][0] + ' ' + tags[2][0]
            org_annotation = '<ORG_ABB>' + org_string + '<\ORG_ABB>'
    return(org_string,org_annotation)


def ner_money(tags):
    money_string = ""
    money_annotation = ""
    if tags[2][0] in money_abbrevs:
        if tags[1][0] in money_multipliers:
            money_string = tags[0][0]+ ' ' + tags[1][0] + ' ' + tags[2][0]
            money_annotation = '<MONEY>' + money_string + '<\MONEY>'
        else:
            money_string = tags[1][0] + ' ' + tags[2][0]
            money_annotation = '<MONEY>' + money_string + '<\MONEY>'
    return(money_string, money_annotation)


def ner_person(tags):
    person_string = 'XYZ'
    person_annotation = ''
    if tags[0][0] in gaz_titles:
        if tags[1][0] in gaz_titles:
               if tags[2][1] in ["NN", "NNP", "JJ"]:
                   person_string = tags[2][0]
                   person_annotation = '<PERSON>' + person_string + '</PERSON>'
        elif tags[1][0] in vornamen:
            if tags[2][1] in ["NN", "NNP", "JJ"]:
                person_string = tags[1][0] + ' ' + tags[2][0]
                person_annotation = '<PERSON>' + person_string + '</PERSON>'
        elif tags[1][1] in ["NN", "NNP", "JJ"]:
            person_string = tags[1][0]
            person_annotation = '<PERSON>' + person_string + '</PERSON>'
    elif tags[0][0] in vornamen:
        if tags[1][0] in vornamen:
            if tags[2][1] in ["NN", "NNP", "JJ"]:
                person_string = tags[0][0] + ' ' + tags[1][0] + ' ' + tags[2][0]
                person_annotation = '<PERSON>' + person_string + '</PERSON>'
        elif tags[1][1] in ["NN", "NNP", "JJ"]:
            person_string = tags[0][0] + ' ' + tags[1][0]
            person_annotation = '<PERSON>' + person_string + '</PERSON>'
    elif tags[0][0] in gaz_human_activities:
        if tags[1][1] in ["NN", "NNP", "JJ"]:
            person_string = tags[1][0]
            person_annotation = '<PERSON>' + person_string + '</PERSON>'
    else:
        person_string = 'XYZ'
        person_annotation = ''
    return(person_string,person_annotation)


def named_entities_trigrams(sentence):
        blob = TextBlobDE(sentence)
        tokens = blob.tokens
        trigrams=list(ngrams(tokens,3))
#        print(trigrams)
        organizations = []
        org_divisions = []
        products = []
        money_expressions = []
        person_expressions = []
        person_string = 'XYZ'
        for trigram in trigrams:
            tstring = ' '.join(list(trigram))
            tags = TextBlobDE(tstring).tags
            if person_string in tstring:
                sentence = sentence
            elif len(tags) == 3:
                    (products_string, products_annotation) = ner_products(tags)
                    if len(products_string) > 0:
                        products.append(products_string)
                        sentence = sentence.replace(products_string,products_annotation)
                    (org_string,org_annotation) = ner_organizations(tags)
                    if len(org_string) > 0:
                        organizations.append(org_string)
                        sentence = sentence.replace(org_string,org_annotation)
                    (money_string, money_annotation) = ner_money(tags)
                    if len(money_string) > 0:
                         money_expressions.append(money_string)
                         sentence = sentence.replace(money_string,money_annotation)
                    (person_string, person_annotation) = ner_person(tags)
                    if person_string != 'XYZ':
                        person_expressions.append(person_string)
                        sentence = sentence.replace(person_string,person_annotation)
        print ("ORGANIZATION: ")
        print (organizations)
        print ("PRODUCT_NAMES: ")
        print (products)
        print("MONEY: ")
        print(money_expressions)
        print("PERSONS: ")
        print(person_expressions)
        print ("ANNOTATED TEXT: ")
#        sentence = sentence.replace(products_string,products_annotation).replace(money_string,money_annotation).replace(org_string,org_annotation).replace(products_string,products_annotation).replace(person_string,person_annotation)
#        sentence = sentence.replace('<PERSON><PERSON>','<PERSON>').replace('</PERSON></PERSON>','</PERSON>')
        print(sentence)



text_nertest = '''Für die meisten anderen wichtigen asiatischen Schwellenländer wird für 2013 von einem rasanten Wachstum der Branche ausgegangen, da eine steigende Inlandsnachfrage sowie höhere Löhne den Umsatz mit nicht essenziellen Konsumartikeln weiter fördern werden. EOS'''
small_nertest = '''Des Weiteren werden Verbesserungen im Einzelhandelssegment sowie bei der Marke Reebok die Entwicklung der Bruttomarge fördern.'''

moskito_test = '''Die zahllosen winzigen Nebeltröpfchen blockieren die Schwingkölbchen der Mücke - zwei kleine, hinter den Flügeln sitzende Lagesensoren. Das haben US-amerikanische Forscher mittels Hochgeschwindigkeitsaufnahmen herausgefunden. Demnach kollidieren die schwingenden Sensoren in jeder Sekunde mit tausenden Nebeltröpfchen und funktionieren dadurch nicht mehr richtig. Als Folge könne die Mücke ihre Körperposition im Flug nicht mehr ermitteln und verliere ihre stabile Fluglage, berichten die Wissenschaftler am Montag auf einer Physiker-Tagung im kalifornischen San Diego.
"Moskitos sind auch im Regen gute Flieger, aber bei Nebel gelingt ihnen dies nicht", schreiben Andrew Dickerson und seine Kollegen vom Georgia Institute of Technology. Ein Regentropfen sei rund 50 Mal so groß wie eine Mücke, ein Zusammenstoß daher vergleichbar der Kollision eines Menschen mit einem Bus. Obwohl das winzige Insekt bei einem Regenguss im Durchschnitt alle 20 Sekunden mit einem Tropfen kollidiere, überstehe es dies schadlos und fliege weiter.'''

#myblob = blob = TextBlobDE(moskito_nertest)
#tags = blob.tags
#print (tags)
#print(named_entities_market(myblob))


