#!/usr/bin/env python3
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

with open("server.key", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )
    privs = private_key.private_numbers()
    pubs = private_key.public_key().public_numbers()
    print("p+q", privs.p + privs.q)
    print()
    print("p", hex(privs.p))
    print()
    print("q", hex(privs.q))
    print()
    print("d", hex(privs.d))