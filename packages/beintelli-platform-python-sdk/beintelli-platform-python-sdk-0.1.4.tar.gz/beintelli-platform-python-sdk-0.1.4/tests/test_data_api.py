"""Contains unittest for functions provided by the data api"""

import asyncio
from datetime import datetime

import pytest

from tests.setup import get_authenticated_user


@pytest.mark.asyncio
async def test_rsu():
    """tests User.data.get_rsu_data()"""
    try:
        user = await (await get_authenticated_user())
        res = await (await user.data.get_rsu_data())
        assert len(res) > 0

    except Exception:
        assert False

@pytest.mark.asyncio
async def test_weather():
    """tests User.data.get_weather_data(...)"""

    try:
        user = await (await get_authenticated_user())
        res = await (
            await user.data.get_weather_data(
                datetime.fromisocalendar(2020, 1, 1), datetime.fromisocalendar(2024, 1, 1)
        ))
        assert len(res) > 0

    except Exception:
        assert False

@pytest.mark.asyncio
async def test_parkinglot_availability():
    """tests User.data.get_parkinglot_availability(...)"""
    try:
        user = await (await get_authenticated_user())
        gap_id = "da5b992e-8893-4be9-a27a-7cd9cc97ced0"
        res = await (await user.data.get_parkinglot_availability(gap_id))
        assert len(res) > 0

    except Exception:
        assert False

@pytest.mark.asyncio
async def test_parkinglot_information():
    """tests User.data.get_parkinglot_information(...)"""
    try:
        user = await (await get_authenticated_user())
        gap_id = "da5b992e-8893-4be9-a27a-7cd9cc97ced0"
        res = await (await user.data.get_parkinglot_information(gap_id))
        assert len(res) > 0

    except Exception:
        assert False

@pytest.mark.asyncio
async def test_hdmap():
    """tests User.data.get_hdmap(...)"""
    try:
        user = await (await get_authenticated_user())
        filename = "BeIntelli_HD_Map_reduced_v_1.osm"
        res = await (await user.data.get_hdmap(filename))
        assert len(res) > 0

    except Exception:
        assert False

@pytest.mark.asyncio
async def test_detection():
    """tests User.data.get_detection_data(...)"""
    try:
        user = await (await get_authenticated_user())
        res = await (
            await user.data.get_detection_data(
                datetime.fromisocalendar(2020, 1, 1), datetime.fromisocalendar(2024, 1, 1)
        ))
        assert len(res) >= 0

    except Exception:
        assert False

@pytest.mark.asyncio
async def test_parking():
    """tests User.data.get_parking_data(...)"""
    try:
        user = await (await get_authenticated_user())
        res = await (
            await user.data.get_parking_data(
                datetime.fromisocalendar(2020, 1, 1), datetime.fromisocalendar(2024, 1, 1)
        ))
        assert len(res) >= 0

    except Exception:
        assert False

@pytest.mark.asyncio
async def test_road():
    """tests User.data.get_road_data(...)"""
    try:
        user = await (await get_authenticated_user())
        res = await (
            await user.data.get_road_data(
                datetime.fromisocalendar(2020, 1, 1), datetime.fromisocalendar(2024, 1, 1)
        ))
        assert len(res) > 0

    except Exception:
        assert False

@pytest.mark.asyncio
async def test_hdmaps():
    """tests User.data.get_hdmaps(...)"""
    try:
        user = await (await get_authenticated_user())
        res = await (await user.data.get_hdmaps())
        assert len(res) > 0

    except Exception:
        assert False

@pytest.mark.asyncio
async def test_drive_data():
    """tests User.data.get_drive_data(...)"""
    try:
        user = await (await get_authenticated_user())
        res = await (
            await user.data.get_drive_data(
                datetime.fromisocalendar(2020, 1, 1), datetime.fromisocalendar(2024, 1, 1)
        ))
        assert len(res) >= 0

    except Exception:
        assert False

@pytest.mark.asyncio
async def test_route_data():
    """tests User.data.get_route_data(...)"""
    try:
        user = await (await get_authenticated_user())
        drive_id = ""  # no known drive id
        res = await (await user.data.get_route_data(drive_id))
        assert len(res) >= 0

    except Exception:
        assert False