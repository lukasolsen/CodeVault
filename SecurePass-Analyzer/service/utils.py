import re
from math import log2


def calculate_length_factor(password: str) -> float:
    return len(password) / 8


def calculate_case_factor(password: str, case: str) -> int:
    return 1 if re.search(f'[{case}]', password) else 0


def contains_digit(password: str) -> int:
    return 1 if re.search(r'\d', password) else 0


def contains_special_char(password: str) -> int:
    return 1 if re.search(r'[!@#$%^&*(),.?":{}|<>]', password) else 0


def calculate_total_score(*factors) -> float:
    return sum(factors)


def determine_rating(total_score: float) -> str:
    if total_score >= 4:
        return "Excellent"
    elif total_score >= 3:
        return "Good"
    elif total_score >= 2:
        return "Moderate"
    else:
        return "Weak"


def calculate_entropy(password: str) -> float:
    char_set = len(set(password))
    return len(password) * log2(char_set) if char_set > 0 else 0
    
