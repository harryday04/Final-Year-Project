import secrets
import numpy as np

def encryptBit(bit, pk):
    r =  np.array([secrets.randbits(1) for i in range(len(pk))])
    return(sum(r[i] * samp[0] for i,samp in enumerate(pk)), int(bit)/2 + sum(r[i] * samp[1] for i,samp in enumerate(pk)))

def main(pt, pk):
    cipher_text = []
    for i in pt:
        cipher_text.append(encryptBit(i,pk))
    return(cipher_text)