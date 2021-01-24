#import access_open_de_wn
#from access_open_de_wn import *
from odenet import *
from nlp_melanie import *
#from nlp_melanie.compounds_syllables import analyze_compound_syls
#from nlp_melanie.compounds import lookup_noun, analyze_compound_2, analyze_compound_3, analyze_compound
#from nlp_melanie.nouns import nouns
#import compound_relations_to_add
#from compound_relations_to_add import c_relations

out = open("out.txt","w",encoding="utf-8")


# find and analyze all nominal compounds in OdeNet

def find_compounds_in_odenet():
    for lexentry in lexicon.iter('LexicalEntry'):
        lemma = lexentry.find('Lemma')
        lemma_value = lemma.attrib['writtenForm']
        if not " " in lemma_value:
            compounds = analyze_compound(lemma_value)
            if len(compounds) > 1:
                head = compounds[-1]
                lemma_id, lemma_value, pos, senses = check_word_lemma(lemma_value)
                out.write(lemma_value + "\t" + str(compounds) + "\t")
                try:
                    head_id, head_value, head_pos, head_senses = check_word_lemma(head)
                    if len(head_senses) == 1 and len(senses) == 1:
                        word_id = senses[0][1]
                        target_id = head_senses[0][1]
                        out.write("relation for synset " + str(word_id) + ':\t')
                        out.write("<SynsetRelation target='" + str(target_id) + "' relType='hypernym'/>\n")
                    else:
                        out.write("multiple senses\n")
                except TypeError:
                    out.write("no entry for " + head + "\n")
    out.close()
                

# add a relation to OdeNet
# only if the relation target is not the same as the relation source
# --> Fachterminus ist synonym zu Terminus
# only in oneline-file!
# add_rel_to_ss(synset,relation,r"C:\Users\melaniesiegel\Documents\05_Projekte\WordNet\OdeNet\deWNaccess\odenet_oneline.xml")

def add_rel_to_ss(synset,relation,wordnetfile):
    if synset not in relation:
        de_wn = open(wordnetfile,"r",encoding="utf-8")
        lines = de_wn.readlines()
        de_wn.close() 
        out_odenet = open(wordnetfile,"w",encoding="utf-8")
        ss_string = '<Synset id="' + synset + '"'
        for line in lines:
            if ss_string in line and relation not in line:
                if '<Example>' in line:
                    line = line.replace('<Example>',relation + '<Example>')
                elif '</Synset>' in line:
                    line = line.replace('</Synset>',relation + '</Synset>')
                else:
                    line = line.replace('/>', '>' + relation + '</Synset>')
            out_odenet.write(line)
        out_odenet.close()

 # add all relations in the relation list

def add_rels_in_list():
     for addrel in c_relations:
         add_rel_to_ss(addrel[0],addrel[1])

# add hyponym relations in case there is a hypernym relation
# only in oneline-file!
# add_hypo_to_hyper(r"C:\Users\Melanie\Documents\05_Projekte\WordNet\OdeNet\odenet.git\trunk\odenet_oneline.xml")

def add_hypo_to_hyper(wordnetfile):
    de_wn = open(wordnetfile,"r",encoding="utf-8")
    lines = de_wn.readlines()
    de_wn.close()
    for synset in lexicon.iter('Synset'):
        ss_id = synset.attrib['id']
        hyp_list = hypernyms(ss_id)
        if len(hyp_list) > 0:
            for hyp_info in hyp_list:
                hyp_id = hyp_info[0]
                hypo_rel = "<SynsetRelation target='" + ss_id + "' relType='hyponym'/>"
                add_rel_to_ss(hyp_id,hypo_rel)

# semi-manual adding of compounds with multiple senses in their head

def compound_multiple_senses(compound):
    lemma_id, lemma_value, pos, senses = check_word_lemma(compound)
    if len(senses) > 1:
        sense_id = input("Welchen Sense von " + compound  + " willst Du bearbeiten? " + str(give_all_senses(compound)) + "\n")
    else:
        sense_id = senses[0][1]
    hyp_list = hypernyms_word(compound)
    if len(hyp_list) > 0:
        already_ok = input("Der Eintrag hat eine Hyperonym-Relation zu " + str(hyp_list) + ". Ist das ausreichend? (j/n)\n")
        if already_ok == "j":
            return
    compounds = analyze_compound(compound)
    if len(compounds) > 1:
        head = compounds[-1]
        lemma_id, lemma_value, pos, senses = check_word_lemma(head)
        head_id = input("Welcher dieser Senses ist der Head? " + str(give_all_senses(head)) + "\n")
        hyper_rel = "<SynsetRelation target='" + head_id + "' relType='hypernym'/>"
        hypo_rel = "<SynsetRelation target='" + sense_id + "' relType='hyponym'/>"
        add_rel_to_ss(sense_id,hyper_rel,r"C:\Users\melaniesiegel\Documents\05_Projekte\WordNet\OdeNet\odenet.git\trunk\odenet_oneline.xml")
        add_rel_to_ss(head_id,hypo_rel,r"C:\Users\melaniesiegel\Documents\05_Projekte\WordNet\OdeNet\odenet.git\trunk\odenet_oneline.xml")

def semi_manual_compounds():
    compound = "new"
    while compound != "quit":
        compound = input("Kompositum: ")
        compound_multiple_senses(compound)
