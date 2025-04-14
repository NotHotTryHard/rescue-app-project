import sys
import os
import json
import pickle
import numpy as np
import numpy.matlib
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import networkx as nx
import scipy
import geopy.distance
from matplotlib import path
from PyQt6 import QtWidgets
from PyQt6.QtCore import QAbstractTableModel, Qt, pyqtSignal, QModelIndex
from PyQt6.QtWidgets import (
    QApplication, QTableView, QVBoxLayout, QWidget, QMessageBox,
    QTabWidget, QLabel, QHBoxLayout, QDialog, QDialogButtonBox
)
from PyQt6.QtGui import QPixmap
import ui_main
import ui_pageAdd
from projectFunctions import *

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
        self.headers = ['№', 'Название', 'Широта', 'Долгота', 'Скорость']

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:  # Номер строки
                return index.row() + 1  # Нумерация с 1
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

    def rowCount(self, index):
        return len(self.stations)

    def columnCount(self, index):
        return len(self.headers)

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.headers[section]

    def flags(self, index):
        return (
            Qt.ItemFlag.ItemIsSelectable |
            Qt.ItemFlag.ItemIsEnabled |
            Qt.ItemFlag.ItemIsEditable
        )

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            station = self.stations[index.row()]
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
        return False

    def addStation(self, station):
        self.beginInsertRows(QModelIndex(), self.rowCount(QModelIndex()), self.rowCount(QModelIndex()))
        self.stations.append(station)
        self.endInsertRows()

    def removeStation(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self.stations[row]
        self.endRemoveRows()

# Класс для дополнительного окна с таблицей для выбора станций
class StationSelectionDialog(QDialog):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Выбор станций для удаления")
        layout = QVBoxLayout()

        self.tableView = QTableView()
        self.tableView.setModel(self.model)
        self.tableView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.tableView.setSelectionMode(QTableView.SelectionMode.MultiSelection)

        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()

        layout.addWidget(self.tableView)

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        # Устанавливаем стиль для черного шрифта
        self.setStyleSheet(
            'background-color: rgb(220, 228, 235); '
            'border: 1px solid rgba(0, 0, 0, 30); '
            'border-radius: 7px; '
            'color: black;'
        )

    def getSelectedRows(self):
        selectedRows = self.tableView.selectionModel().selectedRows()
        return [index.row() for index in selectedRows]

class ResultDialog(QWidget):
    def __init__(self, images, values, plotMask, metricsMask):
        super().__init__()

        self.setWindowTitle("Результаты вычислений")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # Create a tab widget
        self.tab_widget = QTabWidget()

        header_image = [
            'Кратчайшие пути',
            'Сложность достижимости',
            'Разделение зон ответственности'
        ]
        header = [
            "Среднее время спасения",
            "Максимальное время спасения",
            "Условная вероятность спасения (наихудший сценарий) ",
            "Вероятность спасения"
        ]
        filtered_images = [
            elem for elem, m in zip(images, plotMask) if m
        ]
        filtered_values = [
            elem for elem, m in zip(values, metricsMask) if m
        ]
        filtered_header = [
            elem for elem, m in zip(header, metricsMask) if m
        ]
        filtered_header_image = [
            elem for elem, m in zip(header_image, plotMask) if m
        ]

        # Add tabs with images
        for i, image_path in enumerate(filtered_images):
            tab = QWidget()
            tab_layout = QVBoxLayout()

            # Add image
            image_label = QLabel()
            pixmap = QPixmap(image_path)
            image_label.setPixmap(pixmap)
            tab_layout.addWidget(image_label)

            # Add values
            values_layout = QVBoxLayout()

            for value, label_text in zip(filtered_values, filtered_header):
                label = QLabel(f"{label_text}: {value}")
                values_layout.addWidget(label)

            tab_layout.addLayout(values_layout)
            tab.setLayout(tab_layout)
            self.tab_widget.addTab(tab, filtered_header_image[i])

        self.layout.addWidget(self.tab_widget)
        self.setLayout(self.layout)

class StationAddDialog(QtWidgets.QDialog, ui_pageAdd.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавление станции")
        self.setupUi(self)

        # Инициализация переменных
        self.stationName = None
        self.lat_deg = None
        self.lat_min = None
        self.lat_sec = None
        self.long_deg = None
        self.long_min = None
        self.long_sec = None
        self.vel = None

        # Подключение сигналов
        self.pb_save_station.clicked.connect(self.saveStation)

    def get_data(self):
        return [
            self.stationName, self.lat_deg, self.lat_min, self.lat_sec,
            self.long_deg, self.long_min, self.long_sec, self.vel
        ]

    def saveStation(self):
        if self.check_input():
            self.stationName = self.stationName1
            self.lat_deg = self.lat_deg1
            self.lat_min = self.lat_min1
            self.lat_sec = self.lat_sec1
            self.long_deg = self.long_deg1
            self.long_min = self.long_min1
            self.long_sec = self.long_sec1
            self.vel = self.vel1
            self.accept()

    def check_input(self):
        try:
            # Получаем текст из QLineEdit
            self.stationName1 = self.le_stationName.text()
            self.lat_deg1 = float(self.le_lat_deg.text())
            if self.le_lat_min.text() == '':
                self.lat_min1 = 0
            else:
                self.lat_min1 = float(self.le_lat_min.text())

            if self.le_lat_sec.text() == '':
                self.lat_sec1 = 0
            else:
                self.lat_sec1 = float(self.le_lat_sec.text())

            self.long_deg1 = float(self.le_long_deg.text())
            if self.le_long_min.text() == '':
                self.long_min1 = 0
            else:
                self.long_min1 = float(self.le_long_min.text())
            if self.le_long_sec.text() == '':
                self.long_sec1 = 0
            else:
                self.long_sec1 = float(self.le_long_sec.text())

            self.vel1 = float(self.le_stationSpeed.text())
            return True  # Ввод корректен
        except ValueError:
            self.show_error_message()
            return False  # Ввод некорректен

    def show_error_message(self):
        # Создаем и настраиваем окно с сообщением об ошибке
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Ошибка")
        msg.setText("Неверный формат данных")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

class MainWindow(QtWidgets.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        ##############################################################################################################
        # Создание списка спасательных станций
        self.stations = [
            Station('ЦСПС', round(DegreesToDecimalVec((59, 58, 56)), 4), round(DegreesToDecimalVec((30, 13, 19)), 4), 40.0),
            Station('СПС-1', round(DegreesToDecimalVec((60, 11, 17)), 4), round(DegreesToDecimalVec((29, 41, 39)), 4), 40.0),
            Station('СПС-13', round(DegreesToDecimalVec((60, 9, 46)), 4), round(DegreesToDecimalVec((29, 51, 29)), 4), 40.0),
            Station('СПС-23', round(DegreesToDecimalVec((60, 8, 44)), 4), round(DegreesToDecimalVec((29, 55, 30)), 4), 40.0),
            Station('СПС-3', round(DegreesToDecimalVec((60, 5, 31)), 4), round(DegreesToDecimalVec((29, 55, 51)), 4), 40.0),
            Station('СПС-19', round(DegreesToDecimalVec((60, 0, 41.868)), 4), round(DegreesToDecimalVec((29, 57, 52.085)), 4), 40.0),
            Station('СПС-22', round(DegreesToDecimalVec((59, 51, 42)), 4), round(DegreesToDecimalVec((30, 8, 4)), 4), 40.0),
            Station('СПС-10', round(DegreesToDecimalVec((59, 51, 45)), 4), round(DegreesToDecimalVec((30, 2, 44)), 4), 40.0),
            Station('СПС-30', round(DegreesToDecimalVec((59, 54, 33)), 4), round(DegreesToDecimalVec((29, 48, 38)), 4), 40.0),
            Station('СПС-21', round(DegreesToDecimalVec((60, 0, 18.211)), 4), round(DegreesToDecimalVec((29, 43, 0.272)), 4), 40.0),
        ]

        self.stationCoords = np.array([
            ((59, 58, 56), (30, 13, 19)),
            ((60, 11, 17), (29, 41, 39)),
            ((60, 9, 46), (29, 51, 29)),
            ((60, 8, 44), (29, 55, 30)),
            ((60, 5, 31), (29, 55, 51)),
            ((60, 0, 41.868), (29, 57, 52.085)),
            ((59, 51, 42), (30, 8, 4)),
            ((59, 51, 45), (30, 2, 44)),
            ((59, 54, 33), (29, 48, 38)),
            ((60, 0, 18.211), (29, 43, 0.272)),  # kron
        ])

        self.velocities = np.array([40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0])

        ##############################################################################################################

        # Создание модели данных
        self.model = StationTableModel(self.stations)
        # Создание таблицы
        self.tv_stations.setModel(self.model)
        self.tv_stations.resizeColumnsToContents()
        self.init_ui_main()
        self.rb_method_graph.toggled.connect(self.updateFrameStatus)
        self.rb_method_line.toggled.connect(self.updateFrameStatus)
        self.pb_gen_graph.clicked.connect(self.generateGraph)
        self.pb_add_station.clicked.connect(self.openStationAddDialog)
        self.pb_delete_station.clicked.connect(self.openStationSelectionDialog)
        self.pb_start_exp.clicked.connect(self.startExperiment)
        self.le_mesh_width.textChanged.connect(self.activateButtonGG)
        self.le_check_freq.textChanged.connect(self.activateButtonGG)

    def innerDataAdd(self, data):
        """
        Добавляет новый элемент в массивы self.stationCoords и self.velocities.
        """
        new_item = ((data[1], data[2], data[3]), (data[4], data[5], data[6]))
        self.stationCoords = np.append(self.stationCoords, [new_item], axis=0)

        new_velocity = data[7]
        self.velocities = np.append(self.velocities, [new_velocity])

    def innerDataRemove(self, row):
        """
        Удаляет элемент из массивов self.stationCoords и self.velocities по индексу.
        """
        if 0 <= row < len(self.stationCoords):
            self.stationCoords = np.delete(self.stationCoords, row, axis=0)
            self.velocities = np.delete(self.velocities, row)
        else:
            raise IndexError("Индекс вне допустимого диапазона")

    def openStationAddDialog(self):
        dialog = StationAddDialog(self)
        if dialog.exec() == StationAddDialog.DialogCode.Accepted:
            data = dialog.get_data()

            self.innerDataAdd(data)
            self.model.addStation(Station(data[0], round(DegreesToDecimalVec((data[1], data[2], data[3])), 4), round(DegreesToDecimalVec((data[4], data[5], data[6])), 4), data[7]))

    def openStationSelectionDialog(self):
        dialog = StationSelectionDialog(self.model, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selectedRows = dialog.getSelectedRows()
            selectedRows.sort(reverse=True)  # Удаляем с конца, чтобы индексы не сбивались
            for row in selectedRows:
                self.innerDataRemove(row)
                self.model.removeStation(row)

    def openResultWindow(self, plotMask, metricsMask, values):
        images = [
            "output/plot_example.png",
            "output/plot_reachability_example.png",
            "output/plot_reachability_difSt_example.png"
        ]
        self.additional_windows.append(ResultDialog(images, values, plotMask, metricsMask))
        self.additional_windows[-1].show()

    def init_ui_main(self):
        self.rb_method_graph.setChecked(True)
        self.updateFrameStatus()

        self.le_check_freq.setText('40')
        self.le_mesh_width.setText('70')
        self.le_cases_number.setText('5000')
        self.le_median_lifespan.setText('10')
        self.le_max_lifespan.setText('25')
        self.cb_plot_closest_paths.setChecked(True)
        self.cb_metr_avg_time.setChecked(True)
        self.cb_metr_peak_time.setChecked(True)
        self.cb_metr_avg_prob.setChecked(True)
        self.cb_metr_peak_prob.setChecked(True)
        self.additional_windows = []
        self.deactivateButtonGG('Такой граф уже сгененирован')

    def generateGraph(self):
        errorFlag = self.check_input_GG()
        if not errorFlag:
            if os.path.isfile(f'graphs/saved_graph_{self.mesh_width}_{self.check_freq}.pkl'):
                self.deactivateButtonGG('Такой граф уже сгененирован')
            else:
                G, Gmesh, Gmask = makeGraph(self.mesh_width, self.check_freq)
                with open(f'graphs/saved_graph_{self.mesh_width}_{self.check_freq}.pkl', 'wb') as f:
                    pickle.dump({'G': G, 'Gmesh': Gmesh, 'Gmask': Gmask}, f)
                self.deactivateButtonGG('Граф был добавлен')

    def startExperiment(self):
        errorFlag = self.check_input_SE()

        if not errorFlag:
            plotMask = [
                self.cb_plot_closest_paths.isChecked(),
                self.cb_plot_map_reachability.isChecked(),
                self.cb_plot_map_difst_reachability.isChecked()
            ]
            metricsMask = [
                self.cb_metr_avg_time.isChecked(),
                self.cb_metr_peak_time.isChecked(),
                self.cb_metr_avg_prob.isChecked(),
                self.cb_metr_peak_prob.isChecked()
            ]

            if self.rb_method_line.isChecked():
                ptsFromPix, ptsToPix, ptsToMinTimes, plotData = expMakeLine(
                    self.stationCoords, self.velocities, self.cases_number
                )
                values = [
                    round(np.mean(ptsToMinTimes) * 60, 3),
                    round(np.max(ptsToMinTimes) * 60, 3),
                    round(probsFromTimes(np.max(ptsToMinTimes) * 60 + 1.5, self.median_lifespan, self.max_lifespan).mean(), 3),
                    round(probsFromTimes(ptsToMinTimes * 60 + 1.5, self.median_lifespan, self.max_lifespan).mean(), 3)
                ]

                if plotMask[0]:
                    PlotMap(ptsFromPix, ptsToPix, plotData, 0.75, True, True)

                if plotMask[1] or plotMask[2]:
                    width = 4113
                    height = 3145
                    l = 7
                    nxt, nyt = (int(width / l), int(height / l))
                    x = np.linspace(0, width, nxt)
                    y = np.linspace(0, height, nyt)
                    xv, yv = np.meshgrid(x, y)
                    x = xv.flatten()
                    y = yv.flatten()
                    yrev = -(y - height)
                    ptsToPix = np.append(np.array([x]), np.array([yrev]), axis=0).T

                    ptsToPix, ptsToMinTimes, plotData = ClosestPathWithTraceNew(ptsFromPix, ptsToPix, self.velocities)
                    if plotMask[1]:
                        PlotMapReachability(ptsFromPix, ptsToPix, plotData, 1, True, False)
                    if plotMask[2]:
                        PlotMapDifStReachability(ptsFromPix, ptsToPix, plotData, 1, True, False)

                self.openResultWindow(plotMask, metricsMask, values)

            elif self.rb_method_graph.isChecked():
                errorFlag = self.check_input_GG()

                if not errorFlag:
                    if os.path.isfile(f'graphs/saved_graph_{self.mesh_width}_{self.check_freq}.pkl'):
                        with open(f'graphs/saved_graph_{self.mesh_width}_{self.check_freq}.pkl', 'rb') as f:
                            data = pickle.load(f)
                            G = data['G']
                            Gmesh = data['Gmesh']
                            Gmask = data['Gmask']
                    else:
                        G, Gmesh, Gmask = makeGraph(self.mesh_width, self.check_freq)
                        with open(f'graphs/saved_graph_{self.mesh_width}_{self.check_freq}.pkl', 'wb') as f:
                            pickle.dump({'G': G, 'Gmesh': Gmesh, 'Gmask': Gmask}, f)
                    ptsFromPix, ptsToPix, ptsToMinTimes, plotData = expMakeGraph(
                        self.stationCoords, self.velocities, self.cases_number, G, Gmesh, Gmask
                    )
                    values = [
                        round(np.mean(ptsToMinTimes) * 60, 2),
                        round(np.max(ptsToMinTimes) * 60, 2),
                        round(probsFromTimes(np.max(ptsToMinTimes) * 60 + 1.5, self.median_lifespan, self.max_lifespan).mean(), 3),
                        round(probsFromTimes(ptsToMinTimes * 60 + 1.5, self.median_lifespan, self.max_lifespan).mean(), 3)
                    ]

                    if plotMask[0]:
                        PlotMap(ptsFromPix, ptsToPix, plotData, 0.75, True, True)

                    if plotMask[1] or plotMask[2]:
                        width = 4113
                        height = 3145
                        l = 7
                        nxt, nyt = (int(width / l), int(height / l))
                        x = np.linspace(0, width, nxt)
                        y = np.linspace(0, height, nyt)
                        xv, yv = np.meshgrid(x, y)
                        x = xv.flatten()
                        y = yv.flatten()
                        yrev = -(y - height)
                        ptsToPix = np.append(np.array([x]), np.array([yrev]), axis=0).T

                        ptsToPix, ptsToMinTimes, plotData = ClosestPathWithTraceDijkstra(
                            ptsFromPix, ptsToPix, self.velocities, G, Gmesh, Gmask
                        )

                        if plotMask[1]:
                            PlotMapReachability(ptsFromPix, ptsToPix, plotData, 1, True, False)
                        if plotMask[2]:
                            PlotMapDifStReachability(ptsFromPix, ptsToPix, plotData, 1, True, False)

                    self.openResultWindow(plotMask, metricsMask, values)
        #self.activateButton()

        self.pb_start_exp.setEnabled(True)
        self.pb_start_exp.setText('Запуск')
        self.pb_start_exp.setStyleSheet(
            'color: black;'
        )

    def check_input_SE(self):
        errorFlag = False
        # Получаем текст из QLineEdit

        try:
            # Пытаемся конвертировать текст в float
            self.cases_number = int(self.le_cases_number.text())
            self.median_lifespan = float(self.le_median_lifespan.text())
            self.max_lifespan = float(self.le_max_lifespan.text())

        except ValueError:
            # Если возникает ошибка, показываем окно с сообщением
            errorFlag = True
            self.show_error_message()
        return errorFlag

    def check_input_GG(self):
        errorFlag = False
        # Получаем текст из QLineEdit

        try:
            # Пытаемся конвертировать текст в float
            self.mesh_width = int(self.le_mesh_width.text())
            self.check_freq = int(self.le_check_freq.text())

        except ValueError:
            # Если возникает ошибка, показываем окно с сообщением
            errorFlag = True
            self.show_error_message()
        return errorFlag

    def show_error_message(self):
        # Создаем и настраиваем окно с сообщением об ошибке
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Ошибка")
        msg.setText("Неверный формат данных")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def updateFrameStatus(self):
        self.graph_frame.setEnabled(self.rb_method_graph.isChecked())
        self.updateFrameStyle()

    def updateFrameStyle(self):
        if self.graph_frame.isEnabled():
            self.graph_frame.setStyleSheet(
                'background-color: rgba(255, 255, 255, 30); '
                'border: 1px solid rgba(0, 0, 0, 30); '
                'border-radius: 7px; '
                'color: black;'
            )
        else:
            self.graph_frame.setStyleSheet(
                'background-color: rgba(255, 255, 255, 30); '
                'border: 1px solid rgba(0, 0, 0, 30); '
                'border-radius: 7px; '
                'color: grey; '
                'opacity: 0.5;'
            )

    def deactivateButtonGG(self, text=None):
        self.pb_gen_graph.setDisabled(True)

        if text==None:
            self.pb_gen_graph.setText('Граф добавлен')
        else:
            self.pb_gen_graph.setText(text)
        self.pb_gen_graph.setStyleSheet(
            'color: grey;'
            'opacity: 0.5;'
        ) 

    def activateButtonGG(self):
        self.pb_gen_graph.setEnabled(True)
        self.pb_gen_graph.setText('Сгенерировать граф')
        self.pb_gen_graph.setStyleSheet(
            'color: black;'
        )

    def deactivateButton(self):
        self.pb_start_exp.setDisabled(True)
        self.pb_start_exp.setText('Вычисление...')
        self.pb_start_exp.setStyleSheet(
            'color: grey;'
            'opacity: 0.5;'
        )

    def activateButton(self):
        self.pb_start_exp.setEnabled(True)
        self.pb_start_exp.setText('Запуск')
        self.pb_start_exp.setStyleSheet(
            'color: black;'
        )


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainWindow()  # Создаём объект класса MainWindow
    window.show()  # Показываем окно
    app.exec()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
