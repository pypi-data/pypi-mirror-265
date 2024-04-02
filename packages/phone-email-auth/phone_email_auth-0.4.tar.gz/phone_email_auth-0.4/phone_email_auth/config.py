# one_tap_sign_in/config.py

CLIENT_ID = None
ACCESS_TOKEN = None

# one_tap_sign_in/config.py

def set_client_id(client_id):
    """
    Sets the client ID.
    """
    from . import config
    config.CLIENT_ID = client_id

def set_access_token(access_token):
    """
    Sets the access token.
    """
    from . import config
    config.ACCESS_TOKEN = access_token

