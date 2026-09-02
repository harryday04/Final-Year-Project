import numpy as np
import keygen

def decryptBit(ct,sk):
    a,b = ct
    x = (b - (np.dot(a,sk)/keygen.q)) %1
    if min(abs(x-0), 1-abs(x-0)) < min(abs(x-0.5), 1-abs(x-0.5)):
        return 0
    else:
        return 1
    
def main(ct,sk):
    plain_text = []
    for i in ct:
        plain_text.append(decryptBit(i,sk))
    return(plain_text)

