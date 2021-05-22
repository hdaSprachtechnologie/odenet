Open German WordNet
===

Introduction
---

The Open-de-WordNet initiative is based on the idea to have a German resource in a multilingual WordNet initiative, where the concepts (the synsets) of the languages are linked, and where the resources are under an open-source license, being eventually included in the NLTK language processing package. WordNet resources are largely used in NLP projects all over the world. Our idea is to create a German resource that starts from a crowd-developed thesaurus, is going to be open, and included in the NLTK package, such that it will be further developed by researchers while using the resource for their NLP projects.
For the first version, we combined two existing resources: The OpenThesaurus German synonym lexicon (https://www.openthesaurus.de/) and the Open Multilingual WordNet English (http://compling.hss.ntu.edu.sg/omw/) resource, the PrincetonWordNet of English (PWN). The OpenThesaurus is a great chance of using a large resource, generated and updated by the crowd. The PWN resource is a well-developed resource for English concepts. It includes many relations between the concepts and is linked to resources for multiple languages. 
OdeNet is still at the very beginning of its history. The first version was
created in spring 2017 as an experimental project at Darmstadt University
of Applied Sciences. It was completely automatically created. In the
following months up to summer 2017, manual corrections were made
in the domains of project management and business reports. German
definitions were introduced, relations were corrected and supplemented
and ili links (links to the multilingual concepts) were added. In autumn
and winter of 2017 we worked on the syntactic categories. The main focus
was on correcting the POS tags of the multiword lexemes.The next
step in winter 2017/18 was the annotation of basic German words, as
listed in https://de.wiktionary.org/wiki/Verzeichnis:Deutsch
Grundwortschatz. We annotated all lexical entries (except for function
words) of this list with

`dc:type="Basiswortschatz"`

in OdeNet, added missing entries and corrected synsets manually. Then,
we implemented an analysis of German nominal compounds and used
this information for the addition of hypernym relations.

The current version is automatically compiled. We have started to check synsets manually. 

The jupyter notebook file contains methods to access the data.

Installation
---

For an Anaconda environment, where `pip` is available, please `cd`
to the appropriate package directory, where the `setup.py` file is
located and type either

`pip install .`

for a user installation or

`pip install -e .`

for a developer installation (`-e` for editable). 

The difference between those is that the first
copies all files into the Python environment and they can only
be modified directly (which is discouraged) or by reinstalling
the package. The latter option provides only a link from your local
Python environment to the actual directory and therefore it is
possible to modify the files on the fly and still use the package
in a pythonic way.

OdeNet is now released in the WN package and can be downloaded and used from there. Documentation about the usage: https://wn.readthedocs.io/en/latest/index.html

Basic Usage
---

TO BE WRITTEN (depends on interface)

Uninstall
---

Open the Anaconda terminal and type `pip uninstall odenet`.

License
---

The Open German WordNet is openly licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).

The Python code files are openly licensed under the [MIT License](https://opensource.org/licenses/MIT).

Citation
---

The canonical citation(s) are in [citation.bib](citation.bib), in bibtex format.  Please cite them when you write a paper that uses (or refers to) OdeNet.