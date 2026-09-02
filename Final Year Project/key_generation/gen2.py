from random import randint
from random import gauss
import secrets
import numpy as np

np.set_printoptions(legacy='1.25')

#defines the length if our private key vector
length = 1024

#modulus
modulus = 32768

#variables for our guassian
alpha = 3/modulus
sigma = ((alpha) / np.sqrt(2 * np.pi))

#generation of our private key
def private_key(n, q):
    return[secrets.randbelow(q) for i in range(0,n)]

#generation of our vector a
def a_vector(n,q):
    return[secrets.randbelow(q) for i in range(0,n)]

#generation of our noise
def torus(sigma):
    raw = gauss(0.0,sigma)
    print(raw)
    print(raw %1)
    return (raw % 1)

def t(a,s,n,q,e):   
    inner_product = sum(a[i]*s[i] for i in range(n))
    return ((inner_product /q) +e) % 1

def public_key(a,t):
    return [a,t]

s =  private_key(length, modulus)
a = a_vector(length, modulus)
e = torus(sigma)
noise = t(a,s,length,modulus,e)
A = public_key(a, noise)

# print("private key",s)
# print("public key", A)




