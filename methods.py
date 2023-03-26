#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project name: Implementace hybrydního šifrování
autor: Bc. Jakub Komárek
File description: Implementace kryptografických metod
"""

from Crypto.Cipher import PKCS1_OAEP,AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Hash import MD5
from Crypto.Util.number import bytes_to_long,long_to_bytes

# získání RSA klíče ze souboru
def getRsaKeyFromFile(keyPath):
    return RSA.import_key(open(keyPath).read())

# šifrování pomocí veřejného klíče
def rsaEnc(message, key):
    cipher = PKCS1_OAEP.new(key)
    
    ciphertext = cipher.encrypt(message)
    return ciphertext

# dešifrování pomocí soukromého klíče
def rsaDec(ciphertext, key):
    cipher = PKCS1_OAEP.new(key)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

# vytvoření zarovnání na požadovanou velikost - defalutně na 214 (maximální délka šifrovaného textu rsa při použítí 2048 dlouhého klíče)
def rsaPading(text,target=214):
    toBePad=target-len(text)
    pading=get_random_bytes(toBePad)
    res=text+pading
    return res

# odstranění padingu - smazání nežádoucích bytů
def rsaUnPading(text,textLen):
    return text[:textLen]

# podpis pomocí soukromého klíče
def rsaSign(text,privateKey):
    if len(text)>256:
        raise Exception("blbě")
    D=  bytes_to_long(text)
    S=pow(D,privateKey.d, privateKey.n)

    return long_to_bytes(S)

# ověření podpisu - rozšifrování
def rsaSignVer(text,publicKey):
    S=  bytes_to_long(text)
    res=pow(S,publicKey.e ,publicKey.n)
    return long_to_bytes(res)

# vytvoř klíč pro symetrickou kryptografii - defalutně 128 bitový
def aesGenKey(bytesNum=16):
    return get_random_bytes(bytesNum)

# šifrování pomocí aes 
def aesEnc(message, key):
    cipher = AES.new(key, AES.MODE_CFB)
    cipher_text = cipher.encrypt(message)
    iv = cipher.iv # inicializační vektor
    return iv+cipher_text 

# dešifrování pomocí aes   
def aesDec(message, key):
    if(len(message)<16):
        raise Exception("aes decription error: len of message is to low")
    
    iv=message[0:AES.block_size] # inicializační vektor
    cipher_text=message[AES.block_size:]

    decrypt_cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    return decrypt_cipher.decrypt(cipher_text)

# tvorba md5 hashe
def md5CreateHash(messege):
    return MD5.new(messege)


    