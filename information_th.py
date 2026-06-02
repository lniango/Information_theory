"""
# https://www.khanacademy.org/computing/computer-science/informationtheory/info-theory/v/intro-information-theory
# Arithmetic coding: https://github.com/nayuki/Reference-arithmetic-coding/tree/master/cpp
# https://web.stanford.edu/class/ee398a/projects.htm
# https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/pages/lecture-notes/
# Github repo: https://github.com/leandromoreira/digital_video_introduction#vlc-coding
# https://go-compression.github.io/algorithms/arithmetic/
"""

from collections import Counter

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
        #print(f"[{low}, {high}]")
    binary_str = "0." + "".join(str(b) for b in bits)
    
    return binary_str

def size_of_message(min_val, max_val):
    #print(f"Rounded low : {round(min_val, 2)} | Rounded high : {round(max_val, 2)}")
    width = round(max_val, 4) - round(min_val, 4)
    
    if width <= 0:
        return float('inf')  # high value
    
    return -math.log2(width)

def compute_entropy(dictionary):
    """
    Mean of the Minimum value of the length of the code used to encode each symbol 
    
    Input: dictionary
    return: Entropy
    """
    H = 0.0
    for symbol, p in dictionary.items():
        H += -p * math.log2(p)
    return H

def build_proba(message):
    counts = Counter(message)
    total = len(message)
    return {s: c / total for s, c in counts.items()}
        

# Custom arithmetic coding
def arithmetic_coding(message, precision):
    """
    message : string to encode
    precision: number of bits of the final code
    return  : code value, bitstream, interval, entropy
    """

    message = list(message)

    # pbuild robability 
    proba = build_proba(message)

    # sort symbols by probability (important for deterministic intervals)
    dico_sorted = sorted(proba.items(), key=lambda x: x[1], reverse=True)

    # initial full interval
    low, high = 0.0, 1.0

    # build intervals once (global model) from 0 to 1
    intervals = create_intervals(dico_sorted, low, high)

    # arithmetic encoding loop 
    for symbol in message:
        range_width = high - low

        sym_low, sym_high = intervals[symbol]

        new_low  = low + range_width * sym_low
        new_high = low + range_width * sym_high

        low, high = new_low, new_high

        # recompute intervals inside new range
        #intervals = create_intervals(dico_sorted, low, high)

    # final code = any point in final interval (deterministic, NOT random)
    code_val = (low + high) / 2

    # convert to bitstream 
    code_bin = float2bit(code_val, precision)

    # entropy of source model
    H = compute_entropy(proba)
    #print(f"Low: {low} | HIGH: {high}")

    return code_val, code_bin, low, high, H
    
    
#def aritmetic_decoding():
    
#test : Louis Niango
#table = ['N', 'I', 'A', 'N', 'G', 'O', 'L', 'O', 'U', 'I', 'S']
#proba = [1/11, 2/11, 1/11, 2/11, 2/11, 1/11, 1/11, 1/11]
message = "Niango Louis"
code_val, code_bin, min_w, max_w, H = arithmetic_coding(message, 4)
print(f"final interval : [{min_w}, {max_w}]")
print(f"Value to be coded : {code_val} | Bitstream : {code_bin}")
print(f"Size of de coded message: {size_of_message(min_w, max_w)} bits")
print(f"Entropy: {H} bits")