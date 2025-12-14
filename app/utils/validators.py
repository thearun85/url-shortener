from urllib.parse import urlparse
import re

MAX_URL_LENGTH = 2048
SHORT_CODE_PATTERN = re.compile(r"^[a-zA-Z0-9]+$")
MAX_SHORT_CODE_LENGTH = 10

def validate_url(url: str)-> tuple[bool, str | None]:
    if not url:
        return False, "URL cannot be empty"

    if len(url) > MAX_URL_LENGTH:
        return False,f"URL cannot exceed {MAX_URL_LENGTH} characters."

    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):  
            return False, "URL must start with http:// or https://"
        if not parsed.netloc:
            return False, "URL must have valid domain"
    except Exception as e:
        return False, "Invalid URL format"

    return True, None

def validate_shortcode(code: str)-> tuple[bool, str | None]:

    if not code:
        return False, "Short code cannot be empty"

    if len(code) > MAX_SHORT_CODE_LENGTH:
        return False, f"Short code length exceeds {MAX_SHORT_CODE_LENGTH} characters."

    if not SHORT_CODE_PATTERN.match(code):
        return False, "Short code must contain only letters and numbers."

    return True, None
