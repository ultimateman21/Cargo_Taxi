from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtWidgets import QApplication
from interfaces.c_face import *
from interfaces.w_face import *
from interfaces.a_face import *
from config import reg, global_
from hashlib import sha256
from sys import argv, exit


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Вход')
        self.setFixedSize(200, 170)

        self.layout = QVBoxLayout()

        login_l = QLabel('Номер телефона:')
        self.layout.addWidget(login_l)

        self.login_edit = QLineEdit()
        login_regex = QRegularExpression(r'^\+?\d{0,2}\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{2}[\s.-]?\d{2}$')
        self.login_edit.returnPressed.connect(self.handle_enter_key)
        validator = QRegularExpressionValidator(login_regex)
        self.login_edit.setValidator(validator)
        self.layout.addWidget(self.login_edit)

        password_l = QLabel('Пароль:')
        self.layout.addWidget(password_l)

        self.password_edit = QLineEdit()
        self.password_edit.returnPressed.connect(self.handle_enter_key)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_edit)

        self.message = QLabel('Неверные данные или\nотсутствует регистрация')
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.message)
        self.message.hide()

        self.login_b = QPushButton('Войти')
        self.login_b.clicked.connect(self.login)
        self.layout.addWidget(self.login_b)

        reg_b = QPushButton('Зарегистрироваться')
        reg_b.clicked.connect(self.open_reg)
        self.layout.addWidget(reg_b)

        self.setLayout(self.layout)

        self.registration_window = None
        self.client_window = None
        self.worker_window = None
        self.employee_window = None

    def login(self):
        try:
            phone = self.login_edit.text()
            password = sha256(self.password_edit.text().encode('cp1251')).hexdigest()

            if phone and self.password_edit.text():
                with connect(
                    user=reg['user'],
                    password=reg['pass'],
                    host=global_['host'],
                    port=global_['port'],
                    database=global_['db'],
                ) as connection:
                    cursor = connection.cursor()
                    role = cursor.callproc('check_reg', (phone, password, None, None))[-2:]
                    connection.commit()

                    if role[0] is not None:
                        if role[0] == 'client':
                            self.client_window = ClientInterface(self, role[1])
                            self.client_window.show()
                            self.close()
                        elif role[0] == 'worker':
                            self.worker_window = WorkerInterface(self, role[1])
                            self.worker_window.show()
                            self.close()
                        elif role[0] == 'employee':
                            self.employee_window = AdminInterface(self, role[1])
                            self.employee_window.show()
                            self.close()
                        self.message.hide()
                        self.setFixedSize(200, 170)
                    else:
                        self.message.show()
                        self.setFixedSize(200, 210)

        except Exception as e:
            print(e, '|reg')

    def handle_enter_key(self):
        sender = self.sender()
        if sender == self.login_edit:
            self.password_edit.setFocus()
        elif sender == self.password_edit:
            self.login_b.click()

    def open_reg(self):
        self.registration_window = Registration(self)
        self.registration_window.show()
        self.close()


class Registration(QWidget):
    def __init__(self, login):
        super().__init__()
        self.setWindowTitle('Регистрация')
        self.setFixedSize(300, 200)

        self.login = login
        layout = QVBoxLayout()

        name_l = QLabel('ФИО:')
        layout.addWidget(name_l)

        self.name_edit = QLineEdit()
        self.name_edit.returnPressed.connect(self.handle_enter_key)
        layout.addWidget(self.name_edit)

        phone_l = QLabel('Номер телефона:')
        layout.addWidget(phone_l)

        self.phone_edit = QLineEdit()
        phone_regex = QRegularExpression(r'^\+?\d{0,2}\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{2}[\s.-]?\d{2}$')
        self.phone_edit.returnPressed.connect(self.handle_enter_key)
        validator = QRegularExpressionValidator(phone_regex)
        self.phone_edit.setValidator(validator)
        layout.addWidget(self.phone_edit)

        password_l = QLabel('Пароль:')
        layout.addWidget(password_l)

        self.password_edit = QLineEdit()
        self.password_edit.returnPressed.connect(self.handle_enter_key)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_edit)

        self.register_b = QPushButton('Зарегистрироваться')
        self.register_b.clicked.connect(self.register)
        layout.addWidget(self.register_b)

        self.setLayout(layout)

    def register(self):
        try:
            name_1, name_2, name_3 = [item for item in self.name_edit.text().split(' ') if item.strip()]
            phone = self.phone_edit.text()
            password = self.password_edit.text().encode('cp1251')
            password = sha256(password).hexdigest()

            if phone and self.password_edit.text():
                with connect(
                    user=reg['user'],
                    password=reg['pass'],
                    host=global_['host'],
                    port=global_['port'],
                    database=global_['db'],
                ) as connection:
                    cursor = connection.cursor()
                    check = cursor.callproc('register', (name_1, name_2, name_3, phone, password, 1))[-1]
                    connection.commit()

                if check:
                    QMessageBox.information(self, '', 'Регистрация прошла успешно')
                else:
                    QMessageBox.information(self, '', 'Такой пользователь уже существует')

                self.login.show()
                self.login.login_edit.clear()
                self.login.password_edit.clear()
                self.login.login_edit.setFocus()
                self.close()

        except Exception as e:
            print(e, '|registration')

    def handle_enter_key(self):
        sender = self.sender()
        if sender == self.name_edit:
            self.phone_edit.setFocus()
        elif sender == self.phone_edit:
            self.password_edit.setFocus()
        elif sender == self.password_edit:
            self.register_b.click()


if __name__ == '__main__':
    app = QApplication(argv)
    widget = Login()
    widget.show()
    exit(app.exec())
