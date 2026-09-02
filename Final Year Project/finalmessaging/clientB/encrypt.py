import secrets
import numpy as np
import keygen

def encryptBit(bit, pk):
    r =  np.array([secrets.randbits(1) for i in range(len(pk))])

    u = sum(r[i] * samp[0] for i, samp in enumerate(pk))
    u = np.mod(u, keygen.q).astype(np.int64)  # u is still a vector here
    
    v = int(sum(r[i] * samp[1] for i, samp in enumerate(pk))) % keygen.q
    v = (int(bit) * (keygen.q // 2) + v) % keygen.q
    return(u,v)

def main(pt, pk):
    pk = keygen.reconstruct(pk)
    cipher_text = []
    for i in pt:
        cipher_text.append(encryptBit(i,pk))
    return(cipher_text)