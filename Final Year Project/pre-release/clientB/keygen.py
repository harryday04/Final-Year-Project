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


def seed_gen():
    return secrets.token_bytes(32)

def a_vectors(seed):
    rng = np.random.default_rng(np.frombuffer(seed, dtype=np.uint8))
    return rng.integers(0, q, size=(int(m), n), dtype=np.int64)

def reconstruct(pk):
    seed = pk[0]
    a = a_vectors(seed)
    return list(zip(a,pk[1]))

#generation of our private key
def private_key():
    return np.array([secrets.randbelow(q) for i in range(n)])

def sample(a,sk):
    u1 = secrets.SystemRandom().random()
    u2 = secrets.SystemRandom().random()
    while u1 == 0:
        u1 = secrets.SystemRandom().random()
    z= np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
    e = int(round(sigma * z)) % q
    inner_product = int(np.dot(a, sk)) % q
    return ((inner_product + e) % q)

def public_key(sk):
    seed = seed_gen()
    a = a_vectors(seed)
    b = np.array([sample(i,sk) for i in a])
    return seed,b

def main():
    sk = private_key()
    pk = public_key(sk)

    np.save("publickey.npy", np.array(pk, dtype=object))
    np.save("privatekey.npy", np.array(sk, dtype=object))

main()