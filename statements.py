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
        self.dictionary[stem].append(cat)
        
    def getall(self, cat):
        list = []
        for key in self.dictionary.keys():
            if self.dictionary[key] == [cat]:
                list.append(key)
        return list
        

class FactBase:
    """stores unary and binary relational facts"""
    # two dictionaries: one for unary and one for binary
    def __init__(self):
        self.unary = defaultdict(list)
        self.binary = defaultdict(list)
    
    def addUnary(self, pred, e1):
        self.unary[pred] = e1
        
    def queryUnary(self, pred, e1):
        if pred in self.unary.keys():
            if self.unary[pred] == e1:
                return True
            else:
                return False
    
    def addBinary(self, pred, e1, e2):
        self.binary[pred] = (e1, e2)
    
    def queryBinary(self, pred, e1, e2):
        if pred in self.binary.keys():
            if self.binary[pred] == (e1, e2):
                return True
            else:
                return False
    

import re
from nltk.corpus import brown 

def endswith(string, suffix):
    n = len(suffix)
    return (string[-n:] == suffix)

def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    
    # stem ends in anything except s,x,y,z,ch,sh OR a vowel, add s (eats, tells, shows)
    exceptions_1 = ['s','x','y','z','a','e','i','o','u']
    exceptions_2 = ['ch','sh']
    if (s[-2:] != exceptions_1 and s[-3:] != exceptions_2):
        return s[:-1]
    # if the stem ends in y preceeded by a vowel, simply add s (pays, buys)
    if (re.match("[aeiou]y", s[-3:-1])):
        return s[:-1]
    # if the stem ends in y preceded by a non-vowel and contains at least three letters, change the y to ies
    if (endswith(s,'ies')):
        if re.match('.*[^aeiou]$', s[:-3]):
            if len(s) > 4:
                return s[:-3] + 'y'
            elif len(s) == 4:
                return s[:-1]

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

