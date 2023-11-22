import os
import json
from manager.Logger import Logger


class Policies:
    def __init__(self) -> None:
        pass

    def get_policies(self, path: str) -> dict:
        policies = {}

        for root, dirs, files in os.walk(path):
            for file in files:
                if not file.endswith(".json"):
                    Logger().log("wrong_extension_policy", {"policy": file})
                    continue

                policy_path = os.path.join(root, file)
                Logger().log("policy_loaded", {
                    "policy": file, "path": policy_path})

                policy_content = self.get_policy(policy_path)

                if policy_content:
                    policies[file] = {
                        "name": file,
                        "path": policy_path,
                        "content": json.loads(policy_content)
                    }
                else:
                    Logger().log("error_loading_policy", {"policy": file})

            for dir in dirs:
                self.get_policies(dir)

        return policies

    def get_policy(self, path: str) -> str:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                policy = file.read()
        except Exception as e:
            Logger().log("error_loading_policy", {
                "policy": path, "error": str(e)})
            policy = ""

        return policy

    def validate_password(self, password: str, policy: dict) -> bool:
        if len(password) < policy.get("min_length", 0):
            return False

        if policy.get("require_uppercase", False) and not any(char.isupper() for char in password):
            return False

        if policy.get("require_lowercase", False) and not any(char.islower() for char in password):
            return False

        if policy.get("require_digit", False) and not any(char.isdigit() for char in password):
            return False

        if policy.get("require_special_char", False) and not any(char.isalnum() for char in password):
            return False

        return True

    def generate_policy(self, password: str) -> dict:
        # We get a password, now this password is simply going to not be allowed, grab things such as length, uppercase, lowercase, digits, special characters
        # and generate a policy that will not allow this password to be used again
        hasUppercaseLetters = password.isupper()
        hasLowercaseLetters = password.islower()
        hasDigits = password.isdigit()
        hasSpecialCharacters = not password.isalnum()

        policy = {
            "min_length": len(password),
            "require_uppercase": hasUppercaseLetters,
            "require_lowercase": hasLowercaseLetters,
            "require_digit": hasDigits,
            "require_special_char": hasSpecialCharacters
        }

        return policy
