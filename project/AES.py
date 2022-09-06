#here we import the libraries that we will use in this program
#Crypto import Random it return random byte string
from Crypto import Random
#Crypto.Cipher it package contains algorithms for encrypt data... and one of this algorithms is AES
from Crypto.Cipher import AES
# this package for interact with the operating system
import os
#to read, write and, access to different  files & path name manipulation
import os.path
#it returns a list that contains entries in the folder
from os import listdir
#isfile used to know if the file exists or no
from os.path import isfile, join
# handle time-related tasks
import time


class Encryptor:
#__init__ is one of the reserved methods in Python and self is keyword in python
#and can easily access all the instances defined within a class
    def __init__(self, key):
        self.key = key
#this method add characters to a string in the beginning, end or, both
    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)
#This method for encrypting the content of the file
    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)
#this to open the file and extract message then send it to encrypt method to encrypt the message
    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)
#here is the opposite to encrypt method it takes the encrypt message to return the original message
    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")
#it opens the encrypted file to extract the content of the file to send it to the decrypt method
    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

#here we change the format of the key to be invisible/unreadable
key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
enc = Encryptor(key)
clear = lambda: os.system('cls')
#if the user already has a password will be stored in data.txt.enc if the program finds the file the program will do this
if os.path.isfile('data.txt.enc'):
    while True:
        password = str(input("Enter password: "))
        enc.decrypt_file("data.txt.enc")
        p = ''
        with open("data.txt", "r") as f:
            p = f.readlines()
        if p[0] == password:
            enc.encrypt_file("data.txt")
            break
#if the user types his/her password print the message to choose one from these three operation
    while True:
        clear()
        choice = int(input(
            "1. Press '1' to encrypt Messsag.\n2. Press '2' to decrypt Messsag.\n3. Press '3' to exit.\n"))
        clear()
        if choice == 1:
            enc.encrypt_file(str(input("Enter The name of file to encrypt: ")))
        elif choice == 2:
            enc.decrypt_file(str(input("Enter The name of encrypted file to decrypt: ")))
        elif choice == 3:
            exit()
        else:
            print("Please select a valid option!")
#if this is first time for the user his/her have to insert password
else:
    while True:
        clear()
        password = str(input("Setting up stuff. Enter a password that will be used for decryption: "))
        repassword = str(input("Confirm password: "))
        if password == repassword:
            break
        else:
            print("Passwords Mismatched!")
    f = open("data.txt", "w+")
    f.write(password)
    f.close()
    enc.encrypt_file("data.txt")
    #here the user have to close and restart again to encrypt or decrypt file or folder
    print("Please restart the program to complete the setup")
    time.sleep(15)
