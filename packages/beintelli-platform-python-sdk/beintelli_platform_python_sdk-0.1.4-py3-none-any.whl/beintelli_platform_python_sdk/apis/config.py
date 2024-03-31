"""Containing config parameters as global parameters"""

from enum import Enum

BASE_URL: str = "https://api.dev.be-intelli.com/rest"
TIMEOUT_SEC: int = 10

class EndPoints(Enum):
    """Container for different endpoints

    Args:
        Enum (str): endpoint
    """
    RSU = "/rsu_data"
    WEATHER = "/weather_data"
    PARKINGLOT_AVAILABILITY = "/parkinglot_availability"
    PARKINGLOT_INFORMATION = "/parkinglot_information"
    HD_MAP = "/hdmap"
    DETECTION = "/object_detection_data"
    PARKING = "/parking_data"
    ROAD = "/road_data"
    HD_MAPS = "/list_of_hdmaps"
    VEHICLE_DRIVES = "/vehicle_drives_data"
    VEHICLE_DRIVE_ROUTE = "/vehicle_drive_route_data"
    CREATE_SHEET = "/create_sheet"
    ROSBAGS = "/rosbags"
    DOWNLOAD_ROSBAG = "/download_rosbag"
    ROSBAGS_CONVERTED = "/rosbags_converted"
    DOWNLOAD_CONVERTED_ROSBAG = "/download_converted_rosbag"
