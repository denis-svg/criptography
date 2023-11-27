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

def encrypt(public_key, plaintext):
    n, e = public_key
    ciphertext = pow(plaintext, e, n)
    return ciphertext

def decrypt(private_key, ciphertext):
    n, d = private_key
    plaintext = pow(ciphertext, d, n)
    return plaintext

def string_to_numeric(message, chunk_size=4):
    # Convert each character to its Unicode code point and concatenate
    numeric_value = "".join([str(ord(char)).zfill(chunk_size) for char in message])
    return numeric_value

def numeric_to_string(numeric_value, chunk_size=4):
    # Convert the numeric value to its corresponding character
    if len(numeric_value) % 4 != 0:
        for i in range(4 - len(numeric_value) % 4):
            numeric_value = "0" + numeric_value
    return "".join([chr(int(numeric_value[i:i+chunk_size])) for i in range(0, len(numeric_value), chunk_size)])

# Example usage
public_key, private_key = generate_key_pair()

message = "Prodan denis faf-211"
numeric_value = int(string_to_numeric(message, chunk_size=4))

ciphertext = encrypt(public_key, numeric_value)
decrypted_message = decrypt(private_key, ciphertext)

print(f"Original message: {message}")
print(f"Encrypted message: {ciphertext}")
print(f"Decrypted message: {numeric_to_string(str(decrypted_message))}")