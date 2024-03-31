from datetime import datetime

import pytest

from src.beintelli_platform_python_sdk_eliasinguanta.measurement_list import MeasurementList, MeasurementAttribute, NumberAttribute
from src.beintelli_platform_python_sdk_eliasinguanta.user import User
from tests.setup import get_authenticated_user


@pytest.mark.asyncio
async def test_filter_weather():
    try:
        user: User = await (await get_authenticated_user())

        #request data
        my_list: MeasurementList = await (
            await user.data.get_weather_data(
                datetime.fromisocalendar(2020, 1, 1), datetime.fromisocalendar(2024, 1, 1)
        ))
        length = len(my_list)
        assert length == 1800

        #filter data second time by tempc between 10 to 30
        filtered_list1 : MeasurementList = await  (await my_list.filtered_by_range(NumberAttribute.TEMPC,15,20))
        length = len(filtered_list1)
        assert length == 225

        #filter by absolute_humidity between 10 and 15
        filtered_list2 : MeasurementList = await  (await filtered_list1.filtered_by_range(NumberAttribute.ABSOLUTE_HUMIDITY,10,15))
        length = len(filtered_list2)
        assert length == 161

        #filter by air_pressure between 1020.1 and 1020.3
        filtered_list3 : MeasurementList = await  (await filtered_list2.filtered_by_range(NumberAttribute.AIR_PRESSURE,1020.1,1020.3))
        length = len(filtered_list3)
        assert length == 2

        #filter by absolute_precipitation=120.27999877929688
        filtered_list4 : MeasurementList = await  (await filtered_list3.filtered_by_value(MeasurementAttribute.ABSOLUTE_PRECIPITATION,120.27999877929688))
        length = len(filtered_list4)
        assert length == 2

        #filter by weather_id=2
        filtered_list5 : MeasurementList = await  (await filtered_list4.filtered_by_value(MeasurementAttribute.WEATHER_ID,2))
        length = len(filtered_list5)
        assert length == 1

    except Exception:
        assert False

@pytest.mark.asyncio
async def test_filter_road():
    try:
        user: User = await (await get_authenticated_user())

        #request data
        my_list: MeasurementList = await (
            await user.data.get_road_data(
                datetime.fromisocalendar(2020, 1, 1), datetime.fromisocalendar(2024, 1, 1)
        ))
        length = len(my_list)
        assert length == 1800

        #filter data second time by friction between 0.8 to 1
        filtered_list1 : MeasurementList = await  (await my_list.filtered_by_range(NumberAttribute.FRICTION,0.8,1))
        length = len(filtered_list1)
        assert length == 1730

        #filter data second time by road_surface_temperature_c between 32 to 40
        filtered_list2 : MeasurementList = await  (await filtered_list1.filtered_by_range(NumberAttribute.ROAD_SURFACE_TEMPERATURE_C,32,40))
        length = len(filtered_list2)
        assert length == 293

        #filter data second time by road_id == 4
        filtered_list3 : MeasurementList = await  (await filtered_list2.filtered_by_value(MeasurementAttribute.ROAD_ID,4))
        length = len(filtered_list3)
        assert length == 1


    except Exception:
        assert False