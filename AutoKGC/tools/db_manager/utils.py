def validate_keys(expected_keys, actual_keys):
    missing = set(expected_keys) - set(actual_keys)
    if missing:
        raise KeyError(f"Missing expected keys: {missing}")
