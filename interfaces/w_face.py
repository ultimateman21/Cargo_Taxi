from PyQt6.QtCore import QEasingCurve, QRect, QPoint
from PyQt6.QtWidgets import QToolBar
from PyQt6.QtGui import QAction
from widgets.r_vehicle import *
from widgets.l_scroll import *
from widgets.r_chat import *
from widgets.r_map import *
from frames.Drawer import *
from config import w_c


class WorkerInterface(QWidget):
    def __init__(self, login, id_):
        super().__init__()

        self.setWindowTitle('Водитель')
        self.setFixedSize(750, 600)

        self.id_work = id_
        self.login = login

        layout = QVBoxLayout()

        name_box = QGroupBox()

        name_layout = QHBoxLayout()
        name_layout.setContentsMargins(1, 1, 1, 1)

        toolbar = QToolBar('Toolbar', self)

        orders = QAction('Заказы', self)
        orders.triggered.connect(lambda: self.change_content('order'))
        toolbar.addAction(orders)

        toolbar.addSeparator()

        vehicle = QAction('Транспорт', self)
        vehicle.triggered.connect(lambda: self.change_content('vehicle'))
        toolbar.addAction(vehicle)

        name_layout.addWidget(toolbar)

        name_layout.addStretch(1)

        self.username_label = MultiPressableLabel()
        self.username_label.add_action(lambda: self.open_drawer())
        self.mousePressEvent = self.close_drawer
        name_layout.addWidget(self.username_label)
        self.get_name()

        name_box.setLayout(name_layout)

        layout.addWidget(name_box)

        self.bottom_layout = QHBoxLayout()

        self.left = LeftBox(self.id_work, 'worker', w_c)
        self.left.left_box.setTitle('Заказы на выбор')
        self.left.order_info.connect(self.display_order_info)
        self.left.state_click.connect(self.display_chat)
        self.bottom_layout.addWidget(self.left)

        self.right = RightMapBox()
        self.right.button.setText('Выбрать')
        self.right.button.clicked.connect(self.choose_order)
        self.right.button1.clicked.connect(self.cancel_order)
        self.bottom_layout.addWidget(self.right)

        self.left_2 = LeftBox(self.id_work, 'vehicle', w_c)
        self.left_2.left_box.setTitle('Ваши автомобили')
        self.left_2.vehicle_info.connect(self.display_vehicle_info)

        self.right_2 = RightVBox(self.id_work, w_c)
        self.right_2.button.clicked.connect(self.send_info_vehicle)
        self.right_2.clear_orders_when_v.connect(self.clear_orders)

        self.right_3 = RightChatBox(self.id_work, 'worker', w_c)
        self.right_2.hide()

        layout.addLayout(self.bottom_layout)
        self.drawer = Drawer(self.id_work, 'worker', w_c, self)
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
            user=w_c['user'],
            password=w_c['pass'],
            host=global_['host'],
            port=global_['port'],
            database=global_['db'],
        ) as connection:
            cursor = connection.cursor()
            name = cursor.callproc('get_name', ('worker', self.id_work, None))[-1]
            connection.commit()
        self.username_label.setText(name)

    def change_content(self, purpose):
        for i in reversed(range(self.bottom_layout.count())):
            wid = self.bottom_layout.itemAt(i).widget()
            wid.close()
            self.bottom_layout.removeWidget(wid)
        if purpose == 'order':
            self.animate_drawer(self.width())
            self.bottom_layout.addWidget(self.left)
            self.left.show()
            self.bottom_layout.addWidget(self.right)
            self.right.show()
        elif purpose == 'vehicle':
            self.animate_drawer(self.width())
            self.bottom_layout.addWidget(self.left_2)
            self.left_2.show()
            self.bottom_layout.addWidget(self.right_2)
            self.right_2.show()

    def clear_orders(self):
        self.left.clear()
        self.right.clear()

    def display_order_info(self, data):
        if self.right_3.isVisible():
            self.right_3.set_order_id(None)
            self.right_3.hide()
            self.right_3.clear_chat()
            self.bottom_layout.replaceWidget(self.right_3, self.right)
            self.right.show()

        self.right.set_info_to_map(data)

    def choose_order(self):
        try:
            if self.right.button.text() == 'Выбрать':
                with connect(
                    user=w_c['user'],
                    password=w_c['pass'],
                    host=global_['host'],
                    port=global_['port'],
                    database=global_['db'],
                ) as connection:
                    cursor = connection.cursor()
                    cursor.callproc('choose_order', (self.id_work, int(self.right.id_order)))
                    connection.commit()
                self.right.any_selected = True
            elif self.right.button.text() == 'Завершить':
                with connect(
                    user=w_c['user'],
                    password=w_c['pass'],
                    host=global_['host'],
                    port=global_['port'],
                    database=global_['db'],
                ) as connection:
                    cursor = connection.cursor()
                    cursor.callproc('finish_order', [self.right.id_order])
                    connection.commit()
                self.right.any_selected = False
                self.clear_orders()
        except Exception as e:
            print(e, '|w_face choose_order')

    def cancel_order(self):
        try:
            with connect(
                user=w_c['user'],
                password=w_c['pass'],
                host=global_['host'],
                port=global_['port'],
                database=global_['db'],
            ) as connection:
                cursor = connection.cursor()
                cursor.callproc('cancel_order_w', [self.right.id_order])
                connection.commit()
            self.right.any_selected = False
            self.clear_orders()
        except Exception as e:
            print(e, '|w_face cancel_order')

    def send_info_vehicle(self):
        try:
            if self.right_2.button.text() != 'Назад':
                d = self.right_2.return_info()
                with connect(
                    user=w_c['user'],
                    password=w_c['pass'],
                    host=global_['host'],
                    port=global_['port'],
                    database=global_['db'],
                ) as connection:
                    cursor = connection.cursor()
                    cursor.callproc('new_vehicle', (self.id_work, d[0], d[1], d[2], d[3]))
                    connection.commit()
            else:
                self.right_2.clear()
        except Exception as e:
            print(e, '|w_face send_info_vehicle')

    def display_vehicle_info(self, data):
        self.right_2.set_info(data)

    def display_chat(self, id_):
        if not self.right_3.isVisible():
            self.right.hide()
            self.bottom_layout.replaceWidget(self.right, self.right_3)
            self.right_3.set_order_id(id_)
            self.right_3.set_fio_info()
            self.right_3.show()
        else:
            self.right_3.clear_chat()
            if id_ == self.right_3.get_order_id():
                self.right_3.hide()
                self.right_3.set_order_id(None)
                self.bottom_layout.replaceWidget(self.right_3, self.right)
                self.right.show()
            else:
                self.right_3.set_order_id(id_)
                self.right_3.set_fio_info()

    def quit(self):
        self.login.show()
        self.login.login_edit.clear()
        self.login.password_edit.clear()
        self.login.login_edit.setFocus()
        self.right.map.close()
        self.left_2.close()
        self.left.close()
        self.close()
