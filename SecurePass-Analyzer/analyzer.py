from service.utils import calculate_case_factor, calculate_length_factor, calculate_total_score, contains_digit, contains_special_char, determine_rating, calculate_entropy
from service.generator import _generate_strong_password, generate_suggestions
from modules.wordlist import get_wordlists, get_wordlist, word_in_wordlist

from service.paths import Windows_Paths


class PasswordAnalyzer:
    def __init__(self) -> None:
        self.wordlists = get_wordlists(Windows_Paths.get('wordlist'))
        pass

    def analyze(self, password: str, options: dict) -> dict:
        length_factor = calculate_length_factor(password)
        uppercase_factor = calculate_case_factor(password, 'upper')
        lowercase_factor = calculate_case_factor(password, 'lower')
        digit_factor = contains_digit(password)
        special_char_factor = contains_special_char(password)

        total_score = calculate_total_score(
            length_factor, uppercase_factor, lowercase_factor, digit_factor, special_char_factor)

        rating = determine_rating(total_score)

        suggestions = generate_suggestions(
            length_factor, uppercase_factor, lowercase_factor, digit_factor, special_char_factor)

        # Default is OK, when something bad is found, then change to either Critical, or Warning.
        status = "OK"
        wordlist_information = {}

        for wordlist in self.wordlists.values():
            wordlist_data = get_wordlist(wordlist.get("path"))
            if word_in_wordlist(password, wordlist_data):
                status = "Critical"
                wordlist_information[wordlist.get("name")] = {
                    "status": "Found",
                    "wordlist": wordlist.get("name"),
                    "message": "The password was found in the wordlist"
                }

        results = {
            "password": password,
            "status": status,
            "rating": rating,
            "factors": {
                "length_factor": length_factor,
                "uppercase_factor": uppercase_factor,
                "lowercase_factor": lowercase_factor,
                "digit_factor": digit_factor,
                "special_char_factor": special_char_factor,
            },
            "entropy": calculate_entropy(password),
            "wordlist": wordlist_information,
        }

        if options.get('zxcvbn', False):
            from modules.zxcvbn_module import get_zxcvbn, extract_zxcvbn
            zxcvbn_data = extract_zxcvbn(get_zxcvbn(password))
            results["zxcvbn"] = zxcvbn_data

        return results

    def generate_strong_passwords(self, password: str, count: int = 5) -> list:
        strong_passwords = []
        for _ in range(count):
            new_password = _generate_strong_password(password)
            strong_passwords.append(new_password)
        return strong_passwords
