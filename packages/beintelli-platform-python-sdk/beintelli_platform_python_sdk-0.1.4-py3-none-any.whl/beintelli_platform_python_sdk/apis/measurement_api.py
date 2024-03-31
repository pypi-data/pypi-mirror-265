    
import asyncio
import logging
from datetime import datetime

import requests

from .config import BASE_URL, EndPoints, TIMEOUT_SEC
from ..utils.access import Access
from ..utils.types import DetectionData, ParkingData, RoadData, WeatherData, Measurement



class MeasurementApi:
    """
    The measurement api provides http requests as get-methods for weather-, parking-, detection-, and road data
    """

    def __init__(self, acc: Access):
        self._access = acc

    def _get_standard_headers(self):
        return {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer " + self._access.get_access_token(),
        }
    
    async def get_weather_data(self, beginning: datetime, ending: datetime) -> asyncio.Future[list[WeatherData]]:
        """Sends an HTTP request for weather data in a specific time period

        Args:
            beginning (datetime): start of the specific time period
            ending (datetime): end of the specific time period

        Returns:
            asyncio.Future[list[weather_data]]: a future object containing the list of weather data
            sent by the server
        """
        future: asyncio.Future[list[WeatherData]] = asyncio.Future()
        async def task() -> None:
            try:
                #http request params
                url= BASE_URL + EndPoints.WEATHER.value
                params = {"start_tmpstmp": beginning.isoformat(), "end_tmpstmp": ending.isoformat()}
                headers = self._get_standard_headers()
                timeout = TIMEOUT_SEC

                #send http request
                logging.debug(f"Execute requests.get(url={url}, params={params}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, params=params, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack response
                if response.status_code == 200:
                    result: list[list] = response.json().get("message")
                    parsed_result: list[WeatherData] = parsed_weather_data(result)
                    logging.debug(f"Weather data: {parsed_result}")
                    future.set_result(parsed_result)
                else:
                    logging.debug(f"Weather data: {[]}")
                    future.set_result([])

            except Exception as e:
                logging.warning(f"Exception: {e}")
                logging.debug(f"Weather data: {[]}")
                future.set_result([])

        task = await asyncio.create_task(task())
        return future
    
    async def get_detection_data(self, beginning: datetime, ending: datetime) -> asyncio.Future[list[DetectionData]]:
        """Sends an HTTP request for detection data in a specific time period

        Args:
            beginning (datetime): start of the specific time period
            ending (datetime): end of the specific time period

        Returns:
            asyncio.Future[list[detection_data]]: a future object containing the list of detection
            data sent by the server
        """
        future: asyncio.Future[list[DetectionData]] = asyncio.Future()

        async def task():
            try:
                #http request params
                url = BASE_URL + EndPoints.DETECTION.value
                params = {"start_tmpstmp": beginning.isoformat(), "end_tmpstmp": ending.isoformat()}
                headers = self._get_standard_headers()
                timeout = TIMEOUT_SEC


                #send http request
                logging.debug(f"Execute requests.get(url={url}, params={params}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, params=params, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack response
                if response.status_code == 200:
                    result: list[list] = response.json().get("message")
                    parsed_result: list[DetectionData] = parsed_detection_data(result)
                    logging.debug(f"Detection data: {parsed_result}")
                    future.set_result(parsed_result)
                else:
                    logging.debug(f"Detection data: {[]}")
                    future.set_result([])

            except Exception as e:
                logging.warning(f"Exception: {e}")
                logging.debug(f"Detection data: {[]}")
                future.set_result([])

        await asyncio.create_task(task())
        return future
    
    async def get_parking_data(self, beginning: datetime, ending: datetime) -> asyncio.Future[list[ParkingData]]:
        """Sends an HTTP request for parking data in a specific time period

        Args:
            beginning (datetime): start of the specific time period
            ending (datetime): end of the specific time period

        Returns:
            asyncio.Future[list[parking_data]]: a future object containing the list of parking data
            sent by the server
        """
        future: asyncio.Future[list[ParkingData]] = asyncio.Future()

        async def task():
            try:
                #http request params
                url = BASE_URL + EndPoints.PARKING.value
                params = {"start_tmpstmp": beginning.isoformat(), "end_tmpstmp": ending.isoformat()}
                headers = self._get_standard_headers()
                timeout = TIMEOUT_SEC

                #send http request
                logging.debug(f"Execute requests.get(url={url}, params={params}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, params=params, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack response
                if response.status_code == 200:
                    result: list[list] = response.json().get("message")
                    parsed_result: list[ParkingData] = parsed_parking_data(result)
                    logging.debug(f"Parking data: {parsed_result}")
                    future.set_result(parsed_result)
                else:
                    logging.debug(f"Parking data: {[]}")
                    future.set_result([])

            except Exception as e:
                logging.warning(f"Exception: {e}")
                logging.debug(f"Parking data: {[]}")
                future.set_result([])

        await asyncio.create_task(task())
        return future

    async def get_road_data(self, beginning: datetime, ending: datetime) -> asyncio.Future[list[RoadData]]:
        """Sends an HTTP request for road data in a specific time period

        Args:
            beginning (datetime): start of the specific time period
            ending (datetime): end of the specific time period

        Returns:
            asyncio.Future[list[road_data]]: a future object containing the list of road data sent
            by the server
        """
        future: asyncio.Future[list[RoadData]] = asyncio.Future()

        async def task():
            try:
                #http request params
                url = BASE_URL + EndPoints.ROAD.value
                params = {"start_tmpstmp": beginning.isoformat(), "end_tmpstmp": ending.isoformat()}
                headers = self._get_standard_headers()
                timeout = TIMEOUT_SEC

                #send http request
                logging.debug(f"Execute requests.get(url={url}, params={params}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, params=params, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack response
                if response.status_code == 200:
                    result: list[list] = response.json().get("message")
                    parsed_result: list[RoadData] = parsed_road_data(result)
                    logging.debug(f"Road data: {parsed_result}")
                    future.set_result(parsed_result)
                else:
                    logging.debug(f"Road data: {[]}")
                    future.set_result([])
            except Exception as e:
                logging.warning(f"Exception: {e}")
                logging.debug(f"Road data: {[]}")
                future.set_result([])

        await asyncio.create_task(task())
        return future

def parsed_detection_data(outer_list: list[list]) -> list[DetectionData]:
    """Parses a list of lists to a list of detection data

    Args:
        outer_list (list[list])

    Returns:
        list[detection_data]
    """
    parsed_list = []
    for inner_list in outer_list:
        parsed_list.append(
            DetectionData(
                datetime.fromisoformat(inner_list[9]),
                inner_list[0],
                inner_list[1],
                inner_list[2],
                inner_list[3],
                inner_list[4],
                inner_list[5],
                inner_list[6],
                inner_list[7],
                inner_list[8]
            )
        )
    return parsed_list

def parsed_weather_data(outer_list: list[list]) -> list[WeatherData]:
    """Parses a list of lists to a list of weather data

    Args:
        outer_list (list[list])

    Returns:
        list[weather_data]
    """
    parsed_list = []
    for inner_list in outer_list:
        parsed_list.append(
            WeatherData(
                datetime.fromisoformat(inner_list[13]),
                inner_list[0],
                inner_list[1],
                inner_list[2],
                inner_list[3],
                inner_list[4],
                inner_list[5],
                inner_list[6],
                inner_list[7],
                inner_list[8],
                inner_list[9],
                inner_list[10],
                inner_list[11],
                inner_list[12]
            )
        )
    return parsed_list

def parsed_parking_data(outer_list: list[list]) -> list[ParkingData]:
    """Parses a list of lists to a list of parking data

    Args:
        outer_list (list[list])

    Returns:
        list[parking_data]
    """
    parsed_list = []
    for inner_list in outer_list:
        parsed_list.append(
            ParkingData(
                datetime.fromisoformat(inner_list[12]),
                inner_list[0],
                inner_list[1],
                inner_list[2],
                inner_list[3],
                inner_list[4],
                inner_list[5],
                inner_list[6],
                inner_list[7],
                inner_list[8],
                inner_list[9],
                inner_list[10],
                inner_list[11]
            )
        )
    return parsed_list

def parsed_road_data(outer_list: list[list]) -> list[RoadData]:
    """Parses a list of lists to a list of road data

    Args:
        outer_list (list[list])

    Returns:
        list[road_data]
    """
    parsed_list = []
    for inner_list in outer_list:
        parsed_list.append(
            RoadData(
                datetime.fromisoformat(inner_list[13]),
                inner_list[0],
                inner_list[1],
                inner_list[2],
                inner_list[3],
                inner_list[4],
                inner_list[5],
                inner_list[6],
                inner_list[7],
                inner_list[8],
                inner_list[9],
                inner_list[10],
                inner_list[11],
                inner_list[12],
            )
        )
    return parsed_list