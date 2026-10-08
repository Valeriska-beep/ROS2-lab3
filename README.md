# Лабораторна робота №3
## Розробка графічного інтерфейсу керування роботом (Qt + ROS2) 

1. Підготовка середовища 
1.1. Активуємо базове середовище ROS2 Humble та поточний workspace:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
```

1.2. Перевірка списку активних вузлів і топіків:

```bash
ros2 node list
ros2 topic list
```

1.3. Запускаємо Motion Node з ЛБ №2
У першому терміналі:

```bash
cd ~/ros2_ws
```

Потім активуємо наше зібране середовище:

```bash
source install/setup.bash
ros2 run motion_control motion_node
```

Цей термінал поки не закриваємо.
Відкриваємо 2 термінал та перевіряємо активність топіків:

```bash
source /opt/ros/humble/setup.bash
cd ~/ros2_ws
source install/setup.bash

ros2 node list
ros2 topic list
```

2. Створення пакету GUI
2.1. Створення пакету robot_gui типу ament_python.
Залежність std_msgs додається для використання повідомлення std_msgs/msg/String, яке застосовується для передачі текстового статусу робота через топік /motion_status.

Активуємо ROS2:

```bash
source /opt/ros/humble/setup.bash
cd ~/ros2_ws/src
```

Створюємо пакет із залежностями rclpy, geometry_msgs:

```bash
ros2 pkg create --build-type ament_python robot_gui --dependencies rclpy geometry_msgs std_msgs
```

Залежність std_msgs додається одразу, оскільки тип std_msgs/msg/String використовуватиметься для отримання статусу стану робота.

Перевірка вмісту каталогу src робочого простору після створення пакета:

```bash
ls
```

2.2. Перевіряємо залежності
Переходимо всередину нашого нового пакета:

```bash
cd ~/ros2_ws/src/robot_gui
```

Перевіряємо package.xml:

```bash
cat package.xml
```

2.3. Попередня збірка workspace:

```bash
cd ~/ros2_ws
colcon build --packages-select robot_gui
source install/setup.bash
```

Перевіряємо, що ROS2 бачить robot_gui:

```bash
ros2 pkg list | grep robot_gui
```

2.4. Налаштовуємо точку входу (entry point) у setup.py, щоб ROS2 міг запускати вузол через ros2 run:
Відкриваємо:

```bash
nano ~/ros2_ws/src/robot_gui/setup.py
```

У словник entry_points додаємо:

```py
entry_points={
    'console_scripts': [
        'gui_node = robot_gui.gui_node:main',
    ],
},

```

2.5. Перевіряємо наявність бібліотеки PyQt5 у системі:

```bash
python3 -c "import PyQt5; print('PyQt5 OK')"
```

Якщо бібліотека відсутня: sudo apt install python3-pyqt5

3. Розробка GUI.
На цьому етапі створюється базова версія графічного інтерфейсу без підключення до ROS2. Кнопки використовуються для перевірки роботи інтерфейсу та виведення локального повідомлення про натискання.

3.1. Створюємо графічне вікно з кнопками та текстовим полем для відображення статусу.  

```bash
nano ~/ros2_ws/src/robot_gui/robot_gui/gui_node.py
```

Початковий код інтерфейсу (створення віджетів та розмітки):

```python
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

        # Підключення кнопок
        self.forward_button.clicked.connect(
            lambda: self.update_status("Натиснуто: Вперед")
        )

        self.backward_button.clicked.connect(
            lambda: self.update_status("Натиснуто: Назад")
        )

        self.left_button.clicked.connect(
            lambda: self.update_status("Натиснуто: Ліворуч")
        )

        self.right_button.clicked.connect(
            lambda: self.update_status("Натиснуто: Праворуч")
        )

        self.stop_button.clicked.connect(
            lambda: self.update_status("Натиснуто: Стоп")
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

        # Оформлення GUI
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
```

3.2. Перевірка запуску вікна:

```bash
cd ~/ros2_ws
colcon build --packages-select robot_gui
source install/setup.bash
```

Запуск графічного вікна:

```bash
ros2 run robot_gui gui_node
```

4. Інтеграція GUI з ROS2 
Розширюємо функціонал графічного інтерфейсу, інтегруючи зв'язок із системою ROS2:

Публікатор (Publisher): надсилає команди швидкості типу geometry_msgs/msg/Twist у топік /cmd_vel при натисканні кнопок.

Підписник (Subscriber): приймає повідомлення зворотного зв'язку типу std_msgs/msg/String із топіка /motion_status та виводить їх у текстове поле статусу.

Синхронізація подій Qt та ROS2: оскільки прямий виклик rclpy.spin() блокує головний потік графічного інтерфейсу PyQt, для неблокуючої обробки черги повідомлень використано QTimer. Він періодично (кожні 20 мс) викликає rclpy.spin_once(self.ros_node, timeout_sec=0).

Відкриваємо файл для внесення змін:

```bash
nano ~/ros2_ws/src/robot_gui/robot_gui/gui_node.py
```

Оновлюємо файл gui_node.py, замінивши його вміст повною версією з інтеграцією ROS2:

```py
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
```

5. Модифікація вузла motion_node.py (Організація зворотного зв'язку)
Для забезпечення повного циклу обміну повідомленнями додаємо у motion_node.py відправку зворотного зв'язку в топік /motion_status:
Відкриваємо вихідний код вузла руху:

```bash
nano ~/ros2_ws/src/motion_control/motion_control/motion_node.py
```

Повністю оновлюємо вміст файлу:

```py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String


class MotionNode(Node):

    def __init__(self):
        super().__init__('motion_node')

        self.max_linear_speed = 1.0
        self.max_angular_speed = 1.0

        # Підписка на команди з GUI
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        # Publisher для статусу робота
        self.status_publisher = self.create_publisher(
            String,
            '/motion_status',
            10
        )

        self.get_logger().info('Motion Node started')
        self.get_logger().info('Listening to /cmd_vel')

    def cmd_vel_callback(self, msg):
        linear_x = msg.linear.x
        angular_z = msg.angular.z

        # Логіка захисту та обмеження швидкості
        if abs(linear_x) > self.max_linear_speed:
            self.get_logger().warn(
                f'Linear speed limit exceeded: {linear_x:.2f} m/s. '
                f'Limiting to {self.max_linear_speed:.2f} m/s'
            )
            linear_x = max(
                -self.max_linear_speed,
                min(linear_x, self.max_linear_speed)
            )

        if abs(angular_z) > self.max_angular_speed:
            self.get_logger().warn(
                f'Angular speed limit exceeded: {angular_z:.2f} rad/s. '
                f'Limiting to {self.max_angular_speed:.2f} rad/s'
            )
            angular_z = max(
                -self.max_angular_speed,
                min(angular_z, self.max_angular_speed)
            )

        self.get_logger().info(
            f'Processed: linear.x={linear_x:.2f}, '
            f'angular.z={angular_z:.2f}'
        )

        # Визначення та публікація стану робота
        if linear_x > 0:
            status_text = 'Робот рухається вперед'
        elif linear_x < 0:
            status_text = 'Робот рухається назад'
        elif angular_z > 0:
            status_text = 'Робот повертає ліворуч'
        elif angular_z < 0:
            status_text = 'Робот повертає праворуч'
        else:
            status_text = 'Робот зупинений'

        # Публікація статусу
        status_msg = String()
        status_msg.data = status_text
        self.status_publisher.publish(status_msg)


def main(args=None):
    rclpy.init(args=args)

    node = MotionNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

```

6. Збірка та тестування системи
6.1.Збірка оновлених пакетів

```bash
cd ~/ros2_ws
colcon build --packages-select robot_gui motion_control
source install/setup.bash
```

6.2. Запуск та моніторинг (використовуються 4 окремі термінали):
Термінал 1 — запуск вузла керування рухом:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run motion_control motion_node
```

Термінал 2 — запуск графічного інтерфейсу (GUI):

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run robot_gui gui_node
```

Потім перевіримо, чи існує наш новий topic:

```bash
ros2 topic list
```

Термінал 3 — Моніторинг статусу виконання команд (/motion_status):

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 topic echo /motion_status
```

Термінал 4 — моніторинг вихідних команд швидкості /cmd_vel:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 topic echo /cmd_vel
```
