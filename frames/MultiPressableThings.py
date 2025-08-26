from PyQt6.QtWidgets import QWidget, QFrame, QLabel
from PyQt6.QtCore import Qt


class MultiPressableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.styles = {
            'default': {
                'base': 'padding: 5px; border-radius: 3px;',
                'default': '',
                'hover': 'background-color: rgb(190, 190, 190);',
                'pressed': 'background-color: rgb(160, 160, 160);'},
            'green': {
                'base': 'border-radius: 3px; font-size: 20px; font-family: "Segoe UI Symbol";',
                'default': 'background-color: rgb(113, 174, 38);',
                'hover': 'background-color: rgb(89, 138, 30);',
                'pressed': 'background-color: rgb(74, 115, 25);'},
            'flat': {
                'base': 'padding-left: 3px; border-radius: 2px;',
                'default': 'background-color: rgb(250, 250, 250)',
                'hover': 'background-color: rgb(190, 190, 190);',
                'pressed': 'background-color: rgb(160, 160, 160);'}
        }
        self.current_style = self.styles['default']
        self.reset_style()
        self.actions = []

    def add_action(self, handler):
        self.actions.append(handler)

    def set_style(self, style_name):
        if style_name in self.styles:
            self.current_style = self.styles[style_name]
            self.reset_style()

    def reset_style(self):
        self.setStyleSheet(f'{self.__class__.__name__} {{{self.current_style["base"] + self.current_style["default"]}}}'
                           f'{self.__class__.__name__}:hover {{{self.current_style["hover"]}}}')

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setStyleSheet(f'{self.__class__.__name__} {{{self.current_style["base"] + self.current_style["pressed"]}}}')

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.reset_style()
        try:
            for handler in self.actions:
                handler()
        except Exception as e:
            print(e, '| multi')


class MultiPressableFrame(QFrame, MultiPressableWidget):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        MultiPressableWidget.__init__(self, parent)


class MultiPressableLabel(QLabel, MultiPressableWidget):
    def __init__(self, parent=None, style_name='default'):
        QLabel.__init__(self, parent)
        MultiPressableWidget.__init__(self, parent)
        self.set_style(style_name)

    def get_text(self):
        return self.text()
