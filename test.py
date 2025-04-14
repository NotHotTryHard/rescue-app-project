import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class NewWindow(QWidget):
    def __init__(self, mask, value):
        super().__init__()
        self.setWindowTitle("")
        
        # Создаем вертикальный макет
        layout = QVBoxLayout()

        # Создаем метку с переданным значением
        if mask[0] == 1:
            self.label1 = QLabel(f"Значение: {value}")
            layout.addWidget(self.label1)
        if mask[1] == 1:
            self.label2 = QLabel(f"Значение2: {value}")
            layout.addWidget(self.label2)
        if mask[2] == 1:
            self.label3 = QLabel(f"Значение3: {value}")
            layout.addWidget(self.label3)
        if mask[3] == 1:
            self.label4 = QLabel(f"Значение4: {value}")
            layout.addWidget(self.label4)

        self.setLayout(layout)
        self.setFixedSize(200, 100)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Основное окно")

        # Создаем вертикальный макет
        layout = QVBoxLayout()

        self.value = 44
        # Создаем кнопку
        self.button = QPushButton("Открыть новое окно")
        self.button.clicked.connect(self.open_new_window)  # Подключаем сигнал кнопки к методу

        layout.addWidget(self.button)
        self.setLayout(layout)
        self.setFixedSize(300, 100)

    def open_new_window(self):
        # Создаем новое окно и отображаем его
        value = 42  # Значение, которое мы хотим показать
        self.new_window = NewWindow([1, 1, 1, 1], self.value)
        self.new_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())