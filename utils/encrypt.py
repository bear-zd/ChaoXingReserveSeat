from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
from hashlib import md5
import random


def AES_Encrypt(data):
    key = b"u2oh6Vu^HWe4_AES"  # Convert to bytes
    iv = b"u2oh6Vu^HWe4_AES"  # Convert to bytes
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode('utf-8')) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    enctext = base64.b64encode(encrypted_data).decode('utf-8')
    return enctext
    
def resort(submit_info):
    return {key: submit_info[key] for key in sorted(submit_info.keys())}

def enc(submit_info):
    add = lambda x, y: x + y
    processed_info = resort(submit_info)
    needed = [add(add('[', key), '=' + value) + ']' for key, value in processed_info.items()]
    pattern = "%sd`~7^/>N4!Q#){''"
    needed.append(add('[', pattern) + ']')
    seq = ''.join(needed)
    return md5(seq.encode("utf-8")).hexdigest()



def generate_captcha_key(timestamp: int):
    def generate_random_chars():
        hex_chars = '0123456789abcdef'
        random_chars = [random.choice(hex_chars) for _ in range(24)]
        random_chars[14] = '4' 
        random_chars[19] = hex_chars[int(random_chars[19], 16) & 0x3 | 0x8] 
        for pos in [8, 13, 18, 23]:
            random_chars.insert(pos, '-')
        return ''.join(random_chars)
    encoded_timestamp = md5((str(timestamp) + generate_random_chars()).encode("utf-8")).hexdigest()
    timestamp = md5(
        (str(timestamp) + "42sxgHoTPTKbt0uZxPJ7ssOvtXr3ZgZ1" + "slide" + encoded_timestamp).encode("utf-8")
    ).hexdigest() + ":" + str(int(timestamp) + 0x493e0)
    return [encoded_timestamp, timestamp]


if __name__ == "__main__":
    submit_params = {
            "roomId": "1001",
            "startTime": "19:00",
            "endTime": "20:00",
            "day": "2020-10-10",
            "seatNum": "001",
            "captcha": "1",
            "token": "123123132123123",
        }
    print(enc(submit_info=submit_params))