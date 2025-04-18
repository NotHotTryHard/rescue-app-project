"""
Dialog classes for the rescue application.
"""

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTableView, 
    QDialogButtonBox, QLabel, QWidget, 
    QMessageBox, QHBoxLayout, QTabWidget,
    QPushButton, QSizePolicy, QFrame, QGraphicsDropShadowEffect,
    QScrollArea, QApplication
)
from PyQt6.QtGui import QPixmap, QFont, QColor, QIcon, QScreen

import os

from .ui_files.ui_page_add import Ui_Dialog as Ui_AddDialog
from ..utils.coordinates import DegreesToDecimalVec


class StationAddDialog(QtWidgets.QDialog, Ui_AddDialog):
    """Dialog for adding a new rescue station."""
    
    def __init__(self, parent=None):
        """Initialize the dialog."""
        super().__init__(parent)
        self.setWindowTitle("Добавление станции")
        self.setupUi(self)

        # Initialize variables
        self.stationName = None
        self.lat_deg = None
        self.lat_min = None
        self.lat_sec = None
        self.long_deg = None
        self.long_min = None
        self.long_sec = None
        self.vel = None

        # Apply modern styling
        self.apply_styles()

        # Connect signals
        self.pb_save_station.clicked.connect(self.saveStation)

    def apply_styles(self):
        """Apply modern styling to the dialog."""
        # Primary color definition
        primary_color = "#FF8C00"      # Dark Orange
        secondary_color = "#FFA500"    # Orange
        accent_color = "#FF4500"       # OrangeRed
        text_color = "#333333"         # Dark Gray
        bg_color = "#FFF5E9"           # Very Light Orange
        
        # Set dialog background
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_color};
            }}
        """)
        
        # Style the frame
        self.frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        
        # Add shadow to frame for depth
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        self.frame.setGraphicsEffect(shadow)
        
        # Style the heading
        self.label.setStyleSheet(f"""
            font-weight: bold;
            font-size: 16px;
            color: {text_color};
            padding-bottom: 8px;
        """)
        
        # Style the input fields
        input_style = f"""
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
        
        self.le_stationName.setStyleSheet(input_style)
        self.le_lat_deg.setStyleSheet(input_style)
        self.le_lat_min.setStyleSheet(input_style)
        self.le_lat_sec.setStyleSheet(input_style)
        self.le_long_deg.setStyleSheet(input_style)
        self.le_long_min.setStyleSheet(input_style)
        self.le_long_sec.setStyleSheet(input_style)
        self.le_stationSpeed.setStyleSheet(input_style)
        
        # Style the button
        self.pb_save_station.setStyleSheet(f"""
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
        """)
        
        # Add tooltips
        self.le_lat_deg.setToolTip("Градусы широты")
        self.le_lat_min.setToolTip("Минуты широты")
        self.le_lat_sec.setToolTip("Секунды широты")
        self.le_long_deg.setToolTip("Градусы долготы")
        self.le_long_min.setToolTip("Минуты долготы")
        self.le_long_sec.setToolTip("Секунды долготы")
        self.le_stationSpeed.setToolTip("Скорость судна в км/ч")

    def get_data(self):
        """Return the entered data as a list."""
        return [
            self.stationName, self.lat_deg, self.lat_min, self.lat_sec,
            self.long_deg, self.long_min, self.long_sec, self.vel
        ]

    def saveStation(self):
        """Validate and save the station data."""
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
        """Validate the input fields."""
        try:
            self.stationName1 = self.le_stationName.text()
            if not self.stationName1:
                raise ValueError("Имя станции не может быть пустым")
                
            self.lat_deg1 = float(self.le_lat_deg.text())
            
            self.lat_min1 = 0 if self.le_lat_min.text() == '' else float(self.le_lat_min.text())
            self.lat_sec1 = 0 if self.le_lat_sec.text() == '' else float(self.le_lat_sec.text())
            
            self.long_deg1 = float(self.le_long_deg.text())
            self.long_min1 = 0 if self.le_long_min.text() == '' else float(self.le_long_min.text())
            self.long_sec1 = 0 if self.le_long_sec.text() == '' else float(self.le_long_sec.text())
            
            self.vel1 = float(self.le_stationSpeed.text())
            
            # Additional validation
            if self.vel1 <= 0:
                raise ValueError("Скорость должна быть положительной")
                
            return True
        except ValueError as e:
            self.show_error_message(str(e) if str(e) != "" else "Неверный формат данных")
            return False

    def show_error_message(self, message="Неверный формат данных"):
        """Show an error message for invalid input."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Ошибка")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()


class StationSelectionDialog(QDialog):
    """Dialog for selecting stations to delete."""
    
    def __init__(self, model, parent=None):
        """Initialize the dialog with the given model."""
        super().__init__(parent)
        self.model = model
        self.initUI()

    def initUI(self):
        """Setup the dialog UI."""
        # Primary color definition
        primary_color = "#FF8C00"      # Dark Orange
        secondary_color = "#FFA500"    # Orange
        accent_color = "#FF4500"       # OrangeRed
        text_color = "#333333"         # Dark Gray
        bg_color = "#FFF5E9"           # Very Light Orange
        
        self.setWindowTitle("Выбор станций для удаления")
        self.setGeometry(100, 100, 600, 400)  # More reasonable default size
        
        # Set dialog background
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_color};
            }}
        """)
        
        layout = QVBoxLayout()

        # Add header label
        header_label = QLabel("Выберите станции для удаления")
        header_label.setStyleSheet(f"""
            font-weight: bold;
            font-size: 16px;
            color: {text_color};
            padding: 10px 0;
        """)
        layout.addWidget(header_label)

        # Create a frame for the table
        table_frame = QFrame()
        table_frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: none;
                border-radius: 10px;
            }}
        """)
        
        # Add shadow to frame
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        table_frame.setGraphicsEffect(shadow)
        
        table_layout = QVBoxLayout(table_frame)
        
        # Add help text
        help_label = QLabel("Выберите одну или несколько станций из списка и нажмите 'Удалить'")
        help_label.setStyleSheet("color: #666666; font-style: italic;")
        table_layout.addWidget(help_label)

        # Create a table view for showing stations
        self.tableView = QTableView()
        self.tableView.setModel(self.model)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setStyleSheet(f"""
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
        """)
        
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        table_layout.addWidget(self.tableView)
        layout.addWidget(table_frame)

        # Add buttons
        button_box = QDialogButtonBox()
        delete_button = button_box.addButton("Удалить", QDialogButtonBox.ButtonRole.AcceptRole)
        cancel_button = button_box.addButton("Отмена", QDialogButtonBox.ButtonRole.RejectRole)
        
        delete_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {secondary_color};
            }}
            QPushButton:pressed {{
                background-color: {accent_color};
            }}
        """)
        
        cancel_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #e0e0e0;
                color: {text_color};
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: #d0d0d0;
            }}
            QPushButton:pressed {{
                background-color: #c0c0c0;
            }}
        """)
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def getSelectedRows(self):
        """Get the selected rows from the table view."""
        selectedRows = self.tableView.selectionModel().selectedRows()
        return [index.row() for index in selectedRows]


class ResizableImageLabel(QLabel):
    """Custom QLabel to display images that maintains aspect ratio and fits the container."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_pixmap = None
        
    def setPixmap(self, pixmap):
        """Set the pixmap and store original for resizing."""
        self.original_pixmap = pixmap
        self.updatePixmap()
        
    def updatePixmap(self):
        """Update the displayed pixmap based on current size."""
        if self.original_pixmap and not self.original_pixmap.isNull():
            scaled_pixmap = self.original_pixmap.scaled(
                self.width(), self.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            super().setPixmap(scaled_pixmap)
    
    def resizeEvent(self, event):
        """Handle resize events to update the pixmap."""
        self.updatePixmap()
        super().resizeEvent(event)


class ResultDialog(QWidget):
    """Dialog for displaying experiment results."""
    
    def __init__(self, images, values, plotMask, metricsMask, stations=None):
        """Initialize the dialog with values."""
        super().__init__()
        
        # Primary color definition
        self.primary_color = "#FF8C00"      # Dark Orange
        self.secondary_color = "#FFA500"    # Orange
        self.accent_color = "#FF4500"       # OrangeRed
        self.text_color = "#333333"         # Dark Gray
        self.light_text = "#666666"         # Medium Gray
        self.bg_color = "#FFF5E9"           # Very Light Orange
        
        # Dialog properties
        self.setWindowTitle("Результаты эксперимента")
        
        # Make dialog size responsive to screen size
        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(
            screen.width() // 6,
            screen.height() // 6,
            screen.width() * 2 // 3,
            screen.height() * 2 // 3
        )
        
        # Set style
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.bg_color};
                color: {self.text_color};
            }}
        """)
        
        # Store references
        self.images = images
        self.metrics = values
        self.plotMask = plotMask
        self.metricsMask = metricsMask
        self.stations = stations
        
        # Initialize UI
        self.initUI()
        
    def initUI(self):
        """Setup the dialog UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title_label = QLabel("Результаты эксперимента")
        title_label.setStyleSheet(f"""
            font-size: 20px;
            font-weight: bold;
            color: {self.text_color};
            padding: 5px 0;
        """)
        main_layout.addWidget(title_label)
        
        # Tab widget for plots and metrics
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: white;
                border-radius: 10px;
            }}
            QTabBar::tab {{
                background-color: #e0e0e0;
                color: {self.text_color};
                border: none;
                padding: 10px 20px;
                margin-right: 5px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }}
            QTabBar::tab:selected {{
                background-color: {self.primary_color};
                color: white;
                font-weight: bold;
            }}
            QTabBar::tab:hover:!selected {{
                background-color: #d0d0d0;
            }}
        """)
        
        # Add shadow to tab widget
        tab_shadow = QGraphicsDropShadowEffect()
        tab_shadow.setBlurRadius(15)
        tab_shadow.setColor(QColor(0, 0, 0, 30))
        tab_shadow.setOffset(0, 2)
        self.tab_widget.setGraphicsEffect(tab_shadow)
        
        # Create tabs
        self.create_plot_tab()
        self.create_metrics_tab()
        
        main_layout.addWidget(self.tab_widget)
        
        # Bottom button layout
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)
        
        # Add buttons
        self.save_button = QPushButton("Сохранить")
        self.save_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.primary_color};
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {self.secondary_color};
            }}
            QPushButton:pressed {{
                background-color: {self.accent_color};
            }}
        """)
        self.save_button.clicked.connect(self.save_current_plot)
        
        self.close_button = QPushButton("Закрыть")
        self.close_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #e0e0e0;
                color: {self.text_color};
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: #d0d0d0;
            }}
            QPushButton:pressed {{
                background-color: #c0c0c0;
            }}
        """)
        self.close_button.clicked.connect(self.close)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.close_button)
        
        main_layout.addLayout(button_layout)

    def create_plot_tab(self):
        """Create the plot tab with plots and metrics."""
        # Find which plots to show based on plotMask
        header_image = [
            'Кратчайшие пути',
            'Сложность достижимости',
            'Разделение зон ответственности'
        ]
        filtered_images = [img for img, mask in zip(self.images, self.plotMask) if mask]
        filtered_headers = [head for head, mask in zip(header_image, self.plotMask) if mask]
        
        if not filtered_images:
            return
            
        # Add tabs with images
        for i, image_path in enumerate(filtered_images):
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)
            tab_layout.setContentsMargins(10, 10, 10, 10)
            
            # Use a splitter to allow user to adjust the sizes
            splitter = QtWidgets.QSplitter(Qt.Orientation.Vertical)
            splitter.setHandleWidth(8)
            splitter.setStyleSheet(f"""
                QSplitter::handle {{
                    background-color: {self.primary_color};
                    border: none;
                    border-radius: 2px;
                    height: 4px;
                }}
            """)
            
            # Create image widget
            image_widget = QWidget()
            image_layout = QVBoxLayout(image_widget)
            image_layout.setContentsMargins(0, 0, 0, 0)
            
            # Create the image label
            image_label = ResizableImageLabel()
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                image_label.setPixmap(pixmap)
            else:
                # Show placeholder if image not found
                image_label.setText(f"Изображение не найдено: {image_path}")
                image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                image_label.setStyleSheet("color: #999999; background-color: #f0f0f0; padding: 20px;")
                
            image_layout.addWidget(image_label)
            
            # Create metrics widget
            metrics_widget = self.create_metrics_widget()
            
            # Add both sections to the splitter
            splitter.addWidget(image_widget)
            splitter.addWidget(metrics_widget)
            
            # Set initial sizes (70% map, 30% metrics)
            splitter.setSizes([700, 300])
            
            tab_layout.addWidget(splitter)
            self.tab_widget.addTab(tab, filtered_headers[i])

    def create_metrics_tab(self):
        """Create a dedicated metrics tab."""
        # Not implementing a separate metrics tab for now
        # Could be added in the future if needed
        pass
        
    def create_metrics_widget(self):
        """Create a widget with metrics display."""
        metrics_widget = QWidget()
        metrics_layout = QVBoxLayout(metrics_widget)
        
        # Add metrics title
        metrics_title = QLabel("Метрики эффективности")
        metrics_title.setStyleSheet(f"""
            font-weight: bold;
            font-size: 16px;
            color: {self.text_color};
            padding-bottom: 10px;
        """)
        metrics_layout.addWidget(metrics_title)
        
        # Headers for metrics
        header = [
            "Среднее время спасения",
            "Максимальное время спасения",
            "Условная вероятность спасения",
            "Вероятность спасения"
        ]
        
        # Filter metrics based on metricsMask
        filtered_values = [val for val, mask in zip(self.metrics, self.metricsMask) if mask]
        filtered_headers = [head for head, mask in zip(header, self.metricsMask) if mask]
        
        # Add metrics values in a grid
        metrics_grid = QtWidgets.QGridLayout()
        metrics_grid.setColumnStretch(1, 1)  # Make value column expandable
        
        for j, (value, header_text) in enumerate(zip(filtered_values, filtered_headers)):
            # Create label for metric name
            key_label = QLabel(f"{header_text}:")
            key_label.setStyleSheet(f"""
                font-weight: bold;
                color: {self.text_color};
                padding: 8px 5px;
            """)
            
            # Create label for metric value
            value_label = QLabel(f"{value}")
            value_label.setStyleSheet(f"""
                background-color: #FFF0E0;
                border-radius: 6px;
                padding: 8px 12px;
                color: {self.text_color};
                font-family: 'Segoe UI', sans-serif;
            """)
            
            metrics_grid.addWidget(key_label, j, 0)
            metrics_grid.addWidget(value_label, j, 1)
        
        metrics_layout.addLayout(metrics_grid)
        metrics_layout.addStretch()
        
        return metrics_widget
    
    def save_current_plot(self):
        """Save the current plot as an image file."""
        current_tab_index = self.tab_widget.currentIndex()
        if current_tab_index < 0:
            return
            
        # Find the image label in the current tab
        current_tab = self.tab_widget.widget(current_tab_index)
        splitter = current_tab.findChild(QtWidgets.QSplitter)
        if not splitter or splitter.count() <= 0:
            return
            
        map_widget = splitter.widget(0)
        image_label = map_widget.findChild(ResizableImageLabel)
        if not image_label or not hasattr(image_label, 'original_pixmap') or not image_label.original_pixmap:
            return
            
        # Get suggested filename based on tab name
        tab_name = self.tab_widget.tabText(current_tab_index)
        default_filename = f"rescue_plot_{tab_name.replace(' ', '_').lower()}_{QtCore.QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')}.png"
        
        # Open file dialog
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Сохранить изображение",
            default_filename,
            "Изображения (*.png *.jpg *.jpeg *.tif *.bmp);;PNG (*.png);;JPEG (*.jpg *.jpeg);;TIFF (*.tif);;BMP (*.bmp)"
        )
        
        if not file_path:
            return  # User canceled
            
        # Try to save the image
        try:
            # If the original image is available in memory, save it
            if image_label.original_pixmap and not image_label.original_pixmap.isNull():
                if image_label.original_pixmap.save(file_path):
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Icon.Information)
                    msg.setWindowTitle("Файл сохранен")
                    msg.setText(f"Изображение сохранено как {os.path.basename(file_path)}")
                    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                    msg.exec()
                else:
                    raise Exception("Не удалось сохранить файл")
            else:
                # Fallback to copying original file
                current_image_path = self.images[current_tab_index]
                if os.path.exists(current_image_path):
                    import shutil
                    shutil.copy2(current_image_path, file_path)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Icon.Information)
                    msg.setWindowTitle("Файл сохранен")
                    msg.setText(f"Изображение сохранено как {os.path.basename(file_path)}")
                    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                    msg.exec()
                else:
                    raise Exception(f"Исходный файл не найден: {current_image_path}")
                    
        except Exception as e:
            # Show error message
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Icon.Critical)
            error_msg.setWindowTitle("Ошибка")
            error_msg.setText("Не удалось сохранить изображение")
            error_msg.setInformativeText(str(e))
            error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            error_msg.exec() 