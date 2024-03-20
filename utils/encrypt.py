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

def captcha_key_and_token(_0x353d93: int):
    def generate_random_chars():
        _0xa5adc8 = []
        _0x5cdcca = '0123456789abcdef'
        _0xccd6e7 = 0x0
        while _0xccd6e7 < 0x24:
            _0xa5adc8.append(_0x5cdcca[random.randint(0, 0xf)])
            _0xccd6e7 += 1
        _0xa5adc8[0xe] = '4'
        _0xa5adc8[0x13] = _0x5cdcca[int(_0xa5adc8[0x13], 16) & 0x3 | 0x8]
        _0xa5adc8[0x8] = _0xa5adc8[0xd] = _0xa5adc8[0x12] = _0xa5adc8[0x17] = '-'
        return ''.join(_0xa5adc8)

    _0x4471c4 = md5((str(_0x353d93) + generate_random_chars()).encode("utf-8")).hexdigest()
    _0x353d93 = md5(
        (str(_0x353d93) + "42sxgHoTPTKbt0uZxPJ7ssOvtXr3ZgZ1" + "slide" + _0x4471c4).encode("utf-8")
    ).hexdigest() + ":" + str(int(_0x353d93) + 0x493e0)
    return [_0x4471c4, _0x353d93]


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