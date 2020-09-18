# Importe
from odenet.odenet_class import *


## Funktionen für die Arbeit mit OdeNet

# Informationen zu OdeNet hinzufügen
# nur in oneline-Datei!

# Relationen dem Synset hinzufügen
# add_rel_to_ss(synset,relation,r"C:\Users\melaniesiegel\Documents\05_Projekte\WordNet\OdeNet\deWNaccess\odenet_oneline.xml")

de_wn_file = os.path.join(os.path.dirname(__file__), f"wordnet/deWordNet.xml")
de_wn = open(de_wn_file,"r",encoding="utf-8")


# Ziel:  OdeNet editieren, sodass die Einträge jeweils auf einer Zeile stehen

def format_odenet_oneline():
    lines = de_wn.readlines()
    de_wn.close()
    out_odenet = open("odenet_oneline.xml","w", encoding="utf-8")
    for line in lines:
        if re.match(r'^\t*<LexicalEntry', line):
            line = line.strip('\t')
            line = line.strip('\r')
            line = line.strip('\n')
            out_odenet.write(line)
        elif re.match(r'^\t*<Lemma',line):
            line = line.strip('\t')
            line = line.strip('\r')
            line = line.strip('\n')
            out_odenet.write(line)
        elif re.match(r'^\t*<Sense',line):
            line = line.strip('\t')
            line = line.strip('\r')
            line = line.strip('\n')
            out_odenet.write(line)
        elif re.match(r'^\t*</Sense',line):
            line = line.strip('\t')
            line = line.strip('\r')
            line = line.strip('\n')
            out_odenet.write(line)
        elif re.match(r'^\t*<SyntacticBehaviour',line):
            line = line.strip('\t')
            line = line.strip('\r')
            line = line.strip('\n')
            out_odenet.write(line)
        elif re.match(r'^\t*</SyntacticBehaviour',line):
            line = line.strip('\t')
            line = line.strip('\r')
            line = line.strip('\n')
            out_odenet.write(line)
        elif re.match(r'^\t*</LexicalEntry>', line):
            line = line.strip('\t')
            out_odenet.write(line)
        elif re.match(r'^\t*<Synset.*partOfSpeech="[a-z]"/>', line):
            line = line.strip('\t')
            out_odenet.write(line)
        elif re.match(r'^\t*<Synset.*dc:description=".*"/>', line):
            line = line.strip('\t')
            out_odenet.write(line)
        elif re.match(r'^\t*<Synset',line):
            line = line.strip('\t')
            line = line.strip('\r')
            line = line.strip('\n')
            out_odenet.write(line)       
        elif re.match(r'^\t*<Definition', line):
            line = line.strip('\t')
            line = line.strip('\r')
            line = line.strip('\n')
            out_odenet.write(line)
        elif re.match(r'^\t*</Definition', line):
            line = line.strip('\t')
            line = line.strip('\r')
            line = line.strip('\n')
            out_odenet.write(line)
        elif re.match(r'^\t*<Example', line):
            line = line.strip('\t')
            line = line.strip('\r')
            line = line.strip('\n')
            out_odenet.write(line)
        elif re.match(r'^\t*</Example', line):
            line = line.strip('\t')
            line = line.strip('\r')
            line = line.strip('\n')
            out_odenet.write(line)
        elif re.match(r'^\t*</Synset>', line):
            line = line.strip('\t')
            out_odenet.write(line)
        else:
            out_odenet.write(line)
    out_odenet.close()




def add_rel_to_ss(synset,relation,target,wordnetfile):
    if synset not in target:
        de_wn = open(wordnetfile,"r",encoding="utf-8")
        lines = de_wn.readlines()
        de_wn.close() 
        out_odenet = open(wordnetfile,"w",encoding="utf-8")
        ss_string = '<Synset id="' + synset + '"'
        for line in lines:
            if ss_string in line and target not in line:
                if '<Example>' in line:
                    line = line.replace('<Example>',"<SynsetRelation target='" + target + "' relType='" + relation + "'/>" + '<Example>')
                elif '</Synset>' in line:
                    line = line.replace('</Synset>',"<SynsetRelation target='" + target + "' relType='" + relation + "'/>" + '</Synset>')
                else:
                    line = line.replace('/>', '>' + "<SynsetRelation target='" + target + "' relType='" + relation + "'/>" + '</Synset>')
                print(line)
            out_odenet.write(line)
        out_odenet.close()

# Symmetrische Relationen hinzufügen. D.h.: Im Fall von Hyperonym auch die Hyponym-Relation, im Fall von Antonym auch die Rück-Relation usw.

def add_antonym_rel_to_ss(synset, target, wordnetfile):
    add_rel_to_ss(synset,"antonym",target,wordnetfile)
    add_rel_to_ss(target,"antonym",synset,wordnetfile)

def add_hypernym_rel_to_ss(synset,target,wordnetfile):
    add_rel_to_ss(synset,"hypernym",target,wordnetfile)
    add_rel_to_ss(target,"hyponym",synset,wordnetfile)
        
# Attribute in Synsets verändern, z.B. ili
# change_attribute_in_ss('odenet-412-a','ili','i10007',r"C:\Users\melaniesiegel\Documents\05_Projekte\WordNet\OdeNet\deWNaccess\odenet_oneline.xml")

def change_attribute_in_ss(synset,att,value,wordnetfile):
        in_odenet = open(wordnetfile,"r",encoding="utf-8")
        lines = in_odenet.readlines()
        in_odenet.close()
        out_odenet = open(wordnetfile,"w",encoding="utf-8")
        ss_string = '<Synset id="' + synset + '"'
        for line in lines:
            if ss_string in line:
                line = re.sub(att + '="[a-zA-Z0-9]*"', att + '="'+ value +'"', line)
                print(line)
            out_odenet.write(line)
        out_odenet.close()

# Attribute zu Lexentries hinzufügen, z.B. confidenceScore

def change_attribute_in_lexentry(lemma,att,value,wordnetfile):
        de_wn = open(wordnetfile,"r",encoding="utf-8")
        lines = de_wn.readlines()
        de_wn.close()
        out_odenet = open(wordnetfile,"w",encoding="utf-8")
        lemma_string = 'Lemma writtenForm="' + lemma + '"'
        for line in lines:
            if lemma_string in line and att not in line:
                line = line.replace("><Lemma writtenForm=",' ' + att + '="'+ value + '"' + "><Lemma writtenForm=")
                print(line)
            out_odenet.write(line)
        out_odenet.close()
    
# Attribute zu Senses hinzufügen, z.B. note
# Sense id="w18234_4118-n" synset="odenet-4118-n" note="PHON:boːt"/>

def add_attribute_to_sense(sense_id,synset,att,value,wordnetfile):
        de_wn = open(wordnetfile,"r",encoding="utf-8")
        lines = de_wn.readlines()
        de_wn.close()
        out_odenet = open(wordnetfile,"w",encoding="utf-8")
        sense_string = 'Sense id="' + sense_id + '" synset="'+ synset + '"'
        for line in lines:
            if sense_string in line and value not in line:
#            if sense_string in line:
                line = line.replace(sense_string,sense_string + ' ' + att + '="'+ value + '"')
                print(line)
            out_odenet.write(line)
        out_odenet.close()
        

    
# Definitionen zu einem Synset hinzufügen    
def add_definition_to_ss(synset,definition, wordnetfile):
        de_wn = open(wordnetfile,"r",encoding="utf-8")
        lines = de_wn.readlines()
        de_wn.close()
        out_odenet = open(wordnetfile,"w",encoding="utf-8")
        ss_string = '<Synset id="' + synset + '"'
        definition_string = "<Definition>" + definition + "</Definition>"
        for line in lines:
            if ss_string in line and "<Definition>" not in line:
                if '<Example>' in line:
                    line = line.replace('<Example>', definition_string + '<Example>')
                elif '<SynsetRelation' in line:
                    line = line.replace('<SynsetRelation', definition_string + '<SynsetRelation',1)
                elif '</Synset>' in line:
                    line = line.replace('</Synset>', definition_string + '</Synset>')
                else:
                    line = line.replace('/>', '>' + definition_string + '</Synset>')
                print(line)
            out_odenet.write(line)
        out_odenet.close()

# Die englische Definition löschen
def delete_english_definition(synset, wordnetfile):
        de_wn = open(wordnetfile,"r",encoding="utf-8")
        lines = de_wn.readlines()
        de_wn.close()
        out_odenet = open(wordnetfile,"w",encoding="utf-8")
        ss_string = '<Synset id="' + synset + '"'
        for line in lines:
            if ss_string in line and "dc:description" in line:
                line=re.sub('dc:description=".*"','',line)
                print(line)
            out_odenet.write(line)
        out_odenet.close()

# Ein Beispiel einfügen

def add_example_to_ss(synset,example, wordnetfile):
        de_wn = open(wordnetfile,"r",encoding="utf-8")
        lines = de_wn.readlines()
        de_wn.close()
        out_odenet = open(wordnetfile,"w",encoding="utf-8")
        ss_string = '<Synset id="' + synset + '"'
        example_string = "<Example>" + example + "</Example>"
        for line in lines:
            if ss_string in line and "<Example>" not in line:
                if '</Synset>' in line:
                    line = line.replace('</Synset>', example_string + '</Synset>')
                print(line)
            out_odenet.write(line)
        out_odenet.close()



# Die Version ohne Zeilenumbruch als Pretty Print speichern

def prettyprint_odenet():
    oneline_odenet = open(r"odenet_oneline.xml","r", encoding="utf-8")
    lines = oneline_odenet.readlines()
    oneline_odenet.close()
    pretty_odenet = open(de_wn_file,"w",encoding="utf-8")
    for line in lines:
        line = line.replace("<Lemma","\n\t<Lemma")
        line = line.replace("<Sense","\n\t<Sense")
        line = line.replace("</Sense","\n\t</Sense")
        line = line.replace("</LexicalEntry>","\n</LexicalEntry>")
        line = line.replace("<SynsetRelation","\n\t<SynsetRelation")
        line = line.replace("<Definition>","\n\t<Definition>")
        line = line.replace("<Example>","\n\t<Example>")
        line = line.replace("</Synset>","\n</Synset>")
        line = line.replace("<SyntacticBehaviour","\n\t<SyntacticBehaviour")
        pretty_odenet.write(line)
    pretty_odenet.close()



    

