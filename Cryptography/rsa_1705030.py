import random
import math
from BitVector import *
from time import perf_counter
import time


def encryption(text, e, n):
    ciphertext = []
    for i in range(len(text)):
        P = text[i:i+1]
        C = pow(ord(P), int(e), int(n))
        ciphertext.append(C)
    return ciphertext

def decryption(ciphertext, d, n):
    plaintext = ""
    for i in range(len(ciphertext)):
        C = ciphertext[i]
        P = pow(int(C), int(d), int(n))
        plaintext = plaintext + chr(P)
    return plaintext
def generate_parameters(K):
    random.seed(5)
    prime = BitVector(intVal=0)
    count = 0
    p = 0
    q = 0
    while(True):
        prime = prime.gen_rand_bits_for_prime(int(K/2))
        test = prime.test_for_primality()
        if(test >= .99):
            if(count == 0):
                p = prime.intValue()
                count = count + 1
            else:
                q = prime.intValue()
                break
    n = p*q
    phi = (p-1) * (q-1)

    e = random.randint(2, phi-1)
    while(math.gcd(phi, e)!=1):
        e = random.randint(2, phi - 1)

    mod = BitVector(intVal=phi)
    vect = BitVector(intVal=e)
    m_inverse = vect.multiplicative_inverse(mod)
    return n, e, m_inverse.intValue()
def display(plaintext, ctext, text, key_time, en_time, de_time, K):
    print("K:")
    print(K)
    print()
    print("Plain Text:")
    print(plaintext + " [In ASCII]")
    print()
    print("Cipher Text:")
    print(' '.join(map(str, ctext)))
    print()
    print("Deciphered Text:")
    print(text + " [In ASCII]")
    print()
    print("Execution Time")
    print("Key Scheduling: "+str(key_time)+" seconds")
    print("Encryption Time: "+str(en_time)+" seconds")
    print("Decryption Time: "+str(de_time)+" seconds")
    print()
    print()

if __name__ == '__main__':

    time_list = []
    for K in [16, 32, 64, 128]:
        # k_filename = "K.txt"
        text_filename = "plaintext.txt"
        # K = int(open(k_filename, "r").read())
        text = open(text_filename, "r").read()

        start_generation = time.perf_counter()
        n, e, d = generate_parameters(K)
        stop_generation = time.perf_counter()
        key_time = stop_generation-start_generation

        if(d is not None):
            start_encryption = time.perf_counter()
            ciphertext = encryption(text, e, n)
            stop_encryption = time.perf_counter()
            en_time = stop_encryption - start_encryption
            # print(ciphertext)

            start_decryption = time.perf_counter()
            plaintext = decryption(ciphertext, d, n)
            stop_decryption = time.perf_counter()
            de_time = stop_decryption - start_decryption
            time_list.append(str(K)+"      "+str(key_time)+"       "+str(en_time)+"        "+str(de_time))
            # print(plaintext)
            display(plaintext, ciphertext, text, key_time, en_time, de_time, K)
    print("K        Key-Generation                      Encryption                       Decryption")
    for i in range(len(time_list)):
        print(time_list[i])


