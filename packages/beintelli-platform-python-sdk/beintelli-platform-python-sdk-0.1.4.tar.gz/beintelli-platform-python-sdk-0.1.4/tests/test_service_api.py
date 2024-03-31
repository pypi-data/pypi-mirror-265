"""Contains unittest for functions provided by the data api"""

import asyncio
from datetime import datetime
import pytest

from src.beintelli_platform_python_sdk_eliasinguanta.user import User
from src.beintelli_platform_python_sdk_eliasinguanta.utils.types import RosbagInfo
from tests.setup import get_authenticated_user


@pytest.mark.asyncio
async def test_weather_sheet():
    """tests User.service.get_weather_sheet(...)"""
    try:
        user = await (await get_authenticated_user())
        res: bytes = await (
            await user.service.get_weather_sheet(
                datetime.fromisocalendar(2020, 1, 1), datetime.fromisocalendar(2024, 1, 1)
        ))
        assert len(res) > 0

    except Exception:
        assert False

@pytest.mark.asyncio
async def test_parking_sheet():
    """tests User.service.get_parking_sheet(...)"""
    try:
        user = await (await get_authenticated_user())
        res: bytes = await (
            await user.service.get_parking_sheet(
                datetime.fromisocalendar(2020, 1, 1), datetime.fromisocalendar(2024, 1, 1)
        ))
        assert len(res) > 0

    except Exception:
        assert False

@pytest.mark.asyncio
async def test_road_sheet():
    """tests User.service.get_road_sheet(...)"""
    try:
        user = await (await get_authenticated_user())
        res: bytes = await (
            await user.service.get_road_sheet(
                datetime.fromisocalendar(2020, 1, 1), datetime.fromisocalendar(2024, 1, 1)
        ))
        assert len(res) > 0

    except Exception:
        assert False

@pytest.mark.asyncio
async def test_detection_sheet():
    """tests User.service.get_detection_sheet(...)"""
    try:
        user = await (await get_authenticated_user())
        res: bytes = await (
            await user.service.get_detection_sheet(
                datetime.fromisocalendar(2020, 1, 1), datetime.fromisocalendar(2024, 1, 1)
        ))
        assert len(res) > 0

    except Exception:
        assert False

@pytest.mark.asyncio
async def test_get_rosbags():
    """tests User.service.get_rosbags(...)"""
    try:
        user = await (await get_authenticated_user())
        res: list[RosbagInfo] = await (await user.service.get_rosbags())
        assert len(res) > 0

    except Exception:
        assert False

@pytest.mark.asyncio
async def test_get_converted_rosbags():
    """tests User.service.get_converted_rosbags(...)"""
    try:
        user = await (await get_authenticated_user())
        res: list[RosbagInfo] = await (await user.service.get_converted_rosbags())
        assert len(res) > 0

    except Exception:
        assert False

@pytest.mark.asyncio
async def test_get_rosbag():
    """tests User.service.get_rosbags(...)"""
    try:
        user = await (await get_authenticated_user())
        filename = "x"
        await (await user.service.get_rosbag(filename))
        assert True

    except Exception:
        assert False
