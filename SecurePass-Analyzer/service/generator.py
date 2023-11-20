import random
import string


def generate_password(options: dict) -> str:
    length = options.get('length', 14)
    include_uppercase = options.get('include_uppercase', True)
    include_lowercase = options.get('include_lowercase', True)
    include_digits = options.get('include_digits', True)
    include_special_chars = options.get('include_special_chars', False)

    random_chars = ''
    if include_uppercase:
        random_chars += string.ascii_uppercase
    if include_lowercase:
        random_chars += string.ascii_lowercase
    if include_digits:
        random_chars += string.digits
    if include_special_chars:
        random_chars += string.punctuation

    password = ''.join(random.choice(random_chars) for _ in range(length))
    return password


def _generate_strong_password(password: str) -> str:
    # Strengthen the password by adding random characters
    random_chars = string.ascii_letters + string.digits + string.punctuation
    strengthened_password = ''.join(random.choice(
        random_chars) for _ in range(len(password) + 5))
    return strengthened_password


def generate_suggestions(*factors) -> list:
    suggestions = []
    if factors[0] < 1:
        suggestions.append("Consider increasing the password length")
    if factors[1] == 0 or factors[2] == 0:
        suggestions.append(
            "Use a combination of uppercase and lowercase letters")
    if factors[3] == 0:
        suggestions.append("Include at least one digit")
    if factors[4] == 0:
        suggestions.append("Include at least one special character")
    return suggestions
