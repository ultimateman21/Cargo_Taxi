from PyQt6.QtWidgets import QWidget, QGroupBox, QLabel, QPushButton, QLineEdit, QDateEdit, QTimeEdit, QGridLayout, QVBoxLayout, QHBoxLayout
from osmnx import load_graphml, graph_to_gdfs, graph_from_bbox, nearest_nodes
from PyQt6.QtCore import Qt, QThread, QDate, QTime, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView
from folium import Map, Marker, Icon, PolyLine
from geopy.geocoders import Nominatim
from networkx import shortest_path
from os.path import dirname, join
from shapely import Point
from math import ceil

geolocator = Nominatim(user_agent='geoapi2870')


class Mapper(QThread):
    progressChanged = pyqtSignal(int)

    def __init__(self, from_, to_):
        super().__init__()
        self.from_ = from_
        self.to_ = to_

    def run(self):
        try:
            if self.from_ and self.to_:
                s_cord = geolocator.geocode(self.from_)
                f_cord = geolocator.geocode(self.to_)
                s_point = (s_cord.latitude, s_cord.longitude)
                f_point = (f_cord.latitude, f_cord.longitude)

                points = (s_point, f_point)

                n = max((i[0] for i in points)) + 0.05
                s = min((i[0] for i in points)) - 0.05
                e = max((i[1] for i in points)) + 0.05
                w = min((i[1] for i in points)) - 0.05

                graph = load_graphml(join(dirname(__file__), '..', 'source', 'rostov.graphml'))
                polygon = graph_to_gdfs(graph, edges=False).unary_union.convex_hull

                if not polygon.contains(Point(s_point[1], s_point[0])) or not polygon.contains(Point(f_point[1], f_point[0])):
                    graph = graph_from_bbox(bbox=(n, s, e, w), network_type='drive')

                origin_node = nearest_nodes(graph, s_point[1], s_point[0])
                destination_node = nearest_nodes(graph, f_point[1], f_point[0])

                route = shortest_path(graph, origin_node, destination_node, weight='length')

                m = Map(location=s_point, zoom_start=12)
                Marker(location=s_point, icon=Icon(color='green')).add_to(m)
                Marker(location=f_point, icon=Icon(color='red')).add_to(m)

                route_points = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in route]
                PolyLine(route_points, color="blue", weight=4, opacity=1).add_to(m)

                m.save(join(dirname(__file__), '..', 'source', 'map.html'))

                total_distance = int(sum(graph.edges[edge]['length'] for edge in zip(route[:-1], route[1:], [0] * len(route[:-1]))))
                self.progressChanged.emit(total_distance)
            else:
                m = Map(location=(47.2357, 39.7015), zoom_start=11)
                m.save(join(dirname(__file__), '..', 'source', 'map.html'))
                self.progressChanged.emit(0)
        except Exception as e:
            print(e, '|r_map mapper')


class RightMapBox(QWidget):
    def __init__(self):
        super().__init__()

        self.worker_thread = None

        self.id_order = None
        self.state = None
        self.any_selected = False

        layout = QVBoxLayout()

        map_box = QGroupBox('Местоположение')
        map_layout = QVBoxLayout()

        self.map = QWebEngineView()
        map_layout.addWidget(self.map)

        map_box.setLayout(map_layout)
        layout.addWidget(map_box)

        order_box = QGroupBox('Детали заказа')
        order_layout = QVBoxLayout()

        from_to_layout = QGridLayout()

        from_l = QLabel('Откуда:')
        from_l.setStyleSheet('padding-left: 5px; padding-right: 5px; background-color: rgb(113, 174, 38); border-radius: 3px')
        from_to_layout.addWidget(from_l, 0, 0)

        self.from_edit = QLineEdit()
        self.from_edit.returnPressed.connect(self.handle_enter_key)
        self.from_edit.textChanged.connect(self.check_input_fields)
        from_to_layout.addWidget(self.from_edit, 0, 1)

        to_l = QLabel('Куда:')
        to_l.setStyleSheet('padding-left: 5px; padding-right: 5px; background-color: rgb(208, 60, 41); border-radius: 3px')
        from_to_layout.addWidget(to_l, 1, 0)

        self.to_edit = QLineEdit()
        self.to_edit.returnPressed.connect(self.handle_enter_key)
        self.to_edit.textChanged.connect(self.check_input_fields)
        from_to_layout.addWidget(self.to_edit, 1, 1)

        order_layout.addLayout(from_to_layout)

        data_time_dist_layout = QHBoxLayout()

        data_l = QLabel('Дата:')
        data_time_dist_layout.addWidget(data_l)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat('dd-MM-yyyy ')
        current_date = QDate.currentDate()
        self.date_edit.setDate(current_date)
        data_time_dist_layout.addWidget(self.date_edit)

        time_l = QLabel('Время:')
        data_time_dist_layout.addWidget(time_l)

        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat('HH:mm')
        self.time_edit.editingFinished.connect(self.handle_enter_key)
        data_time_dist_layout.addWidget(self.time_edit)

        self.route_b = QPushButton('Построить маршрут')
        self.route_b.clicked.connect(self.map_constructor)
        data_time_dist_layout.addWidget(self.route_b)

        self.dist_edit = QLineEdit()
        self.dist_edit.setReadOnly(True)
        self.dist_edit.textChanged.connect(self.price_constructor)
        data_time_dist_layout.addWidget(self.dist_edit)

        dist_l = QLabel('метров')
        data_time_dist_layout.addWidget(dist_l)

        order_layout.addLayout(data_time_dist_layout)

        order_layout.addLayout(data_time_dist_layout)

        order_box.setLayout(order_layout)
        layout.addWidget(order_box)

        cargo_box = QGroupBox('Параметры груза')
        cargo_layout = QGridLayout()

        space_l = QLabel('Площадь м<sup>2</sup> :')
        cargo_layout.addWidget(space_l, 0, 0)

        self.space_edit = QLineEdit()
        self.space_edit.returnPressed.connect(self.handle_enter_key)
        self.space_edit.textChanged.connect(self.check_input_fields)
        cargo_layout.addWidget(self.space_edit, 0, 1)

        capacity_l = QLabel('Объём м<sup>3</sup> :')
        cargo_layout.addWidget(capacity_l, 0, 2)

        self.capacity_edit = QLineEdit()
        self.capacity_edit.returnPressed.connect(self.handle_enter_key)
        self.capacity_edit.textChanged.connect(self.check_input_fields)
        self.capacity_edit.textChanged.connect(self.price_constructor)
        cargo_layout.addWidget(self.capacity_edit, 0, 3)

        weight_l = QLabel('Вес кг :')
        cargo_layout.addWidget(weight_l, 0, 4)

        self.weight_edit = QLineEdit()
        self.weight_edit.textChanged.connect(self.check_input_fields)
        cargo_layout.addWidget(self.weight_edit, 0, 5)

        price_l = QLabel('Цена руб :')
        cargo_layout.addWidget(price_l, 1, 0)

        self.price_edit = QLineEdit()
        self.price_edit.setReadOnly(True)
        self.price_edit.textChanged.connect(self.check_input_fields)
        cargo_layout.addWidget(self.price_edit, 1, 1)

        button_layout = QHBoxLayout()

        self.button = QPushButton('Оформить заказ')
        self.button.setMinimumWidth(157)
        self.button.setEnabled(False)
        button_layout.addWidget(self.button)

        self.button1 = QPushButton('Отменить')
        self.button1.hide()
        button_layout.addWidget(self.button1)

        cargo_layout.addLayout(button_layout, 1, 2, 1, 4)

        cargo_box.setLayout(cargo_layout)
        layout.addWidget(cargo_box)

        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        m = Map(location=(47.2357, 39.7015), zoom_start=11)

        m.save(join(dirname(__file__), '..', 'source', 'map.html'))
        self.map.setHtml(open(join(dirname(__file__), '..', 'source', 'map.html')).read())

        # self.from_edit.setText('Ростов-на-Дону, улица Волкова, 8 к 1')
        # self.to_edit.setText('Ростов-на-Дону, улица Большая Садовая, 55')

    def handle_enter_key(self):
        sender = self.sender()
        if sender == self.from_edit:
            self.to_edit.setFocus()
        elif sender == self.to_edit:
            self.date_edit.setFocus()
        elif sender == self.time_edit:
            self.space_edit.setFocus()
        elif sender == self.space_edit:
            self.capacity_edit.setFocus()
        elif sender == self.capacity_edit:
            self.weight_edit.setFocus()

    def check_input_fields(self):
        if (self.from_edit.text() and self.to_edit.text() and self.dist_edit.text() and self.space_edit.text() and
                self.capacity_edit.text() and self.weight_edit.text() and self.price_edit.text()):
            self.button.setEnabled(True)
        else:
            self.button.setEnabled(False)

    def price_constructor(self):
        if self.dist_edit.text() and self.capacity_edit.text():
            v = float('.'.join(self.capacity_edit.text().split(',')))
            price = int(ceil(int(self.dist_edit.text()) / 1000) * v * 10)
            order = 10 ** (len(str(price)) - 2)
            price = ceil(price / order) * order
            self.price_edit.setText(str(price))

    def return_info(self):
        return [self.from_edit.text(), self.to_edit.text(), int(self.dist_edit.text()), self.date_edit.text(), self.time_edit.text(),
                int(self.price_edit.text()), float(self.space_edit.text()), float(self.capacity_edit.text()), float(self.weight_edit.text())]

    def map_constructor(self):
        if not self.worker_thread or not self.worker_thread.isRunning():
            self.route_b.setEnabled(False)
            self.worker_thread = Mapper(self.from_edit.text(), self.to_edit.text())
            self.worker_thread.progressChanged.connect(self.dist_view)
            self.worker_thread.finished.connect(self.map_view)
            self.worker_thread.start()

    def dist_view(self, dist):
        if dist:
            self.dist_edit.setText(str(dist))
        else:
            self.dist_edit.setText('')
            self.check_input_fields()

    def map_view(self):
        self.route_b.setEnabled(True)
        self.map.setHtml(open(join(dirname(__file__), '..', 'source', 'map.html')).read())

    def set_info_to_map(self, data):
        wid = [self.from_edit, self.to_edit, self.dist_edit, self.date_edit, self.time_edit,
               self.price_edit, self.space_edit, self.capacity_edit, self.weight_edit]
        for i, info in enumerate(data):
            if i == 0:
                self.id_order = info
            elif i == 4:
                wid[3].setDate(QDate.fromString(str(info), 'dd-MM-yyyy '))
                wid[3].setReadOnly(True)
            elif i == 5:
                wid[4].setTime(QTime.fromString(str(info), 'HH:mm'))
                wid[4].setReadOnly(True)
            elif i == len(data) - 1:
                self.state = info
            else:
                wid[i - 1].setText(str(info))
                wid[i - 1].setReadOnly(True)

        self.route_b.setText('Отобразить маршрут')

        if 'c_face' in str(self.parent()):
            self.button1.hide()
            if not int(self.state):
                self.button1.show()
        elif 'w_face' in str(self.parent()):
            self.button.setText('Выбрать')
            if self.any_selected:
                self.button.setEnabled(False)
            else:
                self.button.setEnabled(True)
            self.button1.hide()
            if int(self.state):
                self.button.setText('Завершить')
                self.button1.show()

        if self.button.text() == 'Оформить заказ':
            self.button.setText('Назад')
        self.button.setEnabled(True)

    def clear(self):
        try:
            wid = [self.from_edit, self.to_edit, self.dist_edit, self.date_edit, self.time_edit,
                   self.price_edit, self.space_edit, self.capacity_edit, self.weight_edit]

            for i, widg in enumerate(wid):
                if i == 3:
                    widg.setDate(QDate.currentDate())
                elif i == 4:
                    widg.setTime(QTime.fromString('00:00', 'HH:mm'))
                else:
                    widg.setText('')
                widg.setReadOnly(False)

            self.button.setEnabled(False)

            self.route_b.setText('Построить маршрут')
            self.button.setText('Оформить заказ')
            if 'c_face' in str(self.parent()):
                self.button1.hide()
            elif 'w_face' in str(self.parent()):
                self.button1.hide()
                self.button.setText('Выбрать')
            self.state = ''
        except Exception as e:
            print(e, '|map clear')
