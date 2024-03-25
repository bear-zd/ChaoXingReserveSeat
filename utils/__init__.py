import os 
from .encrypt import AES_Encrypt, generate_captcha_key, enc
from .reserve import reserve

def _fetch_env_variables(env_name, action):
    try:
        return os.environ[env_name] if action else ""
    except KeyError:
        print(f"Environment variable {env_name} is not configured correctly.")
        return None

def get_user_credentials(action):
    usernames = _fetch_env_variables('USERNAMES', action)
    passwords = _fetch_env_variables('PASSWORDS', action)
    return usernames, passwords