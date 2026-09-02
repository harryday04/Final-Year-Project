
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
    u1 = secrets.SystemRandom().random()
    u2 = secrets.SystemRandom().random()
    z0= np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
    general_form = (sigma * z0)
    return (general_form % 1)

#generation of t
def t(a,s,n,q,e):
    inner_product = np.dot(a, s)
    return ((inner_product /q) +e) % 1

#public key
def public_key(a,t):
    return [a,t]


#calling of each function
s =  private_key(length, modulus)
a = a_vector(length, modulus)
e = torus(sigma)
noise = t(a,s,length,modulus,e)
A = public_key(a, noise)

#outputting of our public and private key pair
print("private key",s)
print("public key", A)




