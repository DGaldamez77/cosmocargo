import hashlib

def create_sha256_hash(input_string: str) -> str:
    # Encode the string to bytes using UTF-8 encoding (common practice)
    string_bytes = input_string.encode('utf-8')

    sha256_hash = hashlib.sha256()

    # Update the hash object with the bytes of the string
    sha256_hash.update(string_bytes)

    # Get the hexadecimal representation of the hash
    hex_digest = sha256_hash.hexdigest()

    return hex_digest

