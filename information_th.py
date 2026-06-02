"""
# https://www.khanacademy.org/computing/computer-science/informationtheory/info-theory/v/intro-information-theory
# Arithmetic coding: https://github.com/nayuki/Reference-arithmetic-coding/tree/master/cpp
# https://web.stanford.edu/class/ee398a/projects.htm
# https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/pages/lecture-notes/
# Github repo: https://github.com/leandromoreira/digital_video_introduction#vlc-coding
"""

import numpy as np 
import matplotlib.pyplot as plt 
import cv2 as cv
import random

def create_intervals(dico_sorted, min, max):
    # create ranges 
    cumulative = min
    intervals  = {}
    for symbol, p in dico_sorted:
        low    = cumulative
        high   = cumulative + p * (max - min)
        
        intervals[symbol] = (low, high)
        cumulative        = high
    print(f"Interval : {intervals}")
    
    return intervals

# Custom arithmetic coding
def arithmetic_coding(table, proba):
    """
    table  : table of symbols
    proba. : likelihood of symbols 
    return : bitstream
    """
    save_table = table
    
    #Create a dictionary
    if len(table) != len(proba):
        #raise KeyError("Please verify table dimensions")
        print("Please verify table dimensions")
    
    dico = {}
    for j in range(len(table)):
        dico[table[j]] = proba[j]
    # Sort dictionary
    dico_sorted = sorted(dico.items(), key = lambda x : x[1], reverse=True)
    
    range_min = 0
    range_max = 1
    min_w, max_w = 1, 1
    
    # create initial intervals
    intervals = create_intervals(dico_sorted, range_min, range_max)
    
    for i in range(len(table)):
        range_min, range_max = intervals[table[i]]
        print(f"Returned interval of {table[i]} ---> [ {range_min}; {range_max} ]")
        #range_min, range_max = range_min * min_w
        min_w, max_w = range_min, range_max
        intervals = create_intervals(dico_sorted, min_w, max_w)
    
    # final range for coding Sequence: [min_w, max_w]
    print(f"Last interval : [{min_w}, {max_w}]")
    code_val = random.uniform(min_w, max_w)
    
    return code_val
    
    
#def aritmetic_decoding():
    
#test
table = ['B', 'A', 'C']
proba = [0.25, 0.25, 0.5]
code_val = arithmetic_coding(table, proba)
print(f"Value to be coded: {code_val}")