import random
import string

CHARSET = string.ascii_letters + string.digits

SHORT_CODE_LENGTH = 3

def get_short_code():
    return "".join(random.choices(CHARSET, k=SHORT_CODE_LENGTH))
