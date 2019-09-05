from base64 import b64encode

from requests import post

from app.settings import ENCODING


def build_payload(username, password):
    """ Take the username and password input and build the payload; grant_type is password"""
    return f"grant_type=password&username={username}&password={password}"


def build_headers(client_id, client_secret):
    """ Build the request header, encode the client_id and client_secret """
    return {
        'content-type': "application/x-www-form-urlencoded",
        'authorization': f"Basic {encode_client_details(client_id, client_secret)}",
        'cache-control': "no-cache"
    }


def encode_client_details(client_id, client_secret):
    """ Base64 encode the client_id and client_secret
    :return str
    """
    encoded_details = b64encode(bytes(f'{client_id}:{client_secret}', ENCODING))
    return str(encoded_details, ENCODING)


def get_token(token_endpoint, payload, headers):
    """ POST request to token endpoint """
    # verify=False - need trusted SSL certificate, bypassing this currently
    return post(token_endpoint, data=payload, headers=headers, verify=False)
