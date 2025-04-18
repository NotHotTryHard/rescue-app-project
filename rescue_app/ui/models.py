"""
UI data models for the rescue application.
"""

from PyQt6.QtCore import QAbstractTableModel, Qt, pyqtSignal, QModelIndex

class StationTableModel(QAbstractTableModel):
    """
    Table model for displaying and editing rescue stations.
    """
    
    def __init__(self, stations=None):
        """
        Initialize the station table model.
        
        Args:
            stations (list): List of Station objects
        """
        super().__init__()
        self.stations = stations or []
        self.headers = ['№', 'Название', 'Широта', 'Долгота', 'Скорость']

    def data(self, index, role):
        """Return the data at the given index for the specified role."""
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:  # Row number
                return index.row() + 1  # 1-based numbering
            else:
                station = self.stations[index.row()]
                if index.column() == 1:
                    return station.name
                elif index.column() == 2:
                    return str(station.latitude)
                elif index.column() == 3:
                    return str(station.longitude)
                elif index.column() == 4:
                    return str(station.speed)
        return None

    def rowCount(self, index):
        """Return the number of rows."""
        return len(self.stations)

    def columnCount(self, index):
        """Return the number of columns."""
        return len(self.headers)

    def headerData(self, section, orientation, role):
        """Return the header data for the given section and orientation."""
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.headers[section]
        return None

    def flags(self, index):
        """Return the flags for the given index."""
        return (
            Qt.ItemFlag.ItemIsSelectable |
            Qt.ItemFlag.ItemIsEnabled |
            Qt.ItemFlag.ItemIsEditable
        )

    def setData(self, index, value, role):
        """Set the data at the given index for the specified role."""
        if role == Qt.ItemDataRole.EditRole:
            station = self.stations[index.row()]
            try:
                if index.column() == 1:
                    station.name = value
                elif index.column() == 2:
                    station.latitude = float(value)
                elif index.column() == 3:
                    station.longitude = float(value)
                elif index.column() == 4:
                    station.speed = float(value)
                self.dataChanged.emit(index, index)
                return True
            except ValueError:
                # Handle conversion errors
                return False
        return False

    def addStation(self, station):
        """Add a new station to the model."""
        self.beginInsertRows(QModelIndex(), self.rowCount(QModelIndex()), self.rowCount(QModelIndex()))
        self.stations.append(station)
        self.endInsertRows()

    def removeStation(self, row):
        """Remove a station from the model by row index."""
        self.beginRemoveRows(QModelIndex(), row, row)
        del self.stations[row]
        self.endRemoveRows()
        
    def getStations(self):
        """Get all stations as a list."""
        return self.stations 