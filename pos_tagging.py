# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    NN = []
    NNS = []
    with open("sentences.txt", "r") as f:
        for line in f:
            # relevant tags = NN and NNS
            wordtags = line.split(" ")
            for pair in wordtags:
                newpair = pair.split("|")
                if (newpair[1] == "NN"):
                    NN.append(newpair[0])
                elif (newpair[1] == "NNS"):
                    NNS.append(newpair[0])
    nounslist = list(set(NN) & set (NNS))
    return nounslist


unchanging_plurals_list = unchanging_plurals()

#print unchanging_plurals_list

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""   
    if (re.match('.*men', s)):
        stem = s[:-3] + 'man'
    elif s in unchanging_plurals_list:
        stem = s
    else:
        stem = verb_stem(s)

    return stem

#print noun_stem("women")
#print noun_stem("sheep")
#print noun_stem("dogs")
#print noun_stem("countries")

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    # add code here
    word_tags = []
    # P A N(NP NS) I(IS IP) T(TS TP)
    # populate the word_tags list
    for word, tag in function_words_tags:
        if word == wd:
            word_tags.append(tag)

    for word in lx.getAll('P'):
        if word == wd:
            word_tags.append('P')
    
    for word in lx.getAll('A'):
        if word == wd:
            word_tags.append('A')

    for word in lx.getAll('N'):
        if (word == wd) or (word == noun_stem(wd)):
            if word in unchanging_plurals_list:
                word_tags.append('Ns')
                word_tags.append('Np')
            elif (noun_stem(wd) == ''): # if the plural form does not exist
                word_tags.append('Ns')
            else:
                word_tags.append('Np')
    
    for word in lx.getAll('I'):
        if (word == wd) or (word == verb_stem(wd)):
            if (verb_stem(wd) == ''):
                word_tags.append('Is')
            else:
                word_tags.append('Ip')

    for word in lx.getAll('T'):
        if (word == wd) or (word == verb_stem(wd)):
            if (verb_stem(wd) == ''):
                word_tags.append('Ts')
            else:
                word_tags.append('Tp')
        
    
    return word_tags
    

#lx1 = Lexicon()
#lx1.add('John', 'P')
#lx1.add('orange', 'N')
#lx1.add('orange', 'A')
#lx1.add('fish', 'N')
#lx1.add('fish', 'I')
#lx1.add('fish', 'T')
#lx1.add('like', 'T')
#lx1.add('duck', 'N')
#lx1.add('fly', 'T') 
#print(tag_word(lx1, 'John'))
#print(tag_word(lx1, 'a'))
#print(tag_word(lx1, 'orange'))
#print(tag_word(lx1, 'fishes'))
#print(tag_word(lx1, 'like'))
#print(tag_word(lx1, 'duck'))
#print(tag_word(lx1, 'fly'))

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.