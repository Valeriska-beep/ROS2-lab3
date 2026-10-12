import sys

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import String

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QTextEdit,
    QVBoxLayout,
    QGridLayout
)

from PyQt5.QtCore import Qt, QTimer


class RobotGuiWindow(QWidget):

    def __init__(self, ros_node):
        super().__init__()

        self.ros_node = ros_node

        # Publisher для /cmd_vel
        self.cmd_vel_publisher = self.ros_node.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Subscriber для /motion_status
        self.status_subscriber = self.ros_node.create_subscription(
            String,
            '/motion_status',
            self.status_callback,
            10
        )

        self.setWindowTitle("Robot Control GUI")
        self.setFixedSize(500, 450)

        self.create_gui()

        # Таймер неблокуючої обробки ROS2 у циклі Qt
        self.ros_timer = QTimer(self)
        self.ros_timer.timeout.connect(self.check_ros_events)
        self.ros_timer.start(20)

    def create_gui(self):

        # Заголовок
        title = QLabel("Керування роботом")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("title")

        # Кнопки
        self.forward_button = QPushButton("Вперед")
        self.backward_button = QPushButton("Назад")
        self.left_button = QPushButton("Ліворуч")
        self.right_button = QPushButton("Праворуч")
        self.stop_button = QPushButton("Стоп")

        # Розмір кнопок
        buttons = [
            self.forward_button,
            self.backward_button,
            self.left_button,
            self.right_button,
            self.stop_button
        ]

        for button in buttons:
            button.setMinimumSize(120, 50)

        # Поле статусу
        status_title = QLabel("Статус системи:")
        status_title.setObjectName("status_title")

        self.status_box = QTextEdit()
        self.status_box.setReadOnly(True)
        self.status_box.setText("Готовий до роботи")

        # Підключення кнопок до ROS2-команд
        self.forward_button.clicked.connect(
            lambda: self.send_velocity(0.5, 0.0, "Вперед")
        )

        self.backward_button.clicked.connect(
            lambda: self.send_velocity(-0.5, 0.0, "Назад")
        )

        self.left_button.clicked.connect(
            lambda: self.send_velocity(0.0, 1.0, "Ліворуч")
        )

        self.right_button.clicked.connect(
            lambda: self.send_velocity(0.0, -1.0, "Праворуч")
        )

        self.stop_button.clicked.connect(
            lambda: self.send_velocity(0.0, 0.0, "Стоп")
        )

        # Розташування кнопок
        button_layout = QGridLayout()

        button_layout.addWidget(
            self.forward_button, 0, 1
        )

        button_layout.addWidget(
            self.left_button, 1, 0
        )

        button_layout.addWidget(
            self.stop_button, 1, 1
        )

        button_layout.addWidget(
            self.right_button, 1, 2
        )

        button_layout.addWidget(
            self.backward_button, 2, 1
        )

        # Основне розташування
        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(status_title)
        main_layout.addWidget(self.status_box)

        self.setLayout(main_layout)

        #Стилізація інтерфейсу 
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

    def send_velocity(self, linear_x, angular_z, direction):
        msg = Twist()
        msg.linear.x = float(linear_x)
        msg.angular.z = float(angular_z)
        self.cmd_vel_publisher.publish(msg)
        self.update_status(f"{direction}: linear.x={linear_x}, angular.z={angular_z}")

    def status_callback(self, msg):
        self.update_status(f"[Статус]: {msg.data}")

    def check_ros_events(self):
        rclpy.spin_once(self.ros_node, timeout_sec=0)

    def update_status(self, message):
        self.status_box.append(message)

    def closeEvent(self, event):
        self.ros_timer.stop()
        event.accept()


def main(args=None):
    rclpy.init(args=args)
    ros_node = Node("robot_gui_node")
    app = QApplication(sys.argv)

    window = RobotGuiWindow(ros_node)
    window.show()

    exit_code = app.exec_()

    ros_node.destroy_node()
    rclpy.shutdown()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
