from information_th import *
from transform import *

if __name__ == '__main__':
    #test : Louis Niango
    #table = ['N', 'I', 'A', 'N', 'G', 'O', 'L', 'O', 'U', 'I', 'S']
    #proba = [1/11, 2/11, 1/11, 2/11, 2/11, 1/11, 1/11, 1/11]
    message = "Niango Louis"
    code_val, code_bin, min_w, max_w, H = arithmetic_coding(message, 16)
    print(f"final interval : [{min_w}, {max_w}]")
    print(f"Value to be coded : {code_val} | Bitstream : {code_bin}")
    print(f"Size of de coded message: {size_of_message(min_w, max_w)} bits | {size_of_message(min_w, max_w) / 8} bytes")
    print(f"Entropy: {H} bits")