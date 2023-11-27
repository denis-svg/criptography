def diffie_hellman(p, g, a, b):
    A = pow(g, a, p)  # Alice's public key
    B = pow(g, b, p)  # Bob's public key

    shared_secret_alice = pow(B, a, p)  # Alice computes shared secret
    shared_secret_bob = pow(A, b, p)    # Bob computes shared secret

    return shared_secret_alice, shared_secret_bob

p = int("""3231700607131100730015351347782516336248805713348907517458843413926
            980683413621000279205636264016468545855635793533081692882902308057347
            262527355474246124574102620252791657297286270630032526342821314576693
            141422365422094111134862999165747826803423055308634905063555771221918
            789033272956969612974385624174123623722519734640269185579776797682301
            462539793305801522685873076119753243646747585546071504389684494036613
            049769781285429595865959756705128385213278446852292550456827287911372
            009893187395914337417583782600027803497319855206060753323412260325468
            4088120031105907484281003994966956119696956248629032338072839127039
            """.replace("\n", "").replace(" ", ""))

g = 2

import secrets

a = secrets.randbits(8)  # Alice
b = secrets.randbits(8)  # Bob

print(f"Alice secret key {a}")
print(f"Bob secret key {b}")

shared_secret_alice, shared_secret_bob = diffie_hellman(p, g, a, b)

print(f"shared_secret_alice {shared_secret_alice}")
print(f"shared_secret_bob {shared_secret_bob}")
print(f"{shared_secret_alice==shared_secret_bob}")
