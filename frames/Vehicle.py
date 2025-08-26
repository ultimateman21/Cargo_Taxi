from PyQt6.QtWidgets import QLabel, QGroupBox, QVBoxLayout, QHBoxLayout
from frames.MultiPressableThings import MultiPressableFrame
from PyQt6.QtCore import Qt


class Vehicle(MultiPressableFrame):
    def __init__(self, id_, data):
        super().__init__()
        self.work_id = id_

        self.id = data[0]
        self.num = data[1]
        self.space = data[2]
        self.capacity = data[3]
        self.weight = data[4]
        self.state_ = data[5]

        self.setFixedSize(200, 75)

        layout = QVBoxLayout()

        self.order_box = QGroupBox(str(self.num))

        sub_layout = QHBoxLayout()

        self.space_l = QLabel(f'{str(self.space)} м<sup>2</sup>')
        sub_layout.addWidget(self.space_l)

        self.capacity_l = QLabel(f'{str(self.capacity)} м<sup>3</sup>')
        sub_layout.addWidget(self.capacity_l)

        self.weight_l = QLabel(f'{str(self.weight)} кг')
        sub_layout.addWidget(self.weight_l)

        sub_layout.addStretch(1)

        self.state = QLabel('✔')
        self.state.setStyleSheet('QLabel {background-color: rgb(113, 174, 38); border-radius: 3px;'
                                 'font-size: 20px; font-family: "Segoe UI Symbol";}')
        self.state.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.state.setFixedSize(40, 25)
        self.state.hide()
        sub_layout.addWidget(self.state)

        self.order_box.setLayout(sub_layout)
        layout.addWidget(self.order_box)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
        self.state_update()

    def return_info(self):
        return [self.id, self.num, self.space, self.capacity, self.weight, self.state_]

    def set_info(self, info):
        self.num = info[1]
        self.space = info[2]
        self.capacity = info[3]
        self.weight = info[4]
        self.state_ = info[5]

        self.order_box.setTitle(str(self.num))
        self.space_l.setText(f'{str(self.space)} м<sup>2</sup>')
        self.capacity_l.setText(f'{str(self.capacity)} м<sup>3</sup>')
        self.weight_l.setText(f'{str(self.weight)} кг')
        self.state_update()

    def get_id(self):
        return self.id

    def state_update(self):
        if self.state_ == '1':
            self.state.show()
        else:
            self.state.hide()
