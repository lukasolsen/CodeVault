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
    data["zxcvbn Score"] = zxcvbn_data.get('score', 0)
    data["zxcvbn Guesses"] = zxcvbn_data.get('guesses', 0)
    data["zxcvbn Guesses Log10"] = zxcvbn_data.get(
        'guesses_log10', 0)

    data["zxcvbn Feedback"] = zxcvbn_data.get(
        'feedback', [])

    custom_sequence = []
    for sequence in zxcvbn_data.get('sequence', []):
        custom_sequence.append({
            "Pattern": sequence.get('pattern', ''),
            "Token": sequence.get('token', ''),
            "Guesses": sequence.get('guesses', 0),
            "Rank": sequence.get('rank', 0),
            "Dictionary_name": sequence.get('dictionary_name', ''),
        })

    data["zxcvbn Sequence"] = custom_sequence

    return data
