
from cryptography.fernet import Fernet

key = Fernet.generate_key()

with open("keys/secret.key", "wb") as key_file:
    key_file.write(key)

print("Secret Key Generated Successfully")

