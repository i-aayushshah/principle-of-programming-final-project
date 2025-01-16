import secrets
import string

def generate_secret_key(length=32):
    """Generate a secure secret key."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# Generate and print a new secret key
print(generate_secret_key())
