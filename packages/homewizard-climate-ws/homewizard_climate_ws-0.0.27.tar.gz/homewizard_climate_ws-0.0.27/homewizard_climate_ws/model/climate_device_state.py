from dataclasses import dataclass
from typing import Optional
from dataclasses_json import dataclass_json, Undefined


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class HomeWizardClimateDeviceState:
    power_on: bool
    mode: Optional[str]
    current_temperature: int
    target_temperature: int
    target_humidity: int
    current_humidity: int
    fan_speed: str
    oscillate: bool
    oscillation: bool
    timer: int
    speed: int
    error: list[str]
    heat_status: str
    vent_heat: bool
    silent: bool
    heater: bool
    swing: bool
    ext_mode: list[str]
    ext_current_temperature: Optional[int]
    ext_target_temperature: Optional[int]
    cool: bool
    mute: bool
    warning: list[str]


def default_state():
    return HomeWizardClimateDeviceState.from_dict(
        {
            "power_on": False,
            "mode": "normal",
            "current_temperature": 0,
            "target_temperature": 0,
            "target_humidity": 0,
            "current_humidity": 0,
            "fan_speed": 'low',
            "oscillate": False,
            "oscillation": False,
            "timer": 0,
            "speed": 1,
            "ext_mode": [],
            "heat_status": "idle",
            "vent_heat": False,
            "silent": False,
            "heater": False,
            "swing": False,
            "error": [],
            "ext_current_temperature": 0,
            "ext_target_temperature": 0,
            "cool": False,
            "mute": False,
            "warning": [],
        }
    )


def diff_states(
    first_state: HomeWizardClimateDeviceState,
    second_state: HomeWizardClimateDeviceState,
) -> str:
    result = ""
    for k, v in first_state.to_dict().items():
        if k in second_state.to_dict():
            second_value = second_state.to_dict().get(k)
            if v != second_value:
                result += f"{k}: {v} -> {second_value}, "

    return result
