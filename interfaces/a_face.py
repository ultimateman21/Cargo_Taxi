from PyQt6.QtWidgets import QToolBar, QTableView, QMenu, QDialog, QFormLayout, QDialogButtonBox
from PyQt6.QtGui import QAction, QUndoCommand, QUndoStack
from PyQt6.QtCore import Qt, QEasingCurve, QRect, QPoint
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from frames.Drawer import *
from config import a_c
import datetime


class AddRowCommand(QUndoCommand):
    def __init__(self, model, data, parent=None):
        super().__init__(parent)
        self.model = model
        self.data = data
        self.row = model.rowCount()

    def redo(self):
        try:
            self.model.insertRow(self.row)
            for column, value in enumerate(self.data):
                if isinstance(value, str) and 'date' in self.model.headerData(column, Qt.Orientation.Horizontal):
                    try:
                        date_obj = datetime.datetime.strptime(value, '%d.%m.%Y %H:%M')
                        value = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                    except ValueError as ve:
                        raise ValueError(f"Некорректный формат даты: {value}")

                if not self.model.setData(self.model.index(self.row, column), value):
                    raise ValueError(f"Ошибка установки данных в колонку {column}: {value}")

            if not self.model.submitAll():
                raise ValueError(f"Ошибка сохранения данных в базу: {self.model.lastError().text()}")
        except Exception as e:
            print(e, '| Ошибка в AddRowCommand redo')

    def undo(self):
        try:
            self.model.removeRow(self.row)
            if not self.model.submitAll():
                raise ValueError(f"Ошибка отката изменений: {self.model.lastError().text()}")
        except Exception as e:
            print(e, '| Ошибка в AddRowCommand undo')


class RemoveRowCommand(QUndoCommand):
    def __init__(self, model, row, parent=None):
        super().__init__(parent)
        self.model = model
        self.row = row
        self.data = [model.data(model.index(row, column)) for column in range(model.columnCount())]

    def redo(self):
        try:
            self.model.removeRow(self.row)
            self.model.submitAll()
            self.model.select()
        except Exception as e:
            print(e, '|a_face RemoveRowCommand redo')

    def undo(self):
        try:
            self.model.insertRow(self.row)
            for column, value in enumerate(self.data):
                self.model.setData(self.model.index(self.row, column), value)
            self.model.submitAll()
            self.model.select()
        except Exception as e:
            print(e, '|a_face RemoveRowCommand undo')


class AddRowDialog(QDialog):
    def __init__(self, headers, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить строку')
        self.layout = QFormLayout(self)

        self.inputs = {}
        for header in headers:
            line_edit = QLineEdit(self)
            self.layout.addRow(header, line_edit)
            self.inputs[header] = line_edit

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def get_data(self):
        return [line_edit.text() for line_edit in self.inputs.values()]


class AdminInterface(QWidget):
    def __init__(self, login, id_):
        super().__init__()
        self.setWindowTitle('Admin')
        self.setFixedSize(1070, 600)

        self.id_em = id_
        self.login = login
        self.undo_stack = QUndoStack(self)

        layout = QVBoxLayout()

        name_box = QGroupBox()

        name_layout = QHBoxLayout()
        name_layout.setContentsMargins(3, 1, 1, 1)
        name_layout.setSpacing(0)

        toolbar = {'Пользователи': ['Клиенты', 'Водители'],
                   'Заказы': ['Выбранные', 'Не выбранные'],
                   'Транспорт': ['Выбранный', 'Не выбранный'],
                   'Сообщения': []}
        self.toolbars = []
        for i in toolbar:
            button = QPushButton(i)
            button.clicked.connect(self.change_toolbar)
            button.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            button.customContextMenuRequested.connect(self.change_tables_content)
            name_layout.addWidget(button)

            bar = QToolBar(i, self)
            bar.addSeparator()

            for j in toolbar[i]:
                action = QAction(j, bar)
                action.triggered.connect(self.change_tables_content)
                bar.addAction(action)
                bar.addSeparator()

            bar.hide()
            name_layout.addWidget(bar)
            self.toolbars.append(bar)

        name_layout.addStretch(1)

        self.username_label = MultiPressableLabel()
        self.username_label.add_action(lambda: self.open_drawer())
        self.mousePressEvent = self.close_drawer
        self.get_name()
        name_layout.addWidget(self.username_label)

        name_box.setLayout(name_layout)

        layout.addWidget(name_box)

        if self.create_connection() is None:
            bottom_layout = QVBoxLayout()

            up_box = QGroupBox('Данные')
            up_box.setFixedHeight(330)
            up_layout = QVBoxLayout()
            up_layout.setSpacing(4)
            up_layout.setContentsMargins(8, 5, 8, 8)

            self.search = QLineEdit()
            self.search.setPlaceholderText('Введите текст для поиска или используйте конструкцию {имя столбца} = {искомое значение}')
            self.search.textChanged.connect(self.search_into)
            up_layout.addWidget(self.search)

            self.table_u = QTableView()
            self.filter = ''
            self.model1 = QSqlTableModel()
            self.model1.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
            self.table_u.setModel(self.model1)
            self.table_u.setSortingEnabled(True)
            self.table_u.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.table_u.customContextMenuRequested.connect(self.context_menu)
            up_layout.addWidget(self.table_u)

            up_box.setLayout(up_layout)
            bottom_layout.addWidget(up_box)

            down_box = QGroupBox('Ссылка')
            down_box.setFixedHeight(203)
            down_layout = QHBoxLayout()
            down_layout.setContentsMargins(8, 5, 8, 8)

            self.table_d = QTableView()
            self.model2 = QSqlTableModel()
            self.model2.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
            self.table_d.setModel(self.model2)
            down_layout.addWidget(self.table_d)

            down_box.setLayout(down_layout)
            bottom_layout.addWidget(down_box)

            layout.addLayout(bottom_layout)

        self.drawer = Drawer(self.id_em, 'employee', a_c, self)
        self.drawer.quit_b.clicked.connect(self.quit)

        self.setLayout(layout)
        self.anim = QPropertyAnimation(self.drawer, b"geometry")
        self.duration = 0
        self.animate_drawer(self.width())

    @staticmethod
    def create_connection():
        db = QSqlDatabase.addDatabase('QMYSQL')
        db.setUserName(a_c['user'])
        db.setPassword(a_c['pass'])
        db.setHostName(global_['host'])
        db.setPort(int(global_['port']))
        db.setDatabaseName(global_['db'])
        if not db.open():
            print('Не удалось подключиться к базе данных')
            print(db.lastError().text())
            return db.lastError().text()
        return None

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
        self.anim.setEndValue(QRect(end_x, 33, self.drawer.width(), self.height() - 20))
        self.anim.start()
        self.duration = 300

    def get_name(self):
        with connect(
            user=a_c['user'],
            password=a_c['pass'],
            host=global_['host'],
            port=global_['port'],
            database=global_['db'],
        ) as connection:
            cursor = connection.cursor()
            name = cursor.callproc('get_name', ('employee', self.id_em, None))[-1]
            connection.commit()
        self.username_label.setText(name)

    def change_toolbar(self):
        try:
            for i in self.toolbars:
                if self.sender().text() == i.windowTitle():
                    if i.isVisible():
                        i.hide()
                    else:
                        for bar in self.toolbars:
                            bar.hide()
                        if self.sender().text() == 'Сообщения':
                            self.change_tables_content()
                        else:
                            i.show()
        except Exception as e:
            print(e, '|a_face change_toolbar')

    def change_tables_content(self, col=None, index=None):
        if self.sender().text() != 'Выбрать':
            context = {'Пользователи': ['human', ''],
                       'Клиенты': ['client', ''],
                       'Водители': ['worker', ''],
                       'Заказы': ['order', ''],
                       'Выбранные': ['order', 'state = "1"'],
                       'Не выбранные': ['order', 'state = "0"'],
                       'Транспорт': ['vehicle', ''],
                       'Выбранный': ['vehicle', 'state = "1"'],
                       'Не выбранный': ['vehicle', 'state = "0"'],
                       'Сообщения': ['message', ''],
                       }
            self.model1.setTable(context[self.sender().text()][0])
            self.filter = context[self.sender().text()][1]
            self.model1.setFilter(self.filter)

            self.model1.select()
            self.table_u.resizeColumnsToContents()
        else:
            context = {'human_id': 'human',
                       'client_id': 'client',
                       'worker_id': 'worker',
                       'order_id': 'order',
                       'vehicle_id': 'vehicle',
                       }
            self.model2.setTable(context[col])
            self.model2.setFilter(f'id ={str(self.table_u.model().data(index, Qt.ItemDataRole.DisplayRole))}')
            self.model2.select()
            self.table_d.resizeColumnsToContents()

    def context_menu(self, position: QPoint):
        try:
            context = {'client': {'human_id'},
                       'worker': {'human_id'},
                       'order': {'client_id', 'vehicle_id'},
                       'vehicle': {'worker_id'},
                       'message': {'order_id'}}
            menu = QMenu()

            indexes = self.table_u.selectedIndexes()
            if indexes and self.model1.tableName() in context:
                column_index = indexes[0].column()
                column_name = self.model1.headerData(column_index, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
                if column_name in context[self.model1.tableName()]:
                    select_action = menu.addAction('Выбрать')
                    select_action.triggered.connect(lambda: self.change_tables_content(column_name, indexes[0]))
            add_action = menu.addAction('Добавить строку')
            add_action.triggered.connect(lambda: self.add_row(self.model1))
            delete_action = menu.addAction('Удалить строку')
            delete_action.triggered.connect(lambda: self.delete_row(self.model1, self.table_u))

            menu.addSeparator()

            undo_action = menu.addAction('Отменить')
            undo_action.setEnabled(self.undo_stack.canUndo())
            undo_action.triggered.connect(self.undo_stack.undo)

            redo_action = menu.addAction('Вернуть')
            redo_action.setEnabled(self.undo_stack.canRedo())
            redo_action.triggered.connect(self.undo_stack.redo)

            menu.exec(self.table_u.viewport().mapToGlobal(position))
        except Exception as e:
            print(e, '|a_face context_menu')

    def add_row(self, model):
        try:
            headers = [model.headerData(i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) for i in range(model.columnCount())]
            dialog = AddRowDialog(headers, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                self.undo_stack.push(AddRowCommand(model, data))
        except Exception as e:
            print(e, '|a_face add_row')

    def delete_row(self, model, table_view):
        try:
            indexes = table_view.selectedIndexes()
            if indexes:
                row = indexes[0].row()
                self.undo_stack.push(RemoveRowCommand(model, row))
        except Exception as e:
            print(e, '|a_face delete_row')

    def search_into(self, text):
        try:
            words = text.strip().split(' ')
            col_names = [self.model1.headerData(i, Qt.Orientation.Horizontal) for i in range(self.model1.columnCount())]

            if len(text) > 1:
                if len(words) == 3 and words[0] in col_names and words[1] == '=':
                    if self.filter:
                        self.model1.setFilter(self.filter + ' AND ' + f'`{words[0]}` LIKE "{words[2]}"')
                    else:
                        self.model1.setFilter(f'`{words[0]}` LIKE "{words[2]}"')
                elif len(words) > 1:
                    self.model1.setFilter(self.filter)
                else:
                    if self.filter:
                        self.model1.setFilter(self.filter + ' AND ' + '(' + ' OR '.join([f'`{i}` LIKE "{text}"' for i in col_names]) + ')')
                    else:
                        self.model1.setFilter('(' + ' OR '.join([f'`{i}` LIKE "{text}"' for i in col_names]) + ')')
            else:
                self.model1.setFilter(self.filter)
        except Exception as e:
            print(e, '|a_face search_info')

    def quit(self):
        self.login.show()
        self.login.login_edit.clear()
        self.login.password_edit.clear()
        self.login.login_edit.setFocus()
        self.close()
