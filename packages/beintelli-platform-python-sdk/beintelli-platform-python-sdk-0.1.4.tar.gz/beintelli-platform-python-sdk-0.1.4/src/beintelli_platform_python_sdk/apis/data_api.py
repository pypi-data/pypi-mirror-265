"""Contains the data api"""

import asyncio
from datetime import datetime

import requests
import logging
from ..measurement_list import MeasurementList
from ..utils.access import Access
from ..utils.types import (
    DetectionData,
    DriveData,
    ParkingData,
    ParkinglotAvailability,
    ParkinglotInformation,
    RoadData,
    RosbagInfo,
    RouteData,
    RsuData,
    WeatherData,
)
from .config import BASE_URL, EndPoints, TIMEOUT_SEC
from .measurement_api import MeasurementApi


class DataApi:
    """
    The data api provides http requests as get-methods for infrastructure and vehicle data
    """

    def __init__(self, acc: Access):
        self._access = acc
        self._measurement_api = MeasurementApi(acc=acc)

    def _get_standard_headers(self):
        return {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer " + self._access.get_access_token(),
        }

    async def get_rsu_data(self) -> asyncio.Future[list[RsuData]]:
        """Sends an HTTP request for RSU data

        Returns:
            asyncio.Future[list[rsu_data]]: a future object containing the list of RSU data
            sent by the server
        """
        future: asyncio.Future[list[RsuData]] = asyncio.Future()

        async def task():
            try:
                #http request params
                url = BASE_URL + EndPoints.RSU.value
                headers = self._get_standard_headers()
                timeout = TIMEOUT_SEC

                #send http request
                logging.debug(f"Execute requests.get(url={url}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack http response
                if response.status_code == 200:
                    result: list[list] = response.json().get("message")
                    parsed_result: list[RsuData] = parsed_rsu_data(result)
                    logging.debug(f"RSU data: {parsed_result}")
                    future.set_result(parsed_result)
                else:
                    logging.debug(f"RSU data: {[]}")
                    future.set_result([])

            except Exception as e:
                logging.warning(f"Exception: {e}")
                logging.debug(f"RSU data: {[]}")
                future.set_result([])

        await asyncio.create_task(task())
        return future

    async def get_weather_data(self, beginning: datetime, ending: datetime) -> asyncio.Future[MeasurementList[WeatherData]]:
        """Sends an HTTP request for weather data in a specific time period

        Args:
            beginning (datetime): start of the specific time period
            ending (datetime): end of the specific time period

        Returns:
            asyncio.Future[list[weather_data]]: a future object containing the list of weather data
            sent by the server
        """
        parsed_future: asyncio.Future[MeasurementList[WeatherData]] = asyncio.Future()
        future: asyncio.Future[list[WeatherData]] = await self._measurement_api.get_weather_data(beginning, ending)

        
        async def task_parse():
            #request weather data
            result: list[WeatherData] = await future

            #parse list[WeatherData] to MeasurementList[WeatherData]
            parsed_result: MeasurementList[WeatherData] = MeasurementList(self._measurement_api,*result)
            logging.debug(f"Parse to MeasurementList: {parsed_result}")

            parsed_future.set_result(parsed_result)

        await asyncio.create_task(task_parse())
        return parsed_future

    async def get_parkinglot_availability(self, gap_id: str) -> asyncio.Future[list[ParkinglotAvailability]]:
        """Sends an HTTP request for 'Parkinglot-Avilability' data

        Args:
            gap_id (str): parkinglot identification

        Returns:
            asyncio.Future[list[parkinglot_availability]]: a future object containing the list of 
            'Parkinglot-Availability' data sent by the server
        """
        future: asyncio.Future[list[ParkinglotAvailability]] = asyncio.Future()

        async def task():
            try:

                #http request params
                url = BASE_URL + EndPoints.PARKINGLOT_AVAILABILITY.value
                params = {"gap_id": gap_id}
                headers = self._get_standard_headers()
                timeout = TIMEOUT_SEC

                #send http request
                logging.debug(f"Execute requests.get(url={url}, params={params}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, params=params, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack response
                if response.status_code == 200:
                    result: list[list] = response.json().get("message")
                    parsed_result: list[ParkinglotAvailability] = parsed_parkinglot_availability(
                        result
                    )
                    logging.debug(f"ParkinglotAvailability data: {parsed_result}")
                    future.set_result(parsed_result)

                else:
                    logging.debug(f"ParkinglotAvailability data: {[]}")
                    future.set_result([])

            except Exception as e:
                logging.warning(f"Exception: {e}")
                logging.debug(f"ParkinglotAvailability data: {[]}")
                future.set_result([])

        await asyncio.create_task(task())
        return future

    async def get_parkinglot_information(self, gap_id: str) -> asyncio.Future[list[ParkinglotInformation]]:
        """Sends an HTTP request for 'Parkinglot-Information' data

        Args:
            gap_id (str): parkinglot identification

        Returns:
            asyncio.Future[list[parkinglot_information]]: a future object containing the list of
            'Parkinglot-Information' data sent by the server
        """
        future: asyncio.Future[list[ParkinglotInformation]] = asyncio.Future()

        async def task():
            try:
                #http request params
                url = BASE_URL + EndPoints.PARKINGLOT_INFORMATION.value
                params = {"gap_id": gap_id}
                headers = self._get_standard_headers()
                timeout = TIMEOUT_SEC

                #send http request
                logging.debug(f"Execute requests.get(url={url}, params={params}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, params=params, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack http response
                if response.status_code == 200:
                    result: list[list] = response.json().get("message")
                    parsed_result: list[ParkinglotInformation] = parsed_parkinglot_information(result)
                    logging.debug(f"ParkinglotInformation data: {parsed_result}")
                    future.set_result(parsed_result)
                else:
                    logging.debug(f"ParkinglotInformation data: {[]}")
                    future.set_result([])
            except Exception as e:
                logging.warning(f"Exception: {e}")
                logging.debug(f"ParkinglotInformation data: {[]}")
                future.set_result([])

        await asyncio.create_task(task())
        return future

    async def get_hdmap(self, filename: str) -> asyncio.Future[bytes]:
        """Sends an HTTP request for an specific hdmap

        Args:
            filename (str): name of hdmap

        Returns:
            asyncio.Future[bytes]: a future object containing the hdmap sent by the server
        """
        future: asyncio.Future[bytes] = asyncio.Future()

        async def task():
            try:
                #http request params
                url=BASE_URL + EndPoints.HD_MAP.value
                params = {"filename": filename}
                headers = self._get_standard_headers()
                timeout = TIMEOUT_SEC

                #send http request
                logging.debug(f"Execute requests.get(url={url}, params={params}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, params=params, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack http response
                if response.status_code == 200:
                    logging.debug(f"HD-Map: {response.content}")
                    future.set_result(response.content)
                else:
                    logging.debug(f"HD-Map: {bytes()}")
                    future.set_result(bytes())
            except Exception as e:
                logging.warning(f"Excepton: {e}")
                logging.debug(f"HD-Map: {bytes()}")
                future.set_result(bytes())

        await asyncio.create_task(task())
        return future

    async def get_detection_data(self, beginning: datetime, ending: datetime) -> asyncio.Future[MeasurementList[DetectionData]]:
        """Sends an HTTP request for detection data in a specific time period

        Args:
            beginning (datetime): start of the specific time period
            ending (datetime): end of the specific time period

        Returns:
            asyncio.Future[list[detection_data]]: a future object containing the list of detection
            data sent by the server
        """

        parsed_future: asyncio.Future[MeasurementList[DetectionData]] = asyncio.Future()
        future: asyncio.Future[list[DetectionData]] = await self._measurement_api.get_detection_data(beginning, ending)


        async def task_parse():
            #get detection data
            result = await future

            #parse list[DetectionData] to MeasurementList[DetectionData]
            parsed_result = MeasurementList(self._measurement_api, *result)
            logging.debug(f"Parse to MeasurementList: {parsed_result}")

            parsed_future.set_result(parsed_result)

        await asyncio.create_task(task_parse())
        return parsed_future

    async def get_parking_data(self, beginning: datetime, ending: datetime) -> asyncio.Future[MeasurementList[ParkingData]]:
        """Sends an HTTP request for parking data in a specific time period

        Args:
            beginning (datetime): start of the specific time period
            ending (datetime): end of the specific time period

        Returns:
            asyncio.Future[list[parking_data]]: a future object containing the list of parking data
            sent by the server
        """
        parsed_future: asyncio.Future[MeasurementList[ParkingData]] = asyncio.Future()
        future: asyncio.Future[list[ParkingData]] = await self._measurement_api.get_parking_data(beginning, ending)

        async def task_parse():
            #get parking data
            result = await future

            #parse list[ParkingData] to MeasurementList[ParkingData]
            parsed_result = MeasurementList(self._measurement_api, *result)
            logging.debug(f"Parse to MeasurementList: {parsed_result}")
            parsed_future.set_result(parsed_result)

        await asyncio.create_task(task_parse())
        return parsed_future

    async def get_road_data(self, beginning: datetime, ending: datetime) -> asyncio.Future[MeasurementList[RoadData]]:
        """Sends an HTTP request for road data in a specific time period

        Args:
            beginning (datetime): start of the specific time period
            ending (datetime): end of the specific time period

        Returns:
            asyncio.Future[list[road_data]]: a future object containing the list of road data sent
            by the server
        """
        parsed_future: asyncio.Future[MeasurementList[RoadData]] = asyncio.Future()
        future: asyncio.Future[list[RoadData]] = await self._measurement_api.get_road_data(beginning, ending)

        async def task_parse():
            #get road data
            result = await future

            #parse list[RoadData] to MeasurementList[RoadData]
            parsed_result = MeasurementList(self._measurement_api, *result)
            logging.debug(f"Parse to MeasurementList: {parsed_result}")
            parsed_future.set_result(parsed_result)

        await asyncio.create_task(task_parse())
        return parsed_future

    async def get_hdmaps(self) -> asyncio.Future[list[str]]:
        """Sends an HTTP request for a list of hdmap-filenames

        Returns:
            asyncio.Future[list[str]]: a future object containing the list of filenames
        """
        future: asyncio.Future[list[str]] = asyncio.Future()

        async def task():
            try:
                #http request params
                url = BASE_URL + EndPoints.HD_MAPS.value
                headers = self._get_standard_headers()
                timeout = TIMEOUT_SEC

                #send http request
                logging.debug(f"Execute requests.get(url={url}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack response
                if response.status_code == 200:
                    result: list[list] = response.json().get("message")
                    parsed_result: list[str] = parsed_hdmaps(result)
                    logging.debug(f"HD-Maps: {parsed_result}")
                    future.set_result(parsed_result)
                else:
                    logging.debug(f"HD-Maps: {[]}")
                    future.set_result([])
            except Exception as e:
                logging.warning(f"Exception: {e}")
                logging.debug(f"HD-Maps: {[]}")
                future.set_result([])

        await asyncio.create_task(task())
        return future

    async def get_drive_data(self, beginning: datetime, ending: datetime, vehicle_id: str = "%") -> asyncio.Future[list[DriveData]]:
        """Sends an HTTP request for road data in a specific time period

        Args:
            beginning (datetime): start of the specific time period
            ending (datetime): end of the specific time period
            vehicle_id (str, optional): vehicle identifier. Defaults to "%".

        Returns:
            asyncio.Future[list[road_data]]: a future object containing the list of drive data sent
            by the server
        """
        future: asyncio.Future[list[DriveData]] = asyncio.Future()

        async def task():
            try:
                #http request params
                url = BASE_URL + EndPoints.VEHICLE_DRIVES.value
                params = {
                    "start_date": beginning.isoformat(),
                    "end_date": ending.isoformat(),
                    "vehicle_id": vehicle_id,
                }
                headers = self._get_standard_headers()
                timeout = TIMEOUT_SEC

                #send http request
                logging.debug(f"Execute requests.get(url={url}, params={params}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, params=params, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack response
                if response.status_code == 200:
                    result: list[list] = response.json().get("message")
                    parsed_result: list[DriveData] = parsed_drive_data(result)
                    logging.debug(f"Drive data: {parsed_result}")
                    future.set_result(parsed_result)
                else:
                    logging.debug(f"Drive data: {[]}")
                    future.set_result([])
            except Exception as e:
                logging.warning(f"Exception: {e}")
                logging.debug(f"Drive data: {[]}")
                future.set_result([])

        await asyncio.create_task(task())
        return future

    async def get_route_data(self, drive_id: str) -> asyncio.Future[list[RouteData]]:
        """Sends an HTTP request for route data in a specific time period

        Args:
            drive_id (str): drive identifier

        Returns:
            asyncio.Future[list[route_data]]: a future object containing the list of route data sent
            by the server
        """
        future: asyncio.Future[list[RouteData]] = asyncio.Future()

        async def task():
            try:
                #http request params
                url = BASE_URL + EndPoints.VEHICLE_DRIVE_ROUTE.value
                params = {"drive_id": drive_id}
                headers = self._get_standard_headers()
                timeout = TIMEOUT_SEC

                #send http request
                logging.debug(f"Execute requests.get(url={url}, params={params}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, params=params, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack response
                if response.status_code == 200:
                    result: list[list] = response.json().get("message")
                    parsed_result: list[RouteData] = parsed_route_data(result)
                    logging.debug(f"Route data: {parsed_result}")
                    future.set_result(parsed_result)
                else:
                    logging.debug(f"Route data: {[]}")
                    future.set_result([])
            except Exception as e:
                logging.warning(f"Exception: {e}")
                logging.debug(f"Route data: {[]}")
                future.set_result([])

        await asyncio.create_task(task())
        return future




def parsed_drive_data(outer_list: list[list]) -> list[DriveData]:
    """Parses a list of lists to a list of drive data

    Args:
        outer_list (list[list])

    Returns:
        list[drive_data]
    """
    parsed_list = []
    for inner_list in outer_list:
        parsed_list.append(
            DriveData(
                inner_list[0],
                inner_list[1],
                inner_list[2],
                inner_list[3],
                inner_list[4],
                inner_list[5],
                inner_list[6],
                inner_list[7],
                inner_list[8],
            )
        )
    return parsed_list


def parsed_parkinglot_availability(outer_list: list[list]) -> list[ParkinglotAvailability]:
    """Parses a list of lists to a list of 'Parkinglot-Availability' data

    Args:
        outer_list (list[list])

    Returns:
        list[parkinglot_availability]
    """
    parsed_list = []
    for inner_list in outer_list:
        parsed_list.append(
            ParkinglotAvailability(
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

def parsed_parkinglot_information(outer_list: list[list]) -> list[ParkinglotInformation]:
    """Parses a list of lists to a list of 'Parkinglot-Information' data

    Args:
        outer_list (list[list])

    Returns:
        list[parkinglot_information]
    """
    parsed_list = []
    for inner_list in outer_list:
        parsed_list.append(
            ParkinglotInformation(
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
                inner_list[13],
                inner_list[14],
                inner_list[15],
                inner_list[16],
                inner_list[17],
            )
        )
    return parsed_list


def parsed_rosbag_info(outer_list: list[list]) -> list[RosbagInfo]:
    """Parses a list of lists to a list of rosbag information

    Args:
        outer_list (list[list])

    Returns:
        list[rosbag_info]
    """
    parsed_list = []
    for inner_list in outer_list:
        parsed_list.append(
            RosbagInfo(
                inner_list[0],
                inner_list[1],
            )
        )
    return parsed_list

def parsed_route_data(outer_list: list[list]) -> list[RouteData]:
    """Parses a list of lists to a list of route data

    Args:
        outer_list (list[list])

    Returns:
        list[route_data]
    """
    parsed_list = []
    for inner_list in outer_list:
        parsed_list.append(RouteData(inner_list))
    return parsed_list

def parsed_rsu_data(outer_list: list[list]) -> list[RsuData]:
    """Parses a list of lists to a list of RSU data

    Args:
        outer_list (list[list])

    Returns:
        list[rsu_data]
    """
    parsed_list = []
    for inner_list in outer_list:
        parsed_list.append(
            RsuData(
                inner_list[0],
                inner_list[1],
            )
        )
    return parsed_list

def parsed_hdmaps(outer_list: list[list[str]])-> list[str]:
    """Parses a list of lists to a list of strings

    Args:
        outer_list (list[list])

    Returns:
        list[str]
    """
    parsed_list = []
    for inner_list in outer_list:
        parsed_list.append(inner_list[0])
    return parsed_list
