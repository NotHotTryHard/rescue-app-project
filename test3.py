import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTabWidget, QLabel, QHBoxLayout
from PyQt6.QtGui import QPixmap

class AdditionalWindow(QWidget):
    def __init__(self, images, values, plotMask, metricsMask):
        super().__init__()

        self.setWindowTitle("Additional Window")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # Create a tab widget
        self.tab_widget = QTabWidget()

        header = ["Среднее время спасения", "Максимальное время спасения", "Условная вероятность спасения (наихудший сценарий) ", "Вероятность спасения"]
        filtered_images = [elem for elem, m in zip(images, plotMask) if m]
        filtered_values = [elem for elem, m in zip(values, metricsMask) if m]
        filtered_header = [elem for elem, m in zip(header, metricsMask) if m]

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
            self.tab_widget.addTab(tab, f"Image {i+1}")

        self.layout.addWidget(self.tab_widget)
        self.setLayout(self.layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 400, 300)

        self.button = QPushButton("Open Additional Window", self)
        self.button.clicked.connect(self.open_additional_window)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def open_additional_window(self):
        plotMask = [True, False, True]
        metricsMask = [True, True, True, False]
        images = ["output/plot_example_graph.png", "output/plot_reachability_example_graph.png", "output/plot_reachability_difSt_example_graph.png"]
        values = [10, 20, 30, 40]
        self.additional_window = AdditionalWindow(images, values, plotMask, metricsMask)
        self.additional_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())