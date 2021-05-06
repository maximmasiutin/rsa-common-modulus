#!/usr/bin/python

# The RSA Common Modulus Attack can be described as follows.
# If a single plaintext has been encrypted to two ciphertexts
# by private keys that have have same modulus but different exponent,
# this plaintext can be recovered if gcd(e1, e2) = 1 and gcd(ct2, n)=1

# This is a script originally written by Andreas Pogiatzis in 2018
# https://infosecwriteups.com/rsa-attacks-common-modulus-7bdb34f331a5
# Maxim Masiutin ported this script in 2021 to Python 3 and added the option to configure output format,
# and the code to check that the plaintexts from both decrypted messages to be the same.

# Copyright 2018 Andreas Pogiatzis
# Copyright 2021 Maxim Masiutin

import argparse
import sys

from math import gcd

parser = argparse.ArgumentParser(description="RSA Common modulus attack")
required_named = parser.add_argument_group("required named arguments")
required_named.add_argument("-n", "--modulus", help="Common modulus", type=int, required=True)
required_named.add_argument("-e1", "--e1", help="First exponent", type=int, required=True)
required_named.add_argument("-e2", "--e2", help="Second exponent", type=int, required=True)
required_named.add_argument("-ct1", "--ct1", help="First ciphertext", type=int, required=True)
required_named.add_argument("-ct2", "--ct2", help="Second ciphertext", type=int, required=True)
parser.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("-of", "--outputformat", type=str, choices=["decimal", "hex", "base64", "quoted", "ascii", "utf-8", "raw"], default="quoted")


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        print("Modular inverse does not exist!", file=sys.stderr)
        sys.exit(1)
    else:
        return x % m


def attack(c1, c2, e1, e2, N):
    g = gcd(e1, e2)
    if g != 1:
        print("Exponents e1 and e2 must be coprime!", file=sys.stderr)
        sys.exit(1)

    s1 = modinv(e1, e2)
    s2 = (g - e1 * s1) // e2

    temp = modinv(c2, N)
    m1 = pow(c1, s1, N)
    m2 = pow(temp, -s2, N)
    r1 = (m1 * m2) % N

    return r1


def main():
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    quiet = args.quiet
    if quiet is None:
        quiet = False
    if not quiet:
        print("Starting the attack...")
    if gcd(args.ct2, args.modulus) != 1:
        print("c2 and n must be coprime!", file=sys.stderr)
        sys.exit(1)

    message1 = attack(args.ct1, args.ct2, args.e1, args.e2, args.modulus)
    message2 = attack(args.ct2, args.ct1, args.e2, args.e1, args.modulus)
    a1 = int.to_bytes(message1, (message1.bit_length() + 7) // 8, byteorder="big")
    a2 = int.to_bytes(message2, (message2.bit_length() + 7) // 8, byteorder="big")

    of = args.outputformat
    if of == "decimal":
        b1 = message1
        b2 = message2
    elif of == "hex":
        import binascii

        b1 = binascii.hexlify(a1).decode("ascii")
        b2 = binascii.hexlify(a2).decode("ascii")
    elif of == "base64":
        import base64

        b1 = base64.b64encode(a1).decode("ascii")
        b2 = base64.b64encode(a2).decode("ascii")
    elif of == "quoted":
        b1 = a1
        b2 = a2
    elif of == "ascii":
        b1 = a1.decode("ascii")
        b2 = a2.decode("ascii")
    elif of == "utf-8":
        b1 = a1.decode("utf-8")
        b2 = a2.decode("utf-8")
    elif of == "raw":
        pass
    else:
        print("Unknown output format!", file=sys.stderr)
        sys.exit(1)

    if message1 != message2:
        if of == "raw":
            pass
        else:
            print("Plaintext message1: ", b1, file=sys.stderr)
            print("Plaintext message2: ", b2, file=sys.stderr)
            print("Decrypted messages must be the same!", file=sys.stderr)
            sys.exit(1)

    if not quiet:
        print("Attack complete.")
        print("Plaintext message:")

    if of == "raw":
        sys.stdout.buffer.write(a1)
    else:
        print(b1)


main()
