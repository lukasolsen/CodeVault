from service.utils import calculate_case_factor, calculate_length_factor, calculate_total_score, contains_digit, contains_special_char, determine_rating, calculate_entropy
from service.generator import generate_suggestions
from manager.Policies import Policies
from manager.Wordlist import Wordlist
from service.paths import Windows_Paths
from datetime import datetime


class PasswordAnalyzer:
    def __init__(self) -> None:
        self.wordlist = Wordlist()
        self.wordlists = self.wordlist.get_wordlists(
            Windows_Paths.get('wordlist'))
        self.policies = Policies().get_policies(Windows_Paths.get('policy'))

    def analyze(self, password: str, options: dict) -> dict:
        status = "OK"

        # Calculate factors
        length_factor = calculate_length_factor(password)
        uppercase_factor = calculate_case_factor(password, 'uppercase')
        lowercase_factor = calculate_case_factor(password, 'lowercase')
        digit_factor = contains_digit(password)
        special_char_factor = contains_special_char(password)

        # Calculate total score and determine rating
        total_score = calculate_total_score(
            length_factor, uppercase_factor, lowercase_factor, digit_factor, special_char_factor)
        rating = determine_rating(total_score)

        # Generate suggestions
        suggestions = generate_suggestions(
            length_factor, uppercase_factor, lowercase_factor, digit_factor, special_char_factor)

        # Check against wordlists
        status_wordlist, wordlist_information = self.check_wordlists(password)

        status_policy, policy_information = self.check_policies(password)

        if status_wordlist == "Critical" or status_policy == "Critical":
            status = "Critical"

        general_information = {
            "Password": password,
            "Timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }

        security_assessment = {
            "Status": status,
            "Rating": rating,
            "Entropy": calculate_entropy(password),
        }

        password_factors = {
            "Length Factor": length_factor,
            "Uppercase Factor": uppercase_factor,
            "Lowercase Factor": lowercase_factor,
            "Digit Factor": digit_factor,
            "Special Character Factor": special_char_factor,
        }

        results = {
            "General Information": general_information,
            "Security Assessment": security_assessment,
            "Password Factors": password_factors,
            "Wordlist Check": wordlist_information,
            "Policy Check": policy_information,
        }

        # Include zxcvbn information if requested
        if options.get('zxcvbn', False):
            from modules.zxcvbn_module import get_zxcvbn, extract_zxcvbn
            zxcvbn_data = extract_zxcvbn(get_zxcvbn(password))
            results["zxcvbn Analysis"] = zxcvbn_data

        return results

    def check_wordlists(self, password: str) -> tuple:
        status = "OK"
        wordlist_information = {}

        for wordlist in self.wordlists.values():
            wordlist_data = self.wordlist.get_wordlist(wordlist.get("path"))
            if self.wordlist.word_in_wordlist(password, wordlist_data):
                status = "Critical"
                wordlist_information[wordlist.get("name")] = {
                    "Status": "Found",
                    "Wordlist": wordlist.get("name"),
                    "Message": "The password was found in the wordlist"
                }

        return status, wordlist_information

    def check_policies(self, password: str) -> tuple:
        status = "OK"
        policy_information = {}

        for policy in self.policies.values():
            if not Policies().validate_password(password, policy.get("content")):
                status = "Critical"
                policy_information[policy.get("name")] = {
                    "Status": "Failed",
                    "Policy": policy.get("name"),
                    "Message": "The password does not meet the policy requirements"
                }

        return status, policy_information
