"""Containing the service api"""

import asyncio
import logging
from datetime import datetime

import requests
from .data_api import parsed_rosbag_info
from .config import BASE_URL, EndPoints, TIMEOUT_SEC
from ..utils.access import Access
from ..utils.types import RosbagInfo


class ServiceApi:
    """The service api provides http requests as get-methods for different serviceses"""

    def __init__(self, acc: Access):
        self._access = acc

    def _get_standard_headers(self):
        return {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer " + self._access.get_access_token(),
        }

    async def get_weather_sheet(self, beginning: datetime, ending: datetime) -> asyncio.Future[bytes]:
        """Sends an HTTP request for an excel sheet of weather data in a specific time frame

        Args:
            beginning (datetime): begin of time frame
            ending (datetime): end of time frame

        Returns:
            asyncio.Future[bytes]: an future object containing an excel sheet
        """
        future: asyncio.Future[bytes] = asyncio.Future()

        async def task():
            try:
                #http request params
                url = BASE_URL + EndPoints.CREATE_SHEET.value
                headers = self._get_standard_headers()
                params = {
                    "start_tmpstmp": beginning.isoformat(),
                    "end_tmpstmp": ending.isoformat(),
                    "end_points": EndPoints.WEATHER.value,
                }
                timeout = TIMEOUT_SEC

                #send http request
                logging.debug(f"Execute requests.get(url={url}, params={params}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, params=params, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack response
                if response.status_code == 200:
                    result: bytes = response.content
                    logging.debug(f"Weather sheet: {result}")
                    future.set_result(result)
                else:
                    logging.debug(f"Weather sheet: {bytes()}")
                    future.set_result(bytes())
            except Exception as e:
                logging.warning(f"Exception: {e}")
                logging.debug(f"Weather sheet: {bytes()}")
                future.set_result(bytes())

        await asyncio.create_task(task())
        return future

    async def get_parking_sheet(self, beginning: datetime, ending: datetime) -> asyncio.Future[bytes]:
        """Sends an HTTP request for an excel sheet of parking data in a specific time frame

        Args:
            beginning (datetime): begin of time frame
            ending (datetime): end of time frame

        Returns:
            asyncio.Future[bytes]: an future object containing an excel sheet
        """
        future: asyncio.Future[bytes] = asyncio.Future()

        async def task():
            try:
                #http request params
                url = BASE_URL + EndPoints.CREATE_SHEET.value
                headers = self._get_standard_headers()
                params = {
                    "start_tmpstmp": beginning.isoformat(),
                    "end_tmpstmp": ending.isoformat(),
                    "end_points": EndPoints.PARKING.value,
                }
                timeout = TIMEOUT_SEC

                #send http request
                logging.debug(f"Execute requests.get(url={url}, params={params}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, params=params, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack response
                if response.status_code == 200:
                    result: bytes = response.content
                    logging.debug(f"Parking sheet: {result}")
                    future.set_result(result)
                else:
                    logging.debug(f"Parking sheet: {bytes()}")
                    future.set_result(bytes())
            except Exception as e:
                logging.warning(f"Exception: {e}")
                logging.debug(f"Parking sheet: {bytes()}")
                future.set_result(bytes())

        await asyncio.create_task(task())
        return future

    async def get_road_sheet(self, beginning: datetime, ending: datetime) -> asyncio.Future[bytes]:
        """Sends an HTTP request for an excel sheet of road data in a specific time frame

        Args:
            beginning (datetime): begin of time frame
            ending (datetime): end of time frame

        Returns:
            asyncio.Future[bytes]: an future object containing an excel sheet
        """
        future: asyncio.Future[bytes] = asyncio.Future()

        async def task():
            try:
                #http request params
                url = BASE_URL + EndPoints.CREATE_SHEET.value
                headers = self._get_standard_headers()
                params = {
                    "start_tmpstmp": beginning.isoformat(),
                    "end_tmpstmp": ending.isoformat(),
                    "end_points": EndPoints.ROAD.value,
                }
                timeout = TIMEOUT_SEC

                #send http request
                logging.debug(f"Execute requests.get(url={url}, params={params}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, params=params, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack response
                if response.status_code == 200:
                    result: bytes = response.content
                    logging.debug(f"Road sheet: {result}")
                    future.set_result(result)
                else:
                    logging.debug(f"Road sheet: {bytes()}")
                    future.set_result(bytes())

            except Exception as e:
                logging.warning(f"Exception: {e}")
                logging.debug(f"Road sheet: {bytes()}")
                future.set_result(bytes())

        await asyncio.create_task(task())
        return future

    async def get_detection_sheet(self, beginning: datetime, ending: datetime) -> asyncio.Future[bytes]:
        """Sends an HTTP request for an excel sheet of detection data in a specific
        time frame

        Args:
            beginning (datetime): begin of time frame
            ending (datetime): end of time frame

        Returns:
            asyncio.Future[bytes]: an future object containing an excel sheet
        """
        future: asyncio.Future[bytes] = asyncio.Future()

        async def task():
            try:
                #http request params
                url = BASE_URL + EndPoints.CREATE_SHEET.value
                headers = self._get_standard_headers()
                params = {
                    "start_tmpstmp": beginning.isoformat(),
                    "end_tmpstmp": ending.isoformat(),
                    "end_points": EndPoints.DETECTION.value,
                }
                timeout = TIMEOUT_SEC

                #send http request
                logging.debug(f"Execute requests.get(url={url}, params={params}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, params=params, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack response
                if response.status_code == 200:
                    result: bytes = response.content
                    logging.debug(f"Detection sheet: {result}")
                    future.set_result(result)
                else:
                    logging.debug(f"Detection sheet: {bytes()}")
                    future.set_result(bytes())

            except Exception as e:
                logging.warning(f"Exception: {e}")
                logging.debug(f"Detection sheet: {bytes()}")
                future.set_result(bytes())

        await asyncio.create_task(task())
        return future

    async def get_rosbags(self) -> asyncio.Future[list[RosbagInfo]]:
        """Sends an HTTP request for rosbags

        Returns:
            asyncio.Future[RosbagInfo]: an future object containing an list of rosbag
            meta data
        """
        future: asyncio.Future[list[RosbagInfo]] = asyncio.Future()

        async def task():
            try:
                #http request params
                url = BASE_URL + EndPoints.ROSBAGS.value
                headers=self._get_standard_headers()
                timeout = TIMEOUT_SEC

                #send http request
                logging.debug(f"Execute requests.get(url={url}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack response
                if response.status_code == 200:
                    result: list[list] = response.json()
                    parsed_result: list[RosbagInfo] = parsed_rosbag_info(result)
                    logging.debug(f"Rosbags: {parsed_result}")
                    future.set_result(parsed_result)
                else:
                    logging.debug(f"Rosbags: {[]}")
                    future.set_result([])

            except Exception as e:
                logging.warning(f"Exception: {e}")
                logging.debug(f"Rosbags: {[]}")
                future.set_result([])

        await asyncio.create_task(task())
        return future

    async def get_converted_rosbags(self) -> asyncio.Future[list[RosbagInfo]]:
        """Sends an HTTP request for converted rosbags

        Returns:
            asyncio.Future[RosbagInfo]: an future object containing an list of converted rosbag
            meta data
        """
        future: asyncio.Future[list[RosbagInfo]] = asyncio.Future()

        async def task():
            try:
                #http request params
                url = BASE_URL + EndPoints.ROSBAGS_CONVERTED.value
                headers = self._get_standard_headers()
                timeout = TIMEOUT_SEC

                #send http request
                logging.debug(f"Execute requests.get(url={url}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack response
                if response.status_code == 200:
                    result: list[list] = response.json()
                    parsed_result: list[RosbagInfo] = parsed_rosbag_info(result)
                    logging.debug(f"Converted rosbags: {parsed_result}")
                    future.set_result(parsed_result)
                else:
                    logging.debug(f"Converted rosbags: {[]}")
                    future.set_result([])

            except Exception as e:
                logging.warning(f"Exception: {e}")
                logging.debug(f"Converted rosbags: {[]}")
                future.set_result([])

        await asyncio.create_task(task())
        return future

    async def get_rosbag(self, filename: str) -> asyncio.Future[bytes]:
        """Sends an HTTP request for a rosbag-file

        Returns:
            asyncio.Future[bytes]: an future object containing rosbag-file
        """
        future: asyncio.Future[bytes] = asyncio.Future()

        async def task():
            try:
                #http request params
                url = BASE_URL + EndPoints.DOWNLOAD_ROSBAG.value + "/" + filename
                headers = self._get_standard_headers()
                timeout = TIMEOUT_SEC

                #send http request
                logging.debug(f"Execute requests.get(url={url}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack response
                if response.status_code == 200:
                    result: bytes = response.content
                    logging.debug(f"Rosbag: {result}")
                    future.set_result(result)
                else:
                    logging.debug(f"Rosbag: {bytes()}")
                    future.set_result(bytes())
            except Exception as e:
                logging.warning(f"Exception: {e}")
                logging.debug(f"Rosbag: {bytes()}")
                future.set_result(bytes())

        await asyncio.create_task(task())
        return future

    async def get_converted_rosbag(self, filename: str) -> asyncio.Future[bytes]:
        """Sends an HTTP request for a converted rosbag-file

        Returns:
            asyncio.Future[bytes]: an future object containing a converted rosbag-file
        """
        future: asyncio.Future[bytes] = asyncio.Future()

        async def task():
            try:
                #http request params
                url = BASE_URL + EndPoints.DOWNLOAD_CONVERTED_ROSBAG.value + "/" + filename
                headers = self._get_standard_headers()
                timeout = TIMEOUT_SEC

                #send http request
                logging.debug(f"Execute requests.get(url={url}, headers={headers}, timeout={timeout})")
                response = requests.get(url=url, headers=headers, timeout=timeout)
                logging.debug(f"Received response: {response}")

                #unpack response
                if response.status_code == 200:
                    result: bytes = response.content
                    logging.debug(f"Converted rosbags: {result}")
                    future.set_result(result)
                else:
                    logging.debug(f"Converted rosbags: {bytes()}")
                    future.set_result(bytes())

            except Exception as e:
                logging.warning(f"Exception: {e}")
                logging.debug(f"Converted rosbags: {bytes()}")
                future.set_result(bytes())

        await asyncio.create_task(task())
        return future

    async def convert_rosbag(self, bag_dir: str, config_path: str, params_dict: dict) -> asyncio.Future[None]:
        """Sends an HTTP request to convert a rosbag-file

        Args:
            bag_dir (str): ???
            config_path (str): ???
            params_dict (dict): ???

        Returns:
            asyncio.Future[None]
        """
        future: asyncio.Future[None] = asyncio.Future()
        future.set_result(None)
        return future

    async def blurred_image(self, image: bytes) -> asyncio.Future[None]:
        """Sends an HTTP request to get a blurred image

        Args:
            image (bytes)

        Returns:
            asyncio.Future[None]
        """
        future: asyncio.Future[None] = asyncio.Future()
        future.set_result(None)
        return future

    async def add_rosbag(self, rosbag: bytes) -> asyncio.Future[None]:
        """Sends an HTTP request to add a rosbag

        Args:
            rosbag (bytes)

        Returns:
            asyncio.Future[None]
        """
        future: asyncio.Future[None] = asyncio.Future()
        future.set_result(None)
        return future
