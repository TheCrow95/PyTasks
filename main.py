from PySide6.QtCore import QSize
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QWidget, QListWidget, QPushButton, QVBoxLayout, QHBoxLayout, QInputDialog, \
    QListWidgetItem

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

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.lw_tasks = QListWidget()
        self.btn_add = QPushButton("Add")
        self.btn_clean = QPushButton("Clean")
        self.btn_quit = QPushButton("Quit")

    def create_layouts(self):
        self.main_layout = QVBoxLayout(self)
        self.layout_buttons = QHBoxLayout()

    def modify_widgets(self):
        pass

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.lw_tasks)
        self.main_layout.addLayout(self.layout_buttons)

        self.layout_buttons.addWidget(self.btn_add)
        self.layout_buttons.addStretch()
        self.layout_buttons.addWidget(self.btn_clean)
        self.layout_buttons.addWidget(self.btn_quit)

    def setup_connections(self):
        self.btn_add.clicked.connect(self.add_task)
        self.lw_tasks.itemClicked.connect(lambda lw_item: lw_item.toggle_state())

    def add_task(self):
        task_name, ok = QInputDialog.getText(self,
                                             "Ajouter une tâche",
                                             "Nom de la tâche: ")
        if ok and task_name:
            API.task.add_task(name=task_name)
            self.get_tasks()

    def get_tasks(self):
        self.lw_tasks.clear()
        tasks = API.task.get_tasks()
        for task_name, done in tasks.items():
            TaskItem(name=task_name, done=done, list_widget=self.lw_tasks)


if __name__ == '__main__':
    app = QApplication()
    main_window = MainWindow()
    main_window.resize(800, 600)
    main_window.show()
    app.exec()
