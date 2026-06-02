"""
# https://www.khanacademy.org/computing/computer-science/informationtheory/info-theory/v/intro-information-theory
# Arithmetic coding: https://github.com/nayuki/Reference-arithmetic-coding/tree/master/cpp
# https://web.stanford.edu/class/ee398a/projects.htm
# https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/pages/lecture-notes/
# Github repo: https://github.com/leandromoreira/digital_video_introduction#vlc-coding
# https://go-compression.github.io/algorithms/arithmetic/
"""

import numpy as np 
import matplotlib.pyplot as plt 
import cv2 as cv
import random
import math

def create_intervals(dico_sorted, min, max):
    """
    create cumulative intervals depending on min and max
    """
    # create ranges 
    cumulative = min
    intervals  = {}
    for symbol, p in dico_sorted:
        low    = cumulative
        high   = cumulative + p * (max - min)
        
        intervals[symbol] = (low, high)
        cumulative        = high
    #print(f"Interval : {intervals}")
    
    return intervals

def float2bit(number, precision):
    """
    Convert a float number between 0 and 1 into bits
    with respect to a precision
    """
    low  = 0
    high = 1
    bits = []
    #mid  = 0
    
    for i in range(precision):
        mid = (high - low) / 2 + low
        if number >= mid:
            bit = 1
            low = mid
        else:
            bit  = 0
            high = mid
        bits.append(bit)
        print(f"[{low}, {high}]")
    binary_str = "0." + "".join(str(b) for b in bits)
    
    return binary_str

def size_of_message(min_val, max_val):
    return -math.log2(max_val - min_val)

def compute_entropy():
    """
    Mean of the Minimum value of the length of the code used to encode each symbol 
    
    Input: dictionary
    """
    
        

# Custom arithmetic coding
def arithmetic_coding(table, proba):
    """
    table  : table of symbols
    proba. : likelihood of symbols 
    return : float value to be coded, bitstream, interval
    """
    save_table = table
    
    #Create a dictionary
    if len(table) != len(proba):
        raise KeyError("Please verify table dimensions")
        #print("Please verify table dimensions")
    
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
        #print(f"Returned interval of {table[i]} ---> [ {range_min}; {range_max} ]")
        #range_min, range_max = range_min * min_w
        min_w, max_w = range_min, range_max
        intervals = create_intervals(dico_sorted, min_w, max_w)
    
    # final range for coding Sequence: [min_w, max_w]
    #print(f"Last interval : [{min_w}, {max_w}]")
    code_val = round(random.uniform(min_w, max_w), 4)
    
    # Conversion: float to bits
    code_bin = float2bit(code_val, 16) 
    
    return code_val, code_bin, min_w, max_w
    
    
#def aritmetic_decoding():
    
#test : Louis Niango
table = ['A', 'I', 'G', 'N', 'O', 'S', 'U', 'L']
proba = [1/11, 2/11, 1/11, 2/11, 2/11, 1/11, 1/11, 1/11]
code_val, code_bin, min_w, max_w = arithmetic_coding(table, proba)
print(f"Size of de coded message: {size_of_message(min_w, max_w)} bits")
print(f"Value to be coded : {code_val} | Bitstream : {code_bin}")