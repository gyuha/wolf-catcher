# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DownloadItem.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_DownloadItem(object):
    def setupUi(self, DownloadItem):
        if not DownloadItem.objectName():
            DownloadItem.setObjectName(u"DownloadItem")
        DownloadItem.resize(725, 94)
        DownloadItem.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(DownloadItem)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.image_label = QLabel(DownloadItem)
        self.image_label.setObjectName(u"image_label")
        self.image_label.setMinimumSize(QSize(80, 80))
        self.image_label.setMaximumSize(QSize(80, 80))
        self.image_label.setAutoFillBackground(False)
        self.image_label.setStyleSheet(u"#image_label {\n"
" background-color: #eee;\n"
"}")

        self.horizontalLayout.addWidget(self.image_label)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 5, -1, -1)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.title_label = QLabel(DownloadItem)
        self.title_label.setObjectName(u"title_label")
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setScaledContents(True)
        self.title_label.setWordWrap(False)

        self.horizontalLayout_2.addWidget(self.title_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.folder_open_button = QPushButton(DownloadItem)
        self.folder_open_button.setObjectName(u"folder_open_button")
        icon = QIcon()
        icon.addFile(u":/icon/icons/folder-open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.folder_open_button.setIcon(icon)
        self.folder_open_button.setFlat(True)

        self.horizontalLayout_2.addWidget(self.folder_open_button)

        self.delete_button = QPushButton(DownloadItem)
        self.delete_button.setObjectName(u"delete_button")
        self.delete_button.setLayoutDirection(Qt.LeftToRight)
        self.delete_button.setAutoFillBackground(False)
        icon1 = QIcon()
        icon1.addFile(u":/icon/icons/trash-delete-bin.png", QSize(), QIcon.Normal, QIcon.Off)
        self.delete_button.setIcon(icon1)
        self.delete_button.setFlat(True)

        self.horizontalLayout_2.addWidget(self.delete_button)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.tag_label = QLabel(DownloadItem)
        self.tag_label.setObjectName(u"tag_label")
        font1 = QFont()
        font1.setBold(True)
        self.tag_label.setFont(font1)
        self.tag_label.setStyleSheet(u"color: #777777;")

        self.horizontalLayout_4.addWidget(self.tag_label)

        self.id_label = QLabel(DownloadItem)
        self.id_label.setObjectName(u"id_label")
        self.id_label.setMaximumSize(QSize(100, 16777215))
        self.id_label.setFont(font1)
        self.id_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.id_label)

        self.state_label = QLabel(DownloadItem)
        self.state_label.setObjectName(u"state_label")
        self.state_label.setMaximumSize(QSize(40, 16777215))
        self.state_label.setStyleSheet(u"#state_label {\n"
"color: #888;\n"
"}")

        self.horizontalLayout_4.addWidget(self.state_label)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.status_label = QLabel(DownloadItem)
        self.status_label.setObjectName(u"status_label")

        self.horizontalLayout_3.addWidget(self.status_label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.progress_bar = QProgressBar(DownloadItem)
        self.progress_bar.setObjectName(u"progress_bar")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progress_bar.sizePolicy().hasHeightForWidth())
        self.progress_bar.setSizePolicy(sizePolicy)
        self.progress_bar.setMaximumSize(QSize(150, 15))
        self.progress_bar.setValue(0)

        self.horizontalLayout_3.addWidget(self.progress_bar)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(DownloadItem)

        QMetaObject.connectSlotsByName(DownloadItem)
    # setupUi

    def retranslateUi(self, DownloadItem):
        DownloadItem.setWindowTitle(QCoreApplication.translate("DownloadItem", u"Form", None))
        self.image_label.setText("")
        self.title_label.setText(QCoreApplication.translate("DownloadItem", u"Loading", None))
        self.folder_open_button.setText("")
        self.delete_button.setText("")
        self.tag_label.setText("")
        self.id_label.setText(QCoreApplication.translate("DownloadItem", u"0", None))
        self.state_label.setText(QCoreApplication.translate("DownloadItem", u"TextLabel", None))
        self.status_label.setText("")
    # retranslateUi

