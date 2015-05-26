# -*- coding: utf-8 -*-
# Natural Language Toolkit: Machine Translation Utilities
#
# Copyright (C) 2001-2014 NLTK Project
# Author: Liling Tan
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#
from __future__ import print_function
import io, gzip, mimetypes

def read_phrase_table(phrasetablefile):
    """
    This module reads a phrase table file that is commonly used by 
    machine translation decoder. The phrase table file is a tab-separated file.
    Each line of the phrase table file contains the:
    a.   source phrase
    b.  target phrase 
    c. translation probabilities 
        c1. inverse phrase translation probability φ(f|e)
        c2. inverse lexical weighting lex(f|e)
        c3. direct phrase translation probability φ(e|f)
        c4. direct lexical weighting lex(e|f)
    d.  word alignments (in pharaoh format)
    
    When translating from source language, e, to target language, f, the noisy
    channel model requires the φ(f|e).
    
    For more information of the phrase table file format, 
    see http://www.statmt.org/moses/?n=FactoredTraining.ScorePhrases 
    
    >>> model_file = get_moses_sample_model('phrase-model', 'phrase-table')
    >>> x = read_phrase_table(model_file)
    >>> x == {u'es gibt': {u'there is': 1.0}, u'klein': {u'small': 0.8, u'little': 0.8}, u'die': {u'the': 0.3}, u'der': {u'the': 0.3}, u'haus': {u'house': 1.0}, u'ist': {u'is': 1.0, u"'s": 1.0}, u'kleines': {u'small': 0.2, u'little': 0.2}, u'gibt': {u'gives': 1.0}, u'es ist': {u'this is': 0.2, u'it is': 0.8}, u'das': {u'this': 0.1, u'the': 0.4, u'it': 0.1}, u'alt': {u'old': 0.8}, u'ein': {u'a': 1.0, u'an': 1.0}, u'altes': {u'old': 0.2}, u'das ist': {u'this is': 0.8, u'it is': 0.2}}
    True
    >>> x['es gibt'] == {u'there is': 1.0}
    True
    
    :type phrasetablefile: str
    :param phrasetablefile: the filename for the phrase table .gz file. 
    :rtype: dict
    :return: a dictionary of dictionary where the keys are the source language 
    phrases and their values are a dictionary of the target language phrases 
    and its probability.
    """
    phrase_table = {}
    
    # Checks if phrase table file is gzip file format.
    if mimetypes.guess_type(phrasetablefile)[1] == 'gzip':
        anyopen = gzip.open
    else: 
        anyopen = io.open
    
    with anyopen(phrasetablefile, 'rb') as fin:
        for line in fin:
            # Splits the tab separated file.
            line = line.decode('latin-1').strip().split(' ||| ')
            # Only first three columns are necessary for phrase-based MT.
            src, trg, probabilities = line[:3]
            # Only the φ(f|e) is required.
            prob = float(probabilities.split( )[0])
            phrase_table.setdefault(src, {})[trg]= prob
        
    return phrase_table



def read_lang_model(arpafile):
    """
    The module reads a ngram language model file in ARPA format. 
    The ngram probabilities and backoff probabilities are stored in 
    tab-separated columns, each row represents an ngram and its probabilities.
    For example:
    
        \data\
        ngram 1=37344
        ngram 2=715602
        
        \1-grams:
        -2.785123    </s>
        -99    <s>    -1.750062      
        
        \2-grams:
        -1.226477    it is    -1.013582
        
    The first column stores the log probabitlity of the ngram
    The second column stores the surface string of the ngram
    The third column stores the backoff probabitlites of the ngram
    
    Note: Rows with less than 2 columns can be ignored as they do not store the
    ngrams, they are usually meta-data on the ngram extracted or comment lines
    to separated to n from the n+1 grams.
    
    For more information on the ARPA format, see
    http://www.speech.sri.com/projects/srilm/manpages/ngram-format.5.html
    
    >>> model_file = get_moses_sample_model('lm','europarl.srilm.gz')
    >>> y = read_lang_model(model_file)
    >>> print(y[('<s>',)])
    (-99.0, -1.750062)
    
    :type arpafile: str
    :param arpafile: the filename for the phrase table .gz file. 
    :rtype: dict
    :return: a dictionary of dictionary where the key is the source language 
    phrase and its value is a dictionary of the target language phrase and its
    probability.
    """
    lang_model = {}
    
    with gzip.open(arpafile, 'r') as fin:
        for line in fin:
            # Splits the tab separated file.
            line = line.decode('latin-1').strip()
            line = line.split('\t')
            if len(line) > 1:
                try: # When backoff is available.
                    prob, ngram, backoff = line[:3]
                except ValueError: # When backoff is not available.
                    prob, ngram, backoff = line[:2] + [0]
                lang_model[tuple(ngram.split())] = (float(prob), float(backoff))
    # Sets a default for unknown words if <unk> not in language model.
    if '<unk>' not in lang_model.keys():
        lang_model[('<unk>',)] = (float(-100), 0)
    return lang_model


def get_moses_sample_model(approach, filename):
    """
    This function returns the nltk_data path that stores the moses sample models. 
    
    >>> model_filename = get_moses_sample_model('lm', 'europarl.srilm.gz')
    >>> "/".join(model_filename.split('/')[-5:])
    'nltk_data/models/moses_sample/lm/europarl.srilm.gz'
    
    These *approach*es are available in the moses_sample directory:
    - lm
    - phrase-model
    - string-to-tree
    - tree-to-tree
    
    :type approach: str
    :param approach: the approach that the model was built on 
    :type filename: str
    :param filename: the name of the file that you want to access from 
    the moses_sample directory 
    :rtype: str
    :return: The full path of the file where nltk_data saves the moses
    sample models. 
    """
    from nltk import data
    nltk_data_path = data.path[0]
    model_file = "/".join([nltk_data_path, 'models/moses_sample',
                           approach, filename]) 
    return model_file

def get_momo(approaches, model_name):
    """
    This is a duck-type function that for get_moses_sample_model().
    This is just to shorted the function call. One could also use:
    
    >>> from util import get_moses_sample_model as get_momo
    """
    return get_moses_sample_model(approaches, model_name)


# run doctests
if __name__ == "__main__":
    import doctest
    doctest.testmod()
