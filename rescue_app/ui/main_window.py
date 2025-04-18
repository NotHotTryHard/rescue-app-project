"""
Main window implementation for the rescue application.
"""

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLabel, QApplication, QScrollArea, QStatusBar, QGraphicsDropShadowEffect
from PyQt6.QtCore import QTimer, QSize, Qt
from PyQt6.QtGui import QMovie, QFont, QColor, QPalette

import numpy as np
import os

from .ui_files.ui_main import Ui_MainWindow
from .models import StationTableModel
from .dialogs import StationAddDialog, StationSelectionDialog, ResultDialog
from ..models import Station
from ..core import Experiment
from ..utils.coordinates import DegreesToDecimalVec
from ..config import DEFAULT_STATIONS, DEFAULT_STATION_COORDS, DEFAULT_VELOCITIES


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main application window handling UI interactions.
    """
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.setupUi(self)  # Setup the UI from the generated file
        
        # Set window title and icon
        self.setWindowTitle("Rescue App - Станции спасения")
        
        # Improve visual style
        self.apply_styles()
        
        # Initialize station data
        self.stations = [
            Station(name, latitude, longitude, speed)
            for name, latitude, longitude, speed in DEFAULT_STATIONS
        ]
        
        # Keep the raw coordinate data for computations
        self.stationCoords = DEFAULT_STATION_COORDS.copy()
        self.velocities = DEFAULT_VELOCITIES.copy()
        
        # Initialize the experiment
        self.experiment = Experiment()
        self.experiment.set_stations(self.stationCoords, self.velocities)
        
        # Setup the model and table
        self.model = StationTableModel(self.stations)
        self.tv_stations.setModel(self.model)
        self.tv_stations.resizeColumnsToContents()
        
        # Setup loading animation
        self.setup_loading_animation()
        
        # Setup UI and connections
        self.init_ui_main()
        self.connect_signals()
        
        # List to store additional dialogs/windows
        self.additional_windows = []
        
    def apply_styles(self):
        """Apply custom styles to the UI elements."""
        # Set a nicer font for the application
        font = QFont("Segoe UI", 10)
        self.setFont(font)

        # Set application background
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFF5E9;
            }
        """)
        
        # Create a warm orange color palette
        primary_color = "#FF8C00"      # Dark Orange
        secondary_color = "#FFA500"    # Orange
        accent_color = "#FF4500"       # OrangeRed
        text_color = "#333333"         # Dark Gray
        light_text = "#666666"         # Medium Gray
        bg_color = "#FFF5E9"           # Very Light Orange
        
        # Style buttons
        button_style = f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {secondary_color};
            }}
            QPushButton:pressed {{
                background-color: {accent_color};
            }}
            QPushButton:disabled {{
                background-color: #dddddd;
                color: #999999;
            }}
        """
        
        self.pb_gen_graph.setStyleSheet(button_style)
        self.pb_add_station.setStyleSheet(button_style)
        self.pb_delete_station.setStyleSheet(button_style)
        self.pb_start_exp.setStyleSheet(button_style)
        
        # Style frames with soft shadows and subtle gradient
        frame_style = f"""
            QFrame {{
                background-color: white;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }}
        """
        
        self.method_frame.setStyleSheet(frame_style)
        self.graph_frame.setStyleSheet(frame_style)
        self.stations_frame.setStyleSheet(frame_style)
        self.exec_frame.setStyleSheet(frame_style)
        
        # Add shadow effects to frames for depth
        for frame in [self.method_frame, self.graph_frame, self.stations_frame, self.exec_frame]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setColor(QColor(0, 0, 0, 30))
            shadow.setOffset(0, 2)
            frame.setGraphicsEffect(shadow)
        
        # Style table
        table_style = f"""
            QTableView {{
                background-color: white;
                border: none;
                border-radius: 6px;
                gridline-color: #eeeeee;
                selection-background-color: #FFF0E0;
                selection-color: {text_color};
                alternate-background-color: #FAFAFA;
            }}
            QHeaderView::section {{
                background-color: {primary_color};
                color: white;
                font-weight: bold;
                padding: 6px;
                border: none;
                border-right: 1px solid white;
            }}
            QTableView::item {{
                padding: 4px;
                border-bottom: 1px solid #f0f0f0;
            }}
        """
        
        self.tv_stations.setStyleSheet(table_style)
        self.tv_stations.setAlternatingRowColors(True)
        
        # Style radio buttons and checkboxes
        toggle_style = f"""
            QRadioButton, QCheckBox {{
                spacing: 8px;
                color: {text_color};
            }}
            QRadioButton::indicator, QCheckBox::indicator {{
                width: 18px;
                height: 18px;
            }}
            QRadioButton::indicator::unchecked {{
                border: 2px solid {primary_color};
                background-color: white;
                border-radius: 9px;
            }}
            QRadioButton::indicator::checked {{
                border: 2px solid {primary_color};
                background-color: {primary_color};
                border-radius: 9px;
            }}
            QCheckBox::indicator::unchecked {{
                border: 2px solid {primary_color};
                background-color: white;
                border-radius: 4px;
            }}
            QCheckBox::indicator::checked {{
                border: 2px solid {primary_color};
                background-color: {primary_color};
                border-radius: 4px;
            }}
        """
        
        self.rb_method_graph.setStyleSheet(toggle_style)
        self.rb_method_line.setStyleSheet(toggle_style)
        
        self.cb_plot_closest_paths.setStyleSheet(toggle_style)
        self.cb_plot_map_reachability.setStyleSheet(toggle_style)
        self.cb_plot_map_difst_reachability.setStyleSheet(toggle_style)
        
        self.cb_metr_avg_time.setStyleSheet(toggle_style)
        self.cb_metr_peak_time.setStyleSheet(toggle_style)
        self.cb_metr_avg_prob.setStyleSheet(toggle_style)
        self.cb_metr_peak_prob.setStyleSheet(toggle_style)
        
        # Style line edits
        lineedit_style = f"""
            QLineEdit {{
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                background-color: white;
            }}
            QLineEdit:focus {{
                border: 1px solid {primary_color};
            }}
        """
        
        self.le_mesh_width.setStyleSheet(lineedit_style)
        self.le_check_freq.setStyleSheet(lineedit_style)
        self.le_cases_number.setStyleSheet(lineedit_style)
        self.le_max_lifespan.setStyleSheet(lineedit_style)
        self.le_median_lifespan.setStyleSheet(lineedit_style)
        
        # Apply styles to section headings
        header_style = f"""
            font-weight: bold;
            font-size: 16px;
            color: {text_color};
            padding-bottom: 8px;
        """
        
        self.label_4.setStyleSheet(header_style)
        self.label.setStyleSheet(header_style)
        self.label_5.setStyleSheet(header_style)
        self.label_6.setStyleSheet(header_style)
        self.label_8.setStyleSheet(header_style)
        self.label_9.setStyleSheet(header_style)
        
    def setup_loading_animation(self):
        """Setup the loading animation widget."""
        # This method is kept empty but maintained for compatibility
        # All animation functionality has been removed to fix glitches
        pass
        
    def update_text_animation(self):
        """Update the text-based loading animation."""
        # This method is kept empty but maintained for compatibility
        pass
        
    def init_ui_main(self):
        """Initialize the main window UI."""
        # Define color variables needed for styling
        primary_color = "#FF8C00"      # Dark Orange
        secondary_color = "#FFA500"    # Orange
        text_color = "#333333"         # Dark Gray
        
        # Save theme colors as class variables for use in other methods
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.text_color = text_color
        
        # Set default values
        self.rb_method_graph.setChecked(True)
        self.updateFrameStatus()
        
        self.le_check_freq.setText('40')
        self.le_mesh_width.setText('70')
        self.le_cases_number.setText('5000')
        self.le_median_lifespan.setText('10')
        self.le_max_lifespan.setText('25')
        
        # Set default checkboxes
        self.cb_plot_closest_paths.setChecked(True)
        self.cb_metr_avg_time.setChecked(True)
        self.cb_metr_peak_time.setChecked(True)
        self.cb_metr_avg_prob.setChecked(True)
        self.cb_metr_peak_prob.setChecked(True)
        
        # Add display settings to the Графики section
        # Find the existing vertical layout in the plots section
        plot_frame_layout = self.verticalLayout_8
        
        # Settings for the display section
        plot_frame_layout.addWidget(QtWidgets.QWidget())  # Add spacing
        
        # Add display settings title
        display_title = QtWidgets.QLabel("Настройки отображения графиков")
        display_title.setStyleSheet(f"""
            font-weight: bold;
            font-size: 16px;
            color: {text_color};
            padding-bottom: 5px;
        """)
        plot_frame_layout.addWidget(display_title)
        
        # Create horizontal layout for controls
        display_controls = QtWidgets.QHBoxLayout()
        
        # Station names toggle
        self.cb_show_station_names = QtWidgets.QCheckBox("Показывать названия станций")
        self.cb_show_station_names.setChecked(True)
        self.cb_show_station_names.setStyleSheet(f"""
            QCheckBox {{
                spacing: 8px;
                color: {text_color};
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
            }}
            QCheckBox::indicator::unchecked {{
                border: 2px solid {primary_color};
                background-color: white;
                border-radius: 4px;
            }}
            QCheckBox::indicator::checked {{
                border: 2px solid {primary_color};
                background-color: {primary_color};
                border-radius: 4px;
            }}
        """)
        display_controls.addWidget(self.cb_show_station_names)
        
        # Add spacer
        display_controls.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))
        
        # Quality selector - combine into one control
        self.quality_selector = QtWidgets.QComboBox()
        self.quality_selector.addItem("Стандартное (300 dpi)")
        self.quality_selector.addItem("Высокое (600 dpi)")
        self.quality_selector.addItem("Максимальное (900 dpi)")
        self.quality_selector.setStyleSheet(f"""
            QComboBox {{
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                background-color: white;
                min-width: 200px;
            }}
            QComboBox:focus {{
                border: 1px solid {primary_color};
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #e0e0e0;
            }}
            QComboBox::down-arrow {{
                image: none;
                width: 0;
            }}
            QComboBox QAbstractItemView {{
                border: 1px solid #e0e0e0;
                border-radius: 0px;
                background-color: white;
                selection-background-color: #FFF0E0;
                selection-color: {text_color};
            }}
        """)
        display_controls.addWidget(self.quality_selector)
        
        # Add controls to the layout
        plot_frame_layout.addLayout(display_controls)
        
        # Set tooltips for better user experience
        self.le_mesh_width.setToolTip("Ширина ячейки сетки для метода графов (по умолчанию 70)")
        self.le_check_freq.setToolTip("Частота проверки пересечения с сушей (по умолчанию 40)")
        self.le_cases_number.setToolTip("Количество случайных точек для моделирования (рекомендуется не менее 1000)")
        self.le_median_lifespan.setToolTip("Медианное время выживания в воде (в минутах)")
        self.le_max_lifespan.setToolTip("Максимальное время выживания в воде (в минутах)")
        self.cb_show_station_names.setToolTip("Отображать названия станций на графиках")
        self.quality_selector.setToolTip("Качество отображения графиков (влияет на четкость изображений)")
        
        # Disable graph button initially
        self.deactivateButtonGG('Такой граф уже сгененирован')
        
    def connect_signals(self):
        """Connect UI signals to their handlers."""
        # Method selection
        self.rb_method_graph.toggled.connect(self.updateFrameStatus)
        self.rb_method_line.toggled.connect(self.updateFrameStatus)
        
        # Buttons
        self.pb_gen_graph.clicked.connect(self.generateGraph)
        self.pb_add_station.clicked.connect(self.openStationAddDialog)
        self.pb_delete_station.clicked.connect(self.openStationSelectionDialog)
        self.pb_start_exp.clicked.connect(self.startExperiment)
        
        # Input validation
        self.le_mesh_width.textChanged.connect(self.activateButtonGG)
        self.le_check_freq.textChanged.connect(self.activateButtonGG)
        
    def openStationAddDialog(self):
        """Open dialog to add a new station."""
        dialog = StationAddDialog(self)
        if dialog.exec() == StationAddDialog.DialogCode.Accepted:
            data = dialog.get_data()
            
            # Add to internal data arrays
            self.innerDataAdd(data)
            
            # Create a new station and add to model
            station = Station(
                data[0],
                round(DegreesToDecimalVec((data[1], data[2], data[3])), 4),
                round(DegreesToDecimalVec((data[4], data[5], data[6])), 4),
                data[7]
            )
            self.model.addStation(station)
            
            # Update experiment data
            self.experiment.set_stations(self.stationCoords, self.velocities)
            
    def openStationSelectionDialog(self):
        """Open dialog to select and delete stations."""
        dialog = StationSelectionDialog(self.model, self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            selectedRows = dialog.getSelectedRows()
            selectedRows.sort(reverse=True)  # Delete from end to avoid index shifts
            
            for row in selectedRows:
                self.innerDataRemove(row)
                self.model.removeStation(row)
                
            # Update experiment data
            self.experiment.set_stations(self.stationCoords, self.velocities)
            
    def openResultWindow(self, plotMask, metricsMask, values):
        """Open result dialog with plots and metrics."""
        images = [
            "output/plot_example.png",
            "output/plot_reachability_example.png",
            "output/plot_reachability_difSt_example.png"
        ]
        # Pass station data to the dialog
        self.additional_windows.append(ResultDialog(images, values, plotMask, metricsMask, self.stations))
        self.additional_windows[-1].show()
        
    def innerDataAdd(self, data):
        """
        Add a new station to internal data arrays.
        
        Args:
            data (list): Station data as a list
        """
        new_item = ((data[1], data[2], data[3]), (data[4], data[5], data[6]))
        self.stationCoords = np.append(self.stationCoords, [new_item], axis=0)
        
        new_velocity = data[7]
        self.velocities = np.append(self.velocities, [new_velocity])
        
    def innerDataRemove(self, row):
        """
        Remove a station from internal data arrays.
        
        Args:
            row (int): Index of the station to remove
        """
        if 0 <= row < len(self.stationCoords):
            self.stationCoords = np.delete(self.stationCoords, row, axis=0)
            self.velocities = np.delete(self.velocities, row)
        else:
            raise IndexError("Индекс вне допустимого диапазона")
            
    def generateGraph(self):
        """Generate a graph for calculations."""
        errorFlag = self.check_input_GG()
        if not errorFlag:
            # Show loading animation
            self.deactivateButtonGG('Генерация графа...')
            QApplication.processEvents()
            
            # Update experiment parameters
            self.experiment.set_parameters(
                mesh_width=self.mesh_width,
                check_freq=self.check_freq
            )
            
            # Generate graph
            is_new = self.experiment.generate_graph()
            
            if is_new:
                self.deactivateButtonGG('Граф был добавлен')
            else:
                self.deactivateButtonGG('Такой граф уже сгененирован')
                
    def startExperiment(self):
        """Run the experiment with selected parameters."""
        errorFlag = self.check_input_SE()
        
        if not errorFlag:
            # Disable button and show loading animation
            self.deactivateButton()
            
            # Get dialog references if they exist
            result_dialog = None
            if self.additional_windows:
                for window in self.additional_windows:
                    if isinstance(window, ResultDialog):
                        result_dialog = window
                        break
            
            # Check display settings
            show_station_names = self.cb_show_station_names.isChecked()
            dpi_values = [300, 600, 900]
            plot_quality = dpi_values[self.quality_selector.currentIndex()]
            
            # Prepare masks for plots and metrics
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
            
            # Update experiment parameters
            self.experiment.set_parameters(
                cases_number=self.cases_number,
                median_lifespan=self.median_lifespan,
                max_lifespan=self.max_lifespan,
                show_station_names=show_station_names,
                plot_dpi=plot_quality
            )
            
            # Close all existing result dialogs
            for widget in QtWidgets.QApplication.topLevelWidgets():
                if isinstance(widget, ResultDialog):
                    widget.close()
            
            # Process events to update UI before starting computations
            QApplication.processEvents()
            
            # Run experiment based on selected method
            if self.rb_method_line.isChecked():
                values, _ = self.experiment.run_experiment_line()
                self.openResultWindow(plotMask, metricsMask, values)
            elif self.rb_method_graph.isChecked():
                # Check graph parameters
                errorFlag = self.check_input_GG()
                
                if not errorFlag:
                    # Update graph parameters
                    self.experiment.set_parameters(
                        mesh_width=self.mesh_width,
                        check_freq=self.check_freq,
                        show_station_names=show_station_names,
                        plot_dpi=plot_quality
                    )
                    
                    # Run experiment
                    values, _ = self.experiment.run_experiment_graph()
                    self.openResultWindow(plotMask, metricsMask, values)
        
        # Re-enable button and hide loading animation
        self.activateButton()
        
    def check_input_SE(self):
        """
        Validate experiment parameters.
        
        Returns:
            bool: True if there's an error, False otherwise
        """
        try:
            self.cases_number = int(self.le_cases_number.text())
            self.median_lifespan = float(self.le_median_lifespan.text())
            self.max_lifespan = float(self.le_max_lifespan.text())
            
            # Some additional validation
            if self.cases_number <= 0:
                raise ValueError("Number of cases must be positive")
            if self.median_lifespan <= 0 or self.max_lifespan <= 0:
                raise ValueError("Lifespan values must be positive")
            if self.median_lifespan > self.max_lifespan:
                raise ValueError("Median lifespan cannot exceed maximum lifespan")
                
            return False
        except ValueError as e:
            self.show_error_message(str(e) if str(e) != "" else "Неверный формат данных")
            return True
            
    def check_input_GG(self):
        """
        Validate graph generation parameters.
        
        Returns:
            bool: True if there's an error, False otherwise
        """
        try:
            self.mesh_width = int(self.le_mesh_width.text())
            self.check_freq = int(self.le_check_freq.text())
            
            # Some additional validation
            if self.mesh_width <= 0 or self.check_freq <= 0:
                raise ValueError("Parameters must be positive")
                
            return False
        except ValueError as e:
            self.show_error_message(str(e) if str(e) != "" else "Неверный формат данных")
            return True
            
    def show_error_message(self, message="Неверный формат данных"):
        """
        Show error message for invalid input.
        
        Args:
            message (str): Error message to display
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Ошибка")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
        
    def updateFrameStatus(self):
        """Update the enabled status of the graph frame."""
        self.graph_frame.setEnabled(self.rb_method_graph.isChecked())
        self.updateFrameStyle()
        
    def updateFrameStyle(self):
        """Update the style of the graph frame based on enabled status."""
        if self.graph_frame.isEnabled():
            self.graph_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 10px;
                }}
            """)
            # Re-add shadow effect
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setColor(QColor(0, 0, 0, 30))
            shadow.setOffset(0, 2)
            self.graph_frame.setGraphicsEffect(shadow)
        else:
            self.graph_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: #f0f0f0;
                    border: none;
                    border-radius: 10px;
                    padding: 10px;
                    color: #888888;
                }}
            """)
            # Disabled shadow
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(10)
            shadow.setColor(QColor(0, 0, 0, 20))
            shadow.setOffset(0, 1)
            self.graph_frame.setGraphicsEffect(shadow)
            
    def deactivateButtonGG(self, text=None):
        """
        Disable the graph generation button.
        
        Args:
            text (str, optional): Text to display on the button
        """
        self.pb_gen_graph.setDisabled(True)
        
        if text is None:
            self.pb_gen_graph.setText('Граф добавлен')
        else:
            self.pb_gen_graph.setText(text)
        
    def activateButtonGG(self):
        """Enable the graph generation button."""
        self.pb_gen_graph.setEnabled(True)
        self.pb_gen_graph.setText('Сгенерировать граф')
        
    def deactivateButton(self):
        """Disable the experiment start button."""
        # Simply change text and disable the button
        self.pb_start_exp.setText("Вычисление...")
        self.pb_start_exp.setEnabled(False)
        
    def activateButton(self):
        """Enable the experiment start button."""
        # Simply restore text and enable the button
        self.pb_start_exp.setText("Запуск")
        self.pb_start_exp.setEnabled(True)
        
    def closeEvent(self, event):
        """Handle window close event to clean up resources."""
        # Close all child windows
        for window in self.additional_windows:
            window.close()
            
        # Accept the close event
        event.accept() 