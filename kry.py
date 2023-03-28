#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project name: Implementace hybrydního šifrování
autor: Bc. Jakub Komárek
File description: Main funkce - parsuje argumenty a volá hlavní moduly programu
"""

from server import startServer
from client import startClient
from keyGen import genNewKeys
from os.path import exists,isdir
from os import makedirs
from pathlib import Path

import sys

if __name__ == "__main__":
    mode="none"
    port=-1
    args=sys.argv

    try:
        for index in range(1,len(args)):
            i=args[index]
            if i== "-h" or i=="--help":
                print("Použití: [TYPE=[c|s] PORT=\"port number\" ] | -g | GEN=\"keyName\"")
                exit(0)
            elif i== "GEN" or i=="--genKeys" or i=="-g":
                genNewKeys("cert/serverKey") 
                genNewKeys("cert/clientKey")
                exit(0)
            else:
                strList=i.split('=')
                if len(strList)<2:
                    raise Exception("Chyba v parametrech, zkuste -h")
                
                name = strList[0]
                value= strList[1]        
                if name.upper()=='TYPE':
                    mode=value.lower()
                elif name.upper()=="PORT":
                    port = int(value)
                elif name.upper()=="GEN":
                    genNewKeys(value)
                    exit(0)
                else:
                    raise Exception("Chyba v parametrech, zkuste -h")
                
        if port<0 or port>65535:
            raise Exception("Port služby je špatně zadán")
        
        if not isdir(Path("cert")):
            makedirs(Path("cert"))
                
        if mode=="c":
            if not(exists(Path("cert/clientKey")) and  exists(Path("cert/clientKeyPub"))):
                print("someKeyMissing - generating new keys")
                genNewKeys("cert/clientKey")
            startClient(port)
        elif mode=="s":
            if not (exists(Path("cert/serverKey"))and exists(Path("cert/serverKeyPub"))):
                print("someKeyMissing - generating new keys")
                genNewKeys("cert/serverKey")  
            startServer(port)
        else:
            raise Exception("Mód zpuštění je špatně zadán")
    except Exception as ex:
        print("Error:",ex)
        exit(-1)
    
