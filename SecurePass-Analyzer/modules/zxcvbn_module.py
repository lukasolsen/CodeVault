import os


def get_zxcvbn(password: str) -> dict:
    # Get the zxcvbn data.
    try:
        import zxcvbn
    except ImportError:
        print(
            "Error: zxcvbn is not installed. Please install it using 'pip install zxcvbn-python'")
        os.system("pip install zxcvbn-python")
        try:
            import zxcvbn
        except ImportError:
            print(
                "Error: zxcvbn is not installed. Please install it using 'pip install zxcvbn-python'")
            return {}

    zxcvbn_data = zxcvbn.zxcvbn(password)
    return zxcvbn_data


def extract_zxcvbn(zxcvbn_data: dict) -> dict:
    # Extract the zxcvbn data.
    data = {}
    data["zxcvbn_score"] = zxcvbn_data.get('score', 0)
    data["zxcvbn_guesses"] = zxcvbn_data.get('guesses', 0)
    data["zxcvbn_guesses_log10"] = zxcvbn_data.get(
        'guesses_log10', 0)

    data["zxcvbn_feedback"] = zxcvbn_data.get(
        'feedback', [])

    custom_sequence = []
    for sequence in zxcvbn_data.get('sequence', []):
        custom_sequence.append({
            "pattern": sequence.get('pattern', ''),
            "token": sequence.get('token', ''),
            "guesses": sequence.get('guesses', 0),
            "rank": sequence.get('rank', 0),
            "dictionary_name": sequence.get('dictionary_name', ''),
        })

    data["zxcvbn_sequence"] = custom_sequence

    return data
