"""Containing class MeasurementList"""
import asyncio
import logging
from datetime import datetime
from enum import Enum
from numbers import Number

from .apis.measurement_api import MeasurementApi
from .utils.types import (
    DetectionData,
    Measurement,
    ParkingData,
    RoadData,
    WeatherData,
)


class MeasurementType(Enum):
    """class to differentiate between types of Attributes"""
    WEATHER = 0
    DETECTION = 1
    PARKING = 2
    ROAD = 3
    ANY = 4

class AttributeValue:
    """Wrapper class to differentiate Attribute objects with same MeasurementType"""
    _measurement_type: MeasurementType

    def __init__(self, measurement_type: MeasurementType):
        self._measurement_type = measurement_type

    def get_type(self) -> MeasurementType:
        """Simple getter

        Returns:
            MeasurementType: wrapped value
        """
        return self._measurement_type

class MeasurementAttribute(Enum):
    """Containing an attribute of type DetectionData or WeatherData or RoadData or Parkingdata"""
    WEATHER_ID = AttributeValue(MeasurementType.WEATHER)
    TEMPC = AttributeValue(MeasurementType.WEATHER)
    HUMIDITY = AttributeValue(MeasurementType.WEATHER)
    ABSOLUTE_HUMIDITY = AttributeValue(MeasurementType.WEATHER)
    AIR_PRESSURE = AttributeValue(MeasurementType.WEATHER)
    ABSOLUTE_PRECIPITATION = AttributeValue(MeasurementType.WEATHER)
    ABSOLUTE_PRECIPITATION_MM = AttributeValue(MeasurementType.WEATHER)
    DIFFERENTIAL_PRECIPITATION = AttributeValue(MeasurementType.WEATHER)
    DIFFERENTIAL_PRECIPITATION_MM = AttributeValue(MeasurementType.WEATHER)
    PRECIPITATION_INTENSITY = AttributeValue(MeasurementType.WEATHER)
    PRECIPITATION_TYPE = AttributeValue(MeasurementType.WEATHER)
    PRECIPITATION = AttributeValue(MeasurementType.WEATHER)
    WEATHER_TOPIC = AttributeValue(MeasurementType.WEATHER)

    PARKING_ID = AttributeValue(MeasurementType.PARKING)
    CUSTOM_STATE = AttributeValue(MeasurementType.PARKING)
    GAP_IDS = AttributeValue(MeasurementType.PARKING)
    NAME = AttributeValue(MeasurementType.PARKING)
    RAW_DATA_ARRIVAL = AttributeValue(MeasurementType.PARKING)
    RAW_DATA_CAR = AttributeValue(MeasurementType.PARKING)
    RAW_DATA_DEPATURE = AttributeValue(MeasurementType.PARKING)
    OCCUPIED = AttributeValue(MeasurementType.PARKING)
    RAW_REF_DATA = AttributeValue(MeasurementType.PARKING)
    REF1 = AttributeValue(MeasurementType.PARKING)
    REF2 = AttributeValue(MeasurementType.PARKING)
    VALID = AttributeValue(MeasurementType.PARKING)

    ROAD_ID = AttributeValue(MeasurementType.ROAD)
    ROAD_SURFACE_TEMPERATURE_C = AttributeValue(MeasurementType.ROAD)
    FREEZING_TEMPERATURE_NAC = AttributeValue(MeasurementType.ROAD)
    WATER_FILM_HEIGHT = AttributeValue(MeasurementType.ROAD)
    ICE_LAYER_THICKNESS = AttributeValue(MeasurementType.ROAD)
    SNOW_HEIGHT = AttributeValue(MeasurementType.ROAD)
    ICE_PERCENTAGE = AttributeValue(MeasurementType.ROAD)
    SALINE_CONCENTRATION = AttributeValue(MeasurementType.ROAD)
    FRICTION = AttributeValue(MeasurementType.ROAD)
    ROAD_CONDITION_TYPE = AttributeValue(MeasurementType.ROAD)
    MEASUREMENT_STATUS_BITS = AttributeValue(MeasurementType.ROAD)
    ROAD_CONDITION = AttributeValue(MeasurementType.ROAD)
    ROAD_TOPIC = AttributeValue(MeasurementType.ROAD)

    DETECTION_ID = AttributeValue(MeasurementType.DETECTION)
    TIMESTAMP = AttributeValue(MeasurementType.DETECTION)
    KAFKA_TOPIC = AttributeValue(MeasurementType.DETECTION)
    TYPE = AttributeValue(MeasurementType.DETECTION)
    LON = AttributeValue(MeasurementType.DETECTION)
    LAT = AttributeValue(MeasurementType.DETECTION)
    TRACK_ID = AttributeValue(MeasurementType.DETECTION)
    HEADING = AttributeValue(MeasurementType.DETECTION)
    SPEED = AttributeValue(MeasurementType.DETECTION)

    TMPSTMP_FOR_ADDING = AttributeValue(MeasurementType.ANY)

class NumberAttribute(Enum):
    """Containing an number attribute of type DetectionData or WeatherData or RoadData or Parkingdata"""

    WEATHER_ID = MeasurementAttribute.WEATHER_ID.value
    TEMPC = MeasurementAttribute.TEMPC.value
    HUMIDITY = MeasurementAttribute.HUMIDITY.value
    ABSOLUTE_HUMIDITY = MeasurementAttribute.ABSOLUTE_HUMIDITY.value
    AIR_PRESSURE = MeasurementAttribute.AIR_PRESSURE.value
    ABSOLUTE_PRECIPITATION = MeasurementAttribute.ABSOLUTE_PRECIPITATION.value
    ABSOLUTE_PRECIPITATION_MM = MeasurementAttribute.ABSOLUTE_PRECIPITATION_MM.value
    DIFFERENTIAL_PRECIPITATION = MeasurementAttribute.DIFFERENTIAL_PRECIPITATION.value
    DIFFERENTIAL_PRECIPITATION_MM = MeasurementAttribute.DIFFERENTIAL_PRECIPITATION_MM.value
    PRECIPITATION_INTENSITY = MeasurementAttribute.PRECIPITATION_INTENSITY.value
    PRECIPITATION_TYPE = MeasurementAttribute.PRECIPITATION_TYPE.value

    PARKING_ID = MeasurementAttribute.PARKING_ID.value

    ROAD_ID = MeasurementAttribute.ROAD_ID.value
    ROAD_SURFACE_TEMPERATURE_C = MeasurementAttribute.ROAD_SURFACE_TEMPERATURE_C.value
    FREEZING_TEMPERATURE_NAC = MeasurementAttribute.FREEZING_TEMPERATURE_NAC.value
    WATER_FILM_HEIGHT = MeasurementAttribute.WATER_FILM_HEIGHT.value
    ICE_LAYER_THICKNESS = MeasurementAttribute.ICE_LAYER_THICKNESS.value
    SNOW_HEIGHT = MeasurementAttribute.SNOW_HEIGHT.value
    ICE_PERCENTAGE = MeasurementAttribute.ICE_PERCENTAGE.value
    SALINE_CONCENTRATION = MeasurementAttribute.SALINE_CONCENTRATION.value
    FRICTION = MeasurementAttribute.FRICTION.value
    ROAD_CONDITION_TYPE = MeasurementAttribute.ROAD_CONDITION_TYPE.value
    MEASUREMENT_STATUS_BITS = MeasurementAttribute.MEASUREMENT_STATUS_BITS.value

class MeasurementList(list[Measurement]):
    """ABSTRACT class. Adds an filter-function to standard list"""
    _measurement_api: MeasurementApi

    def __init__(self, measurement_api: MeasurementApi, *args):
        self._measurement_api = measurement_api
        super().__init__(args)

    def _get_earliest_time(self) -> datetime:
        """returns the datetime of the element with earliest datetime

        Returns:
            datetime: earliest time (or None)
        """
        if len(self)==0:
            return datetime.max
        min_datetime = self[0].tmpstmp_for_adding
        for element in self:
            min_datetime = min(element.tmpstmp_for_adding, min_datetime)
        return min_datetime

    def _get_latest_time(self) -> datetime:
        """returns the datetime of the element with latest datetime

        Returns:
            datetime: latest time (or None)
        """
        if len(self)==0:
            return datetime.max
        max_datetime = self[0].tmpstmp_for_adding
        for element in self:
            max_datetime = max(element.tmpstmp_for_adding,max_datetime)
        return max_datetime

    async def filtered_by_value(self, attribute: MeasurementAttribute, value: object) -> asyncio.Future['MeasurementList']:
        """Filters the current list by an Attribute

        Args:
            by (MeasurementAttribute): attribute type
            value (object): attribute value

        Returns:
            list: _description_
        """
        future : asyncio.Future['MeasurementList'] = asyncio.Future()
        async def task():

            # request data
            # filter for attribute == value
            # map to datetime
            times: list[datetime] = await self._get_filtered_times_by_value(attribute, value)
            logging.debug(f"Times where the requested data has {attribute} == {value}: {times}")

            # filter current list for matching datetimes
            filtered_list: MeasurementList = MeasurementList(self._measurement_api)
            for element in self:
                if element.tmpstmp_for_adding in times:
                    filtered_list.append(element)
            logging.debug(f"Filtered list: {filtered_list}")

            future.set_result(filtered_list)

        await asyncio.create_task(task())
        return future
        

    async def _get_filtered_times_by_value(
        self, attribute: MeasurementAttribute, value: object
    ) -> list[datetime]:
        min_time = self._get_earliest_time()
        max_time = self._get_latest_time()
        if (min_time == datetime.max) or (max_time == datetime.min):
            return []

        #change min_time to start of the day and max_time to end of the day
        min_time = datetime.fromordinal(min_time.toordinal())
        max_time = datetime.fromordinal(max_time.toordinal()+1)

        if attribute.value.get_type() == MeasurementType.WEATHER:

            new_data = await (await self._measurement_api.get_weather_data(min_time, max_time))
            filtered_data: list[WeatherData] = []

            if attribute == MeasurementAttribute.WEATHER_ID:
                for element in new_data:
                    if element.id == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.TEMPC:
                for element in new_data:
                    if element.tempc == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.HUMIDITY:
                for element in new_data:
                    if element.humidity == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.ABSOLUTE_HUMIDITY:
                for element in new_data:
                    if element.absolute_humidity == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.AIR_PRESSURE:
                for element in new_data:
                    if element.air_pressure == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.ABSOLUTE_PRECIPITATION:
                for element in new_data:
                    if element.absolute_precipitation == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.ABSOLUTE_PRECIPITATION_MM:
                for element in new_data:
                    if element.absolute_precipitation_mm == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.DIFFERENTIAL_PRECIPITATION:
                for element in new_data:
                    if element.differential_precipitation == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.DIFFERENTIAL_PRECIPITATION_MM:
                for element in new_data:
                    if element.differential_precipitation_mm == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.PRECIPITATION_INTENSITY:
                for element in new_data:
                    if element.precipitation_intensity == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.PRECIPITATION_TYPE:
                for element in new_data:
                    if element.precipitation_type == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.PRECIPITATION:
                for element in new_data:
                    if element.precipitation == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.WEATHER_TOPIC:
                for element in new_data:
                    if element.topic == value:
                        filtered_data.append(element)

            # map filtered data to datetimes
            logging.debug(f"Filtered weather data {filtered_data}")

            times: list[datetime] = []
            for element in filtered_data:
                times.append(element.tmpstmp_for_adding)
            return times
        if attribute.value.get_type() == MeasurementType.DETECTION:

            new_data = await (await self._measurement_api.get_detection_data(min_time, max_time))
            filtered_data: list[DetectionData] = []
            if attribute == MeasurementAttribute.HEADING:
                for element in new_data:
                    if element.heading == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.DETECTION_ID:
                for element in new_data:
                    if element.id == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.KAFKA_TOPIC:
                for element in new_data:
                    if element.kafka_topic == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.LAT:
                for element in new_data:
                    if element.lat == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.LON:
                for element in new_data:
                    if element.lon == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.SPEED:
                for element in new_data:
                    if element.speed == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.TIMESTAMP:
                for element in new_data:
                    if element.timestamp == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.TRACK_ID:
                for element in new_data:
                    if element.track_id == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.TYPE:
                for element in new_data:
                    if element.detection_type == value:
                        filtered_data.append(element)

            # map filtered data to datetimes
            logging.debug(f"Filtered detection data {filtered_data}")
            times: list[datetime] = []
            for element in filtered_data:
                times.append(element.tmpstmp_for_adding)
            return times
        if attribute.value.get_type() == MeasurementType.PARKING:

            new_data = await (await self._measurement_api.get_parking_data(min_time, max_time))
            filtered_data: list[ParkingData] = []
            if attribute == MeasurementAttribute.CUSTOM_STATE:
                for element in new_data:
                    if element.custom_state == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.GAP_IDS:
                for element in new_data:
                    if element.gap_ids == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.PARKING_ID:
                for element in new_data:
                    if element.id == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.NAME:
                for element in new_data:
                    if element.name == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.OCCUPIED:
                for element in new_data:
                    if element.occupied == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.RAW_DATA_ARRIVAL:
                for element in new_data:
                    if element.raw_data_arrival == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.RAW_DATA_CAR:
                for element in new_data:
                    if element.raw_data_car == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.RAW_DATA_DEPATURE:
                for element in new_data:
                    if element.raw_data_depature == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.REF1:
                for element in new_data:
                    if element.ref1 == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.REF2:
                for element in new_data:
                    if element.ref2 == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.VALID:
                for element in new_data:
                    if element.valid == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.RAW_REF_DATA:
                for element in new_data:
                    if element.raw_ref_data == value:
                        filtered_data.append(element)

            # map filtered data to datetimes
            logging.debug(f"Filtered parking data {filtered_data}")

            times: list[datetime] = []
            for element in filtered_data:
                times.append(element.tmpstmp_for_adding)
            return times

        if attribute.value.get_type() == MeasurementType.ROAD:

            new_data = await (await self._measurement_api.get_road_data(min_time, max_time))
            filtered_data: list[RoadData] = []
            if attribute == MeasurementAttribute.FREEZING_TEMPERATURE_NAC:
                for element in new_data:
                    if element.freezing_temperature_nac == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.FRICTION:
                for element in new_data:
                    if element.friction == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.ICE_LAYER_THICKNESS:
                for element in new_data:
                    if element.ice_layer_thickness == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.ICE_PERCENTAGE:
                for element in new_data:
                    if element.ice_percentage == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.ROAD_ID:
                for element in new_data:
                    if element.id == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.MEASUREMENT_STATUS_BITS:
                for element in new_data:
                    if element.measurement_status_bits == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.ROAD_CONDITION:
                for element in new_data:
                    if element.road_condition == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.ROAD_CONDITION_TYPE:
                for element in new_data:
                    if element.road_condition_type == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.ROAD_SURFACE_TEMPERATURE_C:
                for element in new_data:
                    if element.road_surface_temperature_c == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.SALINE_CONCENTRATION:
                for element in new_data:
                    if element.saline_concentration == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.SNOW_HEIGHT:
                for element in new_data:
                    if element.snow_height == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.ROAD_TOPIC:
                for element in new_data:
                    if element.topic == value:
                        filtered_data.append(element)
            if attribute == MeasurementAttribute.WATER_FILM_HEIGHT:
                for element in new_data:
                    if element.water_film_height == value:
                        filtered_data.append(element)

            # map filtered data to datetimes
            logging.debug(f"Filtered road data {filtered_data}")

            times: list[datetime] = []
            for element in filtered_data:
                times.append(element.tmpstmp_for_adding)
            return times

        if attribute.value.get_type() == MeasurementType.ANY:

            weather_data = await (await self._measurement_api.get_weather_data(min_time, max_time))
            for element in weather_data:
                if element.tmpstmp_for_adding == value:
                    return [element.tmpstmp_for_adding]
            parking_data = await (await self._measurement_api.get_parking_data(min_time, max_time))
            for element in parking_data:
                if element.tmpstmp_for_adding == value:
                    return [element.tmpstmp_for_adding]
            detection_data = await (await self._measurement_api.get_detection_data(min_time, max_time))
            for element in detection_data:
                if element.tmpstmp_for_adding == value:
                    return [element.tmpstmp_for_adding]
            road_data = await (await self._measurement_api.get_road_data(min_time, max_time))
            for element in road_data:
                if element.tmpstmp_for_adding == value:
                    return [element.tmpstmp_for_adding]
        return []

    async def filtered_by_range(self, attribute: NumberAttribute, beginning: Number, ending: Number) -> asyncio.Future['MeasurementList']:
        """Filters the current list by a Measurement Attribute in an specific interval

        Args:
            by (MeasurementAttribute): Attribute
            beginning (Number): start of interval
            ending (Number): end of interval

        Returns:
            list: filtered list
        """
        future : asyncio.Future['MeasurementList'] = asyncio.Future()
        async def task():
            # request data
            # filter for attribute == value
            # map to datetime
            times: list[datetime] = await self._get_filtered_times_by_range(attribute, beginning,ending)
            logging.debug(f"Times where the requested data is {beginning} < {attribute} < {ending}: {times}")

            # filter current list for matching datetimes
            filtered_list: MeasurementList = MeasurementList(self._measurement_api)
            for element in self:
                if element.tmpstmp_for_adding in times:
                    filtered_list.append(element)
            logging.debug(f"Filtered list: {filtered_list}")

            future.set_result(filtered_list)


        await asyncio.create_task(task())
        return future
    
    async def _get_filtered_times_by_range(
        self, attribute: NumberAttribute, beginning: Number, ending: Number
    ) -> list[datetime]:
        min_time = self._get_earliest_time()
        max_time = self._get_latest_time()

        if (min_time == datetime.max) | (max_time == datetime.min):
            return []

        min_time = datetime.fromordinal(min_time.toordinal())
        max_time = datetime.fromordinal(max_time.toordinal()+1)

        if attribute.value.get_type() == MeasurementType.WEATHER:
            new_data = await (await self._measurement_api.get_weather_data(min_time, max_time))
            filtered_data: list[WeatherData] = []

            if attribute == NumberAttribute.WEATHER_ID:
                for element in new_data:
                    if (element.id >= beginning) & (element.id <= ending):
                        filtered_data.append(element)
            if attribute == NumberAttribute.TEMPC:
                for element in new_data:
                    if (element.tempc >= beginning) & (element.tempc <= ending):
                        filtered_data.append(element)
            if attribute == NumberAttribute.HUMIDITY:
                for element in new_data:
                    if (element.humidity >= beginning) & (element.humidity <= ending):
                        filtered_data.append(element)
            if attribute == NumberAttribute.ABSOLUTE_HUMIDITY:
                for element in new_data:
                    if (element.absolute_humidity >= beginning) & (element.absolute_humidity <= ending):
                        filtered_data.append(element)
            if attribute == NumberAttribute.AIR_PRESSURE:
                for element in new_data:
                    if (element.air_pressure >= beginning) & (element.air_pressure <= ending):
                        filtered_data.append(element)
            if attribute == NumberAttribute.ABSOLUTE_PRECIPITATION:
                for element in new_data:
                    if (
                        element.absolute_precipitation
                        >= beginning) & (element.absolute_precipitation
                        <= ending
                    ):
                        filtered_data.append(element)
            if attribute == NumberAttribute.ABSOLUTE_PRECIPITATION_MM:
                for element in new_data:
                    if (
                        element.absolute_precipitation_mm
                        >= beginning) & (element.absolute_precipitation_mm
                        <= ending
                    ):
                        filtered_data.append(element)
            if attribute == NumberAttribute.DIFFERENTIAL_PRECIPITATION:
                for element in new_data:
                    if (
                        element.differential_precipitation
                        >= beginning) & (element.differential_precipitation
                        <= ending
                    ):
                        filtered_data.append(element)
            if attribute == NumberAttribute.DIFFERENTIAL_PRECIPITATION_MM:
                for element in new_data:
                    if (
                        element.differential_precipitation_mm
                        >= beginning) & (element.absolute_precipitation_mm
                        <= ending
                    ):
                        filtered_data.append(element)
            if attribute == NumberAttribute.PRECIPITATION_INTENSITY:
                for element in new_data:
                    if (
                        element.precipitation_intensity
                        >= beginning) & (element.precipitation_intensity
                        <= ending
                    ):
                        filtered_data.append(element)
            if attribute == NumberAttribute.PRECIPITATION_TYPE:
                for element in new_data:
                    if (
                        element.precipitation_type
                        >= beginning) & (element.precipitation_type
                        <= ending
                    ):
                        filtered_data.append(element)

            # map filtered data to datetimes
            logging.debug(f"Filtered weather data {filtered_data}")

            times: list[datetime] = []
            for element in filtered_data:
                times.append(element.tmpstmp_for_adding)
            return times

        if attribute.value.get_type() == MeasurementType.PARKING:

            new_data = await (await self._measurement_api.get_parking_data(min_time, max_time))
            filtered_data: list[ParkingData] = []

            if attribute == NumberAttribute.PARKING_ID:
                for element in new_data:
                    if (element.id >= beginning) & (element.id <= ending):
                        filtered_data.append(element)

            # map filtered data to datetimes
            logging.debug(f"Filtered parking data {filtered_data}")

            times: list[datetime] = []
            for element in filtered_data:
                times.append(element.tmpstmp_for_adding)
            return times
        if attribute.value.get_type() == MeasurementType.ROAD:

            new_data = await (await self._measurement_api.get_road_data(min_time, max_time))
            filtered_data: list[RoadData] = []
            if attribute == NumberAttribute.FREEZING_TEMPERATURE_NAC:
                for element in new_data:
                    if (
                        element.freezing_temperature_nac
                        >= beginning) & (element.freezing_temperature_nac
                        <= ending
                    ):
                        filtered_data.append(element)
            if attribute == NumberAttribute.FRICTION:
                for element in new_data:
                    if (element.friction >= beginning) & (element.friction <= ending):
                        filtered_data.append(element)
            if attribute == NumberAttribute.ICE_LAYER_THICKNESS:
                for element in new_data:
                    if (
                        element.ice_layer_thickness
                        >= beginning) & (element.ice_layer_thickness
                        <= ending
                    ):
                        filtered_data.append(element)
            if attribute == NumberAttribute.ICE_PERCENTAGE:
                for element in new_data:
                    if (element.ice_percentage >= beginning) & (element.ice_percentage <= ending):
                        filtered_data.append(element)
            if attribute == NumberAttribute.ROAD_ID:
                for element in new_data:
                    if (element.id >= beginning) & (element.id <= ending):
                        filtered_data.append(element)
            if attribute == NumberAttribute.MEASUREMENT_STATUS_BITS:
                for element in new_data:
                    if (
                        element.measurement_status_bits
                        >= beginning) & (element.measurement_status_bits
                        <= ending
                    ):
                        filtered_data.append(element)
            if attribute == NumberAttribute.ROAD_CONDITION_TYPE:
                for element in new_data:
                    if (
                        element.road_condition_type
                        >= beginning) & (element.road_condition_type
                        <= ending
                    ):
                        filtered_data.append(element)
            if attribute == NumberAttribute.ROAD_SURFACE_TEMPERATURE_C:
                for element in new_data:
                    if (
                        element.road_surface_temperature_c
                        >= beginning) & (element.road_surface_temperature_c
                        <= ending
                    ):
                        filtered_data.append(element)
            if attribute == NumberAttribute.SALINE_CONCENTRATION:
                for element in new_data:
                    if (
                        element.saline_concentration
                        >= beginning) & (element.saline_concentration
                        <= ending
                    ):
                        filtered_data.append(element)
            if attribute == NumberAttribute.SNOW_HEIGHT:
                for element in new_data:
                    if (element.snow_height >= beginning) & (element.snow_height <= ending):
                        filtered_data.append(element)

            if attribute == NumberAttribute.WATER_FILM_HEIGHT:
                for element in new_data:
                    if (element.water_film_height >= beginning) & (element.water_film_height <= ending):
                        filtered_data.append(element)

            # map filtered data to datetimes
            logging.debug(f"Filtered road data {filtered_data}")

            times: list[datetime] = []
            for element in filtered_data:
                times.append(element.tmpstmp_for_adding)
            return times
        return []
