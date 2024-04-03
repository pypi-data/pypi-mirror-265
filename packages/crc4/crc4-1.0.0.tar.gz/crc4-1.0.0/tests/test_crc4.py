#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test rc4"""

import os
import timeit
from warnings import filterwarnings as filter_warnings

import crc4


def crypt_rc4(data: bytes, key: bytes) -> bytes:
    """rc4 crypto"""

    S = list(range(256))
    j: int = 0
    out: bytearray = bytearray()

    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0

    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(byte ^ S[(S[i] + S[j]) % 256])

    return bytes(out)


def main() -> int:
    """entry / main function"""

    print("Implementation tests...")

    assert (
        crypt_rc4(b"This is data.", b"This is a key.")
        == b"\xce\x90\xacW\x10\x1d\xf3qE\xea\xf5k2"
    ), "Bad Python implementation of RC4."

    assert (
        crc4.rc4(b"This is data.", b"This is a key.")
        == b"\xce\x90\xacW\x10\x1d\xf3qE\xea\xf5k2"
    ), "Bad C implementation of RC4."

    for idx in range(1, 256):
        a: bytes = os.urandom(idx)
        b: bytes = os.urandom(idx * 2)

        print(f"Implementation test: {idx}")

        assert crypt_rc4(a, b) == crc4.rc4(a, b), "Bad implementation of RC4(a, b)."
        assert crypt_rc4(b, a) == crc4.rc4(b, a), "Bad implementation of RC4(b, a)."
        assert crypt_rc4(a, a) == crc4.rc4(a, a), "Bad implementation of RC4(a, a)."
        assert (
            crc4.rc4(crc4.rc4(a, b), b) == a
        ), "Bad implementation of RC4(RC4(a, b), b) (decryption)."

    print("Timing tests...")

    print("Python...", end=" ")
    python: float = timeit.timeit(
        lambda: crypt_rc4(os.urandom(16), os.urandom(32)), number=51200
    )
    print(python)

    print("C...", end=" ")
    c: float = timeit.timeit(
        lambda: crc4.rc4(os.urandom(16), os.urandom(32)), number=51200
    )
    print(c)

    assert (
        python >= c
    ), "Python implementation faster or as performant as the C version."

    return 0


if __name__ == "__main__":
    assert main.__annotations__.get("return") is int, "main() should return an integer"

    filter_warnings("error", category=Warning)
    raise SystemExit(main())
