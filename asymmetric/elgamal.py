import secrets
from rsa import string_to_numeric, numeric_to_string

def generate_key_pair():
    # Choose a large prime number p
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

    # Find a primitive root modulo p (g)
    g = 2

    # Choose a private key (a)
    a = secrets.randbelow(p - 1) + 1

    # Compute the public key (A)
    A = pow(g, a, p)

    public_key = (p, g, A)
    private_key = (p, a)

    return public_key, private_key

def encrypt(public_key, plaintext):
    p, g, A = public_key

    # Choose a random secret key (k)
    k = secrets.randbelow(p - 1) + 1

    # Compute the shared secret (s)
    s = pow(A, k, p)

    # Compute the ciphertext components
    c1 = pow(g, k, p)
    c2 = (plaintext * s) % p

    return (c1, c2)

def decrypt(private_key, ciphertext):
    p, a = private_key
    c1, c2 = ciphertext

    # Compute the shared secret (s)
    s = pow(c1, a, p)

    # Compute the modular inverse of s
    s_inverse = pow(s, -1, p)

    # Decrypt the plaintext
    decrypted_plaintext = (c2 * s_inverse) % p

    return decrypted_plaintext

if __name__ == "__main__":
    # Example usage
    public_key, private_key = generate_key_pair()

    message = "Prodan denis faf-211"
    numeric_value = int(string_to_numeric(message, chunk_size=4))
    ciphertext = encrypt(public_key, numeric_value)
    decrypted_message = decrypt(private_key, ciphertext)

    print(f"Original message: {message}")
    print(f"Encrypted message: {ciphertext}")
    print(f"Decrypted message: {numeric_to_string(str(decrypted_message))}")
