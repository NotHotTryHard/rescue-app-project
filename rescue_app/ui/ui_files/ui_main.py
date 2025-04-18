from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1112, 506)
        MainWindow.setStyleSheet("background-color: rgb(220, 228, 235)")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.method_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.method_frame.setStyleSheet("background-color: rgba(255, 255, 255, 30);\n"
"border: 1px solid rgba(0, 0, 0, 30);\n"
"border-radius: 7px;\n"
"color: black;")
        self.method_frame.setObjectName("method_frame")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.method_frame)
        self.verticalLayout_12.setContentsMargins(8, 1, -1, 16)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_4 = QtWidgets.QLabel(parent=self.method_frame)
        self.label_4.setStyleSheet("color: black;\n"
"font-weight: bold;\n"
"font-size: 15pt;\n"
"background-color: none;\n"
"border: none;")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_12.addWidget(self.label_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.rb_method_graph = QtWidgets.QRadioButton(parent=self.method_frame)
        self.rb_method_graph.setObjectName("rb_method_graph")
        self.verticalLayout.addWidget(self.rb_method_graph)
        self.rb_method_line = QtWidgets.QRadioButton(parent=self.method_frame)
        self.rb_method_line.setObjectName("rb_method_line")
        self.verticalLayout.addWidget(self.rb_method_line)
        self.verticalLayout_5.addLayout(self.verticalLayout)
        self.verticalLayout_12.addLayout(self.verticalLayout_5)
        self.horizontalLayout_4.addWidget(self.method_frame)
        self.graph_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.graph_frame.setStyleSheet("background-color: rgba(255, 255, 255, 30);\n"
"border: 1px solid rgba(0, 0, 0, 30);\n"
"border-radius: 7px;\n"
"color: black;")
        self.graph_frame.setObjectName("graph_frame")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.graph_frame)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label = QtWidgets.QLabel(parent=self.graph_frame)
        self.label.setStyleSheet("\n"
"font-weight: bold;\n"
"font-size: 15pt;\n"
"background-color: none;\n"
"border: none;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_11.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(parent=self.graph_frame)
        self.label_2.setStyleSheet("background-color: none;\n"
"border: none;")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(parent=self.graph_frame)
        self.label_3.setStyleSheet("background-color: none;\n"
"border: none;")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.le_mesh_width = QtWidgets.QLineEdit(parent=self.graph_frame)
        self.le_mesh_width.setObjectName("le_mesh_width")
        self.verticalLayout_2.addWidget(self.le_mesh_width)
        self.le_check_freq = QtWidgets.QLineEdit(parent=self.graph_frame)
        self.le_check_freq.setObjectName("le_check_freq")
        self.verticalLayout_2.addWidget(self.le_check_freq)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_11.addLayout(self.horizontalLayout)
        self.pb_gen_graph = QtWidgets.QPushButton(parent=self.graph_frame)
        self.pb_gen_graph.setObjectName("pb_gen_graph")
        self.verticalLayout_11.addWidget(self.pb_gen_graph)
        self.horizontalLayout_4.addWidget(self.graph_frame)
        self.verticalLayout_13.addLayout(self.horizontalLayout_4)
        self.stations_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.stations_frame.setStyleSheet("color: black;\n"
"background-color: rgba(255, 255, 255, 30);\n"
"border: 1px solid rgba(0, 0, 0, 30);\n"
"border-radius: 7px;")
        self.stations_frame.setObjectName("stations_frame")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.stations_frame)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_5 = QtWidgets.QLabel(parent=self.stations_frame)
        self.label_5.setStyleSheet("color: black;\n"
"font-weight: bold;\n"
"font-size: 15pt;\n"
"background-color: none;\n"
"border: none;")
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_6.addWidget(self.label_5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pb_add_station = QtWidgets.QPushButton(parent=self.stations_frame)
        self.pb_add_station.setObjectName("pb_add_station")
        self.horizontalLayout_2.addWidget(self.pb_add_station)
        self.pb_delete_station = QtWidgets.QPushButton(parent=self.stations_frame)
        self.pb_delete_station.setObjectName("pb_delete_station")
        self.horizontalLayout_2.addWidget(self.pb_delete_station)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.tv_stations = QtWidgets.QTableView(parent=self.stations_frame)
        self.tv_stations.setStyleSheet("QTableView {\n"
"background-color: rgba(255, 255, 255, 30);\n"
"border: 1px solid rgba(0, 0, 0, 30);\n"
"border-radius: 7px;\n"
"}\n"
"\n"
"QTableView::section {\n"
"background-color: rgba(230, 230, 230);\n"
"color: black;\n"
"border: none;\n"
"height: 50px;\n"
"font-size:15pt;\n"
"}\n"
"\n"
"QTableView::item {\n"
"border-style: none;\n"
"border-bottom: rgba(0, 0, 0, 40);\n"
"}\n"
"\n"
"QTableView::item:selected {\n"
"border: none;\n"
"color: rgba(0, 0, 0);\n"
"background-color: rgba(255, 255, 255, 50);\n"
"}")
        self.tv_stations.setObjectName("tv_stations")
        self.verticalLayout_6.addWidget(self.tv_stations)
        self.verticalLayout_13.addWidget(self.stations_frame)
        self.horizontalLayout_5.addLayout(self.verticalLayout_13)
        self.exec_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.exec_frame.setStyleSheet("color: black;\n"
"background-color: rgba(255, 255, 255, 30);\n"
"border: 1px solid rgba(0, 0, 0, 30);\n"
"border-radius: 7px;")
        self.exec_frame.setObjectName("exec_frame")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.exec_frame)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_6 = QtWidgets.QLabel(parent=self.exec_frame)
        self.label_6.setStyleSheet("color: black;\n"
"font-weight: bold;\n"
"font-size: 20pt;\n"
"background-color: none;\n"
"border: none;")
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_10.addWidget(self.label_6)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_7 = QtWidgets.QLabel(parent=self.exec_frame)
        self.label_7.setStyleSheet("background-color: none;\n"
"border: none;")
        self.label_7.setObjectName("label_7")
        self.verticalLayout_7.addWidget(self.label_7)
        self.label_11 = QtWidgets.QLabel(parent=self.exec_frame)
        self.label_11.setStyleSheet("background-color: none;\n"
"border: none;")
        self.label_11.setObjectName("label_11")
        self.verticalLayout_7.addWidget(self.label_11)
        self.label_10 = QtWidgets.QLabel(parent=self.exec_frame)
        self.label_10.setStyleSheet("background-color: none;\n"
"border: none;")
        self.label_10.setObjectName("label_10")
        self.verticalLayout_7.addWidget(self.label_10)
        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.le_cases_number = QtWidgets.QLineEdit(parent=self.exec_frame)
        self.le_cases_number.setObjectName("le_cases_number")
        self.verticalLayout_4.addWidget(self.le_cases_number)
        self.le_max_lifespan = QtWidgets.QLineEdit(parent=self.exec_frame)
        self.le_max_lifespan.setObjectName("le_max_lifespan")
        self.verticalLayout_4.addWidget(self.le_max_lifespan)
        self.le_median_lifespan = QtWidgets.QLineEdit(parent=self.exec_frame)
        self.le_median_lifespan.setObjectName("le_median_lifespan")
        self.verticalLayout_4.addWidget(self.le_median_lifespan)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout_10.addLayout(self.horizontalLayout_3)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_8 = QtWidgets.QLabel(parent=self.exec_frame)
        self.label_8.setStyleSheet("color: black;\n"
"font-weight: bold;\n"
"font-size: 15pt;\n"
"background-color: none;\n"
"border: none;")
        self.label_8.setObjectName("label_8")
        self.verticalLayout_8.addWidget(self.label_8)
        self.cb_plot_closest_paths = QtWidgets.QCheckBox(parent=self.exec_frame)
        self.cb_plot_closest_paths.setObjectName("cb_plot_closest_paths")
        self.verticalLayout_8.addWidget(self.cb_plot_closest_paths)
        self.cb_plot_map_reachability = QtWidgets.QCheckBox(parent=self.exec_frame)
        self.cb_plot_map_reachability.setObjectName("cb_plot_map_reachability")
        self.verticalLayout_8.addWidget(self.cb_plot_map_reachability)
        self.cb_plot_map_difst_reachability = QtWidgets.QCheckBox(parent=self.exec_frame)
        self.cb_plot_map_difst_reachability.setObjectName("cb_plot_map_difst_reachability")
        self.verticalLayout_8.addWidget(self.cb_plot_map_difst_reachability)
        self.verticalLayout_10.addLayout(self.verticalLayout_8)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_9 = QtWidgets.QLabel(parent=self.exec_frame)
        self.label_9.setStyleSheet("color: black;\n"
"font-weight: bold;\n"
"font-size: 15pt;\n"
"background-color: none;\n"
"border: none;")
        self.label_9.setObjectName("label_9")
        self.verticalLayout_9.addWidget(self.label_9)
        self.cb_metr_avg_time = QtWidgets.QCheckBox(parent=self.exec_frame)
        self.cb_metr_avg_time.setObjectName("cb_metr_avg_time")
        self.verticalLayout_9.addWidget(self.cb_metr_avg_time)
        self.cb_metr_peak_time = QtWidgets.QCheckBox(parent=self.exec_frame)
        self.cb_metr_peak_time.setObjectName("cb_metr_peak_time")
        self.verticalLayout_9.addWidget(self.cb_metr_peak_time)
        self.cb_metr_avg_prob = QtWidgets.QCheckBox(parent=self.exec_frame)
        self.cb_metr_avg_prob.setObjectName("cb_metr_avg_prob")
        self.verticalLayout_9.addWidget(self.cb_metr_avg_prob)
        self.cb_metr_peak_prob = QtWidgets.QCheckBox(parent=self.exec_frame)
        self.cb_metr_peak_prob.setObjectName("cb_metr_peak_prob")
        self.verticalLayout_9.addWidget(self.cb_metr_peak_prob)
        self.verticalLayout_10.addLayout(self.verticalLayout_9)
        self.pb_start_exp = QtWidgets.QPushButton(parent=self.exec_frame)
        self.pb_start_exp.setObjectName("pb_start_exp")
        self.verticalLayout_10.addWidget(self.pb_start_exp)
        self.horizontalLayout_5.addWidget(self.exec_frame)
        self.verticalLayout_14.addLayout(self.horizontalLayout_5)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Rescue App"))
        self.label_4.setText(_translate("MainWindow", "Выбор метода"))
        self.rb_method_graph.setText(_translate("MainWindow", "Метод графов"))
        self.rb_method_line.setText(_translate("MainWindow", "Метод прямых"))
        self.label.setText(_translate("MainWindow", "Параметры метода графов"))
        self.label_2.setText(_translate("MainWindow", "Ширина клетки"))
        self.label_3.setText(_translate("MainWindow", "Частота проверки"))
        self.pb_gen_graph.setText(_translate("MainWindow", "Сгенерировать граф"))
        self.label_5.setText(_translate("MainWindow", "Спасательные станции"))
        self.pb_add_station.setText(_translate("MainWindow", "Добавить станцию"))
        self.pb_delete_station.setText(_translate("MainWindow", "Удалить станцию"))
        self.label_6.setText(_translate("MainWindow", "Запуск эксперимента"))
        self.label_7.setText(_translate("MainWindow", "Количество происшествий"))
        self.label_11.setText(_translate("MainWindow", "Предельное время пребывания в воде (мин)"))
        self.label_10.setText(_translate("MainWindow", "Медианное время пребывания в воде (мин)"))
        self.le_cases_number.setPlaceholderText(_translate("MainWindow", "(прим. 10000)"))
        self.le_max_lifespan.setPlaceholderText(_translate("MainWindow", "(прим. 25)"))
        self.le_median_lifespan.setPlaceholderText(_translate("MainWindow", "(прим. 10)"))
        self.label_8.setText(_translate("MainWindow", "Графики"))
        self.cb_plot_closest_paths.setText(_translate("MainWindow", "Кратчайшие пути"))
        self.cb_plot_map_reachability.setText(_translate("MainWindow", "Сложность достижимости"))
        self.cb_plot_map_difst_reachability.setText(_translate("MainWindow", "Разделение зон ответственности"))
        self.label_9.setText(_translate("MainWindow", "Метрики"))
        self.cb_metr_avg_time.setText(_translate("MainWindow", "Среднее время спасения"))
        self.cb_metr_peak_time.setText(_translate("MainWindow", "Максимальное время спасения"))
        self.cb_metr_avg_prob.setText(_translate("MainWindow", "Условная вероятность спасения (наихудший сценарий) "))
        self.cb_metr_peak_prob.setText(_translate("MainWindow", "Вероятность спасения"))
        self.pb_start_exp.setText(_translate("MainWindow", "Запуск")) 