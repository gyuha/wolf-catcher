# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(597, 691)
        icon = QIcon()
        icon.addFile(u":/icon/icons/main-icon.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.action_always_top = QAction(MainWindow)
        self.action_always_top.setObjectName(u"action_always_top")
        self.action_always_top.setCheckable(True)
        self.action_clipboard_toggle = QAction(MainWindow)
        self.action_clipboard_toggle.setObjectName(u"action_clipboard_toggle")
        self.action_clipboard_toggle.setCheckable(True)
        self.action_clipboard_toggle.setChecked(True)
        self.action_exit = QAction(MainWindow)
        self.action_exit.setObjectName(u"action_exit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMaximumSize(QSize(16777215, 16777215))
        self.centralwidget.setAutoFillBackground(False)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.item_list = QListWidget(self.centralwidget)
        self.item_list.setObjectName(u"item_list")
        self.item_list.setAcceptDrops(True)
        self.item_list.setDragDropMode(QAbstractItemView.DropOnly)
        self.item_list.setDefaultDropAction(Qt.LinkAction)

        self.verticalLayout.addWidget(self.item_list)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 5, 10, 5)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.downloaded_label = QLabel(self.centralwidget)
        self.downloaded_label.setObjectName(u"downloaded_label")
        font = QFont()
        font.setBold(True)
        self.downloaded_label.setFont(font)

        self.horizontalLayout.addWidget(self.downloaded_label)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.total_label = QLabel(self.centralwidget)
        self.total_label.setObjectName(u"total_label")
        self.total_label.setFont(font)

        self.horizontalLayout.addWidget(self.total_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.site_open_button = QPushButton(self.centralwidget)
        self.site_open_button.setObjectName(u"site_open_button")
        self.site_open_button.setAcceptDrops(True)

        self.horizontalLayout.addWidget(self.site_open_button)

        self.getButton = QPushButton(self.centralwidget)
        self.getButton.setObjectName(u"getButton")

        self.horizontalLayout.addWidget(self.getButton)

        self.complete_delete_button = QPushButton(self.centralwidget)
        self.complete_delete_button.setObjectName(u"complete_delete_button")

        self.horizontalLayout.addWidget(self.complete_delete_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 597, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.action_exit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Wolf catcher", None))
        self.action_always_top.setText(QCoreApplication.translate("MainWindow", u"\ud56d\uc0c1\uc704", None))
        self.action_clipboard_toggle.setText(QCoreApplication.translate("MainWindow", u"\ud074\ub9bd\ubcf4\ub4dc\uc5d0\uc11c \ucd94\uac00", None))
        self.action_exit.setText(QCoreApplication.translate("MainWindow", u"\uc885\ub8cc(&q)", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc6b4\ub85c\ub4dc : ", None))
        self.downloaded_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"  /  \uc804\uccb4 : ", None))
        self.total_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.site_open_button.setText(QCoreApplication.translate("MainWindow", u"\uc0ac\uc774\ud2b8 \uc5f4\uae30", None))
        self.getButton.setText(QCoreApplication.translate("MainWindow", u"\uc8fc\uc18c \uc5c5\ub370\uc774\ud2b8", None))
        self.complete_delete_button.setText(QCoreApplication.translate("MainWindow", u"\uc644\ub8cc \uc0ad\uc81c", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\uc791\uc5c5", None))
    # retranslateUi

