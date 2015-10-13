# -*- coding: utf-8 -*-
"""
Tests for BLEU translation evaluation metric
"""

import unittest
from nltk.translate.bleu_score import _modified_precision

class TestBLEU(unittest.TestCase):
    def test__modified_precision(self):
        """
        Examples from the original BLEU paper 
        http://www.aclweb.org/anthology/P02-1040.pdf
        """
        # Example 1: the "the*" example.
        # Reference sentences.
        ref1 = 'the cat is on the mat'.split()
        ref2 = 'there is a cat on the mat'.split()
        # Hypothesis sentence(s).
        hyp1 = 'the the the the the the the'.split()
        
        references = [ref1, ref2] 
        
        # Testing modified unigram precision.
        assert (_modified_precision(references, hyp1, n=1) == 0.2857142857142857)
        
        # Testing modified bigram precision.
        assert(_modified_precision(references, hyp1, n=2) == 0.0)
        
        
        # Example 2: the "of the" example.
        # Reference sentences
        ref1 = str('It is a guide to action that ensures that the military '
                   'will forever heed Party commands.').split()
        ref2 = str('It is the guiding principle which guarantees the military '
                   'forces always being under the command of the Party.').split()
        ref3 = str('It is the practical guide for the army always to heed '
                   'the directions of the party').split()
        # Hypothesis sentence(s).
        hyp1 = 'of the'.split()
        
        references = [ref1, ref2, ref3] 
        # Testing modified unigram precision.
        assert (_modified_precision(references, hyp1, n=1) == 1.0)
        
        # Testing modified bigram precision.
        assert(_modified_precision(references, hyp1, n=2) == 1.0)
        

        # Example 3: Proper MT outputs.
        hyp1 = str('It is a guide to action which ensures that the military '
                   'always obeys the commands of the party').split()
        hyp2 = str('It is to insure the troops forever hearing the activity '
                   'guidebook that party direct').split()
        
        references = [ref1, ref2, ref3]
        
        # Unigram precision.
        assert (_modified_precision(references, hyp1, n=1) == 0.9444444444444444)
        assert (_modified_precision(references, hyp2, n=1) == 0.5714285714285714)
        
        # Bigram precision
        assert (_modified_precision(references, hyp1, n=2) == 0.5882352941176471)
        assert (_modified_precision(references, hyp2, n=2) == 0.07692307692307693)

    def test_brevity_penalty(self):
        pass