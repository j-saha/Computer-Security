#ALICE
from aes import *
from rsa import *
import socket
import os

def match_text(dire, d_file, original_text):
    f = open(dire + d_file, "r").read()
    if(f==original_text):
        return True
    return False



s = socket.socket()
print("Socket successfully created")

port = 22367
s.bind(('', port))
print("socket binded to %s" % (port))

s.listen(5)
print("socket is listening")


def send(ciphertext_aes, aes_key, path):
    c.send(str(len(ciphertext_aes)).encode())
    c.send(ciphertext_aes.encode())
    print("AES encrypted ciphertext (CT) sent.")

    # RSA
    k_filename = "K.txt"
    K = int(open(k_filename, "r").read())
    n, e, d = generate_parameters(K)

    if (d is not None):

        ciphertext_rsa = encryption(aes_key, e, n)
        c.send('#'.join(map(str, ciphertext_rsa)).encode())
        print("Encrypted key (EK) sent.")

        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, "private_key.txt"), 'w') as temp_file:
            temp_file.write(str(d) + " " + str(n))
            temp_file.close()

    c.send(str(e).encode())
    c.send(str(n).encode())
    print("Public key(PUK) sent.")
    print()


while True:
    c, addr = s.accept()
    print('Incoming connection from', addr)
    c.send('You are connected!'.encode())
    path = os.path.dirname(os.path.realpath(__file__)) + "\Don’t Open this"

    print("Please Select Mode:")
    print("1. Text")
    print("2. File")
    mode = input()
    c.send(mode.encode())

    if (int(mode) == 1):
        # AES
        text_filename = "plaintext.txt"
        key_filename = "key.txt"
        plaintext = input_and_pad_text(16, ' ', text_filename)
        aes_key = input_key(16, ' ', key_filename)

        key_expansion(10, aes_key)
        ciphertext_aes = full_encryption(plaintext)
        send(ciphertext_aes, aes_key, path)

        if (c.recv(1024).decode() == "Write Successful!" and match_text(path, "\decrypted_plaintext.txt", plaintext)):
            print("Plain text matched!")
        else:
            print("Plain text not matched!")

    elif (int(mode) == 2):
        key_filename = "key.txt"
        filename = "logo.png"
        aes_key = input_key(16, ' ', key_filename)
        key_expansion(10, aes_key)
        plaintext = input_and_pad_file(16, ' ', filename)
        ciphertext_aes = encrypt_file(plaintext)
        send(ciphertext_aes, aes_key, path)
        c.send(filename.encode())

    c.close()
    break