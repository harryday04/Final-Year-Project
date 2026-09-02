import numpy as np
import keygen

def decryptBit(ct,sk):
    a,b = ct
    x = (b - np.dot(a,sk)) % keygen.q
    return 0 if min(x, keygen.q - x)< min(abs(x - keygen.q//2), keygen.q - abs(x - keygen.q//2))else 1

def main(ct,sk):
    plain_text = []
    for i in ct:
        plain_text.append(decryptBit(i,sk))
    return(plain_text)

