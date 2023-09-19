#!/usr/bin/env python3
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric.rsa import rsa_crt_iqmp, rsa_recover_prime_factors, rsa_crt_dmp1, rsa_crt_dmq1, RSAPublicKey, RSAPrivateNumbers
import math

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

with open("extracted.crt", "rb") as crt_file:
    cert = x509.load_pem_x509_certificate(crt_file.read(), backend=default_backend())
    public_key = cert.public_key()
    assert isinstance(public_key, RSAPublicKey)
    public_numbers = public_key.public_numbers()
    n = public_numbers.n
    e = public_numbers.e
    sum = 51185798527813898217244959146174170995277531101327507615647727646782297370477092100612947052593075126252090256589830237695461025840328352294907386530193231382513463790619213034308781492265111628165309249234796437084817436954404110168743332197444382134896981821409728934361468644113472442965544068752549817351859503041640916596760683531014105154550685026237321821927529703563437223245450854402435570693121557472605563998377744946402019831406325544239643303846017705543806966503249955273500139931504149619319741728657922714315834715358161651401725705034822365071109358954590570384504645707607299923584913543739581356124
    D = sum**2 - 4*n
    s_D = math.isqrt(D)
    assert s_D ** 2 == D
    p = (sum + s_D) // 2
    q = sum - p
    assert p*q == n
    lmbd = lcm(p-1, q-1)
    d = rsa_crt_iqmp(lmbd, e)
    assert (e*d) % lmbd == 1
    iqmp = rsa_crt_iqmp(p, q)
    dmp1 = rsa_crt_dmp1(d, p)
    dmq1 = rsa_crt_dmq1(d, q)
    numbers = RSAPrivateNumbers(p, q, d, dmp1, dmq1, iqmp,
                                    public_numbers)
    key = default_backend().load_rsa_private_numbers(numbers)
    pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    print(pem.decode(), end='')