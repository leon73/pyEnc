# -*- coding: ascii -*-
#!/usr/bin/env python

from string import printable as chars
import pyenc


def main():
    get_help()
    while True:
        com = get_command()
        if com[0] == "":
            continue
        elif com[0] == "-c":
            print("Bye!")
            return
        elif com[0] == "-h":
            get_help()
        elif com[0] in ("-e", "-d"):            
            if len(com) < 4:
                print("Invalid syntax!")
                continue
            if check_file(com[1], com[2]):
                text = read_file(com[1])
                if not text:
                    print("Invalid character in the file.")
                    continue
            else:                
                continue            
            text2 = exe_command(com[0], text, com[2], com[3])
            if not text2:
                continue            
        else:
            print("Invalid command!")


def exe_command(com, text, arq, arg):
    if com == "-e":
        lvl = check_lvl(arg)
        if not lvl:
            return False
        try:
            text2 = crypt(text, arq, lvl)
        except:
            print("Error!")
            return False
    else:
        try:
            text2 = decrypt(text, arq, arg)
        except:
            print("Error!")
            return False
    return text2


def check_lvl(lvl):
    try:
        lvl = int(lvl)
    except ValueError:
        print("Encryption level must be an integer greater than zero.")
        return False
    if lvl < 1:
        print("Encryption level must be an integer greater than zero.")
        return False
    return lvl


def get_command():
    com = input("pyEnc> ").lower()
    com = com.split(" ")
    return com


def check_file(file, file2):
    try:
        arq = open(file, "r")
        arq.close()
    except FileNotFoundError:
        print("File not found.")
        return False
    try:
        arq = open(file2, "r")
        arq.close()
        print("New file already exists.")
        return False
    except FileNotFoundError:
        return True


def read_file(file):
    with open(file, "r") as arq:
        text = arq.read()            
        for c in text:
            if c not in chars:                
                return False
        return text


def crypt(text, file_b, lvl):
    print("Processing...")
    with open(file_b, "w") as arq:
        crypt_text, key = pyenc.crypt(text, lvl)
        arq.write(crypt_text)
    print("Success!")
    print("\n=== Key: {} ===\n".format(key))


def decrypt(crypt_text, file_b, key):
    print("Processing...")
    with open(file_b, "w") as arq:
        text = pyenc.decrypt(crypt_text, key)
        arq.write(text)
    print("Success!")


def get_help():
    print('''
GNU GPL Copyright (c) pyEnc Leonardo F Oliveira
Available on github: <https://github.com/leon73/pyEnc.git>

========================= COMMANDS =========================

-e file_name new_file encryption_level => Encrypt
-d file_name new_file encryption_key => Decrypt
-h => Help
-c => Close

============================================================
''')


if __name__ == "__main__":
    main()
