import base64
import json
import logging
import time

import requests

from pybehome.constants import WEBEHOME_BASE_URL, \
    WEBEHOME_DEFAULT_JWT_TOKEN, WEBEHOME_VERSION, WEBEHOME_APPTYPE, \
    WEBEHOME_APP, WEBEHOME_DEVICE_NAME

_LOGGER = logging.getLogger(__name__)


def _build_url(service: str, arg=None) -> str:
   if arg is None:
        return '{}/{}'.format(WEBEHOME_BASE_URL, service)
   else:
       return '{}/{}?arg={}'.format(WEBEHOME_BASE_URL, service, arg)


def request_token(username, password) -> str:
    """Request token."""
    headers = {
        'Authorization': 'Bearer %s' % WEBEHOME_DEFAULT_JWT_TOKEN,
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "Created": int(time.time()),
        "AppVersion": WEBEHOME_VERSION,
        "AppType": WEBEHOME_APPTYPE,
        "App": WEBEHOME_APP,
        "DeviceName": WEBEHOME_DEVICE_NAME,
        "LoginName": username,
        "Password": password
    })
    arg = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
    response = requests.get(
        _build_url('CreateWebTokens/LoginAccountUser', arg), headers=headers)
    response.raise_for_status()
    return response.json().get('jwt')


def request_devices(token: str) -> str:
    """Request devices."""
    headers = {
        'Authorization': 'Bearer %s' % token,
        'Content-Type': 'application/json'
    }
    payload = {
        "Created": int(time.time()),
        "AppVersion": WEBEHOME_VERSION,
        "AppType": WEBEHOME_APPTYPE,
        "App": WEBEHOME_APP
    }
    response = requests.post(
        _build_url('Location/GetDevices'),
        headers=headers,
        json=payload)
    response.raise_for_status()
    return response.json().get('Components')


def request_location(token: str) -> str:
    """Request location."""
    headers = {
        'Authorization': 'Bearer %s' % token,
        'Content-Type': 'application/json'
    }
    payload = {
        "Created": int(time.time()),
        "AppVersion": WEBEHOME_VERSION,
        "AppType": WEBEHOME_APPTYPE,
        "App": WEBEHOME_APP
    }
    response = requests.post(
        _build_url('Location/GetStatus3'),
        headers=headers,
        json=payload)
    response.raise_for_status()
    return response.json().get('ActiveLocation')


def request_set_arm_state(token: str, arm_state: str):
    """Request set arm state."""
    headers = {
        'Authorization': 'Bearer %s' % token,
        'Content-Type': 'application/json'
    }
    payload = {
        "Created": int(time.time()),
        "AppVersion": WEBEHOME_VERSION,
        "AppType": WEBEHOME_APPTYPE,
        "App": WEBEHOME_APP
    }
    response = requests.post(
        _build_url('Location/{}'.format(arm_state)),
        headers=headers,
        json=payload)
    response.raise_for_status()
    return response.json()


def request_token_destroy(token: str):
    """Request a logout and token destroy."""
    headers = {
        'Authorization': 'Bearer %s' % token,
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "Created": int(time.time()),
        "AppVersion": WEBEHOME_VERSION,
        "AppType": WEBEHOME_APPTYPE,
        "App": WEBEHOME_APP
    })
    arg = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
    response = requests.get(
        _build_url('CreateWebTokens/Delete', arg), headers=headers)

    response.raise_for_status()
    return response.json()