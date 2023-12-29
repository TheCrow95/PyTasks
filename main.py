from PySide6.QtWidgets import QApplication, QWidget, QListWidget, QPushButton, QVBoxLayout, QHBoxLayout


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Windows")
        self.setup_ui()

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
        pass


if __name__ == '__main__':
    app = QApplication()
    main_window = MainWindow()
    main_window.resize(800, 600)
    main_window.show()
    app.exec()
