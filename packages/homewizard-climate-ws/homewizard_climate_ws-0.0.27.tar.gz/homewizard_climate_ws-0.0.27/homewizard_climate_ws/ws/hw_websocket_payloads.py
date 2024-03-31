import json
from enum import Enum

from homewizard_climate_ws.api.api import HomeWizardClimateApi
from homewizard_climate_ws.model.climate_device import (
        HomeWizardClimateDevice,
        HomeWizardClimateDeviceType
    )

class HomeWizardClimateWSPayloads:
    def __init__(self, api: HomeWizardClimateApi, device: HomeWizardClimateDevice):
        self._device = device
        self._api = api

    def hello(self) -> str:
        return json.dumps(
            {
                "message_id": "hello",
                "token": self._api.token,
                "type": "hello",
                "source": "https://github.com/mepla/homewizard-climate-websocket",
                "compatibility": 4,
            }
        )

    def subscribe(self) -> str:
        return json.dumps(
            {
                "type": "subscribe_device",
                "device": self._device.identifier,
                "message_id": "subscribe",
            }
        )

    def turn_on(self) -> str:
        return json.dumps(
            {
                "device": self._device.identifier,
                "message_id": "turn_on",
                "type": "json_patch",
                "patch": [{"op": "replace", "path": "/state/power_on", "value": True}],
            }
        )

    def turn_off(self) -> str:
        return json.dumps(
            {
                "device": self._device.identifier,
                "message_id": "turn_off",
                "type": "json_patch",
                "patch": [{"op": "replace", "path": "/state/power_on", "value": False}],
            }
        )

    def turn_on_cool(self) -> str:
        return json.dumps(
            {
                "device": self._device.identifier,
                "type": "json_patch",
                "patch": [{"op": "replace", "path": "/state/cool", "value": True}],
            }
        )

    def turn_off_cool(self) -> str:
        return json.dumps(
            {
                "device": self._device.identifier,
                "type": "json_patch",
                "patch": [{"op": "replace", "path": "/state/cool", "value": False}],
            }
        )

    def set_heater(self) -> str:
        return json.dumps(
            {
                "device": self._device.identifier,
                "type": "json_patch",
                "patch": [{"op": "replace", "path": "/state/heater", "value": True}],
            }
        )

    def set_cooler(self) -> str:
        return json.dumps(
            {
                "device": self._device.identifier,
                "type": "json_patch",
                "patch": [{"op": "replace", "path": "/state/heater", "value": False}],
            }
        )

    def set_target_temperature(self, temp: int) -> str:
        return json.dumps(
            {
                "device": self._device.identifier,
                "type": "json_patch",
                "patch": [
                    {
                        "op": "replace",
                        "path": "/state/target_temperature",
                        "value": temp,
                    }
                ],
            }
        )

    def set_target_humidity(self, humidity: int) -> str:
        return json.dumps(
            {
                "device": self._device.identifier,
                "type": "json_patch",
                "patch": [
                    {
                        "op": "replace",
                        "path": "/state/target_humidity",
                        "value": humidity,
                    }
                ],
            }
        )

    def set_fan_speed(self, speed: str) -> str:
        return json.dumps(
            {
                "device": self._device.identifier,
                "type": "json_patch",
                "patch": [
                    {"op": "replace", "path": "/state/fan_speed", "value": speed}
                ],
            }
        )
    
    def set_speed(self, speed: int) -> str:
        return json.dumps(
            {
                "device": self._device.identifier,
                "type": "json_patch",
                "patch": [
                    {"op": "replace", "path": "/state/speed", "value": speed}
                ],
            }
        )

    def set_timer(self, timer: int) -> str:
        return json.dumps(
            {
                "device": self._device.identifier,
                "type": "json_patch",
                "patch": [
                    {"op": "replace", "path": "/state/timer", "value": timer}
                ],
            }
        )

    def set_mode(self, mode: str) -> str:
        return json.dumps(
            {
                "device": self._device.identifier,
                "type": "json_patch",
                "patch": [
                    {"op": "replace", "path": "/state/mode", "value": mode}
                ],
            }
        )

    def set_swing(self, value: bool) -> str:
        return json.dumps(
            {
                "device": self._device.identifier,
                "type": "json_patch",
                "patch": [
                    {"op": "replace", "path": "/state/swing", "value": value}
                ],
            }
        )

    def turn_on_oscillate(self) -> str:
        path = "/state/oscillate"
        print(self._device.type)
        if self._device.type == HomeWizardClimateDeviceType.FAN:
            path = "/state/oscillation"
        return json.dumps(
            {
                "device": self._device.identifier,
                "type": "json_patch",
                "patch": [{"op": "replace", "path": path, "value": True}],
            }
        )

    def turn_off_oscillate(self) -> str:
        path = "/state/oscillate"
        if self._device.type == HomeWizardClimateDeviceType.FAN:
            path = "/state/oscillation"
        return json.dumps(
            {
                "device": self._device.identifier,
                "type": "json_patch",
                "patch": [
                    {"op": "replace", "path": path, "value": False}
                ],
            }
        )


class HomeWizardClimateStatePath(Enum):
    CURRENT_TEMP = "/state/current_temperature"
