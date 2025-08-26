from PyQt6.QtWidgets import QScrollArea, QWidget, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSignal, QTimer
from mysql.connector import connect
from frames.Vehicle import *
from frames.Order import *
from config import global_


class LeftBox(QWidget):
    order_info = pyqtSignal(list)
    vehicle_info = pyqtSignal(list)
    state_click = pyqtSignal(str)

    def __init__(self, id_, purpose, config):
        super().__init__()

        self.id_ = id_
        self.purpose = purpose
        self.config = config
        self.setFixedWidth(230)

        layout = QVBoxLayout()

        self.left_box = QGroupBox('Сделанные заказы')
        self.left_box.setContentsMargins(0, 18, 0, 0)

        left_box_layout = QVBoxLayout()

        if self.purpose in ('client', 'worker'):
            search_layout = QHBoxLayout()
            search_layout.setSpacing(3)
            search_layout.setContentsMargins(3, 0, 0, 0)
            self.search = QLineEdit()
            self.search.setPlaceholderText('Поиск...')
            self.search.setToolTip('{параметр} {знак} {значение}\nпараметры: откуда, куда, расстояние,'
                                   '\n\t  дата, цена, площадь, объём,\n\t  вес\nзнаки: =, <, >')
            self.search.textChanged.connect(self.search_update)
            search_layout.addWidget(self.search)

            choose_sort = QPushButton('✓')
            choose_sort.setToolTip('ПКМ ‒ обновить')
            choose_sort.setFixedWidth(27)
            choose_sort.clicked.connect(self.choose_sort_)
            choose_sort.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            choose_sort.customContextMenuRequested.connect(self.clear)
            search_layout.addWidget(choose_sort)

            self.date_sort = QPushButton('🡹')
            self.date_sort.setToolTip('ПКМ ‒ обновить')
            self.date_sort.setFixedWidth(27)
            self.date_sort.clicked.connect(self.date_sort_)
            self.date_sort.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.date_sort.customContextMenuRequested.connect(self.clear)
            search_layout.addWidget(self.date_sort)

            left_box_layout.addLayout(search_layout)

        left_scroll_area = QScrollArea()
        left_scroll_area.setWidgetResizable(True)
        left_scroll_area.setFixedWidth(220)
        left_scroll_area.setStyleSheet('QScrollArea {border: none;}')

        scrollWidget = QWidget()

        self.left_layout = QVBoxLayout(scrollWidget)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.addStretch(1)
        left_scroll_area.setWidget(scrollWidget)

        left_box_layout.addWidget(left_scroll_area)
        left_box_layout.setContentsMargins(6, 0, 6, 8)
        self.left_box.setLayout(left_box_layout)

        layout.addWidget(self.left_box)

        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        self.updater = QTimer(self)
        if self.purpose in ('client', 'worker', 'vehicle'):
            self.updater.timeout.connect(self.update_)
        self.updater.start(1000)

    def search_update(self):
        try:
            search_text = self.search.text().lower().strip()
            words = search_text.split(' ')

            context = {'откуда': 'from__',
                       'куда': 'to__',
                       'расстояние': 'dist_',
                       'дата': 'date_time',
                       'цена': 'price_',
                       'площадь': 'space',
                       'объём': 'capacity',
                       'вес': 'weight'}

            if len(search_text) > 1:
                if len(words) == 3 and words[0] in context:
                    for i in range(self.left_layout.count()):
                        widget = self.left_layout.itemAt(i).widget()
                        if widget is not None:
                            if words[1] == '=' and words[2] in getattr(widget, context[words[0]]):
                                widget.show()
                            elif words[1] == '<' and int(words[2]) >= int(getattr(widget, context[words[0]])):
                                widget.show()
                            elif words[1] == '>' and int(words[2]) <= int(getattr(widget, context[words[0]])):
                                widget.show()
                            else:
                                widget.hide()
            else:
                for i in range(self.left_layout.count() - 1):
                    widget = self.left_layout.itemAt(i).widget()
                    widget.show()
        except Exception as e:
            print(e, 'left | search_update')

    def choose_sort_(self):
        labels = [self.left_layout.itemAt(i).widget() for i in range(self.left_layout.count())]
        labels.remove(None)

        labels.sort(key=lambda lb: (lb.state_ == '1', lb.state_))

        for i in reversed(range(self.left_layout.count())):
            self.left_layout.removeWidget(self.left_layout.itemAt(i).widget())

        for label in labels:
            self.left_layout.insertWidget(0, label)

    def date_sort_(self):
        if self.date_sort.text() == '🡻':
            reverse = False
            self.date_sort.setText('🡹')
        else:
            reverse = True
            self.date_sort.setText('🡻')

        labels = [self.left_layout.itemAt(i).widget() for i in range(self.left_layout.count())]
        labels.remove(None)

        labels.sort(key=lambda lb: lb.date_time, reverse=reverse)

        for i in reversed(range(self.left_layout.count())):
            self.left_layout.removeWidget(self.left_layout.itemAt(i).widget())

        for label in labels:
            self.left_layout.insertWidget(0, label)

    def clear(self):
        try:
            for i in reversed(range(self.left_layout.count())):
                wid = self.left_layout.itemAt(i).widget()
                if wid is not None:
                    wid.close()
                self.left_layout.removeWidget(wid)
        except Exception as e:
            print(e, '|l_scroll clear')

    def update_(self):
        try:
            if self.purpose == 'client':
                procedure = 'get_orders_c'
            elif self.purpose == 'worker':
                procedure = 'get_orders_w'
            elif self.purpose == 'vehicle':
                procedure = 'get_vehicles'

            with connect(
                user=self.config['user'],
                password=self.config['pass'],
                host=global_['host'],
                port=global_['port'],
                database=global_['db'],
            ) as connection:
                cursor = connection.cursor()
                data = cursor.callproc(procedure, (self.id_, None))[-1]
                connection.commit()
            if data is not None:
                data = [i.split('|') for i in data.split(';')]
            else:
                return
            frames = [self.left_layout.itemAt(i).widget() for i in range(self.left_layout.count())]
            frames.remove(None)
            ids = [i.get_id() for i in frames]

            for i in data:
                if frames:
                    if i[0] in ids:
                        for j in frames:
                            if i[0] == j.get_id():
                                if i != j.return_info():
                                    j.set_info(i)
                    else:
                        if self.purpose == 'vehicle':
                            self.add_vehicle(i)
                        else:
                            self.add_order(i)
                else:
                    if self.purpose == 'vehicle':
                        self.add_vehicle(i)
                    else:
                        self.add_order(i)
        except Exception as e:
            print(e, 'l_scroll update')

    def add_order(self, info):
        order = Order(info)
        self.left_layout.insertWidget(0, order)
        order.add_action(lambda: self.send_info(order.return_info_map()))
        order.state.add_action(lambda: self.state_clicked(order.get_id()))

    def add_vehicle(self, info):
        vehicle = Vehicle(self.id_, info)
        vehicle.add_action(lambda: self.send_info(vehicle.return_info()))
        self.left_layout.insertWidget(0, vehicle)

    def state_clicked(self, id_):
        self.state_click.emit(id_)

    def send_info(self, info):
        if self.purpose in ('client', 'worker'):
            self.order_info.emit(info)
        elif self.purpose == 'vehicle':
            self.vehicle_info.emit(info)
