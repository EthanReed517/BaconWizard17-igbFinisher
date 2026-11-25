# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_Main.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTabWidget, QToolButton,
    QVBoxLayout, QWidget)
import ui_resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(876, 490)
        icon = QIcon()
        icon.addFile(u":/icons/logo.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_3 = QFrame(self.tab)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMaximumSize(QSize(16777215, 36))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_3.setLineWidth(1)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 3, -1, 0)
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 0))
        self.label_3.setMaximumSize(QSize(16, 16))
        self.label_3.setToolTipDuration(-1)
        self.label_3.setPixmap(QPixmap(u":/ui/info_icon.png"))
        self.label_3.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)


        self.verticalLayout_2.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.tab)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_7 = QFrame(self.frame_4)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 4, -1, 4)
        self.label_4 = QLabel(self.frame_7)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.radioButton = QRadioButton(self.frame_7)
        self.radioButton.setObjectName(u"radioButton")

        self.horizontalLayout_3.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(self.frame_7)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.horizontalLayout_3.addWidget(self.radioButton_2)

        self.lineEdit = QLineEdit(self.frame_7)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.lineEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addWidget(self.frame_7)

        self.frame_10 = QFrame(self.frame_4)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 4, -1, 4)
        self.label_5 = QLabel(self.frame_10)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_4.addWidget(self.label_5)

        self.radioButton_3 = QRadioButton(self.frame_10)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.horizontalLayout_4.addWidget(self.radioButton_3)

        self.radioButton_4 = QRadioButton(self.frame_10)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.horizontalLayout_4.addWidget(self.radioButton_4)

        self.lineEdit_2 = QLineEdit(self.frame_10)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_4.addWidget(self.lineEdit_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addWidget(self.frame_10)

        self.frame_9 = QFrame(self.frame_4)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 4, -1, 4)
        self.label_6 = QLabel(self.frame_9)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_5.addWidget(self.label_6)

        self.radioButton_5 = QRadioButton(self.frame_9)
        self.radioButton_5.setObjectName(u"radioButton_5")

        self.horizontalLayout_5.addWidget(self.radioButton_5)

        self.radioButton_6 = QRadioButton(self.frame_9)
        self.radioButton_6.setObjectName(u"radioButton_6")

        self.horizontalLayout_5.addWidget(self.radioButton_6)

        self.lineEdit_3 = QLineEdit(self.frame_9)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_5.addWidget(self.lineEdit_3)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_3.addWidget(self.frame_9)

        self.frame_8 = QFrame(self.frame_4)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 4, -1, 4)
        self.label_7 = QLabel(self.frame_8)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_6.addWidget(self.label_7)

        self.radioButton_7 = QRadioButton(self.frame_8)
        self.radioButton_7.setObjectName(u"radioButton_7")

        self.horizontalLayout_6.addWidget(self.radioButton_7)

        self.radioButton_8 = QRadioButton(self.frame_8)
        self.radioButton_8.setObjectName(u"radioButton_8")

        self.horizontalLayout_6.addWidget(self.radioButton_8)

        self.lineEdit_4 = QLineEdit(self.frame_8)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_6.addWidget(self.lineEdit_4)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)


        self.verticalLayout_3.addWidget(self.frame_8)


        self.verticalLayout_2.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.tab)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMaximumSize(QSize(16777215, 36))
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, 3, -1, 0)
        self.label_8 = QLabel(self.frame_5)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_7.addWidget(self.label_8)

        self.label_9 = QLabel(self.frame_5)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(16, 16))
        self.label_9.setMaximumSize(QSize(16, 16))
        self.label_9.setToolTipDuration(-1)
        self.label_9.setPixmap(QPixmap(u":/ui/info_icon.png"))
        self.label_9.setScaledContents(True)

        self.horizontalLayout_7.addWidget(self.label_9)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_6)


        self.verticalLayout_2.addWidget(self.frame_5)

        self.frame_6 = QFrame(self.tab)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_6)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_14 = QFrame(self.frame_6)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(-1, 4, -1, 4)
        self.label_10 = QLabel(self.frame_14)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_8.addWidget(self.label_10)

        self.radioButton_10 = QRadioButton(self.frame_14)
        self.radioButton_10.setObjectName(u"radioButton_10")

        self.horizontalLayout_8.addWidget(self.radioButton_10)

        self.radioButton_11 = QRadioButton(self.frame_14)
        self.radioButton_11.setObjectName(u"radioButton_11")

        self.horizontalLayout_8.addWidget(self.radioButton_11)

        self.radioButton_9 = QRadioButton(self.frame_14)
        self.radioButton_9.setObjectName(u"radioButton_9")

        self.horizontalLayout_8.addWidget(self.radioButton_9)

        self.lineEdit_5 = QLineEdit(self.frame_14)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_8.addWidget(self.lineEdit_5)

        self.pushButton = QPushButton(self.frame_14)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMaximumSize(QSize(24, 16777215))

        self.horizontalLayout_8.addWidget(self.pushButton)


        self.verticalLayout_4.addWidget(self.frame_14)

        self.frame_13 = QFrame(self.frame_6)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_13.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(-1, 4, -1, 4)
        self.label_11 = QLabel(self.frame_13)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_9.addWidget(self.label_11)

        self.radioButton_12 = QRadioButton(self.frame_13)
        self.radioButton_12.setObjectName(u"radioButton_12")

        self.horizontalLayout_9.addWidget(self.radioButton_12)

        self.radioButton_15 = QRadioButton(self.frame_13)
        self.radioButton_15.setObjectName(u"radioButton_15")

        self.horizontalLayout_9.addWidget(self.radioButton_15)

        self.radioButton_18 = QRadioButton(self.frame_13)
        self.radioButton_18.setObjectName(u"radioButton_18")

        self.horizontalLayout_9.addWidget(self.radioButton_18)

        self.lineEdit_6 = QLineEdit(self.frame_13)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_9.addWidget(self.lineEdit_6)

        self.toolButton = QToolButton(self.frame_13)
        self.toolButton.setObjectName(u"toolButton")

        self.horizontalLayout_9.addWidget(self.toolButton)


        self.verticalLayout_4.addWidget(self.frame_13)

        self.frame_12 = QFrame(self.frame_6)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(-1, 4, -1, 4)
        self.label_12 = QLabel(self.frame_12)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_10.addWidget(self.label_12)

        self.radioButton_16 = QRadioButton(self.frame_12)
        self.radioButton_16.setObjectName(u"radioButton_16")

        self.horizontalLayout_10.addWidget(self.radioButton_16)

        self.radioButton_13 = QRadioButton(self.frame_12)
        self.radioButton_13.setObjectName(u"radioButton_13")

        self.horizontalLayout_10.addWidget(self.radioButton_13)

        self.radioButton_19 = QRadioButton(self.frame_12)
        self.radioButton_19.setObjectName(u"radioButton_19")

        self.horizontalLayout_10.addWidget(self.radioButton_19)

        self.lineEdit_7 = QLineEdit(self.frame_12)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_10.addWidget(self.lineEdit_7)

        self.toolButton_2 = QToolButton(self.frame_12)
        self.toolButton_2.setObjectName(u"toolButton_2")

        self.horizontalLayout_10.addWidget(self.toolButton_2)


        self.verticalLayout_4.addWidget(self.frame_12)

        self.frame_11 = QFrame(self.frame_6)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(-1, 4, -1, 4)
        self.label_13 = QLabel(self.frame_11)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_11.addWidget(self.label_13)

        self.radioButton_17 = QRadioButton(self.frame_11)
        self.radioButton_17.setObjectName(u"radioButton_17")

        self.horizontalLayout_11.addWidget(self.radioButton_17)

        self.radioButton_14 = QRadioButton(self.frame_11)
        self.radioButton_14.setObjectName(u"radioButton_14")

        self.horizontalLayout_11.addWidget(self.radioButton_14)

        self.radioButton_20 = QRadioButton(self.frame_11)
        self.radioButton_20.setObjectName(u"radioButton_20")

        self.horizontalLayout_11.addWidget(self.radioButton_20)

        self.lineEdit_8 = QLineEdit(self.frame_11)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_11.addWidget(self.lineEdit_8)

        self.toolButton_3 = QToolButton(self.frame_11)
        self.toolButton_3.setObjectName(u"toolButton_3")

        self.horizontalLayout_11.addWidget(self.toolButton_3)


        self.verticalLayout_4.addWidget(self.frame_11)


        self.verticalLayout_2.addWidget(self.frame_6)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_11 = QVBoxLayout(self.tab_2)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.frame_17 = QFrame(self.tab_2)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setMaximumSize(QSize(16777215, 36))
        self.frame_17.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_17.setLineWidth(1)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(-1, 3, -1, 0)
        self.label_27 = QLabel(self.frame_17)
        self.label_27.setObjectName(u"label_27")

        self.horizontalLayout_20.addWidget(self.label_27)

        self.label_28 = QLabel(self.frame_17)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setMinimumSize(QSize(0, 0))
        self.label_28.setMaximumSize(QSize(16, 16))
        self.label_28.setToolTipDuration(-1)
        self.label_28.setPixmap(QPixmap(u":/ui/info_icon.png"))
        self.label_28.setScaledContents(True)

        self.horizontalLayout_20.addWidget(self.label_28)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_11)


        self.verticalLayout_11.addWidget(self.frame_17)

        self.frame_22 = QFrame(self.tab_2)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_22.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_22)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame_23 = QFrame(self.frame_22)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_23.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_21 = QHBoxLayout(self.frame_23)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(-1, 4, -1, 4)
        self.label_29 = QLabel(self.frame_23)
        self.label_29.setObjectName(u"label_29")

        self.horizontalLayout_21.addWidget(self.label_29)

        self.radioButton_35 = QRadioButton(self.frame_23)
        self.radioButton_35.setObjectName(u"radioButton_35")

        self.horizontalLayout_21.addWidget(self.radioButton_35)

        self.radioButton_36 = QRadioButton(self.frame_23)
        self.radioButton_36.setObjectName(u"radioButton_36")

        self.horizontalLayout_21.addWidget(self.radioButton_36)

        self.lineEdit_14 = QLineEdit(self.frame_23)
        self.lineEdit_14.setObjectName(u"lineEdit_14")
        self.lineEdit_14.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_21.addWidget(self.lineEdit_14)


        self.verticalLayout_9.addWidget(self.frame_23)

        self.frame_24 = QFrame(self.frame_22)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_24.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_24)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(-1, 4, -1, 4)
        self.label_30 = QLabel(self.frame_24)
        self.label_30.setObjectName(u"label_30")

        self.horizontalLayout_22.addWidget(self.label_30)

        self.radioButton_37 = QRadioButton(self.frame_24)
        self.radioButton_37.setObjectName(u"radioButton_37")

        self.horizontalLayout_22.addWidget(self.radioButton_37)

        self.radioButton_38 = QRadioButton(self.frame_24)
        self.radioButton_38.setObjectName(u"radioButton_38")

        self.horizontalLayout_22.addWidget(self.radioButton_38)

        self.lineEdit_15 = QLineEdit(self.frame_24)
        self.lineEdit_15.setObjectName(u"lineEdit_15")
        self.lineEdit_15.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_22.addWidget(self.lineEdit_15)


        self.verticalLayout_9.addWidget(self.frame_24)

        self.frame_25 = QFrame(self.frame_22)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_25.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_23 = QHBoxLayout(self.frame_25)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(-1, 4, -1, 4)
        self.label_31 = QLabel(self.frame_25)
        self.label_31.setObjectName(u"label_31")

        self.horizontalLayout_23.addWidget(self.label_31)

        self.radioButton_39 = QRadioButton(self.frame_25)
        self.radioButton_39.setObjectName(u"radioButton_39")

        self.horizontalLayout_23.addWidget(self.radioButton_39)

        self.radioButton_40 = QRadioButton(self.frame_25)
        self.radioButton_40.setObjectName(u"radioButton_40")

        self.horizontalLayout_23.addWidget(self.radioButton_40)

        self.lineEdit_16 = QLineEdit(self.frame_25)
        self.lineEdit_16.setObjectName(u"lineEdit_16")
        self.lineEdit_16.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_23.addWidget(self.lineEdit_16)


        self.verticalLayout_9.addWidget(self.frame_25)

        self.frame_26 = QFrame(self.frame_22)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_26.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_24 = QHBoxLayout(self.frame_26)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(-1, 4, -1, 4)
        self.label_32 = QLabel(self.frame_26)
        self.label_32.setObjectName(u"label_32")

        self.horizontalLayout_24.addWidget(self.label_32)

        self.radioButton_41 = QRadioButton(self.frame_26)
        self.radioButton_41.setObjectName(u"radioButton_41")

        self.horizontalLayout_24.addWidget(self.radioButton_41)

        self.radioButton_42 = QRadioButton(self.frame_26)
        self.radioButton_42.setObjectName(u"radioButton_42")

        self.horizontalLayout_24.addWidget(self.radioButton_42)

        self.lineEdit_17 = QLineEdit(self.frame_26)
        self.lineEdit_17.setObjectName(u"lineEdit_17")
        self.lineEdit_17.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_24.addWidget(self.lineEdit_17)


        self.verticalLayout_9.addWidget(self.frame_26)


        self.verticalLayout_11.addWidget(self.frame_22)

        self.frame_27 = QFrame(self.tab_2)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setMaximumSize(QSize(16777215, 36))
        self.frame_27.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_27.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_27)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(-1, 3, -1, 0)
        self.label_33 = QLabel(self.frame_27)
        self.label_33.setObjectName(u"label_33")

        self.horizontalLayout_25.addWidget(self.label_33)

        self.label_34 = QLabel(self.frame_27)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setMinimumSize(QSize(16, 16))
        self.label_34.setMaximumSize(QSize(16, 16))
        self.label_34.setToolTipDuration(-1)
        self.label_34.setPixmap(QPixmap(u":/ui/info_icon.png"))
        self.label_34.setScaledContents(True)

        self.horizontalLayout_25.addWidget(self.label_34)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_16)


        self.verticalLayout_11.addWidget(self.frame_27)

        self.frame_28 = QFrame(self.tab_2)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_28.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_28)
        self.verticalLayout_10.setSpacing(6)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(9, 4, 9, 4)
        self.checkBox_10 = QCheckBox(self.frame_28)
        self.checkBox_10.setObjectName(u"checkBox_10")
        self.checkBox_10.setChecked(True)

        self.verticalLayout_10.addWidget(self.checkBox_10)

        self.checkBox_11 = QCheckBox(self.frame_28)
        self.checkBox_11.setObjectName(u"checkBox_11")
        self.checkBox_11.setChecked(True)

        self.verticalLayout_10.addWidget(self.checkBox_11)

        self.checkBox_12 = QCheckBox(self.frame_28)
        self.checkBox_12.setObjectName(u"checkBox_12")
        self.checkBox_12.setChecked(True)

        self.verticalLayout_10.addWidget(self.checkBox_12)

        self.checkBox_13 = QCheckBox(self.frame_28)
        self.checkBox_13.setObjectName(u"checkBox_13")
        self.checkBox_13.setChecked(True)

        self.verticalLayout_10.addWidget(self.checkBox_13)


        self.verticalLayout_11.addWidget(self.frame_28)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_3)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_5 = QVBoxLayout(self.tab_3)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame_15 = QFrame(self.tab_3)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(-1, 3, -1, 0)
        self.label_16 = QLabel(self.frame_15)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_12.addWidget(self.label_16)

        self.label_17 = QLabel(self.frame_15)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(16, 16))
        self.label_17.setMaximumSize(QSize(16, 16))
        self.label_17.setPixmap(QPixmap(u":/ui/info_icon.png"))

        self.horizontalLayout_12.addWidget(self.label_17)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_7)


        self.verticalLayout_5.addWidget(self.frame_15)

        self.frame_16 = QFrame(self.tab_3)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_16)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(-1, 4, -1, 4)
        self.checkBox = QCheckBox(self.frame_16)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setChecked(True)

        self.verticalLayout_7.addWidget(self.checkBox)

        self.checkBox_2 = QCheckBox(self.frame_16)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setChecked(True)

        self.verticalLayout_7.addWidget(self.checkBox_2)

        self.checkBox_3 = QCheckBox(self.frame_16)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setChecked(True)

        self.verticalLayout_7.addWidget(self.checkBox_3)

        self.checkBox_4 = QCheckBox(self.frame_16)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setChecked(True)

        self.verticalLayout_7.addWidget(self.checkBox_4)

        self.checkBox_6 = QCheckBox(self.frame_16)
        self.checkBox_6.setObjectName(u"checkBox_6")
        self.checkBox_6.setChecked(True)

        self.verticalLayout_7.addWidget(self.checkBox_6)

        self.checkBox_5 = QCheckBox(self.frame_16)
        self.checkBox_5.setObjectName(u"checkBox_5")
        self.checkBox_5.setChecked(True)

        self.verticalLayout_7.addWidget(self.checkBox_5)

        self.checkBox_7 = QCheckBox(self.frame_16)
        self.checkBox_7.setObjectName(u"checkBox_7")
        self.checkBox_7.setChecked(True)

        self.verticalLayout_7.addWidget(self.checkBox_7)

        self.checkBox_8 = QCheckBox(self.frame_16)
        self.checkBox_8.setObjectName(u"checkBox_8")
        self.checkBox_8.setChecked(True)

        self.verticalLayout_7.addWidget(self.checkBox_8)

        self.checkBox_9 = QCheckBox(self.frame_16)
        self.checkBox_9.setObjectName(u"checkBox_9")
        self.checkBox_9.setChecked(True)

        self.verticalLayout_7.addWidget(self.checkBox_9)


        self.verticalLayout_5.addWidget(self.frame_16)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.tabWidget.addTab(self.tab_4, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.horizontalLayout.addWidget(self.frame)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_14 = QLabel(self.frame_2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMaximumSize(QSize(16777215, 36))

        self.verticalLayout_6.addWidget(self.label_14)

        self.label_15 = QLabel(self.frame_2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFrameShape(QFrame.Shape.Box)
        self.label_15.setPixmap(QPixmap(u":/ui/alchemy_logo.png"))

        self.verticalLayout_6.addWidget(self.label_15)


        self.horizontalLayout.addWidget(self.frame_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 876, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.tabWidget, self.radioButton)
        QWidget.setTabOrder(self.radioButton, self.radioButton_2)
        QWidget.setTabOrder(self.radioButton_2, self.lineEdit)
        QWidget.setTabOrder(self.lineEdit, self.radioButton_3)
        QWidget.setTabOrder(self.radioButton_3, self.radioButton_4)
        QWidget.setTabOrder(self.radioButton_4, self.lineEdit_2)
        QWidget.setTabOrder(self.lineEdit_2, self.radioButton_5)
        QWidget.setTabOrder(self.radioButton_5, self.radioButton_6)
        QWidget.setTabOrder(self.radioButton_6, self.lineEdit_3)
        QWidget.setTabOrder(self.lineEdit_3, self.radioButton_7)
        QWidget.setTabOrder(self.radioButton_7, self.radioButton_8)
        QWidget.setTabOrder(self.radioButton_8, self.lineEdit_4)
        QWidget.setTabOrder(self.lineEdit_4, self.radioButton_10)
        QWidget.setTabOrder(self.radioButton_10, self.radioButton_11)
        QWidget.setTabOrder(self.radioButton_11, self.radioButton_9)
        QWidget.setTabOrder(self.radioButton_9, self.lineEdit_5)
        QWidget.setTabOrder(self.lineEdit_5, self.pushButton)
        QWidget.setTabOrder(self.pushButton, self.radioButton_12)
        QWidget.setTabOrder(self.radioButton_12, self.radioButton_15)
        QWidget.setTabOrder(self.radioButton_15, self.radioButton_18)
        QWidget.setTabOrder(self.radioButton_18, self.lineEdit_6)
        QWidget.setTabOrder(self.lineEdit_6, self.toolButton)
        QWidget.setTabOrder(self.toolButton, self.radioButton_16)
        QWidget.setTabOrder(self.radioButton_16, self.radioButton_13)
        QWidget.setTabOrder(self.radioButton_13, self.radioButton_19)
        QWidget.setTabOrder(self.radioButton_19, self.lineEdit_7)
        QWidget.setTabOrder(self.lineEdit_7, self.toolButton_2)
        QWidget.setTabOrder(self.toolButton_2, self.radioButton_17)
        QWidget.setTabOrder(self.radioButton_17, self.radioButton_14)
        QWidget.setTabOrder(self.radioButton_14, self.radioButton_20)
        QWidget.setTabOrder(self.radioButton_20, self.lineEdit_8)
        QWidget.setTabOrder(self.lineEdit_8, self.toolButton_3)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"igbFinisher", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Processing Settings:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Skin Numbers:", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body>Enter a 4- or 5- digit skin number for each game. Skin numbers are not used by &quot;other&quot; assets. If &quot;None&quot; is selected, the game will be skipped.</body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"XML1:", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"Number:", None))
        self.lineEdit.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"XML2:", None))
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.radioButton_4.setText(QCoreApplication.translate("MainWindow", u"Number:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"MUA1:", None))
        self.radioButton_5.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.radioButton_6.setText(QCoreApplication.translate("MainWindow", u"Number:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"MUA2:", None))
        self.radioButton_7.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.radioButton_8.setText(QCoreApplication.translate("MainWindow", u"Number:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Output Folder Paths:", None))
#if QT_CONFIG(tooltip)
        self.label_9.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Enter the output folder for each game. If &quot;Detect&quot; is selected, output folder detection will be used. If &quot;None&quot; is selected, the game will be skipped.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_9.setText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"XML1:", None))
        self.radioButton_10.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.radioButton_11.setText(QCoreApplication.translate("MainWindow", u"Detect", None))
        self.radioButton_9.setText(QCoreApplication.translate("MainWindow", u"Path:", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"XML2:", None))
        self.radioButton_12.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.radioButton_15.setText(QCoreApplication.translate("MainWindow", u"Detect", None))
        self.radioButton_18.setText(QCoreApplication.translate("MainWindow", u"Path:", None))
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"MUA1:", None))
        self.radioButton_16.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.radioButton_13.setText(QCoreApplication.translate("MainWindow", u"Detect", None))
        self.radioButton_19.setText(QCoreApplication.translate("MainWindow", u"Path:", None))
        self.toolButton_2.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"MUA2", None))
        self.radioButton_17.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.radioButton_14.setText(QCoreApplication.translate("MainWindow", u"Detect", None))
        self.radioButton_20.setText(QCoreApplication.translate("MainWindow", u"Path:", None))
        self.toolButton_3.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Asset", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Special Names:", None))
#if QT_CONFIG(tooltip)
        self.label_28.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Enter a special name to be included in the file name for each game. For &quot;other&quot; assets, this value will be the whole file name. For everything else, it will be added as a suffix in parenthesis. If &quot;None&quot; is selected, the default naming convention will be used.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_28.setText("")
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"XML1:", None))
        self.radioButton_35.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.radioButton_36.setText(QCoreApplication.translate("MainWindow", u"Name:", None))
        self.lineEdit_14.setText("")
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"XML2:", None))
        self.radioButton_37.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.radioButton_38.setText(QCoreApplication.translate("MainWindow", u"Name:", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"MUA1:", None))
        self.radioButton_39.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.radioButton_40.setText(QCoreApplication.translate("MainWindow", u"Name:", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"MUA2:", None))
        self.radioButton_41.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.radioButton_42.setText(QCoreApplication.translate("MainWindow", u"Name:", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Number Ends in XX:", None))
#if QT_CONFIG(tooltip)
        self.label_34.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Select if the last two digits of the skin number in the file name should be &quot;XX&quot; (True) or if the file name should use the full skin number (False). This setting does not apply to files that do not use the skin number in the file name. This setting does not impact hex editing.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_34.setText("")
        self.checkBox_10.setText(QCoreApplication.translate("MainWindow", u"XML1", None))
        self.checkBox_11.setText(QCoreApplication.translate("MainWindow", u"XML2", None))
        self.checkBox_12.setText(QCoreApplication.translate("MainWindow", u"MUA1", None))
        self.checkBox_13.setText(QCoreApplication.translate("MainWindow", u"MUA2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Naming", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Consoles to export for:", None))
#if QT_CONFIG(tooltip)
        self.label_17.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Select which consoles to export assets for. Consoles will be skipped if their game is skipped or if their games do not use the selected asset type. GameCube, PS2, PSP, Wii, and Xbox will be skipped for assets with advanced textures.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_17.setText("")
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"PC", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"Steam", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"GameCube", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"PS2", None))
        self.checkBox_6.setText(QCoreApplication.translate("MainWindow", u"PS3", None))
        self.checkBox_5.setText(QCoreApplication.translate("MainWindow", u"PSP", None))
        self.checkBox_7.setText(QCoreApplication.translate("MainWindow", u"Wii", None))
        self.checkBox_8.setText(QCoreApplication.translate("MainWindow", u"Xbox", None))
        self.checkBox_9.setText(QCoreApplication.translate("MainWindow", u"Xbox 360", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Console", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Other", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Drag and Drop igb Files Below or click to select files:", None))
        self.label_15.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

