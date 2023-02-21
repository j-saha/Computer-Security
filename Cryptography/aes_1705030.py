# -*- coding: utf-8 -*-
from BitVector import *
import time
from time import perf_counter

list_round_key = []

Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]

InvMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
]



def input_key(size, symbol, filename):
    file_key = open(filename, "r")
    key_aes = file_key.read()

    if(size<=len(key_aes)):
        return key_aes[0:size]

    pad_size = size - len(key_aes)%size
    if(pad_size == size):
        return key_aes
    for i in range(pad_size):
        key_aes = key_aes + symbol
    return key_aes

def input_and_pad_file(size, symbol, filename):
    text = open(filename, "rb").read()
    file_bit = BitVector(hexstring=text.hex())
    pad_size = 128 - len(file_bit) % 128
    pad_vec = BitVector(size=pad_size)
    file_bit = file_bit + pad_vec
    return file_bit



def encrypt_file(file_bit):
    block_size = int(len(file_bit) / 128)
    start = 0
    ciphertext = BitVector(size=0)
    for i in range(block_size):
        ciphertext = ciphertext + encryption(file_bit[start:start + 128])
        start = start + 128
    return ciphertext.getHexStringFromBitVector()

def decrypt_file(file_cipher):
    cipher_file = BitVector(hexstring=file_cipher)
    block_size = int(len(cipher_file) / 128)
    start = 0
    file_bit_vect = BitVector(size=0)
    for i in range(block_size):
        file_bit_vect = file_bit_vect + decryption(cipher_file[start:start + 128])
        start = start + 128

    return bytes.fromhex(file_bit_vect[0:len(file_bit_vect)].get_bitvector_in_hex())



def input_and_pad_text(size, symbol, filename):
    text = open(filename, "r").read()
    pad_size = size - len(text)%size
    if(pad_size == size):
        return text
    for i in range(pad_size):
        text = text + symbol
    return text

def key_expansion(no_of_rounds, key):
    list_round_key.clear()
    key_aes = BitVector(hexstring=key.encode('utf-8').hex())
    list_round_key.append(key_aes)
    round_constant = 0;
    for i in range(no_of_rounds):
        round_constant = get_round_constant(i+1, round_constant)
        w0 = list_round_key[i][0:32]
        w1 = list_round_key[i][32:64]
        w2 = list_round_key[i][64:96]
        w3 = list_round_key[i][96:128]
        w3_copy = w3.deep_copy()
        gw3 = w3_copy << 8

        start = 0
        gw3_sub = BitVector(size = 0)
        for j in range(int(len(gw3)/8)):
            sub_byte = Sbox[gw3[start:start+8].intValue()]
            start = start + 8
            gw3_sub = gw3_sub + BitVector(intVal = sub_byte, size = 8)
            # print(gw3_sub)

            # gw3_final = gw3_sub ^ BitVector(hexstring="01000000")
            # print(BitVector(hexstring="01000000").get_bitvector_in_hex())
        # print(gw3_sub.get_bitvector_in_hex())
        gw3_final = gw3_sub ^ (BitVector(intVal=round_constant, size = 8) + BitVector(hexstring="000000"))
        # print((BitVector(intVal=i+1, size = 8) + BitVector(hexstring="000000")).get_bitvector_in_hex())



        # print(gw3_final.get_bitvector_in_hex())
        w4 = w0 ^ gw3_final
        w5 = w4 ^ w1
        w6 = w5 ^ w2
        w7 = w6 ^ w3

        round_key = w4 + w5 + w6 + w7
        # print(round_key.get_bitvector_in_hex())
        list_round_key.append(round_key)


def get_round_constant(round, old_constant):
    if(round==1):
        return 1
    if(old_constant<128):
        return 2*old_constant
    else:
        return (2*old_constant) ^ 283

def add_round_key(plaintext, round):
    return plaintext ^ list_round_key[round]

def get_i_j_th_value(bitvector, i, j):
    start = 32*j + i*8
    return bitvector[start:start+8]


def shift_row(plaintext):
    shifted_plaintext = BitVector(size=0)
    for i in range(4):
        shifted_plaintext = shifted_plaintext + get_i_j_th_value(plaintext, 0, i)
        for j in range(3):
            shifted_plaintext = shifted_plaintext + get_i_j_th_value(plaintext, j+1, (i+j+1)%4)
    return shifted_plaintext

def inverse_shift_row(ciphertext):
    inversed_ciphertext = BitVector(size=0)
    for i in range(4):
        inversed_ciphertext = inversed_ciphertext + get_i_j_th_value(ciphertext, 0, i)
        for j in range(3):
            inversed_ciphertext = inversed_ciphertext + get_i_j_th_value(ciphertext, j+1, ((i-j-1)%4))
    return inversed_ciphertext



def mix_colm(plaintext):
    AES_modulus = BitVector(bitstring='100011011')
    mixed_plaintext = BitVector(size=0)
    for i in range(4):

        for j in range(4):
            s = BitVector(size=0)
            for k in range(4):
                s = s ^ (get_i_j_th_value(plaintext, k, i).gf_multiply_modular(Mixer[j][k], AES_modulus, 8))
            mixed_plaintext = mixed_plaintext + s
    return mixed_plaintext
def inv_mix_colm(ciphertext):
    AES_modulus = BitVector(bitstring='100011011')
    inv_mixed_text = BitVector(size=0)
    for i in range(4):
        for j in range(4):
            s = BitVector(size=0)
            for k in range(4):
                s = s ^ (get_i_j_th_value(ciphertext, k, i).gf_multiply_modular(InvMixer[j][k], AES_modulus, 8))
            inv_mixed_text = inv_mixed_text + s
    return inv_mixed_text

def sub_byte(text, type):
    sub_text = BitVector(size=0)
    start = 0
    for j in range(16):
        if(type=="inverse"):
            sub_byte = InvSbox[text[start:start + 8].intValue()]
        else:
            sub_byte = Sbox[text[start:start + 8].intValue()]
        start = start + 8
        sub_text = sub_text + BitVector(intVal=sub_byte, size=8)
    return sub_text

def encryption(plaintext):


    # print("Round 0: ")
    text = add_round_key(plaintext, 0)
    # print(text.get_bitvector_in_hex())
    for i in range(1, 10):
        # print("Round " + str(i) +" : ")
        text = sub_byte(text, "normal")
        # print(text.get_bitvector_in_hex())
        text = shift_row(text)
        # print(text.get_bitvector_in_hex())
        text = mix_colm(text)
        # print(text.get_bitvector_in_hex())
        text = add_round_key(text, i)
        # print(text.get_bitvector_in_hex())

    # print("Round 10 : ")
    text = sub_byte(text, "normal")
    text = shift_row(text)
    text = add_round_key(text, 10)
    # print(text.get_bitvector_in_hex())
    return text

def decryption(ciphertext):

    # print("Round 0: ")
    ciphertext = add_round_key(ciphertext, 10)
    # print(ciphertext.get_bitvector_in_hex())

    for i in range(1, 10):
        # print("Round " + str(i) +" : ")
        ciphertext = inverse_shift_row(ciphertext)
        ciphertext = sub_byte(ciphertext, "inverse")
        ciphertext = add_round_key(ciphertext, 10-i)
        # print(text.get_bitvector_in_hex())

        # print(text.get_bitvector_in_hex())
        ciphertext = inv_mix_colm(ciphertext)
        # print(text.get_bitvector_in_hex())

        # print(ciphertext.get_bitvector_in_hex())

    # print("Round 10 : ")

    ciphertext = inverse_shift_row(ciphertext)
    ciphertext = sub_byte(ciphertext, "inverse")
    ciphertext = add_round_key(ciphertext, 0)

    # print(bytes.fromhex(ciphertext.get_bitvector_in_hex()).decode('utf-8'))
    return ciphertext

def full_encryption(plain):
    plaintext = BitVector(hexstring=plain.encode('utf-8').hex())

    block_size = int(len(plaintext)/128)
    start = 0
    ciphertext = BitVector(size=0)
    for i in range(block_size):
        ciphertext = ciphertext + encryption(plaintext[start:start+128])
        start = start + 128
    return ciphertext.getHexStringFromBitVector()

def full_decryption(cipher):
    ciphertext = BitVector(hexstring=cipher)
    block_size = int(len(ciphertext)/128)
    start = 0
    text = BitVector(size=0)
    for i in range(block_size):
        text = text + decryption(ciphertext[start:start+128])
        start = start + 128
    return text.get_bitvector_in_ascii()

def display(plaintext, key, ctext, text, key_time, en_time, de_time):
    print("Plain Text:")
    print(plaintext + " [In ASCII]")
    print(plaintext.encode('utf-8').hex() + " [In HEX]")
    print()
    print("Key:")
    print(key + " [In ASCII]")
    print(key.encode('utf-8').hex() + " [In HEX]")
    print()
    print("Cipher Text:")
    print(ctext + " [In HEX]")
    print(BitVector(hexstring=ctext).get_bitvector_in_ascii() + " [In ASCII]")
    print()
    print("Deciphered Text:")
    print(text.encode('utf-8').hex() + " [In HEX]")
    print(text + " [In ASCII]")
    print()
    print("Execution Time")
    print("Key Scheduling: "+str(key_time)+" seconds")
    print("Encryption Time: "+str(en_time)+" seconds")
    print("Decryption Time: "+str(de_time)+" seconds")


if __name__ == '__main__':
    print("Please Select Mode:")
    print("1. Text")
    print("2. File")
    mode = input()

    key_filename = "key.txt"
    key = input_key(16, ' ', key_filename)
    start_scheduling = time.perf_counter()
    key_expansion(10, key)
    stop_scheduling = time.perf_counter()
    key_time = stop_scheduling - start_scheduling
    if(int(mode) == 1):
        text_filename = "plaintext.txt"

        plaintext = input_and_pad_text(16, ' ', text_filename)
        start_encryption = time.perf_counter()
        ciphertext = full_encryption(plaintext)
        stop_encryption = time.perf_counter()
        en_time = stop_encryption-start_encryption


        start_decryption = time.perf_counter()
        text = full_decryption(ciphertext)
        stop_decryption = time.perf_counter()
        de_time = stop_decryption-start_decryption


        display(plaintext, key, ciphertext, text, key_time, en_time, de_time)


    elif (int(mode)== 2):
        file_input_taken = input_and_pad_file(16, ' ', "logo.png")
        file_cipher = encrypt_file(file_input_taken)
        bytes = decrypt_file(file_cipher)

        with open("image.png", "wb") as file:
            file.write(eval(str(bytes)))
    else:
        print("Select valid mode.")
