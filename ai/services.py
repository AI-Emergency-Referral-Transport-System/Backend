import math
import logging
from typing import Dict, List, Any, Optional, Tuple
from decimal import Decimal
logger = logging.getLogger(__name__)
class MapService:
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6371
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    @staticmethod
    def get_eta(minutes_distance: float, mode: str = 'driving') -> int:
        speeds = {'driving': 40, 'walking': 5, 'cycling': 15}
        speed = speeds.get(mode, 40)
        return max(1, int(minutes_distance / speed * 60))
    @staticmethod
    def get_direction_url(origin: Tuple[float, float], destination: Tuple[float, float]) -> str:
        return f"https://www.google.com/maps/dir/{origin[0]},{origin[1]}/{destination[0]},{destination[1]}"
    @staticmethod
    def get_embed_url(lat: float, lon: float, zoom: int = 15) -> str:
        return f"https://www.google.com/maps?q={lat},{lon}&z={zoom}&output=embed"
class AmbulanceService:
    def __init__(self):
        from ..ambulances.models import Ambulance, Driver
        from ..users.models import User
        self.Ambulance = Ambulance
        self.Driver = Driver
        self.User = User
    def get_available_ambulances(self, latitude: float, longitude: float, radius_km: float = 50) -> List[Dict]:
        ambulances = self.Ambulance.objects.filter(
            status='available',
            verification_status='approved'
        ).exclude(latitude__isnull=True, longitude__isnull=True)
        results = []
        for amb in ambulances:
            distance = MapService.calculate_distance(
                latitude, longitude,
                float(amb.latitude), float(amb.longitude)
            )
            if