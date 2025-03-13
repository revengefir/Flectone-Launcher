import minecraft_launcher_lib
from random_username.generate import generate_username
from uuid import uuid1
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets

minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace("minecraft", "flectone")

class LaunchThread(QtCore.QThread):
    launch_setup_signal = QtCore.pyqtSignal(str, str)
    progress_update_signal = QtCore.pyqtSignal(int, int, str)
    state_update_signal = QtCore.pyqtSignal(bool)

    version_id = ""
    username = ''

    progress = 0
    progress_max = 0
    progress_label = ''

    def __init__(self):
        super().__init__()

        self.launch_setup_signal.connect(self.launch_setup)


    def launch_setup(self, version_id, username):
        self.version_id = version_id
        self.username = username

    def update_progress_label(self, value):
        self.progress_label = value
        self.progress_update_signal.emit(self.progress,self.progress_max,self.progress_label)
    def update_progress(self, value):
        self.progress = value
        self.progress_update_signal.emit(self.progress,self.progress_max,self.progress_label)
    def update_progress_max(self, value):
        self.progress_max = value
        self.progress_update_signal.emit(self.progress,self.progress_max,self.progress_label)

   
    def run(self):
        self.state_update_signal.emit(True)

        minecraft_launcher_lib.install.install_minecraft_version(versionid=self.version_id, minecraft_directory=minecraft_directory, callback={"setStatus": self.update_progress_label, "setProgress": self.update_progress, 'setMax': self.update_progress_max})
        
        if self.username == "":
            self.username = generate_username()[0]

        options = {
            'username': self.username,
            'uuid':str(uuid1()),
            'token': ''
        }
        subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version=self.version_id, minecraft_directory=minecraft_directory,options=options))

        self.state_update_signal.emit(False)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Flectone Launcher A.0.4.1")
        MainWindow.resize(755, 716)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.Icon = QtWidgets.QLabel(self.centralwidget)
        self.Icon.setText("")
        self.Icon.setPixmap(QtGui.QPixmap("assets/logo.jpg"))
        self.Icon.setObjectName("Icon")
        self.verticalLayout.addWidget(self.Icon)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.username = QtWidgets.QLineEdit(self.centralwidget)
        self.username.setObjectName("username")
        self.verticalLayout.addWidget(self.username)
        self.version_select = QtWidgets.QComboBox(self.centralwidget)
        self.version_select.setObjectName("version_select")

        for version in minecraft_launcher_lib.utils.get_version_list():
            self.version_select.addItem(version["id"])

        self.verticalLayout.addWidget(self.version_select)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.progress = QtWidgets.QProgressBar(self.centralwidget)
        self.progress.setProperty("value", 24)
        self.progress.setTextVisible(False)
        self.progress.setObjectName("progress")
        self.progress.setVisible(False)
        self.verticalLayout.addWidget(self.progress)
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setObjectName("start_button")
        self.start_button.clicked.connect(self.launch_game)
        self.verticalLayout.addWidget(self.start_button)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.launch_thread = LaunchThread()
        self.launch_thread.state_update_signal.connect(self.state_update)
        #self.launch_thread.progress_update_signal(self.update_progress)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def state_update(self, value):
        self.start_button.setDisabled(value)
        #self.update_progress.setTextVisible(not value)
    def update_progress(self, progress, max_progress, label):
        self.update_progress.setValue(progress)
        self.update_progress.setMaximum(max_progress)
    def launch_game(self):
        self.launch_thread.launch_setup_signal.emit(self.version_select.currentText(), self.username.text())
        self.launch_thread.start()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.username.setPlaceholderText(_translate("MainWindow", "Username"))
        self.start_button.setText(_translate("MainWindow", "Play"))


if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)

    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
