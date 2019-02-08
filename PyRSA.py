#
# P y R S A
# ver. 0.1
# 
#

import sys
import os
import time

import pyfiglet

from termcolor import colored, cprint

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

#####################################
# PUBLIC AND PRIVATE KEY GENERATION #
#####################################

def generateKeys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    file_out = open("private.pem", "wb")
    file_out.write(private_key)

    public_key = key.publickey().export_key()
    file_out = open("public.pem", "wb")
    file_out.write(public_key)

    print("Keys Generated! Exiting...")

##############
# ENCRYPTION #
##############

def encryptMessage():
    data = input("Message > ").encode("utf-8")
    file_out = open("encrypted_data.bin", "wb")

    recipient_key = RSA.import_key(open("public.pem").read())
    session_key = get_random_bytes(16)

    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    [ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]

    print("Encryption Sucessful! Exiting...")
    time.sleep(1)

##############
# DECRYPTION #
##############

def decryptMessage():
    file_in = open("encrypted_data.bin", "rb")
    file_out = open("decrypted_data.txt", "wb")

    private_key = RSA.import_key(open("private.pem").read())

    enc_session_key, nonce, tag, ciphertext = \
    [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    file_out.write(data)

    print("Decryption Sucessful! Exiting...")
    time.sleep(1)

#################
# CLI INTERFACE #
#################

def menu():
    os.system("clear")

    cprint(pyfiglet.figlet_format("P Y R S A", font = "alligator"), "blue", attrs=["bold"])

    print("Available Modes:\n"
    "[0] RSA Key Generation\n"
    "[1] Encryption\n"
    "[2] Decryption\n"
    "[99] Exit\n"
    )
    mode = input("MODE SELECTION > ")

    if mode == "0":
        generateKeys()

    elif mode == "1":
        encryptMessage()

    elif mode == "2":
        decryptMessage()

    elif mode == "99":
        print("\n[i] Seeya later partner!")
        time.sleep(1)
        os.system("clear")
        sys.exit()

    else:
        print("\n[!] CRITICAL: Invalid command!")
        
        time.sleep(2)

        input("Press [Enter] to continue")
        menu()

menu()