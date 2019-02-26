from bitstring import BitArray
import numpy as np
from collections import defaultdict
    
LEGAL = set('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM. ,?!1234567890()&$\'"-')

N = 3

def ngrams():
    """
    returns n-gram counts for shakespeare corpus
    """
    d = defaultdict(int)
    s = ''
    with open('shakespeare.txt', 'r') as f:
        for line in f:
            s += line.strip() + ' '
            for i in range(len(s)-N+1):
                d[s[i:i+N].lower()] += 1
            s = s[-N+1:]
    return d

ngrams = ngrams()

def byteSum(a, b):
    """
    Addition of 8-bit bytes, modulo 256
    :param a: Bits object of length 8
    :param b: Bits object of length 8
    :return: Bits object of length 8, sum of two inputs modulo 256
    """
    mask = (1 << 8) - 1
    return BitArray(uint=(a.uint + b.uint) & mask, length=8)

def readbits():
    """
    returns list of 8-bit BitArray objects, read from cipher.txt
    """
    bits = []
    with open('cipher.txt', "r") as f:
        text = f.readline().strip().split()
        bits = [BitArray(uint=int(h, 16), length=8) for h in text]
    return bits


def choosebest(message, c1, c2):
    """
    chooses the best char to follow the message
    
    returns '1' or [literally anything else]
    """
    # legality check
    if c1 not in LEGAL:
        if c2 not in LEGAL:
            raise "something is wrong"
        return 2

    if c2 not in LEGAL:
        return '1'

    # heuristics
    # captial letters can only come after spaces
    if c1.lower() != c1:
        if message[-1] != ' ':
            return 2
    if c2.lower() != c2:
        if message[-1] != ' ':
            return '1'

    # ngram probability
    print('have to use prob:', c1, c2)
    # use 3-grams for now
    p1 = ngrams[(message[-N+1:] + c1).lower()]
    p2 = ngrams[(message[-N+1:] + c2).lower()]

    print(c1, p1, c2, p2)
    if p1 > p2:
        return '1'
    return 2

def promptpad(message, bits, lastpad):
    """
    returns the next pad
    """
    c = BitArray(uint=int('0x5A', 16), length=8)
    rev = pad
    rev.reverse()
    i = choosebest(message, str(chr((bits ^ rev).uint)), str(chr((bits ^ byteSum(rev, c)).uint)))
    if i == '1':
        return rev
    else:
        return byteSum(rev, c)


bits = readbits()

pad = BitArray(uint=int('0x5a',16), length=8)
message = str(chr((bits.pop(0) ^ pad).uint))
for b in bits:
    print('message so far:', message)
    pad = promptpad(message, b, pad)
    message += str(chr((b ^ pad).uint))

print('"' + message + '"')



