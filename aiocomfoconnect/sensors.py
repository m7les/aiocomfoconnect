"""Sensor definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict

from .const import PdoType
from .util import calculate_airflow_constraints

# Sensors
SENSOR_AIRFLOW_CONSTRAINTS = 230
SENSOR_ANALOG_INPUT_1 = 369
SENSOR_ANALOG_INPUT_2 = 370
SENSOR_ANALOG_INPUT_3 = 371
SENSOR_ANALOG_INPUT_4 = 372
SENSOR_AVOIDED_COOLING = 216
SENSOR_AVOIDED_COOLING_TOTAL = 218
SENSOR_AVOIDED_COOLING_TOTAL_YEAR = 217
SENSOR_AVOIDED_HEATING = 213
SENSOR_AVOIDED_HEATING_TOTAL = 215
SENSOR_AVOIDED_HEATING_TOTAL_YEAR = 214
SENSOR_BYPASS_ACTIVATION_STATE = 66
SENSOR_BYPASS_OVERRIDE = 338
SENSOR_BYPASS_STATE = 227
SENSOR_CHANGING_FILTERS = 18
SENSOR_COMFOFOND_GHE_PRESENT = 419
SENSOR_COMFOFOND_GHE_STATE = 418
SENSOR_COMFOFOND_TEMP_GROUND = 417
SENSOR_COMFOFOND_TEMP_OUTDOOR = 416
SENSOR_COMFORTCONTROL_MODE = 225
SENSOR_DAYS_TO_REPLACE_FILTER = 192
SENSOR_DEVICE_STATE = 16
SENSOR_FAN_EXHAUST_DUTY = 117
SENSOR_FAN_EXHAUST_FLOW = 119
SENSOR_FAN_EXHAUST_SPEED = 121
SENSOR_FAN_MODE_EXHAUST = 71
SENSOR_FAN_MODE_EXHAUST_2 = 55
SENSOR_FAN_MODE_EXHAUST_3 = 343
SENSOR_FAN_MODE_SUPPLY = 70
SENSOR_FAN_MODE_SUPPLY_2 = 54
SENSOR_FAN_MODE_SUPPLY_3 = 342
SENSOR_FAN_SPEED_MODE = 65
SENSOR_FAN_SPEED_MODE_MODULATED = 226
SENSOR_FAN_SUPPLY_DUTY = 118
SENSOR_FAN_SUPPLY_FLOW = 120
SENSOR_FAN_SUPPLY_SPEED = 122
SENSOR_FROSTPROTECTION_UNBALANCE = 228
SENSOR_HUMIDITY_AFTER_PREHEATER = 293
SENSOR_HUMIDITY_EXHAUST = 291
SENSOR_HUMIDITY_EXTRACT = 290
SENSOR_HUMIDITY_OUTDOOR = 292
SENSOR_HUMIDITY_SUPPLY = 294
SENSOR_NEXT_CHANGE_BYPASS = 82
SENSOR_NEXT_CHANGE_COMFOCOOL = 85
SENSOR_NEXT_CHANGE_FAN = 81
SENSOR_NEXT_CHANGE_FAN_EXHAUST = 87
SENSOR_NEXT_CHANGE_FAN_SUPPLY = 86
SENSOR_OPERATING_MODE = 56
SENSOR_OPERATING_MODE_2 = 49
SENSOR_POWER_USAGE = 128
SENSOR_POWER_USAGE_TOTAL = 130
SENSOR_POWER_USAGE_TOTAL_YEAR = 129
SENSOR_PREHEATER_POWER = 146
SENSOR_PREHEATER_POWER_TOTAL = 145
SENSOR_PREHEATER_POWER_TOTAL_YEAR = 144
SENSOR_PROFILE_TEMPERATURE = 67
SENSOR_RF_PAIRING_MODE = 176
SENSOR_RMOT = 209
SENSOR_SEASON_COOLING_ACTIVE = 211
SENSOR_SEASON_HEATING_ACTIVE = 210
SENSOR_TARGET_TEMPERATURE = 212
SENSOR_TEMPERATURE_EXHAUST = 275
SENSOR_TEMPERATURE_EXTRACT = 274
SENSOR_TEMPERATURE_OUTDOOR = 276
SENSOR_TEMPERATURE_OUTDOOR_PREHEATED = 220
SENSOR_TEMPERATURE_OUTDOOR_PREHEATED_2 = 277
SENSOR_TEMPERATURE_SUPPLY = 221
SENSOR_TEMPERATURE_SUPPLY_PREHEATED = 278
SENSOR_UNIT_AIRFLOW = 224
SENSOR_UNIT_TEMPERATURE = 208
SENSOR_COMFOCOOL_STATE = 784
SENSOR_COMFOCOOL_CONDENSOR_TEMP = 802

UNIT_WATT = "W"
UNIT_KWH = "kWh"
UNIT_VOLT = "V"
UNIT_CELCIUS = "°C"
UNIT_PERCENT = "%"
UNIT_RPM = "rpm"
UNIT_M3H = "m³/h"
UNIT_DAYS = "days"
UNIT_SECONDS = "s"


@dataclass
class Sensor:
    """Dataclass for a Sensor"""

    name: str
    unit: str | None
    id: int  # pylint: disable=invalid-name
    type: int
    value_fn: Callable[[int], any] = None


def _t10(x):
    """Decode a temperature stored as tenths of a degree."""
    return x / 10


# For more information, see PROTOCOL-PDO.md
#
# This dict is intended to be an exhaustive transcription of every PDO documented
# in docs/PROTOCOL-PDO.md. Entries whose meaning is still unknown are named
# "sensor_<id>" and carry their documented data type so the value can still be
# pulled and decoded; consumers can surface them as diagnostics (see
# SENSORS_DEBUG). Human-readable labelling/enum decoding is intentionally left to
# consumers (e.g. the Home Assistant integration).
SENSORS: Dict[int, Sensor] = {
    SENSOR_DEVICE_STATE: Sensor("Device State", None, 16, PdoType.TYPE_CN_UINT8),
    17: Sensor("sensor_17", None, 17, PdoType.TYPE_CN_UINT8),
    SENSOR_CHANGING_FILTERS: Sensor("Changing filters", None, 18, PdoType.TYPE_CN_UINT8),
    33: Sensor("sensor_33", None, 33, PdoType.TYPE_CN_UINT8),
    35: Sensor("sensor_35", None, 35, PdoType.TYPE_CN_UINT8),
    36: Sensor("sensor_36", None, 36, PdoType.TYPE_CN_UINT8),
    37: Sensor("sensor_37", None, 37, PdoType.TYPE_CN_UINT8),
    40: Sensor("sensor_40", None, 40, PdoType.TYPE_CN_UINT8),
    42: Sensor("sensor_42", None, 42, PdoType.TYPE_CN_UINT8),
    SENSOR_OPERATING_MODE_2: Sensor("Operating Mode", None, 49, PdoType.TYPE_CN_UINT8),
    50: Sensor("sensor_50", None, 50, PdoType.TYPE_CN_UINT8),
    51: Sensor("sensor_51", None, 51, PdoType.TYPE_CN_UINT8),
    52: Sensor("sensor_52", None, 52, PdoType.TYPE_CN_UINT8),
    53: Sensor("sensor_53", None, 53, PdoType.TYPE_CN_UINT8),
    SENSOR_FAN_MODE_SUPPLY_2: Sensor("Supply Fan Mode", None, 54, PdoType.TYPE_CN_UINT8),
    SENSOR_FAN_MODE_EXHAUST_2: Sensor("Exhaust Fan Mode", None, 55, PdoType.TYPE_CN_UINT8),
    SENSOR_OPERATING_MODE: Sensor("Operating Mode", None, 56, PdoType.TYPE_CN_UINT8),
    57: Sensor("sensor_57", None, 57, PdoType.TYPE_CN_UINT8),
    58: Sensor("sensor_58", None, 58, PdoType.TYPE_CN_UINT8),
    SENSOR_FAN_SPEED_MODE: Sensor("Fan Speed", None, 65, PdoType.TYPE_CN_UINT8),
    SENSOR_BYPASS_ACTIVATION_STATE: Sensor("Bypass Activation State", None, 66, PdoType.TYPE_CN_UINT8),
    SENSOR_PROFILE_TEMPERATURE: Sensor("Temperature Profile Mode", None, 67, PdoType.TYPE_CN_UINT8),
    68: Sensor("sensor_68", None, 68, PdoType.TYPE_CN_UINT8),
    69: Sensor("sensor_69", None, 69, PdoType.TYPE_CN_UINT8),
    SENSOR_FAN_MODE_SUPPLY: Sensor("Supply Fan Mode", None, 70, PdoType.TYPE_CN_UINT8),
    SENSOR_FAN_MODE_EXHAUST: Sensor("Exhaust Fan Mode", None, 71, PdoType.TYPE_CN_UINT8),
    72: Sensor("sensor_72", None, 72, PdoType.TYPE_CN_UINT8),
    73: Sensor("sensor_73", None, 73, PdoType.TYPE_CN_UINT8),
    74: Sensor("sensor_74", None, 74, PdoType.TYPE_CN_UINT8),
    SENSOR_NEXT_CHANGE_FAN: Sensor("Fan Speed Next Change", UNIT_SECONDS, 81, PdoType.TYPE_CN_UINT32),
    SENSOR_NEXT_CHANGE_BYPASS: Sensor("Bypass Next Change", UNIT_SECONDS, 82, PdoType.TYPE_CN_UINT32),
    SENSOR_NEXT_CHANGE_COMFOCOOL: Sensor("ComfoCool Next Change", UNIT_SECONDS, 85, PdoType.TYPE_CN_UINT32),
    SENSOR_NEXT_CHANGE_FAN_SUPPLY: Sensor("Supply Fan Next Change", UNIT_SECONDS, 86, PdoType.TYPE_CN_UINT32),
    SENSOR_NEXT_CHANGE_FAN_EXHAUST: Sensor("Exhaust Fan Next Change", UNIT_SECONDS, 87, PdoType.TYPE_CN_UINT32),
    88: Sensor("sensor_88", None, 88, PdoType.TYPE_CN_UINT32),
    89: Sensor("sensor_89", None, 89, PdoType.TYPE_CN_UINT32),
    90: Sensor("sensor_90", None, 90, PdoType.TYPE_CN_UINT32),
    96: Sensor("sensor_96", None, 96, PdoType.TYPE_CN_BOOL, bool),
    115: Sensor("sensor_115", None, 115, PdoType.TYPE_CN_BOOL, bool),
    116: Sensor("sensor_116", None, 116, PdoType.TYPE_CN_BOOL, bool),
    SENSOR_FAN_EXHAUST_DUTY: Sensor("Exhaust Fan Duty", UNIT_PERCENT, 117, PdoType.TYPE_CN_UINT8),
    SENSOR_FAN_SUPPLY_DUTY: Sensor("Supply Fan Duty", UNIT_PERCENT, 118, PdoType.TYPE_CN_UINT8),
    SENSOR_FAN_EXHAUST_FLOW: Sensor("Exhaust Fan Flow", UNIT_M3H, 119, PdoType.TYPE_CN_UINT16),
    SENSOR_FAN_SUPPLY_FLOW: Sensor("Supply Fan Flow", UNIT_M3H, 120, PdoType.TYPE_CN_UINT16),
    SENSOR_FAN_EXHAUST_SPEED: Sensor("Exhaust Fan Speed", UNIT_RPM, 121, PdoType.TYPE_CN_UINT16),
    SENSOR_FAN_SUPPLY_SPEED: Sensor("Supply Fan Speed", UNIT_RPM, 122, PdoType.TYPE_CN_UINT16),
    SENSOR_POWER_USAGE: Sensor("Power Usage", UNIT_WATT, 128, PdoType.TYPE_CN_UINT16),
    SENSOR_POWER_USAGE_TOTAL_YEAR: Sensor("Power Usage (year)", UNIT_KWH, 129, PdoType.TYPE_CN_UINT16),
    SENSOR_POWER_USAGE_TOTAL: Sensor("Power Usage (total)", UNIT_KWH, 130, PdoType.TYPE_CN_UINT16),
    SENSOR_PREHEATER_POWER_TOTAL_YEAR: Sensor("Preheater Power Usage (year)", UNIT_KWH, 144, PdoType.TYPE_CN_UINT16),
    SENSOR_PREHEATER_POWER_TOTAL: Sensor("Preheater Power Usage (total)", UNIT_KWH, 145, PdoType.TYPE_CN_UINT16),
    SENSOR_PREHEATER_POWER: Sensor("Preheater Power Usage", UNIT_WATT, 146, PdoType.TYPE_CN_UINT16),
    SENSOR_RF_PAIRING_MODE: Sensor("RF Pairing Mode", None, 176, PdoType.TYPE_CN_UINT8),
    SENSOR_DAYS_TO_REPLACE_FILTER: Sensor("Days remaining to replace the filter", UNIT_DAYS, 192, PdoType.TYPE_CN_UINT16),
    SENSOR_UNIT_TEMPERATURE: Sensor("Device Temperature Unit", None, 208, PdoType.TYPE_CN_UINT8, lambda x: "celcius" if x == 0 else "farenheit"),
    SENSOR_RMOT: Sensor("Running Mean Outdoor Temperature (RMOT)", UNIT_CELCIUS, 209, PdoType.TYPE_CN_INT16, _t10),
    SENSOR_SEASON_HEATING_ACTIVE: Sensor("Heating Season is active", None, 210, PdoType.TYPE_CN_BOOL, bool),
    SENSOR_SEASON_COOLING_ACTIVE: Sensor("Cooling Season is active", None, 211, PdoType.TYPE_CN_BOOL, bool),
    SENSOR_TARGET_TEMPERATURE: Sensor("Target Temperature", UNIT_CELCIUS, 212, PdoType.TYPE_CN_INT16, _t10),
    SENSOR_AVOIDED_HEATING: Sensor("Avoided Heating Power Usage", UNIT_WATT, 213, PdoType.TYPE_CN_UINT16),
    SENSOR_AVOIDED_HEATING_TOTAL_YEAR: Sensor("Avoided Heating Power Usage (year)", UNIT_KWH, 214, PdoType.TYPE_CN_UINT16),
    SENSOR_AVOIDED_HEATING_TOTAL: Sensor("Avoided Heating Power Usage (total)", UNIT_KWH, 215, PdoType.TYPE_CN_UINT16),
    SENSOR_AVOIDED_COOLING: Sensor("Avoided Cooling Power Usage", UNIT_WATT, 216, PdoType.TYPE_CN_UINT16),
    SENSOR_AVOIDED_COOLING_TOTAL_YEAR: Sensor("Avoided Cooling Power Usage (year)", UNIT_KWH, 217, PdoType.TYPE_CN_UINT16),
    SENSOR_AVOIDED_COOLING_TOTAL: Sensor("Avoided Cooling Power Usage (total)", UNIT_KWH, 218, PdoType.TYPE_CN_UINT16),
    219: Sensor("sensor_219", None, 219, PdoType.TYPE_CN_UINT16),
    SENSOR_TEMPERATURE_OUTDOOR_PREHEATED: Sensor("Outdoor Air Temperature (preheated)", UNIT_CELCIUS, 220, PdoType.TYPE_CN_INT16, _t10),
    SENSOR_TEMPERATURE_SUPPLY: Sensor("Supply Air Temperature", UNIT_CELCIUS, 221, PdoType.TYPE_CN_INT16, _t10),
    SENSOR_UNIT_AIRFLOW: Sensor("Device Airflow Unit", None, 224, PdoType.TYPE_CN_UINT8, lambda x: "m3ph" if x == 3 else "lps"),
    SENSOR_COMFORTCONTROL_MODE: Sensor("Sensor based ventilation mode", None, 225, PdoType.TYPE_CN_UINT8),
    SENSOR_FAN_SPEED_MODE_MODULATED: Sensor("Fan Speed (modulated)", None, 226, PdoType.TYPE_CN_UINT16),
    SENSOR_BYPASS_STATE: Sensor("Bypass State", UNIT_PERCENT, 227, PdoType.TYPE_CN_UINT8),
    SENSOR_FROSTPROTECTION_UNBALANCE: Sensor("frostprotection_unbalance", None, 228, PdoType.TYPE_CN_UINT8),
    229: Sensor("sensor_229", None, 229, PdoType.TYPE_CN_BOOL, bool),
    SENSOR_AIRFLOW_CONSTRAINTS: Sensor("Airflow constraints", None, 230, PdoType.TYPE_CN_INT64, calculate_airflow_constraints),
    256: Sensor("sensor_256", None, 256, PdoType.TYPE_CN_UINT8),
    257: Sensor("sensor_257", None, 257, PdoType.TYPE_CN_UINT8),
    SENSOR_TEMPERATURE_EXTRACT: Sensor("Extract Air Temperature", UNIT_CELCIUS, 274, PdoType.TYPE_CN_INT16, _t10),
    SENSOR_TEMPERATURE_EXHAUST: Sensor("Exhaust Air Temperature", UNIT_CELCIUS, 275, PdoType.TYPE_CN_INT16, _t10),
    SENSOR_TEMPERATURE_OUTDOOR: Sensor("Outdoor Air Temperature", UNIT_CELCIUS, 276, PdoType.TYPE_CN_INT16, _t10),
    SENSOR_TEMPERATURE_OUTDOOR_PREHEATED_2: Sensor("Outdoor Air Temperature (preheated, alt)", UNIT_CELCIUS, 277, PdoType.TYPE_CN_INT16, _t10),
    SENSOR_TEMPERATURE_SUPPLY_PREHEATED: Sensor("Supply Air Temperature (preheated)", UNIT_CELCIUS, 278, PdoType.TYPE_CN_INT16, _t10),
    SENSOR_HUMIDITY_EXTRACT: Sensor("Extract Air Humidity", UNIT_PERCENT, 290, PdoType.TYPE_CN_UINT8),
    SENSOR_HUMIDITY_EXHAUST: Sensor("Exhaust Air Humidity", UNIT_PERCENT, 291, PdoType.TYPE_CN_UINT8),
    SENSOR_HUMIDITY_OUTDOOR: Sensor("Outdoor Air Humidity", UNIT_PERCENT, 292, PdoType.TYPE_CN_UINT8),
    SENSOR_HUMIDITY_AFTER_PREHEATER: Sensor("Outdoor Air Humidity (after preheater)", UNIT_PERCENT, 293, PdoType.TYPE_CN_UINT8),
    SENSOR_HUMIDITY_SUPPLY: Sensor("Supply Air Humidity", UNIT_PERCENT, 294, PdoType.TYPE_CN_UINT8),
    321: Sensor("sensor_321", None, 321, PdoType.TYPE_CN_UINT16),
    325: Sensor("sensor_325", None, 325, PdoType.TYPE_CN_UINT16),
    328: Sensor("sensor_328", None, 328, PdoType.TYPE_CN_UINT16),
    330: Sensor("sensor_330", None, 330, PdoType.TYPE_CN_UINT16),
    337: Sensor("sensor_337", None, 337, PdoType.TYPE_CN_UINT32),
    SENSOR_BYPASS_OVERRIDE: Sensor("Bypass Override", None, 338, PdoType.TYPE_CN_UINT32),
    341: Sensor("sensor_341", None, 341, PdoType.TYPE_CN_UINT32),
    SENSOR_FAN_MODE_SUPPLY_3: Sensor("Supply Fan Mode", None, 342, PdoType.TYPE_CN_UINT32),
    SENSOR_FAN_MODE_EXHAUST_3: Sensor("Exhaust Fan Mode", None, 343, PdoType.TYPE_CN_UINT32),
    344: Sensor("sensor_344", None, 344, PdoType.TYPE_CN_UINT32),
    345: Sensor("sensor_345", None, 345, PdoType.TYPE_CN_UINT32),
    346: Sensor("sensor_346", None, 346, PdoType.TYPE_CN_UINT32),
    SENSOR_ANALOG_INPUT_1: Sensor("Analog Input 1", UNIT_VOLT, 369, PdoType.TYPE_CN_UINT8, _t10),
    SENSOR_ANALOG_INPUT_2: Sensor("Analog Input 2", UNIT_VOLT, 370, PdoType.TYPE_CN_UINT8, _t10),
    SENSOR_ANALOG_INPUT_3: Sensor("Analog Input 3", UNIT_VOLT, 371, PdoType.TYPE_CN_UINT8, _t10),
    SENSOR_ANALOG_INPUT_4: Sensor("Analog Input 4", UNIT_VOLT, 372, PdoType.TYPE_CN_UINT8, _t10),
    384: Sensor("sensor_384", None, 384, PdoType.TYPE_CN_INT16, _t10),
    386: Sensor("sensor_386", None, 386, PdoType.TYPE_CN_BOOL, bool),
    400: Sensor("sensor_400", None, 400, PdoType.TYPE_CN_INT16, _t10),
    401: Sensor("sensor_401", None, 401, PdoType.TYPE_CN_UINT8),
    402: Sensor("sensor_402", None, 402, PdoType.TYPE_CN_BOOL, bool),
    SENSOR_COMFOFOND_TEMP_OUTDOOR: Sensor("ComfoFond Outdoor Air Temperature", UNIT_CELCIUS, 416, PdoType.TYPE_CN_INT16, _t10),
    SENSOR_COMFOFOND_TEMP_GROUND: Sensor("ComfoFond Ground Temperature", UNIT_CELCIUS, 417, PdoType.TYPE_CN_INT16, _t10),
    SENSOR_COMFOFOND_GHE_STATE: Sensor("ComfoFond GHE State Percentage", UNIT_PERCENT, 418, PdoType.TYPE_CN_UINT8),
    SENSOR_COMFOFOND_GHE_PRESENT: Sensor("ComfoFond GHE Present", None, 419, PdoType.TYPE_CN_BOOL, bool),
    513: Sensor("sensor_513", None, 513, PdoType.TYPE_CN_UINT16),
    514: Sensor("sensor_514", None, 514, PdoType.TYPE_CN_UINT16),
    515: Sensor("sensor_515", None, 515, PdoType.TYPE_CN_UINT16),
    516: Sensor("sensor_516", None, 516, PdoType.TYPE_CN_UINT16),
    517: Sensor("sensor_517", None, 517, PdoType.TYPE_CN_UINT8),
    518: Sensor("sensor_518", None, 518, PdoType.TYPE_CN_UINT8),
    519: Sensor("sensor_519", None, 519, PdoType.TYPE_CN_UINT8),
    520: Sensor("sensor_520", None, 520, PdoType.TYPE_CN_UINT8),
    521: Sensor("sensor_521", None, 521, PdoType.TYPE_CN_INT16),
    522: Sensor("sensor_522", None, 522, PdoType.TYPE_CN_INT16),
    523: Sensor("sensor_523", None, 523, PdoType.TYPE_CN_INT16),
    524: Sensor("sensor_524", None, 524, PdoType.TYPE_CN_UINT8),
    SENSOR_COMFOCOOL_STATE: Sensor("ComfoCool State", None, 784, PdoType.TYPE_CN_UINT8),
    785: Sensor("sensor_785", None, 785, PdoType.TYPE_CN_BOOL, bool),
    801: Sensor("sensor_801", UNIT_CELCIUS, 801, PdoType.TYPE_CN_INT16, _t10),
    SENSOR_COMFOCOOL_CONDENSOR_TEMP: Sensor("ComfoCool Condensor Temperature", UNIT_CELCIUS, 802, PdoType.TYPE_CN_INT16, _t10),
    803: Sensor("sensor_803", UNIT_CELCIUS, 803, PdoType.TYPE_CN_INT16, _t10),
    1024: Sensor("sensor_1024", None, 1024, PdoType.TYPE_CN_UINT16),
    1025: Sensor("sensor_1025", None, 1025, PdoType.TYPE_CN_UINT16),
    1026: Sensor("sensor_1026", None, 1026, PdoType.TYPE_CN_UINT16),
    1027: Sensor("sensor_1027", None, 1027, PdoType.TYPE_CN_UINT16),
    1028: Sensor("sensor_1028", None, 1028, PdoType.TYPE_CN_UINT16),
    1029: Sensor("sensor_1029", None, 1029, PdoType.TYPE_CN_UINT16),
    1030: Sensor("sensor_1030", None, 1030, PdoType.TYPE_CN_UINT16),
    1031: Sensor("sensor_1031", None, 1031, PdoType.TYPE_CN_UINT16),
    1056: Sensor("sensor_1056", None, 1056, PdoType.TYPE_CN_INT16),
    1124: Sensor("sensor_1124", None, 1124, PdoType.TYPE_CN_INT16),
    1125: Sensor("sensor_1125", None, 1125, PdoType.TYPE_CN_INT16),
    1126: Sensor("sensor_1126", None, 1126, PdoType.TYPE_CN_INT16),
    1127: Sensor("sensor_1127", None, 1127, PdoType.TYPE_CN_INT16),
    1281: Sensor("sensor_1281", None, 1281, PdoType.TYPE_CN_UINT16),
    1282: Sensor("sensor_1282", None, 1282, PdoType.TYPE_CN_UINT16),
    1283: Sensor("sensor_1283", None, 1283, PdoType.TYPE_CN_UINT16),
    1284: Sensor("sensor_1284", None, 1284, PdoType.TYPE_CN_UINT16),
    1285: Sensor("sensor_1285", None, 1285, PdoType.TYPE_CN_UINT16),
    1286: Sensor("sensor_1286", None, 1286, PdoType.TYPE_CN_UINT16),
    1287: Sensor("sensor_1287", None, 1287, PdoType.TYPE_CN_UINT16),
    1288: Sensor("sensor_1288", None, 1288, PdoType.TYPE_CN_UINT16),
    1297: Sensor("sensor_1297", None, 1297, PdoType.TYPE_CN_BOOL, bool),
    1298: Sensor("sensor_1298", None, 1298, PdoType.TYPE_CN_BOOL, bool),
    1299: Sensor("sensor_1299", None, 1299, PdoType.TYPE_CN_BOOL, bool),
    1300: Sensor("sensor_1300", None, 1300, PdoType.TYPE_CN_BOOL, bool),
    1301: Sensor("sensor_1301", None, 1301, PdoType.TYPE_CN_BOOL, bool),
    1302: Sensor("sensor_1302", None, 1302, PdoType.TYPE_CN_BOOL, bool),
    1303: Sensor("sensor_1303", None, 1303, PdoType.TYPE_CN_BOOL, bool),
    1304: Sensor("sensor_1304", None, 1304, PdoType.TYPE_CN_BOOL, bool),
}

# IDs of PDOs whose meaning is not (yet) documented. Consumers can use this to
# surface them as disabled-by-default diagnostic entities.
SENSORS_DEBUG = frozenset(sensor_id for sensor_id, sensor in SENSORS.items() if sensor.name.startswith("sensor_"))

# IDs of PDOs with a known meaning (the complement of SENSORS_DEBUG).
SENSORS_STANDARD = frozenset(SENSORS) - SENSORS_DEBUG
