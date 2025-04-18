"""
Station model representing a rescue station with location and speed information.
"""

class Station:
    """
    Represents a rescue station with a name, geographical coordinates, and speed capability.
    """
    
    def __init__(self, name, latitude, longitude, speed):
        """
        Initialize a rescue station.
        
        Args:
            name (str): Station name
            latitude (float): Station latitude in decimal format
            longitude (float): Station longitude in decimal format
            speed (float): Station speed capability in km/h
        """
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed
    
    def __repr__(self):
        """Return string representation of the station."""
        return f"Station(name='{self.name}', lat={self.latitude}, long={self.longitude}, speed={self.speed})"
        
    def get_coordinates(self):
        """Return the coordinates as a tuple."""
        return (self.latitude, self.longitude) 