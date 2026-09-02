
import secrets
import numpy as np

np.set_printoptions(legacy='1.25')

#defines the length if our private key vector
length = 256

#modulus
modulus = 32768

# samples
m = (1+0.1)*(length+1)*np.log2(modulus)

#variables for our guassian
sigma = np.sqrt(length)

#generation of our private key
def private_key(n, q):
    return np.array([secrets.randbelow(q) for i in range(n)])

def sample(n,q,sigma,s):
    a = np.array([secrets.randbelow(q) for i in range(n)])
    u1 = secrets.SystemRandom().random()
    u2 = secrets.SystemRandom().random()
    z0= np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
    general_form = (sigma * z0)
    e = general_form /q
    inner_product = np.dot(a, s)
    return (a, ((inner_product /q) +e) % 1)

def public_key(n,q,sigma,s,m):
    return [sample(n,q,sigma,s)for i in range(int(m))]

def encrypt(bit, pk):
    r =  np.array([secrets.randbits(1) for i in range(len(pk))])
    return(sum(r[i] * samp[0] for i,samp in enumerate(pk)), bit/2 + sum(r[i] * samp[1] for i,samp in enumerate(pk)))

def decrypt(ct,sk,q):
    a,b = ct
    x = (b - (np.dot(a,sk)/q)) %1
    if min(abs(x-0), 1-abs(x-0)) < min(abs(x-0.5), 1-abs(x-0.5)):
        return 0
    else:
        return 1


#calling of each function
secret = private_key(length, modulus)
public = public_key(length, modulus, sigma,secret,m)
#outputting of our public and private key pair
# print("private key",private)
# print("public key", public)

bit = secrets.randbits(1)
ct = encrypt(bit,public)
pt = decrypt(ct,secret,modulus)

print(bit, pt)