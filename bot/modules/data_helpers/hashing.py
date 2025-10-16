import secrets
import string
import uuid

def random_hash(length: int) -> str:
    alphabet = string.ascii_letters + string.digits  # letters + numbers
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def uuid_hash():
    return uuid.uuid4().hex