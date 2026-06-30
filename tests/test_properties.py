"""Tests for the RMI property getters/setters added to ComfoConnect."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from aiocomfoconnect.comfoconnect import ComfoConnect
from aiocomfoconnect.exceptions import ComfoConnectRmiError

LOCAL_UUID = "00000000000000000000000000000001"


@pytest.fixture
def comfoconnect():
    """Create a ComfoConnect instance for testing."""
    return ComfoConnect("192.168.1.100", LOCAL_UUID, sensor_callback=Mock(), alarm_callback=Mock(), sensor_delay=0, connect_timeout=1)


def _resp(message: bytes):
    response = Mock()
    response.message = message
    return response


@pytest.mark.asyncio
async def test_get_firmware_version_decoded(comfoconnect):
    """Firmware version is decoded into a human-readable string."""
    with patch.object(comfoconnect, "cmd_rmi_request", AsyncMock(return_value=_resp((0x00541040).to_bytes(4, "little")))):
        assert await comfoconnect.get_firmware_version() == "U5.260.64"


@pytest.mark.asyncio
async def test_get_serial_number_string(comfoconnect):
    """String properties are decoded and null-trimmed."""
    with patch.object(comfoconnect, "cmd_rmi_request", AsyncMock(return_value=_resp(b"BEA009999999999\x00"))):
        assert await comfoconnect.get_serial_number() == "BEA009999999999"


@pytest.mark.asyncio
async def test_get_orientation(comfoconnect):
    """Orientation maps 0/1 to left/right."""
    with patch.object(comfoconnect, "cmd_rmi_request", AsyncMock(return_value=_resp(bytes([0])))):
        assert await comfoconnect.get_orientation() == "left"
    with patch.object(comfoconnect, "cmd_rmi_request", AsyncMock(return_value=_resp(bytes([1])))):
        assert await comfoconnect.get_orientation() == "right"


@pytest.mark.asyncio
async def test_get_target_temperature(comfoconnect):
    """Target temperature is decoded as tenths of a degree."""
    with patch.object(comfoconnect, "cmd_rmi_request", AsyncMock(return_value=_resp((230).to_bytes(2, "little", signed=True)))):
        assert await comfoconnect.get_target_temperature("warm") == 23.0


@pytest.mark.asyncio
async def test_set_target_temperature_encodes_value(comfoconnect):
    """Setting a target temperature multiplies by 10 and addresses the right property."""
    with patch.object(comfoconnect, "cmd_rmi_request", AsyncMock(return_value=_resp(b""))) as mock_rmi:
        await comfoconnect.set_target_temperature("cool", 19.0)
        sent = bytes(mock_rmi.call_args[0][0])
        # 0x03 = set, 0x1D = TEMPHUMCONTROL, 0x01 = subunit, 0x0C = cooling target, then INT16 190 little-endian
        assert sent == bytes([0x03, 0x1D, 0x01, 0x0C]) + (190).to_bytes(2, "little", signed=True)


@pytest.mark.asyncio
async def test_invalid_profile_raises(comfoconnect):
    """An unknown profile raises ValueError."""
    with pytest.raises(ValueError):
        await comfoconnect.get_target_temperature("tropical")


@pytest.mark.asyncio
async def test_get_unbalance(comfoconnect):
    """Unbalance is decoded as tenths of a percent and signed."""
    with patch.object(comfoconnect, "cmd_rmi_request", AsyncMock(return_value=_resp((-99).to_bytes(2, "little", signed=True)))):
        assert await comfoconnect.get_unbalance() == -9.9


@pytest.mark.asyncio
async def test_get_node_info_best_effort(comfoconnect):
    """get_node_info omits properties that fail rather than raising."""

    async def flaky(*_args, **_kwargs):
        raise ComfoConnectRmiError("not gettable")

    with patch.object(comfoconnect, "cmd_rmi_request", AsyncMock(side_effect=flaky)):
        assert await comfoconnect.get_node_info() == {}
