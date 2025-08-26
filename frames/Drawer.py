from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLineEdit, QGroupBox, QHBoxLayout, QLabel, QGraphicsDropShadowEffect, \
    QSizePolicy, QScrollArea, QMessageBox
from config import global_, mysqldump_path, mysql_path, backup_dir
from frames.MultiPressableThings import MultiPressableLabel
from PyQt6.QtCore import QPropertyAnimation, QDate, QTime
from os import listdir, path, makedirs
from mysql.connector import connect
from subprocess import run, PIPE
from datetime import datetime
from re import sub


class Drawer(QWidget):
    def __init__(self, id_, purpose, config, parent=None):
        super().__init__(parent)

        self.setGeometry(0, 0, 230, self.parent().height())
        self.setStyleSheet('background-color: rgb(240, 240, 240)')
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        self.id = id_
        self.role = purpose
        self.config = config
        self.expanded = False

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(-1, 1)
        self.setGraphicsEffect(self.shadow)

        layout = QVBoxLayout()

        drawer_box = QGroupBox()
        item_layout = QVBoxLayout()

        phone_box = QGroupBox('Номер телефона')
        phone_layout = QVBoxLayout()
        phone_layout.setContentsMargins(8, 4, 8, 8)

        self.phone_l = QLabel()
        phone_layout.addWidget(self.phone_l)
        self.get_phone()

        phone_edit_layout = QHBoxLayout()

        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText('Новый номер')
        self.phone_edit.setStyleSheet('background-color: white;')
        phone_edit_layout.addWidget(self.phone_edit)

        self.phone_edit_b = QPushButton('Изменить')
        self.phone_edit_b.setEnabled(False)
        phone_edit_layout.addWidget(self.phone_edit_b)

        phone_layout.addLayout(phone_edit_layout)
        phone_box.setLayout(phone_layout)
        item_layout.addWidget(phone_box)

        password_box = QGroupBox('Смена пароля')
        password_layout = QVBoxLayout()
        password_layout.setContentsMargins(8, 4, 8, 8)

        self.password_1_edit = QLineEdit()
        self.password_1_edit.setStyleSheet('background-color: white;')
        self.password_1_edit.setPlaceholderText('Новый пароль')
        self.password_1_edit.returnPressed.connect(self.handle_enter_key)
        password_layout.addWidget(self.password_1_edit)

        self.password_2_edit = QLineEdit()
        self.password_2_edit.setStyleSheet('background-color: white;')
        self.password_2_edit.setPlaceholderText('Повторите пароль')
        password_layout.addWidget(self.password_2_edit)

        password_b = QPushButton('Изменить')
        password_b.setEnabled(False)
        password_layout.addWidget(password_b)

        password_box.setLayout(password_layout)
        item_layout.addWidget(password_box)

        self.context = {'client': ['История заказов', 'Посмотреть', 150],
                        'worker': ['История заказов', 'Посмотреть', 150],
                        'employee': ['Сохранение/Восстановление', 'Восстановить', 70]}

        drop_box = QGroupBox(self.context[self.role][0])
        drop_layout = QVBoxLayout()
        drop_layout.setContentsMargins(8, 4, 8, 8)

        if self.role == 'employee':
            drop_b1 = QPushButton('Сохранить')
            drop_b1.clicked.connect(self.toggle_save)
            drop_layout.addWidget(drop_b1)

        drop_b2 = QPushButton(self.context[self.role][1])
        drop_b2.clicked.connect(self.toggle_exp)
        drop_layout.addWidget(drop_b2)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMaximumHeight(0)
        self.scroll_area.setMinimumHeight(0)

        scrollWidget = QWidget()
        scrollWidget.setStyleSheet('QWidget {background-color: rgb(250, 250, 250)}')
        self.drop_l_layout = QVBoxLayout(scrollWidget)
        self.drop_l_layout.setContentsMargins(3, 3, 3, 3)
        self.drop_l_layout.addStretch(0)
        self.scroll_area.setWidget(scrollWidget)

        drop_layout.addWidget(self.scroll_area)
        drop_box.setLayout(drop_layout)
        item_layout.addWidget(drop_box)

        self.animation_min = QPropertyAnimation(self.scroll_area, b"minimumHeight")
        self.animation_max = QPropertyAnimation(self.scroll_area, b"maximumHeight")

        self.quit_b = QPushButton('Выйти')
        self.quit_b.setStyleSheet('margin-top: 15px; padding: 5px')
        item_layout.addWidget(self.quit_b)

        item_layout.addStretch(1)
        drawer_box.setLayout(item_layout)
        layout.addWidget(drawer_box)

        self.setLayout(layout)

    def handle_enter_key(self):
        sender = self.sender()
        if sender == self.password_1_edit:
            self.password_2_edit.setFocus()

    def get_phone(self):
        with connect(
                user=self.config['user'],
                password=self.config['pass'],
                host=global_['host'],
                port=global_['port'],
                database=global_['db'],
        ) as connection:
            cursor = connection.cursor()
            phone = cursor.callproc('get_phone', (self.id, self.role, None))[-1]
            connection.commit()
        self.phone_l.setText(phone)

    def toggle_save(self):
        try:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Подтверждение')
            msg_box.setText('Создать дамп?')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            response = msg_box.exec()

            if response == QMessageBox.StandardButton.Yes:
                timestamp = datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
                output_folder = path.join(backup_dir, 'dumps')
                output_file = path.join(output_folder, f'{timestamp}.sql')

                if not path.exists(output_folder):
                    makedirs(output_folder)

                command = [mysqldump_path, '-h', global_['host'], '-P', global_['port'], '-u', self.config['user'], f'-p{self.config["pass"]}',
                           global_['db'], '--routines', '--triggers', '--single-transaction']

                with open(output_file, 'w') as outfile:
                    run(command, stdout=outfile, stderr=PIPE, text=True)

                with connect(
                        user=self.config['user'],
                        password=self.config['pass'],
                        host=global_['host'],
                        port=global_['port'],
                        database=global_['db'],
                ) as connection:
                    cursor = connection.cursor()
                    grants = cursor.callproc('get_user_grants', ('reg, client, worker', 'localhost, localhost, localhost', None))[-1]
                    connection.commit()

                grants = sub(r'(\w+)\.(\w+)', r'`\1`.`\2`', grants)
                grants = sub(r'(\w+)@(\w+)', r'`\1`@`\2`', grants)

                with open(output_file, 'r') as file:
                    lines = file.readlines()

                lines.insert(0, 'START TRANSACTION;\n')
                lines.append(grants)
                lines.append('COMMIT;\n')

                with open(output_file, 'w') as file:
                    file.writelines(lines)

                self.clear()
                self.load_dumps_labels()
        except Exception as e:
            print(e, '|drawer toggle_save')

    def toggle_exp(self):
        if self.expanded:
            self.collapse()
            self.clear()
        elif self.role in ['client', 'worker']:
            self.load_h_orders()
            self.expand()
        elif self.role == 'employee':
            self.load_dumps_labels()
            self.expand()

    def expand(self):
        self.expanded = True

        self.animation_min.setDuration(300)
        self.animation_max.setDuration(300)

        self.animation_min.setStartValue(0)
        self.animation_min.setEndValue(self.context[self.role][2])
        self.animation_max.setStartValue(0)
        self.animation_max.setEndValue(self.context[self.role][2])

        self.animation_min.start()
        self.animation_max.start()

    def collapse(self):
        self.expanded = False

        self.animation_min.setDuration(300)
        self.animation_max.setDuration(300)

        self.animation_min.setStartValue(self.context[self.role][2])
        self.animation_min.setEndValue(0)
        self.animation_max.setStartValue(self.context[self.role][2])
        self.animation_max.setEndValue(0)

        self.animation_min.start()
        self.animation_max.start()

    def load_dumps_labels(self):
        try:
            if not path.exists(path.join(backup_dir, 'dumps')):
                makedirs(path.join(backup_dir, 'dumps'))

            files = [f for f in listdir(path.join(backup_dir, 'dumps')) if f.endswith('.sql')]
            for i in files:
                self.add_dump(i)
        except Exception as e:
            print(e, '|drawer load_dumps_labels')

    def add_dump(self, text):
        dump = MultiPressableLabel(style_name='flat')
        dump.setText(text[:-4])
        self.drop_l_layout.insertWidget(0, dump)
        dump.add_action(lambda: self.load_dump(dump.get_text()))

    def load_h_orders(self):
        try:
            if self.role == 'client':
                procedure = 'get_h_orders_c'
            elif self.role == 'worker':
                procedure = 'get_h_orders_w'

            with connect(
                    user=self.config['user'],
                    password=self.config['pass'],
                    host=global_['host'],
                    port=global_['port'],
                    database=global_['db'],
            ) as connection:
                cursor = connection.cursor()
                text = cursor.callproc(procedure, (self.id, None))[-1]
                connection.commit()

            if text is not None:
                data = [i.split('|') for i in text.split(';')]
            else:
                return

            context = ['Откуда', 'Куда', 'Расстояние м ', 'Дата', 'Время', 'Цена руб ', 'Площадь м<sup>2</sup> ',
                       'Объём м<sup>3</sup> ', 'Вес кг ', 'Состояние']
            for i in data:
                text = []
                tooltip = []
                for j, el in enumerate(i):
                    if j in [0, 1]:
                        text.append(', '.join(str(el).split(', ')[1:]))
                        tooltip.append(f'{context[j]}: {el}')
                    elif j == 3:
                        d_t = str(el).split(' ')
                        text.insert(0, QDate.fromString(d_t[0], 'yyyy-MM-dd').toString('dd-MM-yyyy ') +
                                    QTime.fromString(d_t[1], 'hh:mm:ss').toString('hh:mm'))
                        tooltip.append(f"{context[3]}: {QDate.fromString(d_t[0], 'yyyy-MM-dd').toString('dd-MM-yyyy ')}")
                        tooltip.append(f"{context[4]}: {QTime.fromString(d_t[1], 'hh:mm:ss').toString('hh:mm')}")
                    elif j == len(i) - 1:
                        if el == '2':
                            text[0] = text[0] + '\t✗'
                            tooltip.append(f'{context[j + 1]}: Отменён')
                        elif el == '3':
                            text[0] = text[0] + '\t✔'
                            tooltip.append(f'{context[j + 1]}: Завершён')
                    else:
                        if j == 2:
                            tooltip.append(f'{context[j]}: {el}')
                        else:
                            tooltip.append(f'{context[j + 1]}: {el}')

                self.add_h_order('\n'.join(text), tooltip)
        except Exception as e:
            print(e, '|load_h_orders drawer')

    def add_h_order(self, text, tooltip):
        h_order = MultiPressableLabel(style_name='flat')
        h_order.setText(text)
        h_order.setToolTip(f"<html>{'<br>'.join(tooltip)}</html>")
        self.drop_l_layout.insertWidget(0, h_order)

    def clear(self):
        for i in reversed(range(self.drop_l_layout.count())):
            wid = self.drop_l_layout.itemAt(i).widget()
            if wid is not None:
                wid.close()
            self.drop_l_layout.removeWidget(wid)

    def load_dump(self, text):
        try:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Подтверждение')
            msg_box.setText('Загрузить дамп?')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            response = msg_box.exec()
            if response == QMessageBox.StandardButton.Yes:
                folder = path.join(backup_dir, f'dumps/{text}.sql')
                command = [mysql_path, '-h', global_['host'], '-P', global_['port'], '-u',
                           self.config['user'], f'-p{self.config["pass"]}', global_['db']]
                with open(folder, 'r') as file:
                    run(command, stdin=file, stdout=PIPE, stderr=PIPE, text=True)
        except Exception as e:
            print(e, '|drawer load_dump')
