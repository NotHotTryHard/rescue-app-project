"""
Coordinate conversion utilities.
"""

def DegreesToDecimal(deg, min, sec):
    """
    Convert degrees, minutes, seconds to decimal degrees.
    
    Args:
        deg (float): Degrees
        min (float): Minutes
        sec (float): Seconds
        
    Returns:
        float: Decimal degrees
    """
    return deg + min/60 + sec/3600

def DegreesToDecimalVec(degminsec):
    """
    Convert (degrees, minutes, seconds) tuple to decimal degrees.
    
    Args:
        degminsec (tuple): Tuple of (degrees, minutes, seconds)
        
    Returns:
        float: Decimal degrees
    """
    return DegreesToDecimal(degminsec[0], degminsec[1], degminsec[2])

def DecimalToDegrees(dec):
    """
    Convert decimal degrees to degrees, minutes, seconds.
    
    Args:
        dec (float): Decimal degrees
        
    Returns:
        tuple: (degrees, minutes, seconds)
    """
    degrees = int(dec)
    minutes_float = (dec - degrees) * 60
    minutes = int(minutes_float)
    seconds = (minutes_float - minutes) * 60
    return (degrees, minutes, seconds)

def DecimalToPixel(latitude, longitude):
    """
    Convert decimal coordinates to pixel coordinates on the map.
    
    Args:
        latitude (float): Latitude in decimal degrees
        longitude (float): Longitude in decimal degrees
        
    Returns:
        tuple: (x, y) pixel coordinates
    """
    # Constants for the map projection
    long1, long2 = 29.24, 30.75
    lat1, lat2 = 60.18, 59.80
    
    # Image dimensions
    width, height = 4113, 3145
    
    # Linear interpolation
    x = (longitude - long1) / (long2 - long1) * width
    y = (lat1 - latitude) / (lat1 - lat2) * height
    
    return (x, y)

def DecimalToPixelVec(latlong):
    """
    Convert (latitude, longitude) tuple to pixel coordinates.
    
    Args:
        latlong (tuple): Tuple of (latitude, longitude) in decimal degrees
        
    Returns:
        tuple: (x, y) pixel coordinates
    """
    return DecimalToPixel(latlong[0], latlong[1])

def PixelToDecimal(longpix, latpix):
    """
    Convert pixel coordinates to decimal coordinates.
    
    Args:
        longpix (float): X pixel coordinate
        latpix (float): Y pixel coordinate
        
    Returns:
        tuple: (latitude, longitude) in decimal degrees
    """
    # Constants for the map projection
    long1, long2 = 29.24, 30.75
    lat1, lat2 = 60.18, 59.80
    
    # Image dimensions
    width, height = 4113, 3145
    
    # Linear interpolation
    longitude = long1 + (longpix / width) * (long2 - long1)
    latitude = lat1 - (latpix / height) * (lat1 - lat2)
    
    return (latitude, longitude)

def PixelToDecimalVec(longlatpix):
    """
    Convert (x, y) pixel coordinates to decimal coordinates.
    
    Args:
        longlatpix (tuple): Tuple of (x, y) pixel coordinates
        
    Returns:
        tuple: (latitude, longitude) in decimal degrees
    """
    return PixelToDecimal(longlatpix[0], longlatpix[1]) 