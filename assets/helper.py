
from math import radians, sin, cos, sqrt, atan2
from .models import *
def haversine(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate distance between two points on the earth
    R = 6371  # Earth radius in kilometers

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c  # Distance in kilometers
    return distance

def update_location(tracker_id, latitude, longitude):
    # handle incoming GPS data and update the location and speed
    location = GPSData.objects.filter(tracker_id=tracker_id).order_by('-timestamp').first()

    if location:
        distance = haversine(location.latitude, location.longitude, float(latitude), float(longitude))
        time_diff = (location.timestamp - location.timestamp).seconds / 3600  # in hours
        speed = distance / time_diff if time_diff > 0 else None
    else:
        speed = None
    location.objects.create(tracker_id=tracker_id, latitude=latitude, longitude=longitude, speed=speed)
    