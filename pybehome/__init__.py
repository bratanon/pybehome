import logging

from requests import HTTPError

from pybehome import api

_LOGGER = logging.getLogger(__name__)

class PyBeHome:
    def __init__(self, username, password):
        self._username = username
        self._password = password

        self._token = None
        self.session = None

    def login(self) -> bool:
        if self.get_auth_token():
            return True

        _LOGGER.warning("Unable to login to WeBeHome.")
        return False

    def get_auth_token(self):
        _LOGGER.debug("Getting auth token.")
        try:
            self._token = api.request_token(self._username, self._password)
            return True
        except HTTPError as error:
            _LOGGER.warning(error)
            return False

    def get_devices(self):
        _LOGGER.debug("Getting devices.")
        try:
            return api.request_devices(self._token)
        except HTTPError as error:
            _LOGGER.warning(error)

    def get_location(self):
        _LOGGER.debug("Getting location.")
        try:
            return api.request_location(self._token)
        except HTTPError as error:
            _LOGGER.warning(error)

    def set_arm_state(self, arm_state: str):
        _LOGGER.debug("Setting arm state to %s.", arm_state)
        try:
            return api.request_set_arm_state(self._token, arm_state)
        except HTTPError as error:
            _LOGGER.warning(error)

    def token_destroy(self):
        _LOGGER.debug("Destroying token.")
        try:
            return api.request_token_destroy(self._token)
        except HTTPError as error:
            _LOGGER.warning(error)
