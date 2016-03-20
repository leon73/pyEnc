# -*- coding: ascii -*-
#!/usr/bin/env python
# Metodos PyEnc

from random import randint as rand
from sys import stdout as cmd
import string


digs = string.digits
chars = string.digits + string.ascii_lowercase


class PyEnc(object):

    def mdc(self, z, i):
        x = i
        while z % x != 0 or i % x != 0:
            x -= 1
        return x

    def check_numb(self, num):
        i = 2
        while i < num:
            if num % i == 0:
                return False
            i += 1
        return True

    def get_num(self, num, p = 0):
        while not self.check_numb(num) or num == p:
            num += 1
        return num

    def toStr(self, n, base):
        if n < base:
            return chars[n]
        else:
            return self.toStr(n // base, base) + chars[n % base]

    def get_keys(self, lvl):
        p = self.get_num(rand(10 ** lvl, 10 ** (lvl + 1)))
        q = self.get_num(rand(10 ** lvl, 10 ** (lvl + 1)), p)
        n = p * q
        z = (p - 1) * (q - 1)
        for i in range(2, z):
            if self.mdc(z, i) == 1:
                e = i
                break
        d = 0
        while e * d % z != 1 or d == e:
            d += 1
        return e, d, n

    def crypt(self, text, lvl):
        cmd.write("Step 1: 0%")
        e, d, n = self.get_keys(lvl)
        cmd.write("\rStep 1: 100%")
        crypt_text = self.crypt_layer1(text, e, n)
        crypt_digs = self.crypt_layer2(crypt_text, n)
        print("")
        d, n = self.toStr(d, 36), self.toStr(n, 36)
        key = str("{}-{}").format(d, n)
        return crypt_digs, key

    def decrypt(self, crypt_digs, key):
        cmd.write("Step 1: 0%")
        key = key.split("-")
        key[0], key[1] = int(key[0], 36), int(key[1], 36)
        d, n = int(key[0]), int(key[1])
        cmd.write("\rStep 1: 100%")
        crypt_text = self.dec_layer1(crypt_digs, n)
        text = self.dec_layer2(crypt_text, d, n)
        print("")
        return text

    def crypt_layer1(self, text, e, n):
        print("")
        crypt_text = list()
        porc = 0
        for char in text:
            m = ord(char)
            c = m ** e % n
            comp = len(str(n))
            crypt_text.append("{:0>{}}".format(str(c), len(str(n))))
            porc += 1
            cmd.write("\rStep 2: {:.0%}".format(porc / len(text)))
        crypt_text = "".join(crypt_text)
        return crypt_text

    def crypt_layer2(self, crypt_text, n):
        print("")
        crypt_digs = str()
        i = 0
        porc = 0
        for num in crypt_text:
            pos = int(num) + int(str(n)[i])
            if pos > 9:
                pos -= 10
            crypt_digs += digs[pos]
            i += 1
            if i == len(str(n)):
                i = 0
            porc += 1
            cmd.write("\rStep 3: {:.0%}".format(porc / len(crypt_text)))
        return crypt_digs

    def dec_layer1(self, crypt_digs, n):
        print("")
        crypt_text = []
        i, s = 0, str()
        porc = 0
        for num in crypt_digs:
            pos = int(num) - int(str(n)[i])
            if pos < 0:
                pos += 10
            s += digs[pos]
            i += 1
            if i == len(str(n)):
                crypt_text.append(s)
                s = str()
                i = 0
            porc += 1
            cmd.write("\rStep 2: {:.0%}".format(porc / len(crypt_digs)))
        crypt_text = " ".join(crypt_text)
        return crypt_text

    def dec_layer2(self, crypt_text, d, n):
        print("")
        crypt_text = crypt_text.split(" ")
        text = str()
        porc = 0
        for code in crypt_text:
            c = int(code)
            m = c ** d % n
            text += chr(m)
            porc += 1
            cmd.write("\rStep 3: {:.0%}".format(porc / len(crypt_text)))
        return text


_inst = PyEnc()
crypt = _inst.crypt
decrypt = _inst.decrypt
