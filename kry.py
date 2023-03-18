#!/usr/bin/env python3

import sys

from server import startServer
from client import startClient

if __name__ == "__main__":
    mode="none"
    port=-1
    args=sys.argv
    
    for index in range(1,len(args)):
        i=args[index]
        if i== "-h" or i=="--help":
            print("help")
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
            else:
                raise Exception("Chyba v parametrech, zkuste -h")
            
    if port<0 or port>65535:
        raise Exception("Port služby je špatně zadán")
    if mode=="c":
        startClient(port)
    elif mode=="s":
        startServer(port)
    else:
        raise Exception("Mód zpuštění je špatně zadán")