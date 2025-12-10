import random
import string

CHARSET = string.ascii_letters + string.digits ## 62 chars
CODE_LENGTH = 3

def get_short_code():
    return "".join(random.choices(CHARSET, k=CODE_LENGTH))
