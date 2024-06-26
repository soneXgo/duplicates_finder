from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QListWidget, QWidget, \
    QListWidgetItem, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from datetime import datetime
import os
from send2trash import send2trash


class DuplicateDetailsDialog(QDialog):
    def __init__(self, file_path, duplicates, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.creation_date = datetime.fromtimestamp(os.path.getctime(self.file_path)).strftime('%d/%m/%y %H:%M:%S')
        self.duplicates = duplicates
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"{os.path.basename(self.file_path)}")
        self.resize(800, 560)
        self.setFont(QFont("OpenSans", 10))
        layout = QVBoxLayout(self)

        # текущий файл
        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        main_image_label = QLabel(self)
        main_image_label.setFixedSize(200, 200)
        pixmap = QPixmap(self.file_path)
        main_image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        left_layout.addWidget(main_image_label)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignVCenter)
        file_name = os.path.basename(self.file_path)
        name_label = QLabel(f"<b>Name:</b> {file_name}")
        name_label.setWordWrap(True)
        path_label = QLabel(f"<b>Path:</b> {self.file_path}")
        path_label.setWordWrap(True)
        creation_date_label = QLabel(f"<b>Creation Date:</b> {self.creation_date}")
        creation_date_label.setWordWrap(True)
        right_layout.addWidget(name_label)
        right_layout.addWidget(path_label)
        right_layout.addWidget(creation_date_label)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout, 1)
        layout.addLayout(main_layout)

        # список дубликатов
        duplicates_label = QLabel("Duplicates:")
        layout.addWidget(duplicates_label)

        self.duplicates_list = QListWidget()
        for duplicate_path in self.duplicates:
            item = QListWidgetItem()
            widget = QWidget()
            widget_layout = QHBoxLayout(widget)

            # изображения дубликатов
            duplicate_image_label = QLabel()
            duplicate_image_label.setFixedSize(80, 80)
            pixmap = QPixmap(duplicate_path)
            duplicate_image_label.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio))
            widget_layout.addWidget(duplicate_image_label)

            # путь к дубликатам
            duplicate_path_label = QLabel(duplicate_path)
            duplicate_path_label.setWordWrap(True)
            widget_layout.addWidget(duplicate_path_label, 1)

            # кнопка перемещения
            move_button = QPushButton("Move")
            move_button.clicked.connect(lambda _, p=duplicate_path: self.move_file(p))
            widget_layout.addWidget(move_button)

            # кнопка удаления
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, p=duplicate_path: self.delete_file(p))
            widget_layout.addWidget(delete_button)

            item.setSizeHint(widget.sizeHint())
            self.duplicates_list.addItem(item)
            self.duplicates_list.setItemWidget(item, widget)

        layout.addWidget(self.duplicates_list)

    def move_file(self, file_path):
        pass

    def delete_file(self, file_path):
        if os.path.isfile(file_path):
            path_to_delete = file_path.replace("/", "\\")
            send2trash(path_to_delete)
        else:
            QMessageBox.warning(self, "Error occurred",
                                "<h3>File doesn\'t exist</h3>"
                                "The file may have already been deleted.<br/><br/>")  
