import numpy as np
import keygen
import encrypt
import decrypt

def main():
    pk = np.load("publickey.npy", allow_pickle= True)
    sk = np.load("privatekey.npy", allow_pickle=True)

    bit_string = str(input("please enter a bit string: "))

    cipher_text = encrypt.main(bit_string, pk)

    plain_text = decrypt.main(cipher_text,sk)

    print([plain_text])

main()