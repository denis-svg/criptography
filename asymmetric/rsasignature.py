import chilkat2
from rand import generate_random_prime

def generate_key_pair():
    # Choose two distinct prime numbers
    p = generate_random_prime(2048)
    q = generate_random_prime(2048)

    # Compute n and totient
    n = p * q
    totient = (p - 1) * (q - 1)

    # Choose public key exponent (e)
    e = 65537  # Commonly used value

    # Calculate private key exponent (d)
    d = pow(e, -1, totient)

    public_key = (n, e)
    private_key = (n, d)

    return public_key, private_key

crypt = chilkat2.Crypt2()

content = "abcdefghijklmnopqrstuvwxyz"
crypt.EncodingMode = "dec"
crypt.HashAlgorithm = "ripemd320"

def sign(private_key, message):
    n, d = private_key

    # Calculate the hash of the message using RipeMD-320
    hash_value = int(crypt.HashStringENC(message))
    print("Message hash:", hash_value)

    # Sign the hash value using the private key
    signature = pow(hash_value, d, n)
    print("Signature:", signature)
    return signature

def verify(public_key, message, signature):
    n, e = public_key

    # Calculate the hash of the message using RipeMD-320
    hash_value = int(crypt.HashStringENC(message))

    # Verify the signature using the public key
    hash_from_signature = pow(signature, e, n)
    print("Hash from signature:", hash_from_signature)
    return hash_from_signature == hash_value

public_key, private_key = generate_key_pair()
signature = sign(private_key, "denis")
print(verify(public_key, "denis", signature))