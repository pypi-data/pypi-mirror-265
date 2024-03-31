"""Containing different record data types and matching parsers"""
from datetime import datetime
from dataclasses import dataclass
@dataclass(frozen=True)
class Measurement:
    "A class to represent Measurement data"
    tmpstmp_for_adding: datetime

@dataclass(frozen=True)
class DetectionData(Measurement):
    """A class to represent detection data"""
    id: object
    timestamp: object
    kafka_topic: object
    detection_type: object
    lon: object
    lat: object
    track_id: object
    heading: object
    speed: object

@dataclass
class DriveData:
    """A class to represent drive data"""
    id: str
    value1: str
    value2: str
    value3: str
    value4: float
    value5: float
    value6: float
    value7: float
    value8: float

@dataclass(frozen=True)
class ParkingData(Measurement):
    """A class to represent parking data"""
    id: int
    custom_state: str
    gap_ids: str
    name: str
    raw_data_arrival: str
    raw_data_car: str
    raw_data_depature: str
    occupied: str
    raw_ref_data: str
    ref1: str
    ref2: str
    valid: str

@dataclass
class ParkinglotAvailability:
    """A class to represent "Parkinglot-Availability" data"""
    value1: int
    value2: str
    gap_id: str
    value3: str
    value4: str
    value5: str
    value6: str
    value7: str
    value8: str
    value9: str
    value10: str
    value11: str
    value12: str

@dataclass
class ParkinglotInformation:
    """A class to represent "Parkinglot-Information" data"""
    gap_id: str
    value1: str
    value2: str
    value3: int
    value4: str
    value5: str
    value6: str
    value7: str
    value8: float
    value9: float
    value10: float
    value11: float
    value12: float
    value13: float
    value14: float
    value15: float
    value16: float
    value17: float

@dataclass(frozen=True)
class RoadData(Measurement):
    """A class to represent road data"""
    id: int
    road_surface_temperature_c: float
    freezing_temperature_nac: float
    water_film_height: float
    ice_layer_thickness: float
    snow_height: float
    ice_percentage: float
    saline_concentration: float
    friction: float
    road_condition_type: float
    measurement_status_bits: float
    road_condition: str
    topic: str

@dataclass
class RosbagInfo:
    """A class to represent rosbag meta information"""
    folder_name: str
    size_bytes: int

@dataclass
class RouteData:
    """A class to represent route data"""
    route: list

@dataclass
class RsuData:
    """A class to represent RSU data"""
    value1: str
    value2: str

@dataclass(frozen=True)
class WeatherData(Measurement):
    """A class to represent weather data"""
    id: int
    tempc: float
    humidity: float
    absolute_humidity: float
    air_pressure: float
    absolute_precipitation: float
    absolute_precipitation_mm: float
    differential_precipitation: float
    differential_precipitation_mm: float
    precipitation_intensity: float
    precipitation_type: float
    precipitation: str
    topic: str
