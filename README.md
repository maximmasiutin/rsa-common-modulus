# rsa-common-modulus
A Python 3 script to describe the RSA Common Modulus Attack. Supports various output formats.

The RSA Common Modulus Attack can be explained the following way.
If a single plaintext has been encrypted to two ciphertexts 
by private keys that have have same modulus but different exponent,
this plaintext can be recovered if `gcd(e1, e2) = 1` and `gcd(ct2, n)=1`.

This is a script originally written by Andreas Pogiatzis in 2018
<https://infosecwriteups.com/rsa-attacks-common-modulus-7bdb34f331a5>

Maxim Masiutin ported this script in 2021 to Python 3 and added the option to configure output format,
and the code to check that the plaintexts from both decrypted messages to be the same.

Copyright 2018 Andreas Pogiatzis

Copyright 2021 Maxim Masiutin

```
./rsa-common-modulus.py --help
usage: rsa-common-modulus.py [-h] -n MODULUS -e1 E1 -e2 E2 -ct1 CT1 -ct2 CT2 [-q] [-of {decimal,hex,base64,quoted,ascii,utf-8,raw}]

RSA Common modulus attack

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet
  -of {decimal,hex,base64,quoted,ascii,utf-8,raw}, --outputformat {decimal,hex,base64,quoted,ascii,utf-8,raw}

required named arguments:
  -n MODULUS, --modulus MODULUS
                        Common modulus
  -e1 E1, --e1 E1       First exponent
  -e2 E2, --e2 E2       Second exponent
  -ct1 CT1, --ct1 CT1   First ciphertext
  -ct2 CT2, --ct2 CT2   Second ciphertext
```
