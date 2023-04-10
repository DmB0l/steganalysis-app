from PyQt5 import QtCore, QtGui, QtWidgets
import os
from tensorflow import keras
import numpy as np
from keras.utils import plot_model
import pickle
from PIL import Image


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.scanComplited = False
        self.log = ""

        self.model = keras.models.load_model('D:/ProgectsPyton/neuronNet/model3_03_new/model05.h5')

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: white;")

        font = QtGui.QFont()
        font.setPointSize(10)
        self.text = QtWidgets.QLabel(self.centralwidget)
        self.text.setAlignment(QtCore.Qt.AlignLeft)
        self.text.setStyleSheet("padding: 5px")
        self.text.setFont(font)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 100, 800, 500))
        self.scrollArea.setFont(font)
        self.scrollArea.setStyleSheet("background-color: rgb(238, 238, 238);")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 779, 489))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.text)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 75, 200, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.progress = QtWidgets.QProgressBar(self.centralwidget)
        self.progress.setGeometry(QtCore.QRect(200, 75, 400, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.progress.setFont(font)
        self.progress.setObjectName("progress")
        self.progress.setVisible(False)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("border-radius: 10px;\n"
                                      "border: 2px solid rgba(0, 0, 0, 0.8);\n"
                                      "background-color: rgb(238, 238, 238);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.getFileNames)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(418, 10, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("border-radius: 10px;\n"
                                        "border: 2px solid rgba(0, 0, 0, 0.8);\n"
                                        "background-color: rgb(238, 238, 238);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.changeLabel)
        self.pushButton_2.clicked.connect(self.scan)

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(621, 10, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("border-radius: 10px;\n"
                                        "border: 2px solid rgba(0, 0, 0, 0.8);\n"
                                        "background-color: rgb(238, 238, 238);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.saveLog)

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(214, 10, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("border-radius: 10px;\n"
                                        "border: 2px solid rgba(0, 0, 0, 0.8);\n"
                                        "background-color: rgb(238, 238, 238);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.clearChoose)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Сryptanalysis scanner"))
        self.label.setText(_translate("MainWindow", "Выберите файл"))
        self.pushButton.setText(_translate("MainWindow", "Выбрать файл"))
        self.pushButton_2.setText(_translate("MainWindow", "Сканировать"))
        self.pushButton_3.setText(_translate("MainWindow", "Сохранить логи"))
        self.pushButton_4.setText(_translate("MainWindow", "Очистить выбор"))

    def getFileNames(self):
        filenames, ok = QtWidgets.QFileDialog.getOpenFileNames(
            self.centralwidget,
            "Выбрать файл",
            "D:/Datasets/dataset_0.3/test/encode",
            "Images (*.png *.jpg)"
        )
        if filenames:
            self.progress.setVisible(False)
            _translate = QtCore.QCoreApplication.translate
            if len(filenames) > 1:
                self.label.setText(_translate("MainWindow", "Просканируйте файлы"))
            elif len(filenames) == 1:
                self.label.setText(_translate("MainWindow", "Просканируйте файл"))
            else:
                self.label.setText(_translate("MainWindow", "Сначала необходимо выбрать файл"))

            if self.scanComplited:
                str = ""
            else:
                str = self.text.text()

            for filename in filenames:
                str = str + filename + '\n'

            self.nameFiles = filename
            self.scanComplited = False
            self.text.setText(str)

    def saveLog(self):
        filename, ok = QtWidgets.QFileDialog.getSaveFileName(self.centralwidget,
                                                             "Сохранить файл",
                                                             ".",
                                                             "Text files (*.txt);")
        if filename:
            with open(filename, 'w') as f:
                f.write(self.log)

    def changeLabel(self):
        if self.nameFiles:
            _translate = QtCore.QCoreApplication.translate
            self.label.setText(_translate("MainWindow", "Идет сканирование..."))

    def clearChoose(self):
        self.label.setText("Выберите файл")
        self.text.setText("")
        self.progress.setVisible(False)
        self.scanComplited = False

    def scan(self):
        str = self.text.text()
        paths = []
        s = ""
        for c in str:
            if c == '\n':
                paths.append(s)
                s = ""
            else:
                s = s + c

        new_str = ""

        self.progress.setVisible(True)
        self.progress.setMaximum(len(paths))
        counter = 0
        for path in paths:
            image = keras.utils.load_img(path)
            input_arr = keras.utils.img_to_array(image)
            input_arr = np.array([input_arr])  # Convert single image to a batch.
            predictions = self.model.predict(input_arr)
            res = np.argmax(predictions)
            if res == 1:
                new_str = new_str + path + \
                          "<span style=\" font-size:8pt; font-weight:600; color:red;\" > Скрытая информация " \
                          "обнаружена </span><br>"
                self.log = self.log + path + " Скрытая информация обнаружена \n"
            else:
                new_str = new_str + path + \
                          "<span style=\" font-size:8pt; font-weight:600; color:green;\" > Скрытая информация НЕ " \
                          "обнаружена </span><br> "
                self.log = self.log + path + " Скрытая информация НЕ обнаружена \n"
            counter += 1
            self.progress.setValue(counter)

        self.text.setText(new_str)
        self.scanComplited = True
        _translate = QtCore.QCoreApplication.translate
        if len(paths) > 1:
            self.label.setText(_translate("MainWindow", "Файлы отсканированы"))
        elif len(paths) == 1:
            self.label.setText(_translate("MainWindow", "Файл отсканирован"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
