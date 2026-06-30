"""Tests for the sensor (PDO) catalog."""

import re
from pathlib import Path

from aiocomfoconnect import sensors
from aiocomfoconnect.const import PdoType

DOC = Path(__file__).resolve().parent.parent / "docs" / "PROTOCOL-PDO.md"

# Map the CN_* type names from PROTOCOL-PDO.md to PdoType values.
TYPE_NAME_TO_PDO = {
    "CN_BOOL": PdoType.TYPE_CN_BOOL,
    "CN_UINT8": PdoType.TYPE_CN_UINT8,
    "CN_UINT16": PdoType.TYPE_CN_UINT16,
    "CN_UINT32": PdoType.TYPE_CN_UINT32,
    "CN_INT8": PdoType.TYPE_CN_INT8,
    "CN_INT16": PdoType.TYPE_CN_INT16,
    "CN_INT64": PdoType.TYPE_CN_INT64,
    "CN_STRING": PdoType.TYPE_CN_STRING,
    "CN_TIME": PdoType.TYPE_CN_TIME,
    "CN_VERSION": PdoType.TYPE_CN_VERSION,
}


def _parse_doc():
    """Parse the 'Overview of known sensors' table from PROTOCOL-PDO.md."""
    rows = {}
    in_overview = False
    for line in DOC.read_text(encoding="utf-8").splitlines():
        if line.startswith("# Overview of known sensors"):
            in_overview = True
            continue
        if not in_overview:
            continue
        m = re.match(r"\|\s*(\d+)\s*\|\s*([A-Z0-9_]*)\s*\|", line)
        if m:
            rows[int(m.group(1))] = m.group(2) or None
    return rows


def test_every_documented_pdo_is_present():
    """Every PDO documented in PROTOCOL-PDO.md must exist in SENSORS."""
    doc = _parse_doc()
    assert doc, "Failed to parse PROTOCOL-PDO.md"
    missing = sorted(set(doc) - set(sensors.SENSORS))
    assert not missing, f"Documented PDOs missing from SENSORS: {missing}"


def test_no_extra_sensors_beyond_doc():
    """SENSORS should not contain PDOs that are not documented."""
    doc = _parse_doc()
    extra = sorted(set(sensors.SENSORS) - set(doc))
    assert not extra, f"SENSORS contains undocumented PDOs: {extra}"


def test_sensor_key_matches_id():
    """Each SENSORS key must equal the Sensor.id it maps to."""
    mismatches = [key for key, sensor in sensors.SENSORS.items() if key != sensor.id]
    assert not mismatches, f"Key/id mismatches: {mismatches}"


# PDOs where the library intentionally diverges from the documented type.
# 212 (target temperature) is documented as CN_UINT8 but has always been decoded
# as a signed INT16 tenths-of-a-degree value; keeping that for backward compat.
TYPE_EXCEPTIONS = {212}


def test_sensor_types_match_doc():
    """Where the doc declares a type, the Sensor.type should match it."""
    doc = _parse_doc()
    mismatches = []
    for pdid, type_name in doc.items():
        if not type_name or pdid in TYPE_EXCEPTIONS:  # blank type column or known exception
            continue
        expected = TYPE_NAME_TO_PDO[type_name]
        if sensors.SENSORS[pdid].type != expected:
            mismatches.append((pdid, type_name, sensors.SENSORS[pdid].type))
    assert not mismatches, f"Type mismatches vs doc: {mismatches}"


def test_debug_set_is_complement_of_standard():
    """SENSORS_DEBUG and SENSORS_STANDARD partition SENSORS."""
    assert sensors.SENSORS_DEBUG | sensors.SENSORS_STANDARD == set(sensors.SENSORS)
    assert not (sensors.SENSORS_DEBUG & sensors.SENSORS_STANDARD)
    # Known sensors should not be flagged as debug.
    assert sensors.SENSOR_TEMPERATURE_EXTRACT in sensors.SENSORS_STANDARD
    assert sensors.SENSOR_POWER_USAGE in sensors.SENSORS_STANDARD
    # Unknown sensors should be flagged as debug.
    assert 1024 in sensors.SENSORS_DEBUG


def test_temperature_scaling():
    """INT16 temperature sensors decode tenths of a degree."""
    assert sensors.SENSORS[sensors.SENSOR_TEMPERATURE_EXTRACT].value_fn(171) == 17.1
    assert sensors.SENSORS[sensors.SENSOR_RMOT].value_fn(117) == 11.7
    # Newly-relabelled preheated temps decode the same way.
    assert sensors.SENSORS[sensors.SENSOR_TEMPERATURE_OUTDOOR_PREHEATED].value_fn(75) == 7.5
    assert sensors.SENSORS[sensors.SENSOR_TEMPERATURE_SUPPLY_PREHEATED].value_fn(184) == 18.4
