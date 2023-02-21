#BOB
from aes import *
from rsa import *
import socket
import os
def write_to_file(path, filename, content):
    with open(os.path.join(path, filename), 'w') as temp_file:
        temp_file.write(content)
        temp_file.close()
s = socket.socket()
port = 22367
s.connect(('127.0.0.1', port))

thank_you = s.recv(1024).decode()


mode = s.recv(1024).decode()

length = s.recv(1024).decode()
ciphertext_aes_text = s.recv(int(length)+100).decode()

print("AES encrypted ciphertext (CT) received.")
ciphertext_aes_key_str = s.recv(1024).decode()
print("Encrypted key (EK) received.")
ciphertext_aes_key = ciphertext_aes_key_str.split("#")
public_key_e = s.recv(1024).decode()
public_key_n = s.recv(1024).decode()
print("Public key(PUK) received.")


dir = "Don’t Open this\\"
private_key_d, private_key_n = open(dir+"private_key.txt", "r").read().split(" ")


#decrypt the AES key using RSA


aes_key = decryption(ciphertext_aes_key, private_key_d, private_key_n)


#decrypt the message using AES


key_expansion(10, aes_key)


if (int(mode) == 1):
    final_text = full_decryption(ciphertext_aes_text)
    print()
    print("Decrypt Successful!")
    write_to_file(dir, "decrypted_plaintext.txt", final_text)
    s.send("Write Successful!".encode())
    print("Write Successful!")
elif (int(mode) == 2):
    bytes = decrypt_file(ciphertext_aes_text)
    filename = "decrypted_" + s.recv(1024).decode()
    with open(filename, "wb") as file:
        file.write(eval(str(bytes)))

s.close()


