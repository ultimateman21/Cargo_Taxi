from frames.MultiPressableThings import MultiPressableFrame, MultiPressableLabel
from PyQt6.QtWidgets import QLabel, QGroupBox, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QDate, QTime


class Order(MultiPressableFrame):
    def __init__(self, data):
        super().__init__()

        self.id = data[0]
        self.from__ = data[1]
        self.to__ = data[2]
        self.dist_ = data[3]
        self.date_time = data[4]
        self.date_ = QDate.fromString(str(data[4].split(' ')[0]), 'yyyy-MM-dd').toString('dd-MM-yyyy ')
        self.time_ = QTime.fromString(str(data[4].split(' ')[1]), 'hh:mm:ss').toString('hh:mm')
        self.price_ = data[5]
        self.space = data[6]
        self.capacity = data[7]
        self.weight = data[8]
        self.state_ = data[9]

        self.setFixedSize(200, 125)

        layout = QVBoxLayout()

        self.order_box = QGroupBox(str(self.date_))
        order_layout = QVBoxLayout()

        time_dist_layout = QHBoxLayout()

        self.time = QLabel(str(self.time_))
        time_dist_layout.addWidget(self.time)

        self.dist = QLabel(f'{str(self.dist_)} метров')
        time_dist_layout.addWidget(self.dist)

        time_dist_layout.addStretch(1)

        self.state = MultiPressableLabel(style_name='green')
        self.state.setText('✔')
        self.state.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.state.setFixedSize(40, 25)
        self.state.hide()
        time_dist_layout.addWidget(self.state)

        order_layout.addLayout(time_dist_layout)

        self.from_ = QLabel(','.join(str(self.from__).split(',')[1:]))
        order_layout.addWidget(self.from_)

        self.to_ = QLabel(','.join(str(self.to__).split(',')[1:]))
        order_layout.addWidget(self.to_)

        self.order_box.setLayout(order_layout)
        layout.addWidget(self.order_box)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

        self.state_update()

    def return_info_map(self):
        return [self.id, self.from__, self.to__, self.dist_, self.date_, self.time_,
                self.price_, self.space, self.capacity, self.weight, self.state_]

    def return_info(self):
        return [self.id, self.from__, self.to__, self.dist_, self.date_time, self.price_,
                self.space, self.capacity, self.weight, self.state_]

    def set_info(self, info):
        f = ['id', 'from__', 'to__', 'dist_', 'date_time', 'date_', 'time_', 'price_', 'space', 'capacity', 'weight', 'state_']
        for i, data in enumerate(info):
            if i < 4:
                setattr(self, f[i], data)
            elif i == 4:
                setattr(self, f[4], str(data))
                setattr(self, f[5], QDate.fromString(str(data.split(' ')[0]), 'yyyy-MM-dd').toString('dd-MM-yyyy '))
                setattr(self, f[6], QTime.fromString(str(data.split(' ')[1]), 'hh:mm:ss').toString('hh:mm'))
            else:
                setattr(self, f[i + 2], data)

        self.order_box.setTitle(str(self.date_))
        self.time.setText(str(self.time_))
        self.dist.setText(f'{str(self.dist_)} метров')
        self.from_.setText(','.join(str(self.from__).split(',')[1:]))
        self.to_.setText(','.join(str(self.to__).split(',')[1:]))
        self.state_update()

    def state_update(self):
        if self.state_ == '1':
            self.state.show()
        else:
            self.state.hide()

    def get_state(self):
        return self.state_

    def set_state(self, state):
        self.state_ = str(state)
        self.state_update()

    def get_id(self):
        return self.id
