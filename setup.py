"""
Setup odenet.
"""

from setuptools import setup

long_description=\
"""
Open German Wordnet
---

* German resource in a multi-lingual WordNet intitiative
* Combined from two sources:
   - The OpenThesaurus German synonym lexicon (https://www.openthesaurus.de/)
   - the Open Multilingual WordNet English (http://compling.hss.ntu.edu.sg/omw/) resource, the PrincetonWordNet of English (PWN).
* Goals:
   - Including resource into NLTK
   - Provide ILI links to other languages
   - ...
"""

setup(
    name="odenet",
    packages=["odenet"],
    package_data={"odenet": ["wordnet/deWordNet.xml"]},
    include_package_data=True,
    version="0.1.0",
    description="Open German WordNet",
    author="Melanie Siegel",
    author_email="melanie.siegel@h-da.de",
    url="https://ikum.mediencampus.h-da.de/projekt/open-de-wordnet-initiative/",
    keywords=["german", "wordnet", "xml"],
    classifiers=[
          'Development Status :: 2 - Pre-Alpha',  # can be updated, when project is more mature
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',  # TODO: is it really usable by End Users?
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',  # Python codes, there is no License classifier for CC-BY-SA 4.0
          'Natural Language :: German',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Education',
          'Topic :: Text Processing :: Linguistic',
          'Topic :: Utilities'
    ],
    long_description=long_description
)
