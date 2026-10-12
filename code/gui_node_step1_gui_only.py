import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QTextEdit,
    QVBoxLayout,
    QGridLayout
)
from PyQt5.QtCore import Qt


class RobotGuiWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Robot Control GUI")
        self.setFixedSize(500, 450)

        self.create_gui()

    def create_gui(self):
        title = QLabel("Керування роботом")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("title")

        self.forward_button = QPushButton("Вперед")
        self.backward_button = QPushButton("Назад")
        self.left_button = QPushButton("Ліворуч")
        self.right_button = QPushButton("Праворуч")
        self.stop_button = QPushButton("Стоп")

        for button in (self.forward_button, self.backward_button,
                       self.left_button, self.right_button,
                       self.stop_button):
            button.setMinimumSize(120, 50)

        status_title = QLabel("Статус системи:")
        status_title.setObjectName("status_title")

        self.status_box = QTextEdit()
        self.status_box.setReadOnly(True)
        self.status_box.setText("Готовий до роботи")

        # Кнопки -> команди в /cmd_vel
        self.forward_button.clicked.connect(
            lambda: self.update_status("Натиснуто: Вперед"))
        self.backward_button.clicked.connect(
            lambda: self.update_status("Натиснуто: Назад"))
        self.left_button.clicked.connect(
            lambda: self.update_status("Натиснуто: Ліворуч"))
        self.right_button.clicked.connect(
            lambda: self.update_status("Натиснуто: Праворуч"))
        self.stop_button.clicked.connect(
            lambda: self.update_status("Натиснуто: Стоп"))

        button_layout = QGridLayout()
        button_layout.addWidget(self.forward_button, 0, 1)
        button_layout.addWidget(self.left_button, 1, 0)
        button_layout.addWidget(self.stop_button, 1, 1)
        button_layout.addWidget(self.right_button, 1, 2)
        button_layout.addWidget(self.backward_button, 2, 1)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(status_title)
        main_layout.addWidget(self.status_box)
        self.setLayout(main_layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #FFE6F2;
                color: #8E2457;
                font-family: Arial;
                font-size: 14px;
            }
            QLabel#title {
                color: #C2185B;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
            QLabel#status_title {
                color: #AD1457;
                font-size: 16px;
                font-weight: bold;
                padding-top: 10px;
            }
            QPushButton {
                background-color: #F8BBD0;
                color: #880E4F;
                border: 2px solid #EC6FA5;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #F48FB1;
                border: 2px solid #C2185B;
            }
            QPushButton:pressed {
                background-color: #EC407A;
                color: white;
            }
            QTextEdit {
                background-color: white;
                color: #6A1B45;
                border: 2px solid #F48FB1;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
        """)

    def update_status(self, message):
        self.status_box.append(message)


def main():
    app = QApplication(sys.argv)

    window = RobotGuiWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
