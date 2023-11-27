import secrets
import chilkat2

crypt = chilkat2.Crypt2()

content = "abcdefghijklmnopqrstuvwxyz"
crypt.EncodingMode = "dec"
crypt.HashAlgorithm = "ripemd320"

# ElGamal Key Pair Generation
def generate_elgamal_key_pair():
    # Given prime p and generator g
    p = p = int("""3231700607131100730015351347782516336248805713348907517458843413926
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

    # Choose a private key (a)
    a = secrets.randbelow(p - 1) + 1

    # Compute the public key (A)
    A = pow(g, a, p)

    public_key = (p, g, A)
    private_key = (p, a)

    return public_key, private_key

# ElGamal Signature Generation
def sign_elgamal(private_key, message):
    p, a = private_key
    g = 2  # Generator

    # Choose a random secret key (k)
    k = secrets.randbelow(p - 2) + 1

    # Compute r and s components of the signature
    r = pow(g, k, p)
    hash_value = int(crypt.HashStringENC(message))
    s = (hash_value - a * r) * pow(k, -1, p - 1) % (p - 1)

    return r, s

# ElGamal Signature Verification
def verify_elgamal(public_key, message, signature):
    p, g, A = public_key
    r, s = signature

    # Verify that 0 < r < p and 0 < s < p-1
    if not (0 < r < p and 0 < s < p - 1):
        return False

    # Compute the hash value of the message
    hash_value = int(crypt.HashStringENC(message))

    # Compute the components of the verification equation
    v1 = pow(A, r, p) * pow(r, s, p) % p
    v2 = pow(g, hash_value, p)

    return v1 == v2

if __name__ == "__main__":
    elgamal_public_key, elgamal_private_key = generate_elgamal_key_pair()

    message = "Prodan denis faf-211"
    signature = sign_elgamal(elgamal_private_key, message)
    is_valid = verify_elgamal(elgamal_public_key, message, signature)

    print(f"Original message: {message}")
    print(f"ElGamal Signature: {signature}")
    print(f"Is ElGamal signature valid? {is_valid}")