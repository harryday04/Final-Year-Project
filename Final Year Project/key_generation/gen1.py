from random import randint
from random import gauss
import numpy as np

np.set_printoptions(legacy='1.25')

#defines the max size of our generation, we want to keep it small for now,
size = 256
#defines the length if our private key vector
length = 2

#choice of our random modulus
modulus = randint(0,size)

#variables for our guassian
alpha = 0.1
sigma = np.sqrt(np.square(alpha) / (2 * np.pi))

#generation of our private key
def private_key(n, q):
    return[randint(0,(q-1)) for i in range(0,n)]

#generation of our vector a
def a_vector(n,q):
    return[randint(0,(q-1)) for i in range(0,n)]

#generation of our noise
def torus(sigma):
    raw = gauss(0.0,sigma)
    return (raw % 1)

def t(a,s,n,q,e):
    inner_product = 0
    for i in range(0,n-1):
        inner_product += a[i] * s[i]
    return (inner_product /q) +e

def public_key(a,t):
    return [a,t]

s =  private_key(length, modulus)
a = a_vector(length, modulus)
e = torus(sigma)
noise = t(a,s,length,modulus,e)
A = public_key(a, noise)

print(s, A)





