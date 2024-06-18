import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, QVBoxLayout, \
    QHBoxLayout, QFileDialog, QListWidget, QMessageBox, QDesktopWidget, QMainWindow, QAction, QMenu, QActionGroup, \
    QUndoStack, QToolButton, QDialog
from PyQt5.QtGui import QIcon, QFont, QCursor
from PyQt5.QtCore import Qt, QFileInfo, QRect
from PyQt5.undo_commands import AddFolderCommand, ClearSearchListCommand, RemoveSelFolderCommand
from PyQt5.options_dialog import OptionsDialog
from PyQt5.options_manager import *
from file_search.fileSearcher import FileSearcher
from duplicates_finder.duplicatesFinder import DuplicatesFinder
from duplicates_finder.comparisonMethod import ComparisonMethod


class ImgDuplicatesFinder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.undo_stack = QUndoStack(self)
        self.options_manager = OptionsManager()
        self._createActions()
        self._createToolbar()
        self._createMenuBar()
        self._createStatusBar()

        self.file_searcher = FileSearcher()
        self.method = ComparisonMethod()
        self.search_list = self.file_searcher.folders_for_search
        self.excluded_list = self.file_searcher.excluded_folders

        self.initUI()

    def _createActions(self):
        # File
        self.exitAction = QAction(QIcon("static/quit.png"), "&Quit", self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Quit application')
        self.exitAction.triggered.connect(self.close)
        # Edit
        self.undoAction = QAction(QIcon("static/undo.png"), "&Undo", self)
        self.undoAction.setShortcut('Ctrl+Z')
        self.undoAction.setStatusTip('Undo')
        self.undoAction.triggered.connect(self.undo_action)
        self.redoAction = QAction(QIcon("static/redo.png"), "&Redo", self)
        self.redoAction.setShortcut('Ctrl+Shift+Z')
        self.redoAction.setStatusTip('Redo')
        self.redoAction.triggered.connect(self.redo_action)
        self.addFolderAction = QAction(QIcon("static/add.png"), "&Add", self)
        self.addFolderAction.setShortcut('Ctrl+M')
        self.addFolderAction.setStatusTip('Add a new folder to search list')
        self.addFolderAction.triggered.connect(self.browse_folder)
        self.removeSelAction = QAction(QIcon("static/remove.png"), "&Remove", self)
        self.removeSelAction.setShortcut('Delete')
        self.removeSelAction.setStatusTip('Remove selected folder from search list')
        self.removeSelAction.triggered.connect(self.remove_sel_folder)
        self.clearFoldersAction = QAction("&Clear", self)
        self.clearFoldersAction.setStatusTip('Clear search list')
        self.clearFoldersAction.triggered.connect(self.clear_search_list)

        # *** Search options
        # Folders
        self.recursiveSearchAction = QAction(QIcon("static/recursive.png"), "&Recursive Search", self)
        self.recursiveSearchAction.setStatusTip("Search only in the specified folders")
        self.recursiveSearchAction.triggered.connect(lambda: self.options_manager.set_option("recursive_search", True))
        self.currentSearchAction = QAction(QIcon("static/current.png"), "In the &Current Folder", self)
        self.currentSearchAction.setStatusTip("Search in folders and their subfolders")
        self.currentSearchAction.triggered.connect(lambda: self.options_manager.set_option("recursive_search", False))
        self.recursiveSearchAction.setCheckable(True)
        self.currentSearchAction.setCheckable(True)
        folder_options_group = QActionGroup(self)
        folder_options_group.addAction(self.recursiveSearchAction)
        folder_options_group.addAction(self.currentSearchAction)
        folder_options_group.setExclusive(True)
        self.recursiveSearchAction.setChecked(True)
        # Search by
        self.byContentAction = QAction("&Content", self)
        self.byContentAction.setStatusTip("Search for similar images")
        self.byContentAction.triggered.connect(lambda: self.options_manager.set_option("search_by", "Content"))
        self.byNameAction = QAction("&Name", self)
        self.byNameAction.setStatusTip("Search for images with the same name")
        self.byNameAction.triggered.connect(lambda: self.options_manager.set_option("search_by", "Name"))
        self.bySizeAction = QAction("&Size", self)
        self.bySizeAction.setStatusTip("Search for images of the same size")
        self.bySizeAction.triggered.connect(lambda: self.options_manager.set_option("search_by", "Size"))
        self.byContentAction.setCheckable(True)
        self.byNameAction.setCheckable(True)
        self.bySizeAction.setCheckable(True)
        search_by_group = QActionGroup(self)
        search_by_group.addAction(self.byContentAction)
        search_by_group.addAction(self.byNameAction)
        search_by_group.addAction(self.bySizeAction)
        search_by_group.setExclusive(True)
        self.byContentAction.setChecked(True)
        # Algorithms
        self.aHashAction = QAction("a&Hash", self)
        self.aHashAction.setStatusTip("Use aHash comparison algorithm")
        self.aHashAction.triggered.connect(lambda: self.options_manager.set_option("algorithm", "aHash"))
        self.pHashAction = QAction("p&Hash", self)
        self.pHashAction.setStatusTip("Use pHash comparison algorithm")
        self.pHashAction.triggered.connect(lambda: self.options_manager.set_option("algorithm", "pHash"))
        self.orbAction = QAction("&ORB", self)
        self.orbAction.setStatusTip("Use ORB comparison algorithm")
        self.orbAction.triggered.connect(lambda: self.options_manager.set_option("algorithm", "ORB"))
        self.aHashAction.setCheckable(True)
        self.pHashAction.setCheckable(True)
        self.orbAction.setCheckable(True)
        self.algorithms_group = QActionGroup(self)
        self.algorithms_group.addAction(self.aHashAction)
        self.algorithms_group.addAction(self.pHashAction)
        self.algorithms_group.addAction(self.orbAction)
        self.algorithms_group.setExclusive(True)
        self.aHashAction.setChecked(True)
        # More
        self.openSettingsAction = QAction(QIcon("static/settings.png"), "&More...", self)
        self.openSettingsAction.setShortcut('Ctrl+Alt+S')
        self.openSettingsAction.setStatusTip("Open detailed settings")
        self.openSettingsAction.triggered.connect(self.open_options_dialog)

        # Help
        self.helpContentAction = QAction(QIcon("static/readme.png"), "&Help Content", self)
        self.helpContentAction.setStatusTip("Launch the Help manual")
        self.aboutAction = QAction(QIcon("static/about.png"), "&About", self)
        self.aboutAction.setStatusTip("Show the Img Duplicates Finder's About box")
        self.aboutAction.triggered.connect(self.about)

    def _createToolbar(self):
        toolbar = self.addToolBar('Tools')
        toolbar.setFloatable(False)
        # Edit
        toolbar.addAction(self.addFolderAction)
        toolbar.addAction(self.removeSelAction)
        toolbar.addSeparator()
        # Folders
        toolbar.addAction(self.recursiveSearchAction)
        toolbar.addAction(self.currentSearchAction)
        toolbar.addSeparator()
        # Search by
        search_by_menu = QMenu(self)
        search_by_menu.addActions([self.byContentAction, self.byNameAction, self.bySizeAction])
        search_by_tool = QToolButton(self)
        search_by_tool.setToolTip("Search by")
        search_by_tool.setIcon(QIcon("static/search_by.png"))
        search_by_tool.setPopupMode(QToolButton.InstantPopup)
        search_by_tool.setMenu(search_by_menu)
        toolbar.addWidget(search_by_tool)
        toolbar.addSeparator()
        # Algorithms
        algorithms_menu = QMenu(self)
        algorithms_menu.addActions([self.aHashAction, self.pHashAction, self.orbAction])
        algorithms_tool = QToolButton(self)
        algorithms_tool.setToolTip("Algorithm")
        algorithms_tool.setIcon(QIcon("static/algorithm.png"))
        algorithms_tool.setPopupMode(QToolButton.InstantPopup)
        algorithms_tool.setMenu(algorithms_menu)
        toolbar.addWidget(algorithms_tool)

    def _createMenuBar(self):
        menubar = self.menuBar()
        # File
        file_menu = menubar.addMenu("&File")
        open_recent_menu = file_menu.addMenu("&Open Recent")
        file_menu.addAction(self.exitAction)
        # Edit
        edit_menu = menubar.addMenu("&Edit")
        edit_menu.addAction(self.undoAction)
        edit_menu.addAction(self.redoAction)
        edit_menu.addAction(self.addFolderAction)
        edit_menu.addAction(self.removeSelAction)
        edit_menu.addAction(self.clearFoldersAction)
        # *** Options
        options_menu = menubar.addMenu("&Options")
        # Folders
        folders_menu = options_menu.addMenu("&Folders")
        folders_menu.addAction(self.recursiveSearchAction)
        folders_menu.addAction(self.currentSearchAction)
        # Search by
        search_by_menu = options_menu.addMenu("&Search by")
        search_by_menu.addActions([self.byContentAction, self.byNameAction, self.bySizeAction])
        # Algorithms
        algorithms_menu = options_menu.addMenu("&Algorithm")
        algorithms_menu.addActions([self.aHashAction, self.pHashAction, self.orbAction])
        # More
        more_menu = options_menu.addAction(self.openSettingsAction)
        # Help
        help_menu = menubar.addMenu("&Help")
        help_menu.addAction(self.helpContentAction)
        help_menu.addAction(self.aboutAction)

    def _createStatusBar(self):
        statusbar = self.statusBar()
        # постоянное сообщение
        constant_message = "Constant"
        constant_message_label = QLabel(f"{constant_message}")
        statusbar.addPermanentWidget(constant_message_label)

    def contextMenuEvent(self, event):
        context_menu = QMenu(self.central_widget)
        separator = QAction(self)
        separator.setSeparator(True)
        context_menu.addAction(self.recursiveSearchAction)
        context_menu.addAction(self.currentSearchAction)
        context_menu.addAction(separator)
        context_menu.addAction(self.aHashAction)
        context_menu.addAction(self.pHashAction)
        context_menu.addAction(self.orbAction)
        context_menu.exec(event.globalPos())

    def initUI(self):
        self.resize(800, 600)
        self.center()
        self.setWindowTitle("Image Duplicates Finder")
        self.setWindowIcon(QIcon("static/icon.ico"))
        self.setFont(QFont("OpenSans", 10))
        self.setAcceptDrops(True)

        # рабочая область
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # выбор папки
        folder_label = QLabel("Drag folders here to add them to your search list")
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_folder)
        self.dnd_space = QListWidget()
        self.dnd_space.setWordWrap(True)
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(self.remove_sel_folder)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_search_list)

        # макет блока для секции выбора папки
        folder_layout = QVBoxLayout()
        folder_layout.addWidget(folder_label, alignment=Qt.AlignCenter)
        folder_layout.addWidget(self.dnd_space)
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(browse_button)
        buttons_layout.addWidget(remove_button)
        buttons_layout.addWidget(clear_button)
        folder_layout.addLayout(buttons_layout)

        # кнопка начала поиска
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.start_search)

        # дисплей результатов поиска
        result_label = QLabel("Results:")
        self.result_listbox = QListWidget()

        # установка макетов
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.addLayout(folder_layout)
        main_layout.addWidget(search_button)
        main_layout.addWidget(result_label)
        main_layout.addWidget(self.result_listbox)

        self.show()

    # выбор папки для поиска
    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path and folder_path not in self.search_list:
            command = AddFolderCommand(folder_path, self.dnd_space, self.search_list)
            self.undo_stack.push(command)

    # обработчик кнопки поиска
    def start_search(self):
        if not self.search_list:
            QMessageBox.warning(self, "Empty Folder Path", "Please select a folder for search.")
            return

        self.file_searcher.file_formats = ['.png', '.jpg', '.jpeg']
        # img params
        images = self.file_searcher.search()
        # method params
        dupl_finder = DuplicatesFinder(self.method)
        dupl_finder.files = images[0]
        # finder params
        dupl_finder.find()

        # self.display_results(dups)

    # вывод результатов
    def display_results(self, duplicates):
        self.result_listbox.clear()
        if duplicates:
            for dup in duplicates:
                self.result_listbox.addItem(f"{dup[0]} and {dup[1]}")
        else:
            self.result_listbox.addItem("No duplicate images found.")

    # подтверждение выхода
    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, 'Confirm Quit', "Are you sure to quit?",
    #                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    # центрирование окна
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # о приложении
    def about(self):
        QMessageBox.about(self, "About Img Duplicates Finder", "<h3>About Img Duplicates Finder</h3>"
                                                               "<a href='https://github.com/soneXgo/img_duplicates_finder'>GitHub</a>")

    # drag'n'drop
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        dnd_rect = self.dnd_space.rect()
        mouse_pos = self.dnd_space.mapFromGlobal(QCursor.pos())
        if dnd_rect.contains(mouse_pos):
            paths = set([u.toLocalFile() for u in event.mimeData().urls()])
            for path in paths:
                if QFileInfo(path).isDir() and path not in self.search_list:
                    command = AddFolderCommand(path, self.dnd_space, self.search_list)
                    self.undo_stack.push(command)

    def clear_search_list(self):
        if self.search_list:
            command = ClearSearchListCommand(self.dnd_space, self.search_list)
            self.undo_stack.push(command)

    def undo_action(self):
        self.undo_stack.undo()

    def redo_action(self):
        self.undo_stack.redo()

    def remove_sel_folder(self):
        sel_item = self.dnd_space.currentItem()
        if sel_item:
            command = RemoveSelFolderCommand(sel_item.text(), self.dnd_space, self.search_list)
            self.undo_stack.push(command)

    def open_options_dialog(self):
        dialog = OptionsDialog(self.options_manager.options, self)
        if dialog.exec_() == QDialog.Accepted:
            self.options_manager.options = dialog.get_options()
            self.update_options()
            print(self.options_manager.options)

    def update_options(self):
        self.recursiveSearchAction.setChecked(self.options_manager.options["recursive_search"])
        self.currentSearchAction.setChecked(not self.options_manager.options["recursive_search"])

        search_by = self.options_manager.options.get("search_by")
        if search_by == "Content":
            self.byContentAction.setChecked(True)
        elif search_by == "Name":
            self.byNameAction.setChecked(True)
        elif search_by == "Size":
            self.bySizeAction.setChecked(True)

        algorithm = self.options_manager.options.get("algorithm")
        if algorithm == "aHash":
            self.aHashAction.setChecked(True)
        elif algorithm == "pHash":
            self.pHashAction.setChecked(True)
        elif algorithm == "ORB":
            self.orbAction.setChecked(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImgDuplicatesFinder()
    sys.exit(app.exec_())
