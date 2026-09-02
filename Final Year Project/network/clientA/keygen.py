import secrets
import numpy as np
#defines the length if our private key vector
n = 256

#modulus
q = 32768

# samples
m = (1+0.1)*(n+1)*np.log2(q)

#variables for our guassian
sigma = np.sqrt(n)

#generation of our private key
def private_key():
    return np.array([secrets.randbelow(q) for i in range(n)])

def sample():
    a = np.array([secrets.randbelow(q) for i in range(n)])
    u1 = secrets.SystemRandom().random()
    u2 = secrets.SystemRandom().random()
    z0= np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
    general_form = (sigma * z0)
    e = general_form /q
    inner_product = np.dot(a, sk)
    return (a, ((inner_product /q) +e) % 1)

def public_key():
    return [sample() for i in range(int(m))]


sk = private_key()
pk = public_key()

np.save("publickey.npy", np.array(pk, dtype=object))
np.save("privatekey.npy", np.array(sk, dtype=object))