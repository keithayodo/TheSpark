class DRFUtils:
    def check_missing_keys(data, required_keys):
        return [key for key in required_keys
            # Key must exist and have a non-empty value.
            if key not in data or
            (isinstance(data[key], str) and len(data[key]) > 0)]
