
import secrets
import numpy as np

np.set_printoptions(legacy='1.25')

#defines the length if our private key vector
length = 2

#modulus
modulus = 32768

#samples
# m = (1+0.1)*(length+1)*np.log2(modulus)
m = 2

#variables for our guassian
sigma = 3.2

#generation of our private key
def private_key(n, q):
    return[secrets.randbelow(q) for i in range(n)]

def sample(n,q,sigma,s):
    a = [secrets.randbelow(q) for i in range(n)]
    u1 = secrets.SystemRandom().random()
    u2 = secrets.SystemRandom().random()
    z0= np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
    general_form = (sigma * z0)
    e = general_form %1
    inner_product = np.dot(a, s)
    return (a, ((inner_product /q) +e) % 1)

def public_key(n,q,sigma,s,m):
    return[sample(n,q,sigma,s)for i in range(int(m))]

def encrypt(bit):
    return([sum(i[0]) for i in public], bit/2 + sum(i[1] for i in public))

def decrypt(ct, s,q):
    a,b = ct
    x = (b - (np.dot(a,s)/q)) %1
    if abs(x - 0) < abs(x- 0.5):
        return 0
    else:
        return 1


#calling of each function
private = private_key(length, modulus)
public = public_key(length, modulus, sigma,private,m)
#outputting of our public and private key pair
# print("private key",private)
# print("public key", public)

bit = secrets.randbits(1)
cipher = encrypt(bit)
dec = decrypt(cipher,private,modulus)
print(bit, encrypt(bit), dec)





