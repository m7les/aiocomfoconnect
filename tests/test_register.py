"""Tests for ComfoConnect.register()."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from aiocomfoconnect import Bridge
from aiocomfoconnect.comfoconnect import ComfoConnect
from aiocomfoconnect.exceptions import ComfoConnectNotAllowed

LOCAL_UUID = "00000000000000000000000000000001"


@pytest.fixture
def comfoconnect():
    """Create a ComfoConnect instance for testing."""
    return ComfoConnect("192.168.1.100", LOCAL_UUID, sensor_callback=Mock(), alarm_callback=Mock(), sensor_delay=0, connect_timeout=1)


@pytest.mark.asyncio
async def test_register_already_registered(comfoconnect):
    """If the session starts cleanly, the app was already registered."""
    with (
        patch.object(Bridge, "connect", AsyncMock()),
        patch.object(Bridge, "disconnect", AsyncMock()) as mock_disconnect,
        patch.object(comfoconnect, "cmd_start_session", AsyncMock()),
        patch.object(comfoconnect, "cmd_register_app", AsyncMock()) as mock_register,
    ):
        assert await comfoconnect.register(LOCAL_UUID, "test") is True
        mock_register.assert_not_called()
        mock_disconnect.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_new_app(comfoconnect):
    """A not-allowed session start triggers registration, then a retry."""
    with (
        patch.object(Bridge, "connect", AsyncMock()),
        patch.object(Bridge, "disconnect", AsyncMock()) as mock_disconnect,
        patch.object(comfoconnect, "cmd_start_session", AsyncMock(side_effect=[ComfoConnectNotAllowed("nope"), None])),
        patch.object(comfoconnect, "cmd_register_app", AsyncMock()) as mock_register,
    ):
        assert await comfoconnect.register(LOCAL_UUID, "test", 1234) is False
        mock_register.assert_awaited_once_with(LOCAL_UUID, "test", 1234)
        # The socket is always torn down afterwards.
        mock_disconnect.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_bad_pin_disconnects(comfoconnect):
    """A wrong PIN propagates ComfoConnectNotAllowed but still disconnects."""
    with (
        patch.object(Bridge, "connect", AsyncMock()),
        patch.object(Bridge, "disconnect", AsyncMock()) as mock_disconnect,
        patch.object(comfoconnect, "cmd_start_session", AsyncMock(side_effect=ComfoConnectNotAllowed("nope"))),
        patch.object(comfoconnect, "cmd_register_app", AsyncMock(side_effect=ComfoConnectNotAllowed("bad pin"))),
    ):
        with pytest.raises(ComfoConnectNotAllowed):
            await comfoconnect.register(LOCAL_UUID, "test", 9999)
        mock_disconnect.assert_awaited_once()
