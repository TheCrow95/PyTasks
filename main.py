import platform

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QApplication, QWidget, QListWidget, QPushButton, QVBoxLayout, QHBoxLayout, QInputDialog, \
    QListWidgetItem, QSystemTrayIcon

import API.task

COLORS = {False: (235, 64, 52), True: (160, 237, 83)}


class TaskItem(QListWidgetItem):
    def __init__(self, name, done, list_widget):
        super().__init__(name)

        self.list_widget = list_widget
        self.done = done
        self.name = name

        self.setSizeHint(QSize(1, 50))
        self.list_widget.addItem(self)
        self.set_background_color()

    def toggle_state(self):
        self.done = not self.done
        API.task.set_tasks_status(name=self.name, done=self.done)
        self.set_background_color()

    def set_background_color(self):
        color = COLORS.get(self.done)
        self.setBackground(QColor(*color))
        stylesheet = f"""QListView::item:selected {{background: rgb{color};
                                                    color: rgb(0, 0, 0);}}"""
        self.list_widget.setStyleSheet(stylesheet)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Windows")
        self.setup_ui()
        self.get_tasks()
        self.center_under_tray()

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.create_tray_icon()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.lw_tasks = QListWidget()
        self.btn_add = QPushButton()
        self.btn_clean = QPushButton()
        self.btn_quit = QPushButton()

    def create_layouts(self):
        self.main_layout = QVBoxLayout(self)
        self.layout_buttons = QHBoxLayout()

    def create_tray_icon(self):
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon(r"icones/icon.png"))
        self.tray.setVisible(True)

    def modify_widgets(self):
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setStyleSheet("border: none;")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        self.btn_add.setIcon(QIcon(r"icones/add.svg"))
        self.btn_clean.setIcon(QIcon(r"icones/clean.svg"))
        self.btn_quit.setIcon(QIcon(r"icones/close.svg"))

        self.btn_add.setFixedSize(36, 36)
        self.btn_clean.setFixedSize(36, 36)
        self.btn_quit.setFixedSize(36, 36)

        self. lw_tasks.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lw_tasks.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.lw_tasks)
        self.main_layout.addLayout(self.layout_buttons)

        self.layout_buttons.addWidget(self.btn_add)
        self.layout_buttons.addStretch()
        self.layout_buttons.addWidget(self.btn_clean)
        self.layout_buttons.addWidget(self.btn_quit)

    def setup_connections(self):
        self.btn_add.clicked.connect(self.add_task)
        self.btn_clean.clicked.connect(self.clean_task)
        self.btn_quit.clicked.connect(self.close)
        self.lw_tasks.itemClicked.connect(lambda lw_item: lw_item.toggle_state())
        self.tray.activated.connect(self.tray_icon_click)

    def add_task(self):
        task_name, ok = QInputDialog.getText(self,
                                             "Ajouter une tâche",
                                             "Nom de la tâche: ")
        if ok and task_name:
            API.task.add_task(name=task_name)
            self.get_tasks()

    def clean_task(self):
        for i in range(self.lw_tasks.count()):
            lw_item = self.lw_tasks.item(i)
            if lw_item.done:
                API.task.remove_task(name=lw_item.name)
        self.get_tasks()
        self.lw_tasks.repaint()  # corrige le défaut de suppression que lorsqu'on change la taille de la fenêtre

    def get_tasks(self):
        self.lw_tasks.clear()
        tasks = API.task.get_tasks()
        for task_name, done in tasks.items():
            TaskItem(name=task_name, done=done, list_widget=self.lw_tasks)

    def tray_icon_click(self):
        if self.isHidden():
            self.showNormal()
        else:
            self.hide()

    def center_under_tray(self):
        tray_x = self.tray.geometry().x()
        tray_y = self.tray.geometry().y()
        w, h = self.sizeHint().toTuple()
        if platform.system() == "Windows":
            self.move(tray_x - (w / 2), tray_y - h)
        else:
            self.move(tray_x - (w / 2), 25)


if __name__ == '__main__':
    app = QApplication()
    main_window = MainWindow()
    #main_window.resize(800, 600)
    main_window.show()
    app.exec()
