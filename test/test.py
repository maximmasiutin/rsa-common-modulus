#!/usr/bin/python

# This program prepares test keys to demonstrate the use of rsa-common-modulus.py
# It outputs a sample command line for the rsa-common-modulus.py
# You can just execute the produced output

import sys
import math

from gmpy2 import is_prime


def modinv(a, b):
    return pow(a, -1, b)


def call_lcm(a, b):
    if "lcm" in dir(math):
        return math.lcm(a, b)
    else:
        return abs(a * b) // math.gcd(a, b)


def test_e(arg_e, arg_lam, arg_n):
    if arg_e <= 1 or arg_e >= arg_lam or arg_e >= arg_n or math.gcd(arg_e, arg_n) != 1:
        print("Invalid e!")
        sys.exit(1)


def int_to_bytes(arg_message):
    return int.to_bytes(
        arg_message, (arg_message.bit_length() + 7) // 8, byteorder="big"
    )


def main():

    text = 'Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, "and what is the use of a book," thought Alice "without pictures or conversation?" So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up'
    binary = text.encode("ascii")
    plaintext = int.from_bytes(binary, byteorder="big", signed=False)
    plaintext_len_bits = int.bit_length(plaintext)

    p = 0x00E5B5B1EDC8DF0F307C2220151CFCBE31F69B15659A5D6FBA1E50F55A08B341218312D707CFC16ED86A1765F5AEAFA7E6A11C4431038914C76F0F398FE6BE031E289B220D13D9E02226C691D15BC6E1186EA18222D93F52A393BE1DA1A42853512419B5E6E304FD02E962A4C2D0ECDDB8F44AC094FACA8333AE94110A5B10DA539C24A96F08530E7699E3F705165CF14B7F90A2F32ED28D21615F91D7C808AC566D6EEEF6773450AB53542CDAC337C3124530CB16319752267C3422149D41543D8742586BAB578F4E06360745AE0BD8F0E800D1920DC1F3661287367A78967458383A82465C5D966E7299EFCF58BD860185F96655E1F8D300F6B096DFE883CF15
    q = 0x00D9757338E9A6B363F227F3104EDEF6240C0CAF53B7D509F48870553C4A821F460469AE5616301B9CC30FBF4598A176B84284AF3A41D697A34CDC2C8D88A4C4BE82AE8DB5347511FE5B4DD915CA6A728CCFD0444CE38FC7190824059D86A9083C273581EA5AD1D5E3A8D8EC6858F291A5EADA98B0F5FD7C8E8CA6226657B8B7955796B22899B087714E293A86C78D42A7021754A6220F1D0A9588C280DD9AEC376E421D539F30A3053D95C7D70F24B471D14ECF282FA3E0B1CED2C405BA22404F3B75CD961A46097D7C098324FC47281D298734DA0DFCD8AF82E685657C926672727296147867EAEDFDEF89A79DE81FF104CF7D9157EF65A1BC333C98A7FED685

    if not is_prime(p):
        print("p is not a prime!")
        sys.exit(1)

    if not is_prime(q):
        print("q is not a prime!")
        sys.exit(1)

    # prepare keys
    n = p * q
    modulus_len_bits = int.bit_length(n)

    pm1 = p - 1
    qm1 = q - 1
    lam = call_lcm(pm1, qm1)
    e1 = 3
    e2 = 65537
    test_e(e1, lam, n)
    test_e(e2, lam, n)
    d1 = modinv(e1, lam)
    d2 = modinv(e2, lam)

    # produce ciphertexts
    if plaintext_len_bits > modulus_len_bits:
        print(
            "Plaintext is too long for this modulus! Plaintext:",
            plaintext_len_bits,
            "bits, modulus:",
            modulus_len_bits,
            "bits!",
        )
        sys.exit(1)

    c1 = pow(plaintext, e1, n)
    c2 = pow(plaintext, e2, n)

    # verify ciphertexts
    m1 = pow(c1, d1, n)
    m2 = pow(c2, d2, n)

    if m1 != plaintext or m2 != plaintext:
        print(int_to_bytes(plaintext))
        print(int_to_bytes(m1))
        print(int_to_bytes(m2))
        sys.exit(1)

    output = "./rsa-common-modulus.py --modulus {n} --e1 {e1} --ct1 {ct1} --e2 {e2} --ct2 {ct2} --outputformat ascii --quiet".format(
        n=n, e1=e1, ct1=c1, e2=e2, ct2=c2
    )
    print(output)


main()
