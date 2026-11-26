# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_About.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QSizePolicy, QVBoxLayout, QWidget)
from . import ui_resources_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(292, 422)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/icons/logo.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(18, -1, 18, -1)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setPixmap(QPixmap(u":/icons/logo.ico"))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.label_name = QLabel(Dialog)
        self.label_name.setObjectName(u"label_name")
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.label_name.setFont(font)
        self.label_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_name)

        self.label_version = QLabel(Dialog)
        self.label_version.setObjectName(u"label_version")
        self.label_version.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_version)

        self.label_desc = QLabel(Dialog)
        self.label_desc.setObjectName(u"label_desc")
        self.label_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_desc)

        self.label_url = QLabel(Dialog)
        self.label_url.setObjectName(u"label_url")
        self.label_url.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_url.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.label_url)

        self.label_url_github = QLabel(Dialog)
        self.label_url_github.setObjectName(u"label_url_github")
        self.label_url_github.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_url_github.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.label_url_github)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"About igbFinisher", None))
        self.label.setText("")
        self.label_name.setText(QCoreApplication.translate("Dialog", u"APP_NAME", None))
        self.label_version.setText(QCoreApplication.translate("Dialog", u"Version v{APP_VERSION}", None))
        self.label_desc.setText(QCoreApplication.translate("Dialog", u"APP_DESCRIPTION", None))
        self.label_url.setText(QCoreApplication.translate("Dialog", u"<a href=\"{APP_URL}\">Project Page</a>", None))
        self.label_url_github.setText(QCoreApplication.translate("Dialog", u"<a href=\"{APP_GITHUB}\">GitHub Page</a>", None))
    # retranslateUi

