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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QRadioButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTabWidget, QTextEdit,
    QToolButton, QVBoxLayout, QWidget)
from . import ui_resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(911, 504)
        icon = QIcon()
        icon.addFile(u":/icons/logo.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionExit.setMenuRole(QAction.MenuRole.TextHeuristicRole)
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

        self.radioButton_xml1_num_none = QRadioButton(self.frame_7)
        self.radioButton_xml1_num_none.setObjectName(u"radioButton_xml1_num_none")

        self.horizontalLayout_3.addWidget(self.radioButton_xml1_num_none)

        self.radioButton_xml1_num = QRadioButton(self.frame_7)
        self.radioButton_xml1_num.setObjectName(u"radioButton_xml1_num")

        self.horizontalLayout_3.addWidget(self.radioButton_xml1_num)

        self.lineEdit_xml1_num = QLineEdit(self.frame_7)
        self.lineEdit_xml1_num.setObjectName(u"lineEdit_xml1_num")
        self.lineEdit_xml1_num.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.lineEdit_xml1_num)

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

        self.radioButton_xml2_num_none = QRadioButton(self.frame_10)
        self.radioButton_xml2_num_none.setObjectName(u"radioButton_xml2_num_none")

        self.horizontalLayout_4.addWidget(self.radioButton_xml2_num_none)

        self.radioButton_xml2_num = QRadioButton(self.frame_10)
        self.radioButton_xml2_num.setObjectName(u"radioButton_xml2_num")

        self.horizontalLayout_4.addWidget(self.radioButton_xml2_num)

        self.lineEdit_xml2_num = QLineEdit(self.frame_10)
        self.lineEdit_xml2_num.setObjectName(u"lineEdit_xml2_num")
        self.lineEdit_xml2_num.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_4.addWidget(self.lineEdit_xml2_num)

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

        self.radioButton_mua1_num_none = QRadioButton(self.frame_9)
        self.radioButton_mua1_num_none.setObjectName(u"radioButton_mua1_num_none")

        self.horizontalLayout_5.addWidget(self.radioButton_mua1_num_none)

        self.radioButton_mua1_num = QRadioButton(self.frame_9)
        self.radioButton_mua1_num.setObjectName(u"radioButton_mua1_num")

        self.horizontalLayout_5.addWidget(self.radioButton_mua1_num)

        self.lineEdit_mua1_num = QLineEdit(self.frame_9)
        self.lineEdit_mua1_num.setObjectName(u"lineEdit_mua1_num")
        self.lineEdit_mua1_num.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_5.addWidget(self.lineEdit_mua1_num)

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

        self.radioButton_mua2_num_none = QRadioButton(self.frame_8)
        self.radioButton_mua2_num_none.setObjectName(u"radioButton_mua2_num_none")

        self.horizontalLayout_6.addWidget(self.radioButton_mua2_num_none)

        self.radioButton_mua2_num = QRadioButton(self.frame_8)
        self.radioButton_mua2_num.setObjectName(u"radioButton_mua2_num")

        self.horizontalLayout_6.addWidget(self.radioButton_mua2_num)

        self.lineEdit_mua2_num = QLineEdit(self.frame_8)
        self.lineEdit_mua2_num.setObjectName(u"lineEdit_mua2_num")
        self.lineEdit_mua2_num.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_6.addWidget(self.lineEdit_mua2_num)

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

        self.toolButton_5 = QToolButton(self.frame_14)
        self.toolButton_5.setObjectName(u"toolButton_5")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen))
        self.toolButton_5.setIcon(icon1)

        self.horizontalLayout_8.addWidget(self.toolButton_5)


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
        self.toolButton.setIcon(icon1)

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
        self.toolButton_2.setIcon(icon1)

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
        self.toolButton_3.setIcon(icon1)

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
        self.verticalLayout_8 = QVBoxLayout(self.tab_4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.frame_18 = QFrame(self.tab_4)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(-1, 3, -1, 0)
        self.label_18 = QLabel(self.frame_18)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_13.addWidget(self.label_18)

        self.label_19 = QLabel(self.frame_18)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setPixmap(QPixmap(u":/ui/info_icon.png"))

        self.horizontalLayout_13.addWidget(self.label_19)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_8)


        self.verticalLayout_8.addWidget(self.frame_18)

        self.frame_19 = QFrame(self.tab_4)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_19)
        self.verticalLayout_12.setSpacing(6)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(-1, 4, -1, 4)
        self.frame_20 = QFrame(self.frame_19)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_20.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_20)
        self.horizontalLayout_14.setSpacing(6)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.checkBox_14 = QCheckBox(self.frame_20)
        self.checkBox_14.setObjectName(u"checkBox_14")

        self.horizontalLayout_14.addWidget(self.checkBox_14)

        self.label_20 = QLabel(self.frame_20)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setPixmap(QPixmap(u":/ui/info_icon.png"))

        self.horizontalLayout_14.addWidget(self.label_20)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_9)


        self.verticalLayout_12.addWidget(self.frame_20)

        self.frame_21 = QFrame(self.frame_19)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_21.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_21)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.checkBox_15 = QCheckBox(self.frame_21)
        self.checkBox_15.setObjectName(u"checkBox_15")

        self.horizontalLayout_15.addWidget(self.checkBox_15)

        self.label_21 = QLabel(self.frame_21)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setPixmap(QPixmap(u":/ui/info_icon.png"))

        self.horizontalLayout_15.addWidget(self.label_21)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_10)


        self.verticalLayout_12.addWidget(self.frame_21)

        self.frame_29 = QFrame(self.frame_19)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_29.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_29)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.checkBox_16 = QCheckBox(self.frame_29)
        self.checkBox_16.setObjectName(u"checkBox_16")

        self.horizontalLayout_16.addWidget(self.checkBox_16)

        self.label_22 = QLabel(self.frame_29)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setPixmap(QPixmap(u":/ui/info_icon.png"))

        self.horizontalLayout_16.addWidget(self.label_22)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_12)


        self.verticalLayout_12.addWidget(self.frame_29)

        self.frame_30 = QFrame(self.frame_19)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_30.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_30)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.checkBox_17 = QCheckBox(self.frame_30)
        self.checkBox_17.setObjectName(u"checkBox_17")

        self.horizontalLayout_17.addWidget(self.checkBox_17)

        self.label_23 = QLabel(self.frame_30)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setPixmap(QPixmap(u":/ui/info_icon.png"))

        self.horizontalLayout_17.addWidget(self.label_23)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_13)


        self.verticalLayout_12.addWidget(self.frame_30)

        self.frame_31 = QFrame(self.frame_19)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_31.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_31)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.checkBox_18 = QCheckBox(self.frame_31)
        self.checkBox_18.setObjectName(u"checkBox_18")

        self.horizontalLayout_18.addWidget(self.checkBox_18)

        self.label_24 = QLabel(self.frame_31)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setPixmap(QPixmap(u":/ui/info_icon.png"))

        self.horizontalLayout_18.addWidget(self.label_24)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_14)


        self.verticalLayout_12.addWidget(self.frame_31)

        self.frame_32 = QFrame(self.frame_19)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_32.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_32)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.checkBox_19 = QCheckBox(self.frame_32)
        self.checkBox_19.setObjectName(u"checkBox_19")

        self.horizontalLayout_19.addWidget(self.checkBox_19)

        self.label_25 = QLabel(self.frame_32)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setPixmap(QPixmap(u":/ui/info_icon.png"))

        self.horizontalLayout_19.addWidget(self.label_25)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_15)


        self.verticalLayout_12.addWidget(self.frame_32)

        self.frame_34 = QFrame(self.frame_19)
        self.frame_34.setObjectName(u"frame_34")
        self.frame_34.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_34.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.frame_34)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.checkBox_20 = QCheckBox(self.frame_34)
        self.checkBox_20.setObjectName(u"checkBox_20")

        self.horizontalLayout_28.addWidget(self.checkBox_20)

        self.label_38 = QLabel(self.frame_34)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setPixmap(QPixmap(u":/ui/info_icon.png"))

        self.horizontalLayout_28.addWidget(self.label_38)

        self.lineEdit_9 = QLineEdit(self.frame_34)
        self.lineEdit_9.setObjectName(u"lineEdit_9")

        self.horizontalLayout_28.addWidget(self.lineEdit_9)

        self.toolButton_4 = QToolButton(self.frame_34)
        self.toolButton_4.setObjectName(u"toolButton_4")
        self.toolButton_4.setIcon(icon1)

        self.horizontalLayout_28.addWidget(self.toolButton_4)


        self.verticalLayout_12.addWidget(self.frame_34)

        self.line_2 = QFrame(self.frame_19)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_12.addWidget(self.line_2)

        self.frame_33 = QFrame(self.frame_19)
        self.frame_33.setObjectName(u"frame_33")
        self.frame_33.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_33.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_26 = QHBoxLayout(self.frame_33)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.label_26 = QLabel(self.frame_33)
        self.label_26.setObjectName(u"label_26")

        self.horizontalLayout_26.addWidget(self.label_26)

        self.comboBox = QComboBox(self.frame_33)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setEditable(True)
        self.comboBox.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        self.horizontalLayout_26.addWidget(self.comboBox)

        self.label_35 = QLabel(self.frame_33)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setPixmap(QPixmap(u":/ui/info_icon.png"))

        self.horizontalLayout_26.addWidget(self.label_35)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_17)


        self.verticalLayout_12.addWidget(self.frame_33)

        self.frame_35 = QFrame(self.frame_19)
        self.frame_35.setObjectName(u"frame_35")
        self.frame_35.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_35.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_27 = QHBoxLayout(self.frame_35)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.label_36 = QLabel(self.frame_35)
        self.label_36.setObjectName(u"label_36")

        self.horizontalLayout_27.addWidget(self.label_36)

        self.comboBox_forced_assets = QComboBox(self.frame_35)
        self.comboBox_forced_assets.addItem("")
        self.comboBox_forced_assets.setObjectName(u"comboBox_forced_assets")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_forced_assets.sizePolicy().hasHeightForWidth())
        self.comboBox_forced_assets.setSizePolicy(sizePolicy)
        self.comboBox_forced_assets.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        self.horizontalLayout_27.addWidget(self.comboBox_forced_assets)

        self.label_37 = QLabel(self.frame_35)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setPixmap(QPixmap(u":/ui/info_icon.png"))

        self.horizontalLayout_27.addWidget(self.label_37)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_27.addItem(self.horizontalSpacer_18)


        self.verticalLayout_12.addWidget(self.frame_35)


        self.verticalLayout_8.addWidget(self.frame_19)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_4)

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
        self.frame_2.setMinimumSize(QSize(0, 0))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame_36 = QFrame(self.frame_2)
        self.frame_36.setObjectName(u"frame_36")
        self.frame_36.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_36.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.frame_36)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.label_14 = QLabel(self.frame_36)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMaximumSize(QSize(16777215, 36))

        self.verticalLayout_13.addWidget(self.label_14)

        self.label_15 = QLabel(self.frame_36)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFrameShape(QFrame.Shape.Box)
        self.label_15.setPixmap(QPixmap(u":/ui/alchemy_logo.png"))
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_13.addWidget(self.label_15)


        self.verticalLayout_6.addWidget(self.frame_36)

        self.frame_37 = QFrame(self.frame_2)
        self.frame_37.setObjectName(u"frame_37")
        self.frame_37.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_37.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.frame_37)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.label_39 = QLabel(self.frame_37)
        self.label_39.setObjectName(u"label_39")

        self.verticalLayout_14.addWidget(self.label_39)

        self.textEdit = QTextEdit(self.frame_37)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setEnabled(False)

        self.verticalLayout_14.addWidget(self.textEdit)


        self.verticalLayout_6.addWidget(self.frame_37)


        self.horizontalLayout.addWidget(self.frame_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 911, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.tabWidget, self.radioButton_xml1_num_none)
        QWidget.setTabOrder(self.radioButton_xml1_num_none, self.radioButton_xml1_num)
        QWidget.setTabOrder(self.radioButton_xml1_num, self.lineEdit_xml1_num)
        QWidget.setTabOrder(self.lineEdit_xml1_num, self.radioButton_xml2_num_none)
        QWidget.setTabOrder(self.radioButton_xml2_num_none, self.radioButton_xml2_num)
        QWidget.setTabOrder(self.radioButton_xml2_num, self.lineEdit_xml2_num)
        QWidget.setTabOrder(self.lineEdit_xml2_num, self.radioButton_mua1_num_none)
        QWidget.setTabOrder(self.radioButton_mua1_num_none, self.radioButton_mua1_num)
        QWidget.setTabOrder(self.radioButton_mua1_num, self.lineEdit_mua1_num)
        QWidget.setTabOrder(self.lineEdit_mua1_num, self.radioButton_mua2_num_none)
        QWidget.setTabOrder(self.radioButton_mua2_num_none, self.radioButton_mua2_num)
        QWidget.setTabOrder(self.radioButton_mua2_num, self.lineEdit_mua2_num)
        QWidget.setTabOrder(self.lineEdit_mua2_num, self.radioButton_10)
        QWidget.setTabOrder(self.radioButton_10, self.radioButton_11)
        QWidget.setTabOrder(self.radioButton_11, self.radioButton_9)
        QWidget.setTabOrder(self.radioButton_9, self.lineEdit_5)
        QWidget.setTabOrder(self.lineEdit_5, self.radioButton_12)
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
#if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+F4", None))
#endif // QT_CONFIG(shortcut)
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Processing Settings:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Skin Numbers:", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body>Enter a 4- or 5- digit skin number for each game. Skin numbers are not used by &quot;other&quot; assets. If &quot;None&quot; is selected, the game will be skipped.</body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"XML1:", None))
        self.radioButton_xml1_num_none.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.radioButton_xml1_num.setText(QCoreApplication.translate("MainWindow", u"Number:", None))
        self.lineEdit_xml1_num.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"XML2:", None))
        self.radioButton_xml2_num_none.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.radioButton_xml2_num.setText(QCoreApplication.translate("MainWindow", u"Number:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"MUA1:", None))
        self.radioButton_mua1_num_none.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.radioButton_mua1_num.setText(QCoreApplication.translate("MainWindow", u"Number:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"MUA2:", None))
        self.radioButton_mua2_num_none.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.radioButton_mua2_num.setText(QCoreApplication.translate("MainWindow", u"Number:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Output Folder Paths:", None))
#if QT_CONFIG(tooltip)
        self.label_9.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Enter the output folder for each game. If &quot;Detect&quot; is selected, output folder detection will be used. If &quot;None&quot; is selected, the game will be skipped.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_9.setText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"XML1:", None))
        self.radioButton_10.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.radioButton_11.setText(QCoreApplication.translate("MainWindow", u"Detect", None))
        self.radioButton_9.setText(QCoreApplication.translate("MainWindow", u"Path:", None))
        self.toolButton_5.setText(QCoreApplication.translate("MainWindow", u"...", None))
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
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Other Settings:", None))
#if QT_CONFIG(tooltip)
        self.label_19.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Additional settings that control the output.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_19.setText("")
        self.checkBox_14.setText(QCoreApplication.translate("MainWindow", u"Process with big textures", None))
#if QT_CONFIG(tooltip)
        self.label_20.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>If oversized textures should preserve their original size on weaker consoles (GameCube, PS2, PSP). This is ignored for 2D assets.</p><p>This is recomended for large characters like Galactus/Ymir or for specific assets like maps, where it will preserve the original texture size for XML1, XML2, and MUA1 PS2 and only cut it in half for GameCube, PSP, and MUA2 PS2. Otherwise, it should be turned off, and the textures will be scaled to the maximum recommended size for that console. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_20.setText("")
#if QT_CONFIG(tooltip)
        self.frame_21.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>If this is a secondary skin (like Human Torch's flame on skin), which should have its texture size cut in half on weaker consoles (GameCube, PS2, and PSP). This setting only applies to Skins. For XML1/XML2/MUA1 PS2, this setting also applies to Other models, which are sometimes the same resolution as the more powerful consoles, but sometimes they are the same as the weaker consoles.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_15.setText(QCoreApplication.translate("MainWindow", u"Secondary skin", None))
        self.label_21.setText("")
        self.checkBox_16.setText(QCoreApplication.translate("MainWindow", u"Untextured models are okay", None))
#if QT_CONFIG(tooltip)
        self.label_22.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Whether untextured models can be processed. Only applies to 3D assets, as 2D assets always need a texture.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_22.setText("")
        self.checkBox_17.setText(QCoreApplication.translate("MainWindow", u"Generate collision", None))
#if QT_CONFIG(tooltip)
        self.label_23.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>If collision should be generated with the Alchemy 3.2 &quot;igCollideHullRaven&quot; optimization. This setting only applies to Other models and is only recommended for maps and map models.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_23.setText("")
        self.checkBox_18.setText(QCoreApplication.translate("MainWindow", u"Convert igBlend transparency attributes to igAlpha", None))
#if QT_CONFIG(tooltip)
        self.label_24.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>If igBlendFunctionAttr should be hex edited to igAlphaFunctionAttr and igBlendStateAttr should be hex edited to igAlphaStateAttr to allow transparent textures to appear correctly.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_24.setText("")
        self.checkBox_19.setText(QCoreApplication.translate("MainWindow", u"Skip subfolder", None))
#if QT_CONFIG(tooltip)
        self.label_25.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>If the console-specific sub-folder should be skipped when exporting the assets, and the asset will just be exported directly to the chosen export directory. This is only recommended if you are exporting for one game/console.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_25.setText("")
        self.checkBox_20.setText(QCoreApplication.translate("MainWindow", u"Advanced texture ini", None))
#if QT_CONFIG(tooltip)
        self.label_38.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>If an ini file for advanced textures should be used. If an advanced texture ini file is used, the asset will only be exported for MUA1 PC, Steam, PS3, and Xbox 360. This only works with 3D assets.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_38.setText("")
        self.toolButton_4.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Folder Grouping:", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Automatic", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Advanced Texture Folders (PC with Xbox 360, Steam with PS3)", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Advanced Texture Folders (PC with PS3, Steam with Xbox 360)", None))

#if QT_CONFIG(tooltip)
        self.label_35.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>If folders for certain consoles should be grouped together. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_35.setText("")
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Forced Asset Type:", None))
        self.comboBox_forced_assets.setItemText(0, QCoreApplication.translate("MainWindow", u"New Item", None))

#if QT_CONFIG(tooltip)
        self.label_37.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>If a specific asset type should be forced, regardless of file name.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_37.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Other", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Drag and Drop igb Files Below or click to select files:", None))
        self.label_15.setText("")
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Console", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

