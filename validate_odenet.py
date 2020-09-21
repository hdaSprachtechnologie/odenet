# OdeNet-Validierung
# angelehnt an https://github.com/globalwordnet/english-wordnet/blob/master/scripts/validate.py

# Importe

from odenet import *

########## LexEntries ######

# Prüfung, ob es für ein Lemma mehrere LexEntries gibt
# Das sind immer noch ganz schön viele!

def find_duplicate_lexentries():
    lemma_list = []
    for lexentry in lexicon.iter('LexicalEntry'):
        lemma = lexentry.find('Lemma')
        lemma_value = lemma.attrib['writtenForm']
        lemma_id = lexentry.attrib['id']
        if lemma_value in lemma_list:
            find_all_lexentries(lemma_value)
        else:
            lemma_list.append(lemma_value)
    print("Es gibt doppelte Einträge für " + str(len(lemma_list)) + " Lemmata!")

########## POS ###########

# 1. LexEntries mit mehreren Senses, die POS haben, das anders als das POS des Lemmas ist
# 2. Alle Wörter mit Großbuchstaben, die POS v oder a haben
# 3. Wörter auf -lich und -isch, die kein Adjektiv sind.

def test_lexentries_pos():
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
                words = words_in_synset(synset_id)
#                out.write("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
                print("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
        if re.match(r'^[A-ZÄÜÖ][a-zäöüß]+$',lemma_value):
            if pos == 'v':
                synset_id = sense.attrib['synset']
                words = words_in_synset(synset_id)
#                out.write("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
                print("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
        if re.match(r'^[a-zäöü]+lich$',lemma_value):
            if pos == 'n':
                synset_id = sense.attrib['synset']
                words = words_in_synset(synset_id)
#                out.write("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
                print("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
            elif pos == 'v':
                synset_id = sense.attrib['synset']
                words = words_in_synset(synset_id)
#                out.write("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
                print("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
        if re.match(r'^[a-zäöü]+isch$',lemma_value):
            if pos == 'n':
                synset_id = sense.attrib['synset']
                words = words_in_synset(synset_id)
#                out.write("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
                print("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
            elif pos == 'v':
                synset_id = sense.attrib['synset']
                words = words_in_synset(synset_id)
#                out.write("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
                print("-- " + lemma_value + " : " + pos + ": " + synset_id + " " + str(words) + " \n\n")
#    out.close()



# Prüfung darauf, ob alle POS in einem Synset dieselben sind
# 1. stimmt der POS aus der ID mit dem aus dem Attribut überein?

def test_synsets_pos():
    for synset in lexicon.iter('Synset'):
        if synset.attrib['id'][-1] != synset.attrib['partOfSpeech']:
            print("Multiple POS values in " + synset.attrib['id'])


# Prüfung darauf, ob POS in Synset und Relation Target übereinstimmen
# Das sind immer noch ziemlich viele

def test_relation_pos():
    for synset in lexicon.iter('Synset'):
        synset_pos = synset.attrib['partOfSpeech']
        for relation in synset.iter('SynsetRelation'):
            if relation.attrib['target'][-1] != synset_pos:
                print("Synset " + synset.attrib['id'] + " has different POS values in relation targets")
        

# Prüfung darauf, ob POS in OdeNet und PWN übereinstimmen

########### SYNSET #############

# Prüfung auf Synsets ohne LexEntries

def test_for_empty_synsets():
    for synset in lexicon.iter('Synset'):
        wlist = words_in_synset(synset.attrib['id'])
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

def test_for_valid_ids():
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
                


######### RELATIONEN ########

# 1. Prüfung, ob Relationen das Target fehlt
# 2. Prüfung auf Loops: Synsets, die als Target einer Relation sich selbst haben


def test_target_in_relation():
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

def get_all_hyponym_hypernym_relations():
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

# Prüfung auf fehlende symmetrische Relationen (Antonym, Hypero-Hyponym)

def test_for_missing_symmetry(hyponym_relations,hypernym_relations):
    for relation in hyponym_relations:
        converse_relation = [relation[1],relation[0]]
        if converse_relation not in hypernym_relations:
            print("Asymmetric relation: " + str(relation))
    for relation in hypernym_relations:
        converse_relation = [relation[1],relation[0]]
        if converse_relation not in hyponym_relations:
            print("Asymmetric relation: " + str(relation))

def test_for_loops_in_relations():
    hyponym_relations,hypernym_relations = get_all_hyponym_hypernym_relations()
    test_for_loops_in_hypo_relations(hyponym_relations)
    test_for_loops_in_hypo_relations(hypernym_relations)
    test_for_missing_symmetry(hyponym_relations,hypernym_relations)

  





# höchste Synset-ID

def highest_synset_id():
    top_id = 0
    for synset in lexicon.iter('Synset'):
        synset_id = synset.attrib['id']
        odenet, number, pos = synset_id.split("-")
        if number > top_id:
            top_id = number
        else:
            top_id = top_id
    print("Highest_Synset ID: " + str(top_id))
    return(top_id)

# höchste LexEntry-ID


def test_necessary_conditions():
    print("Test for POS in LexEntries ...")
    test_lexentries_pos()
    print("Test for POS in Synsets ...")
    test_synsets_pos()
    print("Test für valid IDs")
    test_for_valid_ids()
    print("Test for targets in relations ...")
    test_target_in_relation()
    print("Test for loops and missing symmetry in relations ...")
    test_for_loops_in_relations()
#    print("Test for synsets without words ...")
#    test_for_empty_synsets()
    
    
