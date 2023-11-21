from service.utils import calculate_case_factor, calculate_length_factor, calculate_total_score, contains_digit, contains_special_char, determine_rating, calculate_entropy
from service.generator import generate_suggestions
from modules.wordlist import get_wordlists, get_wordlist, word_in_wordlist
from manager.Policies import Policies
from service.paths import Windows_Paths
from datetime import datetime


class PasswordAnalyzer:
    def __init__(self) -> None:
        self.wordlists = get_wordlists(Windows_Paths.get('wordlist'))
        self.policies = Policies().get_policies(Windows_Paths.get('policy'))

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

        status, wordlist_information = self.check_wordlists(
            password)

        if status == "OK":
            status, policy_information = self.check_policies(password)
        else:
            policy_information = self.check_policies(password)[1]

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
            "policy": policy_information,
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }

        if options.get('zxcvbn', False):
            from modules.zxcvbn_module import get_zxcvbn, extract_zxcvbn
            zxcvbn_data = extract_zxcvbn(get_zxcvbn(password))
            results["zxcvbn"] = zxcvbn_data

        return results

    def check_wordlists(self, password: str) -> tuple:
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

        return status, wordlist_information

    def check_policies(self, password: str) -> tuple:
        status = "OK"
        policy_information = {}

        for policy in self.policies.values():
            if not Policies().validate_password(password, policy.get("content")):

                status = "Critical"
                policy_information[policy.get("name")] = {
                    "status": "Failed",
                    "policy": policy.get("name"),
                    "message": "The password does not meet the policy requirements"
                }

        return status, policy_information
