# OdeNet-Validierung
# angelehnt an https://github.com/globalwordnet/english-wordnet/blob/master/scripts/validate.py

# Importe

#from odenet import *
from xml.etree import ElementTree as ET
from lxml import etree
import re

g_wordDict = None

########## Zugriff auf das Wordnet #######

def get_wordnet_lexicon_local(wnfile):
     loc_wn = open(wnfile,"r",encoding="utf-8")
     wntree = ET.parse(loc_wn)
     wnroot = wntree.getroot()
     lexicon = wnroot.find('Lexicon')
     return lexicon


########## LexEntries ######
def get_word_dict(wordnet):
    lexicon = get_wordnet_lexicon_local(wordnet)            
    wordDict = {}        
    for synset in lexicon.findall('./Synset'):
        wordDict[synset.attrib['id']] = []
    for lexentry in lexicon.findall('./LexicalEntry'):
        for sense in lexentry.findall('./Sense'):                
            lemma = lexentry.find('Lemma').attrib['writtenForm']
            wordDict[sense.attrib['synset']].append(lemma)

    return wordDict        


def check_word_id(word_id, wordnet):
    lexicon = get_wordnet_lexicon_local(wordnet)
    for lexentry in lexicon.iter('LexicalEntry'):
        lemma = lexentry.find('Lemma')
        lemma_value = lemma.attrib['writtenForm']
        lemma_id = lexentry.attrib['id']
        if lemma_id == word_id:
            pos = lemma.attrib['partOfSpeech']
            senses = []
            for sense in lexentry.iter('Sense'):
                sense_id = sense.attrib['id']
                synset_id = sense.attrib['synset']
                senses.append([sense_id,synset_id])
            print("LEMMA: " + lemma_value + "\nPOS: " + pos + "\nSENSE ID: " + sense_id)

def find_all_lexentries(word_to_check, wordnet):
    lexicon = get_wordnet_lexicon_local(wordnet)
    for lexentry in lexicon.iter('LexicalEntry'):
        lemma = lexentry.find('Lemma')
        lemma_value = lemma.attrib['writtenForm']
        lemma_id = lexentry.attrib['id']
        word_id_list = []
        if lemma_value == word_to_check:
            word_id_list.append(lemma_id)
        for wid in word_id_list:
            check_word_id(wid, wordnet)    

# Prüfung, ob es für ein Lemma mehrere LexEntries gibt

def find_duplicate_lexentries(wordnet):
    lexicon = get_wordnet_lexicon_local(wordnet)
    lemma_list = []
    for lexentry in lexicon.iter('LexicalEntry'):
        lemma = lexentry.find('Lemma')
        lemma_value = lemma.attrib['writtenForm']
        lemma_id = lexentry.attrib['id']
        if lemma_value in lemma_list:
            find_all_lexentries(lemma_value,wordnet)
        else:
            lemma_list.append(lemma_value)
#    print("Es gibt doppelte Einträge für " + str(len(lemma_list)) + " Lemmata!")

# Prüfung, ob die Lex-ID mit der Sense-ID übereinstimmt

def find_inconsistent_lexids(wordnet):
    lexicon = get_wordnet_lexicon_local(wordnet)
    for lexentry in lexicon.iter('LexicalEntry'):
        lemma_id = lexentry.attrib['id']
        for sense in lexentry.iter('Sense'):
            sense_id = sense.attrib['id']
            sense_w_id = sense_id.split('_')[0]
            if sense_w_id != lemma_id:
                print ("LexIDs inkonsistent in: " + lemma_id + ": " +  sense_w_id)

# Prüfung, ob eine Synset-ID im LexEntry überhaupt existiert
# und ob eine Synset-ID in einer Relation überhaupt existiert

def test_for_existance_of_synset(wordnet):
    lexicon = get_wordnet_lexicon_local(wordnet)
    list_of_synsets = []
    for synset in lexicon.iter('Synset'):
        list_of_synsets.append(synset.attrib['id'])
    for lexentry in lexicon.iter('LexicalEntry'):
        lemma_id = lexentry.attrib['id']
        for sense in lexentry.iter('Sense'):
            sense_synset = sense.attrib['synset']
            if sense_synset not in list_of_synsets:
                print("Synset " + sense_synset + " from LexEntry " + lemma_id + " is not defined!")
    for synset in lexicon.iter('Synset'):
        for relation in synset.iter('SynsetRelation'):
            if relation.attrib['target'] not in list_of_synsets:
                print("Synset " + synset.attrib['id'] + " has a relation to " + relation.attrib['target'] + ", but the target is not defined!") 

########## POS ###########

def words_in_synset(id, wordnet):        
    return(g_wordDict[id])
    

# 1. LexEntries mit mehreren Senses, die POS haben, das anders als das POS des Lemmas ist
# 2. Alle Wörter mit Großbuchstaben, die POS v oder a haben
# 3. Wörter auf -lich und -isch, die kein Adjektiv sind.

def test_lexentries_pos(wordnet):
    lexicon = get_wordnet_lexicon_local(wordnet)
#    out = open("out.txt","w",encoding="utf-8")
    for lexentry in lexicon.iter('LexicalEntry'):
        lemma = lexentry.find('Lemma')
        lemma_value = lemma.attrib['writtenForm']
#        pos = lemma.attrib['partOfSpeech']
        try:
            pos = lemma.attrib['partOfSpeech']
        except:
            print('problem with ' + lemma_value)
        for sense in lexentry.iter('Sense'):
            synset_id = sense.attrib['synset']
            if not synset_id[-1] == pos:
                words = words_in_synset(synset_id,wordnet)
#                out.write("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
                print("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
        if re.match(r'^[A-ZÄÜÖ][a-zäöüß]+$',lemma_value):
            if pos == 'v':
                synset_id = sense.attrib['synset']
                words = words_in_synset(synset_id,wordnet)
#                out.write("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
                print("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
        if re.match(r'^[a-zäöü]+lich$',lemma_value):
            if pos == 'n':
                synset_id = sense.attrib['synset']
                words = words_in_synset(synset_id,wordnet)
#                out.write("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
                print("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
            elif pos == 'v':
                synset_id = sense.attrib['synset']
                words = words_in_synset(synset_id,wordnet)
#                out.write("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
                print("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
        if re.match(r'^[a-zäöü]+isch$',lemma_value):
            if pos == 'n':
                synset_id = sense.attrib['synset']
                words = words_in_synset(synset_id,wordnet)
#                out.write("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
                print("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
            elif pos == 'v':
                synset_id = sense.attrib['synset']
                words = words_in_synset(synset_id,wordnet)
#                out.write("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
                print("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
#    out.close()



# Prüfung darauf, ob alle POS in einem Synset dieselben sind
# 1. stimmt der POS aus der ID mit dem aus dem Attribut überein?

def test_synsets_pos(wordnet):
    lexicon = get_wordnet_lexicon_local(wordnet)
    for synset in lexicon.iter('Synset'):
        if synset.attrib['id'][-1] != synset.attrib['partOfSpeech']:
            print("Multiple POS values in " + synset.attrib['id'])


# Prüfung darauf, ob POS in Synset und Relation Target übereinstimmen


def test_relation_pos(wordnet):
    lexicon = get_wordnet_lexicon_local(wordnet)
    for synset in lexicon.iter('Synset'):
        synset_pos = synset.attrib['partOfSpeech']
        for relation in synset.iter('SynsetRelation'):
            if relation.attrib['target'][-1] != synset_pos:
                print("Synset " + synset.attrib['id'] + " has different POS values in relation targets")
        

# Prüfung darauf, ob POS in OdeNet und PWN übereinstimmen --> TODO

########### SYNSET #############

# Prüfung auf Synsets ohne LexEntries

def test_for_empty_synsets(wordnet):
    lexicon = get_wordnet_lexicon_local(wordnet)
    for synset in lexicon.iter('Synset'):
        wlist = words_in_synset(synset.attrib['id'],wordnet)
        if len(wlist) == 0:
            print("Synset " + synset.attrib['id'] + " has no words!")


# Prüfung auf valide ids

valid_word_id = re.compile("^w[0-9]+$")

valid_sense_id = re.compile("^w[0-9]+_[0-9]+-[nvapx]$")

valid_synset_id = re.compile("^odenet-[0-9]+-[nvapx]$")

def is_valid_word_id(xml_id):
    return bool(valid_word_id.match(xml_id))

def is_valid_synset_id(xml_id):
    return bool(valid_synset_id.match(xml_id))

def is_valid_sense_id(xml_id):
    return bool(valid_sense_id.match(xml_id))

def test_for_valid_ids(wordnet):
        lexicon = get_wordnet_lexicon_local(wordnet)
        for lexentry in lexicon.iter('LexicalEntry'):
            if not is_valid_word_id(lexentry.attrib['id']):
                print(lexentry.attrib['id'] + " is not valid")
            for sense in lexentry.iter('Sense'):
                if not is_valid_sense_id(sense.attrib['id']):
                    print("Sense ID " + sense.attrib['id'] + " is not valid")
                if not is_valid_synset_id(sense.attrib['synset']):
                    print("Synset ID " + sense.attrib['synset'] + " is not valid")
        for synset in lexicon.iter('Synset'):
            if not is_valid_synset_id(synset.attrib['id']):
                    print("Synset ID " + synset.attrib['id'] + " is not valid")
                
# Prüfen, ob ilis doppelt vergeben wurden

def test_for_duplicate_ilis(wordnet):
    lexicon = get_wordnet_lexicon_local(wordnet)
    ili_list = []
    for synset in lexicon.iter('Synset'):
        synset_ili = synset.attrib['ili']
        if len(synset_ili) > 0:
            if synset_ili in ili_list:
                print("Duplicated ILI: " + str(synset_ili))
            else:
                ili_list.append(synset_ili)
        

######### RELATIONEN ########

# 1. Prüfung, ob Relationen das Target fehlt
# 2. Prüfung auf Loops: Synsets, die als Target einer Relation sich selbst haben


def test_target_in_relation(wordnet):
    lexicon = get_wordnet_lexicon_local(wordnet)
    for synset in lexicon.iter('Synset'):
        id = synset.attrib['id']
        for relation in synset.iter('SynsetRelation'):
            try:
                reltarget = relation.attrib['target']
            except KeyError:
                print(id + " is missing the target!")
            if relation.attrib['target'] == id:
                print(id + " has a relation to itself!")

# Prüfung auf Loops: Zwei Synsets zeigen gegenseitig auf sich mit derselben Relation
''' Z.B.:

<Synset id="odenet-10502-n" ili="i112933" partOfSpeech="n"><SynsetRelation target='odenet-10742-n' relType='hyponym'/></Synset>

<Synset id="odenet-10742-n" ili="i112931" partOfSpeech="n"><SynsetRelation target='odenet-10502-n' relType='hyponym'/></Synset>

'''
# 1. Ich erstelle eine Liste von allen Hypernym-Relationen und eine Liste von allen Hyponym-Relationen

def get_all_hyponym_hypernym_relations(wordnet):
    lexicon = get_wordnet_lexicon_local(wordnet)
    hyponym_relations = []
    hypernym_relations = []
    for synset in lexicon.iter('Synset'):
        synset_id = synset.attrib['id']
        for relation in synset.iter('SynsetRelation'):
            if relation.attrib['relType'] == 'hyponym':
                hyponym_relations.append([synset_id,relation.attrib['target']])
            elif relation.attrib['relType'] == 'hypernym':
                hypernym_relations.append([synset_id,relation.attrib['target']])
    return(hyponym_relations,hypernym_relations)



def test_for_loops_in_hypo_relations(hypo_list):
    for relation in hypo_list:
        if hypo_list.count(relation) > 1:
            print("Duplicate relation: " + str(relation))
        converse_relation = [relation[1],relation[0]]
        if converse_relation in hypo_list:
            print("Loop in relation " + str(relation))

# Prüfung auf fehlende symmetrische Relationen (Hypero-Hyponym)

def test_for_missing_symmetry(hyponym_relations,hypernym_relations):
    for relation in hyponym_relations:
        converse_relation = [relation[1],relation[0]]
        if converse_relation not in hypernym_relations:
            print("Asymmetric relation: " + str(relation))
    for relation in hypernym_relations:
        converse_relation = [relation[1],relation[0]]
        if converse_relation not in hyponym_relations:
            print("Asymmetric relation: " + str(relation))

def test_for_loops_in_relations(wordnet):
    hyponym_relations,hypernym_relations = get_all_hyponym_hypernym_relations(wordnet)
    test_for_loops_in_hypo_relations(hyponym_relations)
    test_for_loops_in_hypo_relations(hypernym_relations)
    test_for_missing_symmetry(hyponym_relations,hypernym_relations)

 
# höchste Synset-ID

def highest_synset_id(wordnet):
    lexicon = get_wordnet_lexicon_local(wordnet)
    top_id = 0
    for synset in lexicon.iter('Synset'):
        synset_id = synset.attrib['id']
        odenet, number, pos = synset_id.split("-")
        if int(number) > top_id:
            top_id = int(number)
        else:
            top_id = top_id
    print("Highest synset ID: " + str(top_id))
    return(top_id)

# höchste LexEntry-ID

def highest_lex_id(wordnet):
    lexicon = get_wordnet_lexicon_local(wordnet)
    top_id = 0
    for lexentry in lexicon.iter('LexicalEntry'):
        lex_id = lexentry.attrib['id'][1:]
        if int(lex_id) > top_id:
            top_id = int(lex_id)
        else:
            top_id = top_id
    print("Highest lexentry ID: w" + str(top_id))
    return(top_id)
    
# Test auf valides XML

def test_valid_xml(wordnet):
    parser = etree.XMLParser(dtd_validation=True, no_network=False)
    tree = etree.parse(wordnet, parser)


def test_necessary_conditions(wordnet):
#    lexicon = get_wordnet_lexicon_local(wordnet)
    g_wordDict = get_word_dict(wordnet)
    print("Test for valid xml ...")
    test_valid_xml(wordnet)
    highest_synset_id(wordnet)
    highest_lex_id(wordnet)
    print("Test for inconstent IDs in LexEntries ...")
    find_inconsistent_lexids(wordnet)
    print("Test for POS in LexEntries ...")
    test_lexentries_pos(wordnet)
    print("Test for POS in Synsets ...")
    test_synsets_pos(wordnet)
    print("Test for POS in Relations ...")
    test_relation_pos(wordnet)
    print("Test for valid IDs")
    test_for_valid_ids(wordnet)
    print("Test for targets in relations ...")
    test_target_in_relation(wordnet)
    print("Test for loops and missing symmetry in relations ...")
    test_for_loops_in_relations(wordnet)
    print("Test for existance of synsets ...")
    test_for_existance_of_synset(wordnet)
    print("Test for duplicate ilis...")
    test_for_duplicate_ilis(wordnet)
#    print("Test for duplicate LexEntries ...") 
#    find_duplicate_lexentries(wordnet)
    print("Test for synsets without words ...") 
    test_for_empty_synsets(wordnet) 


#Main Program
g_wordDict = get_word_dict('odenet/wordnet/deWordNet.xml')
test_necessary_conditions('odenet/wordnet/deWordNet.xml')
