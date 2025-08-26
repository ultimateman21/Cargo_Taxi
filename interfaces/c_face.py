from PyQt6.QtCore import QEasingCurve, QRect
from widgets.l_scroll import *
from widgets.r_chat import *
from widgets.r_map import *
from frames.Drawer import *
from config import c_c


class ClientInterface(QWidget):
    def __init__(self, login, id_):
        super().__init__()
        self.setWindowTitle('Клиент')
        self.setFixedSize(750, 600)

        self.id_client = id_
        self.login = login

        layout = QVBoxLayout()

        name_box = QGroupBox()

        name_layout = QHBoxLayout()
        name_layout.setContentsMargins(1, 1, 1, 1)

        name_layout.addStretch(1)

        self.username_label = MultiPressableLabel()
        self.username_label.add_action(lambda: self.open_drawer())
        self.mousePressEvent = self.close_drawer
        name_layout.addWidget(self.username_label)
        self.get_name()

        name_box.setLayout(name_layout)

        layout.addWidget(name_box)

        self.bottom_layout = QHBoxLayout()

        self.left = LeftBox(self.id_client, 'client', c_c)
        self.left.order_info.connect(self.display_order_info)
        self.left.state_click.connect(self.display_chat)
        self.bottom_layout.addWidget(self.left)

        self.right = RightMapBox()
        self.right.button.clicked.connect(self.send_info_order)
        self.right.button1.clicked.connect(self.cancel_order)
        self.bottom_layout.addWidget(self.right)

        self.right_2 = RightChatBox(self.id_client, 'client', c_c)
        self.right_2.hide()

        layout.addLayout(self.bottom_layout)

        self.drawer = Drawer(self.id_client, 'client', c_c, self)
        self.drawer.quit_b.clicked.connect(self.quit)

        self.setLayout(layout)
        self.anim = QPropertyAnimation(self.drawer, b"geometry")
        self.duration = 0
        self.animate_drawer(self.width())

    def open_drawer(self):
        if self.drawer.x() < self.width():
            self.animate_drawer(self.width())
        else:
            self.drawer.raise_()
            self.animate_drawer(self.width() - self.drawer.width() + 10)

    def close_drawer(self, event):
        if self.drawer.isVisible() and not self.drawer.geometry().contains(event.pos()):
            self.animate_drawer(self.width())

    def animate_drawer(self, end_x):
        self.anim.setDuration(self.duration)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.anim.setStartValue(self.drawer.geometry())
        self.anim.setEndValue(QRect(end_x, 30, self.drawer.width(), self.height() - 20))
        self.anim.start()
        self.duration = 300

    def get_name(self):
        with connect(
            user=c_c['user'],
            password=c_c['pass'],
            host=global_['host'],
            port=global_['port'],
            database=global_['db'],
        ) as connection:
            cursor = connection.cursor()
            name = cursor.callproc('get_name', ('client', self.id_client, None))[-1]
            connection.commit()
        self.username_label.setText(name)

    def send_info_order(self):
        if self.right.button.text() != 'Назад':
            d = self.right.return_info()
            with connect(
                user=c_c['user'],
                password=c_c['pass'],
                host=global_['host'],
                port=global_['port'],
                database=global_['db'],
            ) as connection:
                cursor = connection.cursor()
                cursor.callproc('new_order', (self.id_client, d[0], d[1], d[2], d[3] + d[4], d[5], d[6], d[7], d[8]))
                connection.commit()
        else:
            self.right.clear()

    def cancel_order(self):
        try:
            with connect(
                user=c_c['user'],
                password=c_c['pass'],
                host=global_['host'],
                port=global_['port'],
                database=global_['db'],
            ) as connection:
                cursor = connection.cursor()
                cursor.callproc('cancel_order_c', [self.right.id_order])
                connection.commit()
            self.right.clear()
            self.left.clear()
        except Exception as e:
            print(e, '|c_face cancel_order')

    def display_order_info(self, data):
        if self.right_2.isVisible():
            self.right_2.set_order_id(None)
            self.right_2.hide()
            self.right_2.clear_chat()
            self.bottom_layout.replaceWidget(self.right_2, self.right)
            self.right.show()

        self.right.set_info_to_map(data)

    def display_chat(self, id_):
        if not self.right_2.isVisible():
            self.right.hide()
            self.bottom_layout.replaceWidget(self.right, self.right_2)
            self.right_2.set_order_id(id_)
            self.right_2.set_fio_info()
            self.right_2.show()
        else:
            self.right_2.clear_chat()
            if id_ == self.right_2.get_order_id():
                self.right_2.hide()
                self.right_2.set_order_id(None)
                self.bottom_layout.replaceWidget(self.right_2, self.right)
                self.right.show()
            else:
                self.right_2.set_order_id(id_)
                self.right_2.set_fio_info()

    def quit(self):
        self.login.show()
        self.login.login_edit.clear()
        self.login.password_edit.clear()
        self.login.login_edit.setFocus()
        self.right.map.close()
        self.left.close()
        self.close()

# start_l = 'Ростов-на-Дону, улица Волкова, 8 к 1'
# finish_l = 'Ростов-на-Дону, улица Большая Садовая, 55'
# Шахты, улица Рылеева, 53
