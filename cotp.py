"""
6.857 Spring, 2019
PSet 1
Problem 1-2
cotp.py

This file implements the cheap one-time pad and was used to generate the challenge ciphertext. Feel
free to use this code as part of your solution or to test your solution.

Packages Required: bitstring, random
See https://pythonhosted.org/bitstring/constbitarray.html for bitstring docs
This code was tested using Python 3.6.7.
"""

from bitstring import Bits
from random import SystemRandom

def byteSum(a, b):
    """
    Addition of 8-bit bytes, modulo 256
    :param a: Bits object of length 8
    :param b: Bits object of length 8
    :return: Bits object of length 8, sum of two inputs modulo 256
    """
    mask = (1 << 8) - 1
    return Bits(uint=(a.uint + b.uint) & mask, length=8)

def generatePadByte(prevByte):
    """
    Computes and returns the next byte of the pad, following the formula
    p_i = (reverse(p_{i-1}) + (r_i * 0x5A)) % 256
    :param prevByte: Bits object of length 8
    :return: Bits object of length 8, representing the next byte of the pad
    """
    c = Bits(hex='0x5A')
    r_i = SystemRandom().randint(0,1)
    mask = Bits(uint=((1 << 8) - 1) * r_i, length=8) & c
    reverse = Bits(bytes=prevByte.tobytes())[::-1]
    return byteSum(reverse, mask)

def generatePad(length):
    """
    Given a length n of a pad P, generates a pad P = (p_1, .., p_n) from the following formula
    p_i = (reverse(p_{i-1}) + (r_i * 0x5A)) % 256
    :param length: length of bytes in pad P, also n
    :return: Bits object containing the pad
    """
    if (length <= 0):
        raise ValueError("Message length must be nonzero")
    # initialize p_0 to be 0, but this is not included in the n-byte pad P
    prevByte = Bits('0x00')
    pad = Bits()
    # pad is length n, as p_1, ..., p_n, not including p_0
    for i in range(length):
        currByte = generatePadByte(prevByte)
        # concatenate pad bytes
        pad += currByte
        prevByte = currByte
    return pad

def charToBits(char):
    """
    Converts char to Bits object
    :param char: unicode character
    :return: Bits object of the char
    """
    return Bits(uint=ord(char), length=8)

def encrypt(message, verbose=False):
    """
    Given a message as a string, encrypts it using COTP.
    :param message: string
    :return: tuple of the form (ciphertext, pad), where both are Bits objects
    """
    if len(message) == 0:
        raise ValueError("Message must be nonempty")

    # encodedMessage is M = (m_1, ..., m_n)
    # i.e. concatenated bytes representing the chars
    encodedMessage = charToBits(message[0])
    for i in range(1, len(message)):
        encodedMessage += charToBits(message[i])

    pad = generatePad(len(message))

    ciphertext = encodedMessage ^ pad
    assert (ciphertext ^ pad == encodedMessage)

    if verbose:
        print("Pad = " + str(pad.bin))
        print("Ciphertext = " + str(ciphertext.bin))

    return (ciphertext, pad)


def decrypt(ciphertext, pad, verbose=False):
    """
    Given a ciphertext and pad, decrypts to get the message
    Note: can be used for partial ciphertexts and pads up to a certain same length
    :param ciphertext: Bits object of the ciphertext
    :param pad: Bits object of the pad
    :return: message as a string
    """
    if not isinstance(ciphertext, Bits):
        raise ValueError("Ciphertext must be a Bits object")
    if not isinstance(pad, Bits):
        raise ValueError("Pad must be a Bits object")
    if len(ciphertext) != len(pad):
        raise ValueError("Ciphertext (length: %d) and pad (length: %d) must have the same length"
         % (len(ciphertext),len(pad)))
    if len(ciphertext) == 0:
        raise ValueError("Ciphertext must be nonempty")
    if len(ciphertext) % 8 != 0:
        raise ValueError("Ciphertext must consist of complete bytes")

    encodedMessage = ciphertext ^ pad
    message = ""
    for i in range(0, len(encodedMessage), 8):
        message += chr(encodedMessage[i:i+8].uint)

    if verbose:
        print("message = " + message)

    return message

### Commented out below is the script code used to generate the message ciphertext. ###
### Note that the 504 long character message has been omitted. ###
 
## def main():
##     message = "**REDACTED**"
##     ciphertext, pad = encrypt(message)
## 
##     with open('cipher.txt', "w+") as f:
##         hexstring = ciphertext.hex
##         # insert a space between every hex byte
##         hexstring = " ".join(hexstring[i:i+2] for i in range(0, len(hexstring), 2))
##         f.write(hexstring)
## 
## if __name__ == "__main__":
##     main()
