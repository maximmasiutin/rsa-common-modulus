#!/usr/bin/python

import sys
import math
import time
import secrets

from gmpy2 import is_prime, invert
from gmpy2 import gcd as gmpy2_gcd

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv_egcd(a, b):
    g, x, y = egcd(a, b)
    if g != 1:
        print("Modular inverse does not exist!", file=sys.stderr)
        sys.exit(1)
    else:
        return x % b

def modinv_pow(a, b):
    return pow(a, -1, b)

def modinv_gmpy(a, b):
    return invert(a, b)



def call_lcm(a, b):
    if "lcm" in dir(math):
        return math.lcm(a, b)
    else:
        return abs(a * b) // math.gcd(a, b)


def invalid_e(arg_e, arg_lam, arg_n):
    return arg_e <= 1 or arg_e >= arg_lam or arg_e >= arg_n or math.gcd(arg_e, arg_n) != 1

def main():

    p = 0x00E5B5B1EDC8DF0F307C2220151CFCBE31F69B15659A5D6FBA1E50F55A08B341218312D707CFC16ED86A1765F5AEAFA7E6A11C4431038914C76F0F398FE6BE031E289B220D13D9E02226C691D15BC6E1186EA18222D93F52A393BE1DA1A42853512419B5E6E304FD02E962A4C2D0ECDDB8F44AC094FACA8333AE94110A5B10DA539C24A96F08530E7699E3F705165CF14B7F90A2F32ED28D21615F91D7C808AC566D6EEEF6773450AB53542CDAC337C3124530CB16319752267C3422149D41543D8742586BAB578F4E06360745AE0BD8F0E800D1920DC1F3661287367A78967458383A82465C5D966E7299EFCF58BD860185F96655E1F8D300F6B096DFE883CF15
    q = 0x00D9757338E9A6B363F227F3104EDEF6240C0CAF53B7D509F48870553C4A821F460469AE5616301B9CC30FBF4598A176B84284AF3A41D697A34CDC2C8D88A4C4BE82AE8DB5347511FE5B4DD915CA6A728CCFD0444CE38FC7190824059D86A9083C273581EA5AD1D5E3A8D8EC6858F291A5EADA98B0F5FD7C8E8CA6226657B8B7955796B22899B087714E293A86C78D42A7021754A6220F1D0A9588C280DD9AEC376E421D539F30A3053D95C7D70F24B471D14ECF282FA3E0B1CED2C405BA22404F3B75CD961A46097D7C098324FC47281D298734DA0DFCD8AF82E685657C926672727296147867EAEDFDEF89A79DE81FF104CF7D9157EF65A1BC333C98A7FED685
    if not is_prime(p):
        print("p is not a prime!")
        sys.exit(1)
    if not is_prime(q):
        print("q is not a prime!")
        sys.exit(1)
    n = p * q
    pm1 = p - 1
    qm1 = q - 1
    lam = call_lcm(pm1, qm1)
    e = 65537
    if invalid_e(e, lam, n):
        print("Invalid e!")
        sys.exit(1)

    e_len_bits = int.bit_length(e)
    e_len_bytes = (e_len_bits+7)//8
    message_bytes = secrets.token_bytes(e_len_bytes-1)
    m = int.from_bytes(message_bytes, byteorder="big", signed=False)

    c = pow(m, e, n)

    counter = 100000

    start_egcd = time.time()
    for i in range(counter):
       d = modinv_egcd(e, lam)
    end_egcd = time.time()
    elapsed_egcd = end_egcd - start_egcd

    m2 = pow(c, d, n)
    if m2 != m:
      print("Message mismatch error on egcd")
      sys.exit(1)

    start_pow = time.time()
    for i in range(counter):
       d = modinv_pow(e, lam)
    end_pow = time.time()
    elapsed_pow = end_pow - start_pow

    m2 = pow(c, d, n)
    if m2 != m:
      print("Message mismatch error on pow")
      sys.exit(1)

    start_gmpy = time.time()
    for i in range(counter):
       d = modinv_gmpy(e, lam)
    end_gmpy = time.time()
    elapsed_gmpy = end_gmpy - start_gmpy

    m2 = pow(c, d, n)
    if m2 != m:
      print("Message mismatch error on gmpy")
      sys.exit(1)


    start_g_gcd = time.time()
    for i in range(counter):
       d = gmpy2_gcd(pm1, qm1)
    end_g_gcd = time.time()
    elapsed_g_gcd = end_g_gcd - start_g_gcd

    start_m_gcd = time.time()
    for i in range(counter):
       d = math.gcd(pm1, qm1)
    end_m_gcd = time.time()
    elapsed_m_gcd = end_m_gcd - start_m_gcd



    print("modinv egcd:",elapsed_egcd)
    print(" modinv pow:",elapsed_pow)
    print("modinv gmpy:",elapsed_gmpy)

    print("gcd gmpy:",elapsed_g_gcd)
    print("gcd math:",elapsed_m_gcd)

main()
