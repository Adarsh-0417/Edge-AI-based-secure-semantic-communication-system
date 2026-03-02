import json
from cryptography.fernet import Fernet

# Generate once and keep fixed (for demo)
SECRET_KEY = b'XoKaZtDVbgUfpPX9dJflwcOwLce29SbmP0sZ3n4XlAo='

cipher = Fernet(SECRET_KEY)

def encrypt_data(data: dict) -> bytes:
    json_data = json.dumps(data).encode()
    return cipher.encrypt(json_data)

def decrypt_data(token: bytes) -> dict:
    decrypted = cipher.decrypt(token)
    return json.loads(decrypted.decode())