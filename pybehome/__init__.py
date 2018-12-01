import logging

from requests import RequestException

from pybehome import api

_LOGGER = logging.getLogger(__name__)


class PyBeHome:
    def __init__(self, username, password):
        self._username = username
        self._password = password

        self._token = None
        self.session = None

        self.devices = {}
        self.location = None

    def login(self) -> bool:
        if self.get_auth_token():
            return True

        _LOGGER.warning("Unable to login to WeBeHome.")
        return False

    def get_auth_token(self):
        _LOGGER.debug("Getting auth token from OPEN API.")
        try:
            self._token = api.request_token(self._username, self._password)
            return True
        except RequestException as error:
            _LOGGER.warning(error)
            return False

    def update_devices(self):
        _LOGGER.debug("Getting device data from OPEN API.")
        try:
            device_list = list(filter(lambda item: 'SubUnitID' in item,
                                  api.request_devices(self._token)))
            for device_data in device_list:
                device = Device(device_data)
                self.devices[device.device_id] = device
        except RequestException as error:
            _LOGGER.warning(error)

    def get_device(self, device_id):
        return self.devices.get(device_id)

    def get_devices(self):
        return self.devices.values()

    def update_location(self):
        _LOGGER.debug("Getting location data from OPEN API.")
        try:
            location_data = api.request_location(self._token)
            del location_data['Tabs']
            self.location = Location(location_data)
        except RequestException as error:
            _LOGGER.warning(error)

    def get_location(self):
        return self.location

    def set_alarm_state(self, arm_state: str):
        _LOGGER.debug("Setting arm state to %s.", arm_state)
        try:
            return api.request_set_arm_state(self._token, arm_state)
        except RequestException as error:
            _LOGGER.warning(error)

    def token_destroy(self):
        _LOGGER.debug("Destroying token.")
        try:
            return api.request_token_destroy(self._token)
        except RequestException as error:
            _LOGGER.warning(error)


class Device(object):
    def __init__(self, device):
        self._device = device

    @property
    def device(self):
        return self._device

    @property
    def device_id(self):
        return self.device.get('SubUnitUniqueID')

    @property
    def name(self):
        return self.device.get('Descr')

    @property
    def type(self):
        return self.device.get('SubUnitTypeDescr')

    @property
    def display_type(self):
        return int(self.device.get('DisplayType'))

    @property
    def battery_level(self):
        return int(self.device.get('BatteryLevel'))

    @property
    def operation_status(self):
        return int(self.device.get('OperationStatus'))

    @property
    def last_event_time(self):
        return self.device.get('ReadingUpdated')

    @property
    def last_event_data(self):
        return self.device.get('LastDataEvent')

    @property
    def lost_connection(self):
        return bool(self.device.get('LostConnection'))

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Location(object):
    def __init__(self, location):
        self._location = location

    @property
    def location(self):
        return self._location

    @property
    def base_unit_id(self):
        return self.location.get('BaseUnitID')

    @property
    def name(self):
        return self.location.get('Descr')

    @property
    def operation_status(self):
        return self.location.get('OperationStatus')

    @property
    def operation_status_info(self):
        return self.location.get('OperationStatusInfo')

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
