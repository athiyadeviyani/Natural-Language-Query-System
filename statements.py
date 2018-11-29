# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

# use defaultdict to create a dictionary WITHOUT unique keys
from collections import defaultdict

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    def __init__(self):
        self.dictionary = defaultdict(list)
    
    def add(self, stem, cat):
        add(self.dictionary[cat], stem)
        
    def getAll(self, cat):
        return self.dictionary[cat]

   

class FactBase:
    """stores unary and binary relational facts"""
    # two dictionaries: one for unary and one for binary
    def __init__(self):
        self.unary = defaultdict(list)
        self.binary = defaultdict(list)
    
    def addUnary(self, pred, e1):
        add(self.unary[pred], e1)

    def addBinary(self, pred, e1, e2):
        add(self.binary[pred], (e1, e2))
        
    def queryUnary(self, pred, e1):
        if (e1 in self.unary[pred]):
            return True
        return False
    
    def queryBinary(self, pred, e1, e2):
        if ((e1, e2) in self.binary[pred]):
            return True
        return False
    

import re
from nltk.corpus import brown 

def endswith(string, suffix):
    n = len(suffix)
    return (string[-n:] == suffix)

def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    if re.match('.*s$', s):

    # if the stem ends in y preceded by a non vowel and contains at least three letters, change the y to ies
    # flies, tries, unifies
        if re.match('.*ies', s):
            if s == 'unties':
                return 'untie'

    # if the stem is of the form Xie where X is a single letter other than a vowel, simply add s 
    # dies, lies, ties - note that this doesn't account for unties
            elif (re.match('[^aeiou]ies', s) and len(s) == 4):
                return s[:-1]
            else:
                if len(s) >= 5:
                    return s[:-3]+'y'

    # if the stem ends in y preceded by a vowel, simply add s
    # pays, buys
        if re.match('.*[aeiou]ys$', s):
            return s[:-1]

    # if the stem ends in o, x, ch, sh, ss, or zz, add es
    # goes, boxes, attaches, washes, dresses, fizzes
        if re.match('.*([ox]|ch|sh|ss|zz)es',s):
            return s[:-2]
    
    # if the stem ends in se or ze but not in sse or zze, add s 
    # loses, dazes, lapses, analyses
        if re.match('.*([^sz])(se|ze)s', s):
            return s[:-1]

    # if the stem ends in e not preceded by i, o, s, x, z, ch, sh, just add s
    # likes, hates, bathes
        if re.match('.*[^iosxz]es', s):
            return s[:-1]
    
    # if the stem ends in anything except s,x,y,z,ch,sh or a vowel, simply add s
    # eats, tells, shows
        if re.match('.*[^sxyzaeiou]s', s):
            return s[:-1]
        
        else:
            return ""

    # if the stem is have, its 3s form is has
    if (s == 'have'):
        return 'has'

    else:
        return ""

######## TEST CODE    

#a = ["eats","tells","shows"]
#b = ["pays","buys"]
#c = ["flies","tries","unifies"]
#d = ["dies","lies","ties","unties"]
#e = ["goes","boxes","attaches","washes","dresses","fizzes"]
#f = ["loses","dazes","lapses","analyses"]
#g = ["have"]
#h = ["likes","hates","bathes"]

#for verb in a:
#    print verb_stem(str(verb))

#for verb in b:
#    print verb_stem(str(verb))

#for verb in c:
#    print verb_stem(str(verb))

#for verb in d:
#    print verb_stem(str(verb))

#for verb in e:
#    print verb_stem(str(verb))

#for verb in f:
#    print verb_stem(str(verb))

#for verb in g:
#    print verb_stem(str(verb))

#for verb in h:
#    print verb_stem(str(verb))

#print verb_stem("flys")


def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.