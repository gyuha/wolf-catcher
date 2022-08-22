/********************************************************************************
** Form generated from reading UI file 'MainWindow.ui'
**
** Created by: Qt User Interface Compiler version 6.3.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QAction *action_always_top;
    QAction *action_clipboard_toggle;
    QAction *action_exit;
    QWidget *centralwidget;
    QVBoxLayout *verticalLayout;
    QListWidget *item_list;
    QHBoxLayout *horizontalLayout;
    QSpacerItem *horizontalSpacer;
    QPushButton *pushButton_2;
    QPushButton *getButton;
    QMenuBar *menubar;
    QMenu *menu;
    QMenu *menu_2;
    QMenu *menu_3;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(434, 631);
        action_always_top = new QAction(MainWindow);
        action_always_top->setObjectName(QString::fromUtf8("action_always_top"));
        action_always_top->setCheckable(true);
        action_clipboard_toggle = new QAction(MainWindow);
        action_clipboard_toggle->setObjectName(QString::fromUtf8("action_clipboard_toggle"));
        action_clipboard_toggle->setCheckable(true);
        action_clipboard_toggle->setChecked(true);
        action_exit = new QAction(MainWindow);
        action_exit->setObjectName(QString::fromUtf8("action_exit"));
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        centralwidget->setMaximumSize(QSize(16777215, 16777215));
        centralwidget->setAutoFillBackground(false);
        verticalLayout = new QVBoxLayout(centralwidget);
        verticalLayout->setSpacing(0);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        verticalLayout->setContentsMargins(0, 0, 0, 0);
        item_list = new QListWidget(centralwidget);
        item_list->setObjectName(QString::fromUtf8("item_list"));

        verticalLayout->addWidget(item_list);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer);

        pushButton_2 = new QPushButton(centralwidget);
        pushButton_2->setObjectName(QString::fromUtf8("pushButton_2"));

        horizontalLayout->addWidget(pushButton_2);

        getButton = new QPushButton(centralwidget);
        getButton->setObjectName(QString::fromUtf8("getButton"));

        horizontalLayout->addWidget(getButton);


        verticalLayout->addLayout(horizontalLayout);

        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName(QString::fromUtf8("menubar"));
        menubar->setGeometry(QRect(0, 0, 434, 22));
        menu = new QMenu(menubar);
        menu->setObjectName(QString::fromUtf8("menu"));
        menu_2 = new QMenu(menubar);
        menu_2->setObjectName(QString::fromUtf8("menu_2"));
        menu_3 = new QMenu(menubar);
        menu_3->setObjectName(QString::fromUtf8("menu_3"));
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName(QString::fromUtf8("statusbar"));
        MainWindow->setStatusBar(statusbar);

        menubar->addAction(menu->menuAction());
        menubar->addAction(menu_3->menuAction());
        menubar->addAction(menu_2->menuAction());
        menu->addAction(action_exit);
        menu_3->addAction(action_always_top);
        menu_3->addAction(action_clipboard_toggle);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "Wolf catcher", nullptr));
        action_always_top->setText(QCoreApplication::translate("MainWindow", "\355\225\255\354\203\201\354\234\204", nullptr));
        action_clipboard_toggle->setText(QCoreApplication::translate("MainWindow", "\355\201\264\353\246\275\353\263\264\353\223\234\354\227\220\354\204\234 \354\266\224\352\260\200", nullptr));
        action_exit->setText(QCoreApplication::translate("MainWindow", "\354\242\205\353\243\214(&q)", nullptr));
        pushButton_2->setText(QCoreApplication::translate("MainWindow", "PushButton", nullptr));
        getButton->setText(QCoreApplication::translate("MainWindow", "Get Button", nullptr));
        menu->setTitle(QCoreApplication::translate("MainWindow", "\354\236\221\354\227\205", nullptr));
        menu_2->setTitle(QCoreApplication::translate("MainWindow", "\353\217\204\354\233\200\353\247\220", nullptr));
        menu_3->setTitle(QCoreApplication::translate("MainWindow", "\354\230\265\354\205\230", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // MAINWINDOW_H
