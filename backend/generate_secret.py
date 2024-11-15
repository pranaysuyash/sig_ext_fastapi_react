from secrets import token_hex

def generate_secret_key():
    """Generate a secure secret key."""
    return token_hex(32)

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("\nGenerated secure secret key:")
    print(secret_key)
    print("\nUpdate your .env file with:")
    print(f"JWT_SECRET={secret_key}\n")