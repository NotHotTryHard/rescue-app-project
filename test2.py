import sys
from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtWidgets import QApplication, QTableView, QVBoxLayout, QWidget

# Класс, представляющий спасательную станцию
class Station:
    def __init__(self, name, latitude, longitude, speed):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed

# Класс, представляющий модель данных для таблицы
class StationTableModel(QAbstractTableModel):
    def __init__(self, stations):
        super().__init__()
        self.stations = stations
        self.headers = ['Название', 'Широта', 'Долгота', 'Скорость']

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            station = self.stations[index.row()]
            if index.column() == 0:
                return station.name
            elif index.column() == 1:
                return str(station.latitude)
            elif index.column() == 2:
                return str(station.longitude)
            elif index.column() == 3:
                return str(station.speed)

    def rowCount(self, index):
        return len(self.stations)

    def columnCount(self, index):
        return len(self.headers)

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.headers[section]

# Создание приложения
app = QApplication(sys.argv)

# Создание списка спасательных станций
stations = [
    Station('Станция 1', 45.0, 30.0, 50),
    Station('Станция 2', 46.0, 31.0, 60),
    Station('Станция 3', 47.0, 32.0, 70),
]

# Создание модели данных
model = StationTableModel(stations)

# Создание таблицы
view = QTableView()
view.setModel(model)

# Создание окна
window = QWidget()
layout = QVBoxLayout()
layout.addWidget(view)
window.setLayout(layout)

# Отображение окна
window.show()

# Запуск приложения
sys.exit(app.exec())