import secrets
import string


def generate_verification_code(length: int = 6) -> str:
    """
    Generate a secure numeric verification code (OTP).
    Default length is 6 digits.
    """
    digits = string.digits  # "0123456789"
    return "".join(secrets.choice(digits) for _ in range(length))


def generate_random_code(length: int = 8) -> str:
    """
    Generate a secure alphanumeric random code.
    Useful for: referral codes, temporary tokens, filenames, etc.
    """
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))
