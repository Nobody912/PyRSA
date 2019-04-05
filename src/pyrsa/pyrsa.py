#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import pyfiglet
from halo import Halo
from termcolor import cprint

if sys.version_info < (3, 4):
    sys.exit('Sorry, Python < 3.4 is not supported')

#####################################
# PUBLIC AND PRIVATE KEY GENERATION #
#####################################

def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    file_out = open("private.pem", "wb")
    file_out.write(private_key)

    public_key = key.publickey().export_key()
    file_out = open("public.pem", "wb")
    file_out.write(public_key)

    print("[i] Keys Generated!")
    input("Press [Enter] to continue.")
    main()

##############
# ENCRYPTION #
##############

def encrypt_data():
    print("[i] Zip files are preferred for compatibility purposes.")
    data_type = input("Message or File (m/f) > ")

    if data_type == "f":
        filename = input("Source Filename > ")
        try:
            data = open(filename, "rb").read()

        except FileNotFoundError:
            print("[!] CRITICAL: File", filename, "not found!")
            input("Press [Enter] to continue.")
            main()

    elif data_type == "m":
        filename = input("New Filename > ")
        data = input("Message > ").encode("utf-8")

    else:
        print("\n[!] CRITICAL: Invalid option!")
        input("Press [Enter] to continue.")
        main()

    spinner = Halo(text='Encrypting...', spinner='dots')
    spinner.start()


    file_out = open(filename + ".bin", "wb")

    recipient_key = RSA.import_key(open("public.pem").read())
    session_key = get_random_bytes(16)

    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    _ = [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]

    spinner.stop()
    print("[i] Encryption Sucessful!")
    input("Press [Enter] to continue.")
    main()

##############
# DECRYPTION #
##############

def decrypt_data():
    filename = input("Enter file > ")

    file_in = open(filename, "rb")
    file_out = open(filename.replace(".bin", ""), "wb")

    spinner = Halo(text='Encrypting...', spinner='dots')
    spinner.start()

    private_key = RSA.import_key(open("private.pem").read())

    enc_session_key, nonce, tag, ciphertext = \
    _ = [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]

    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    file_out.write(data)

    spinner.stop()
    print("[i] Decryption Sucessful!")
    input("Press [Enter] to continue.")
    main()

#################
# CLI INTERFACE #
#################

def main():
    os.system("clear")

    cprint(pyfiglet.figlet_format("P Y R S A", font="alligator"), "blue", attrs=["bold"])
    print('''
Available Modes:
[1] RSA Key Generation
[2] Encryption
[3] Decryption
[i] Information
[e] Exit
    ''')
    mode = input("MODE SELECTION > ")

    if mode == "1":
        generate_keys()
        main()

    elif mode == "2":
        encrypt_data()
        main()
    elif mode == "3":
        decrypt_data()
        main()

    elif mode == "i":
        print('''
I N F O:
PyRSA
[ver. 1.0] > Pre-Release Edition
Python Standalone Edition
Erik Ji | Nobody912
https://github.com/Nobody912/PyRSA
        ''')

        input("Press [Enter] to continue.")
        os.system("clear")
        main()

    elif mode == "e":
        print("\n[i] Seeya later partner!")
        input("Press [Enter] to continue.")
        os.system("clear")
        sys.exit()

    else:
        print("\n[!] CRITICAL: Invalid command!")
        input("Press [Enter] to continue.")
        main()

if __name__ == "__main__":
    main()
