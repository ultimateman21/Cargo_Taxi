from PyQt6.QtWidgets import QWidget, QGroupBox, QLabel, QVBoxLayout, QScrollArea, QHBoxLayout, QTextEdit, QFrame
from frames.MultiPressableThings import MultiPressableLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QTextCursor
from mysql.connector import connect
from datetime import datetime
from config import global_


class Message(QFrame):
    def __init__(self, text, date, parent=None):
        super().__init__(parent)

        self.original_date = date

        layout = QVBoxLayout()

        self.text = QLabel(str(text))

        self.text.setWordWrap(True)
        if len(str(text)) < 66:
            self.text.setWordWrap(False)
            self.text.setMinimumHeight(15)
            self.text.setMinimumWidth(int(len(str(text)) * 1.4))
        else:
            self.text.setMinimumWidth(self.parent().width() - 100)
            if 65 < len(str(text)) < 131:
                self.text.setMinimumHeight(1)
            elif 130 < len(str(text)) < 201:
                self.text.setMinimumHeight(45)

        layout.addWidget(self.text)

        self.date = QLabel(f'{date.split(" ")[1][:-3]} {date.split(" ")[0]}')
        self.date.setStyleSheet('font-size: 10px;')
        self.date.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.date, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

    def get_date(self):
        return self.original_date


class AutoTextEdit(QTextEdit):
    def __init__(self, max_height=30, max_length=200):
        super(AutoTextEdit, self).__init__()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.max_height = max_height
        self.max_length = max_length
        self.textChanged.connect(self.update_size)
        self.textChanged.connect(self.enforce_max_length)
        self.update_size()

    def update_size(self):
        doc_height = self.document().size().height()
        if doc_height > 0:
            new_height = min(doc_height, self.max_height)
            self.setMinimumHeight(int(new_height))
            self.setMaximumHeight(int(new_height))

    def enforce_max_length(self):
        text = self.toPlainText()
        if len(text) > self.max_length:
            self.blockSignals(True)
            self.setText(text[:self.max_length])
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.setTextCursor(cursor)
            self.blockSignals(False)


class RightChatBox(QWidget):
    def __init__(self, id_, purpose, config):
        super().__init__()
        self.setFixedWidth(492)

        self.id_ = id_
        self.purpose = purpose
        self.config = config
        self.order_id = None
        self.chat_scroll_flag = False

        layout = QVBoxLayout()

        worker_box = QGroupBox('Водитель')
        worker_layout = QHBoxLayout()

        self.fio_e_w = QLabel()
        worker_layout.addWidget(self.fio_e_w)

        worker_layout.addStretch(1)

        self.num_e_w = QLabel()
        worker_layout.addWidget(self.num_e_w)

        worker_box.setLayout(worker_layout)
        layout.addWidget(worker_box)

        client_box = QGroupBox('Клиент')
        client_layout = QHBoxLayout()

        self.fio_e_c = QLabel()
        client_layout.addWidget(self.fio_e_c)

        client_layout.addStretch()

        self.num_e_c = QLabel()
        client_layout.addWidget(self.num_e_c)

        client_box.setLayout(client_layout)
        layout.addWidget(client_box)

        chat_box = QGroupBox('Чат')
        chat_box.setContentsMargins(0, 18, 0, 0)

        chat_box_layout = QVBoxLayout()

        self.chat_scroll_area = QScrollArea()
        self.chat_scroll_area.setWidgetResizable(True)
        self.chat_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.chat_scroll_area.setStyleSheet('QScrollArea {border: none;}')

        scrollWidget = QWidget()

        self.chat_layout = QVBoxLayout(scrollWidget)
        self.chat_layout.setContentsMargins(0, 0, 0, 0)

        self.chat_layout.addStretch(1)
        self.chat_scroll_area.setWidget(scrollWidget)

        chat_box_layout.addWidget(self.chat_scroll_area)

        send_layout = QHBoxLayout()

        self.e_message = AutoTextEdit(80)
        send_layout.addWidget(self.e_message)

        self.send_b = MultiPressableLabel(style_name='green')
        self.send_b.setText('➦')
        self.send_b.setFixedSize(40, 25)
        self.send_b.add_action(lambda: self.send_message())
        self.send_b.setAlignment(Qt.AlignmentFlag.AlignCenter)
        send_layout.addWidget(self.send_b, alignment=Qt.AlignmentFlag.AlignTop)

        chat_box_layout.addLayout(send_layout)

        chat_box_layout.setContentsMargins(6, 0, 6, 6)
        chat_box.setLayout(chat_box_layout)

        layout.addWidget(chat_box)

        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.updater = QTimer(self)
        self.updater.timeout.connect(self.update_)

    def set_order_id(self, id_):
        try:
            self.order_id = id_
            if self.order_id is not None:
                self.updater.start(1000)
            else:
                self.updater.stop()
        except Exception as e:
            print(e, '|r_chat set_order_id')

    def get_order_id(self):
        return self.order_id

    def send_message(self):
        try:
            if self.e_message.toPlainText():
                with connect(
                    user=self.config['user'],
                    password=self.config['pass'],
                    host=global_['host'],
                    port=global_['port'],
                    database=global_['db'],
                ) as connection:
                    cursor = connection.cursor()
                    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    text = self.e_message.toPlainText()
                    self.e_message.clear()
                    cursor.callproc('new_message', (self.order_id, date, text, self.purpose))
                    connection.commit()
        except Exception as e:
            print(e, '|r_chat send_message')

    def update_(self):
        try:
            with connect(
                user=self.config['user'],
                password=self.config['pass'],
                host=global_['host'],
                port=global_['port'],
                database=global_['db'],
            ) as connection:
                cursor = connection.cursor()
                data = cursor.callproc('get_messages', (self.order_id, None))[-1]
                connection.commit()

            if data is not None:
                data = sorted([i.split('|') for i in data.split(';')], key=lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S'))
            else:
                self.clear_chat()
                return

            messages = [self.chat_layout.itemAt(i).widget() for i in range(self.chat_layout.count())]
            messages.remove(None)
            dates = [i.get_date() for i in messages]

            for i in data:
                if messages:
                    if i[0] not in dates:
                        self.add_message(i[1], i[0], i[2])
                else:
                    self.add_message(i[1], i[0], i[2])

            if self.chat_scroll_flag:
                self.chat_scroll_area.verticalScrollBar().setValue(self.chat_scroll_area.verticalScrollBar().maximum())
                self.chat_scroll_flag = False

        except Exception as e:
            print(e, '|r_chat update')

    def add_message(self, text, date, role):
        m = Message(text, date, self)
        if role == self.purpose:
            m.setStyleSheet('background-color: rgb(80, 90, 170); border-radius: 15px;')
            alignment = Qt.AlignmentFlag.AlignRight
        else:
            m.setStyleSheet('background-color: rgb(170, 170, 170); border-radius: 15px;')
            alignment = Qt.AlignmentFlag.AlignLeft
        self.chat_layout.insertWidget(-1, m, alignment=alignment)
        self.chat_scroll_flag = True

    def clear_chat(self):
        for i in reversed(range(self.chat_layout.count())):
            wid = self.chat_layout.itemAt(i).widget()
            if wid is not None:
                wid.close()
                self.chat_layout.removeWidget(wid)
                wid.deleteLater()

    def set_fio_info(self):
        try:
            self.fio_e_w.clear()
            self.num_e_w.clear()
            self.fio_e_c.clear()
            self.num_e_c.clear()

            with connect(
                user=self.config['user'],
                password=self.config['pass'],
                host=global_['host'],
                port=global_['port'],
                database=global_['db'],
            ) as connection:
                cursor = connection.cursor()
                data = cursor.callproc('get_chat_fios', (self.order_id, None, None))[-2:]
                connection.commit()

            self.fio_e_w.setText(data[0].split(';')[0])
            self.num_e_w.setText(data[0].split(';')[1])

            self.fio_e_c.setText(data[1].split(';')[0])
            self.num_e_c.setText(data[1].split(';')[1])

        except Exception as e:
            print(e, '|r_chat set_fio_info')
