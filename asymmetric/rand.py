import secrets
import sympy

def generate_random_prime(bits):
    while True:
        candidate = secrets.randbits(bits)
        if sympy.isprime(candidate):
            return candidate