from PyQt6.QtWidgets import QWidget, QGroupBox, QLabel, QPushButton, QLineEdit, QGridLayout, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from mysql.connector import connect
from config import global_


class RightVBox(QWidget):
    clear_orders_when_v = pyqtSignal()

    def __init__(self, id_w, config):
        super().__init__()

        self.id_w = id_w
        self.config = config
        self.id_v = '-1'

        layout = QVBoxLayout()

        vehicle_box = QGroupBox('Автомобиль')
        self.vehicle_layout = QGridLayout()

        num_l = QLabel('Номер:')
        self.vehicle_layout.addWidget(num_l, 0, 0)

        self.num_edit = QLineEdit()
        self.num_edit.returnPressed.connect(self.handle_enter_key)
        self.num_edit.textChanged.connect(self.check_input_fields)
        self.vehicle_layout.addWidget(self.num_edit, 0, 1)

        space_l = QLabel('Площадь м<sup>2</sup>:')
        self.vehicle_layout.addWidget(space_l, 1, 0)

        self.space_edit = QLineEdit()
        self.space_edit.returnPressed.connect(self.handle_enter_key)
        self.space_edit.textChanged.connect(self.check_input_fields)
        self.vehicle_layout.addWidget(self.space_edit, 1, 1)

        capacity_l = QLabel('Объём м<sup>3</sup>:')
        self.vehicle_layout.addWidget(capacity_l, 2, 0)

        self.capacity_edit = QLineEdit()
        self.capacity_edit.returnPressed.connect(self.handle_enter_key)
        self.capacity_edit.textChanged.connect(self.check_input_fields)
        self.vehicle_layout.addWidget(self.capacity_edit, 2, 1)

        weight_l = QLabel('Вес кг:')
        self.vehicle_layout.addWidget(weight_l, 3, 0)

        self.weight_edit = QLineEdit()
        self.weight_edit.returnPressed.connect(self.handle_enter_key)
        self.weight_edit.textChanged.connect(self.check_input_fields)
        self.vehicle_layout.addWidget(self.weight_edit, 3, 1)

        self.button = QPushButton('Добавить')
        self.button.setEnabled(False)
        self.vehicle_layout.addWidget(self.button, 4, 0, 1, 2)

        self.choose_b = QPushButton('Выбрать')
        self.choose_b.clicked.connect(self.choose_vehicle)
        self.vehicle_layout.addWidget(self.choose_b, 5, 0, 1, 2)
        self.choose_b.hide()

        vehicle_box.setLayout(self.vehicle_layout)
        layout.addWidget(vehicle_box)

        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def handle_enter_key(self):
        sender = self.sender()
        if sender == self.num_edit:
            self.space_edit.setFocus()
        elif sender == self.space_edit:
            self.capacity_edit.setFocus()
        elif sender == self.capacity_edit:
            self.weight_edit.setFocus()

    def check_input_fields(self):
        if (self.num_edit.text() and self.space_edit.text() and
                self.capacity_edit.text() and self.weight_edit.text()):
            self.button.setEnabled(True)
        else:
            self.button.setEnabled(False)

    def return_info(self):
        return [self.num_edit.text(), int(self.space_edit.text()), int(self.capacity_edit.text()), int(self.weight_edit.text())]

    def set_info(self, data):
        wid = [self.num_edit, self.space_edit, self.capacity_edit, self.weight_edit]

        self.id_v = str(data[0])

        for i, widg in enumerate(wid):
            widg.setText(str(data[i + 1]))
            widg.setReadOnly(True)

        if self.button.text() == 'Добавить':
            self.button.setText('Назад')
            self.choose_b.show()
        self.button.setEnabled(True)

    def clear(self):
        try:
            self.choose_b.hide()
            wid = [self.num_edit, self.space_edit, self.capacity_edit, self.weight_edit]

            for i, widg in enumerate(wid):
                widg.setText('')
                widg.setReadOnly(False)

            self.id_v = '-1'

            self.button.setEnabled(False)
            self.button.setText('Добавить')
        except Exception as e:
            print(str(e), '|r_vehicle clear')

    def choose_vehicle(self):
        try:
            with connect(
                user=self.config['user'],
                password=self.config['pass'],
                host=global_['host'],
                port=global_['port'],
                database=global_['db'],
            ) as connection:
                cursor = connection.cursor()
                cursor.callproc('choose_vehicle', (int(self.id_w), int(self.id_v)))
                connection.commit()
            self.clear_orders_when_v.emit()
        except Exception as e:
            print(e, '|r_vehicle choose_vehicle')
