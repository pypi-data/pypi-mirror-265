from . import superpowered


def set_api_key(key_id: str, key_secret: str):
    """
    Set the API key to use for all API calls.

    Args:
        key_id (str): The API key ID.
        key_secret (str): The API key secret.
    """
    superpowered._set_api_key(key_id, key_secret)


def set_base_url(base_url: str):
    """
    Set the base URL to use for all API calls.

    Args:
        base_url (str): The base URL to use for all API calls.
    """
    superpowered._set_base_url(base_url)