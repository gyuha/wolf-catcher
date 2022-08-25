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
#include <QtWidgets/QLabel>
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
    QLabel *label;
    QLabel *downloaded_label;
    QLabel *label_3;
    QLabel *total_label;
    QSpacerItem *horizontalSpacer;
    QPushButton *getButton;
    QPushButton *complete_delete_button;
    QMenuBar *menubar;
    QMenu *menu;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(582, 633);
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
        horizontalLayout->setContentsMargins(10, 5, 10, 5);
        label = new QLabel(centralwidget);
        label->setObjectName(QString::fromUtf8("label"));

        horizontalLayout->addWidget(label);

        downloaded_label = new QLabel(centralwidget);
        downloaded_label->setObjectName(QString::fromUtf8("downloaded_label"));
        QFont font;
        font.setBold(true);
        downloaded_label->setFont(font);

        horizontalLayout->addWidget(downloaded_label);

        label_3 = new QLabel(centralwidget);
        label_3->setObjectName(QString::fromUtf8("label_3"));

        horizontalLayout->addWidget(label_3);

        total_label = new QLabel(centralwidget);
        total_label->setObjectName(QString::fromUtf8("total_label"));
        total_label->setFont(font);

        horizontalLayout->addWidget(total_label);

        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer);

        getButton = new QPushButton(centralwidget);
        getButton->setObjectName(QString::fromUtf8("getButton"));

        horizontalLayout->addWidget(getButton);

        complete_delete_button = new QPushButton(centralwidget);
        complete_delete_button->setObjectName(QString::fromUtf8("complete_delete_button"));

        horizontalLayout->addWidget(complete_delete_button);


        verticalLayout->addLayout(horizontalLayout);

        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName(QString::fromUtf8("menubar"));
        menubar->setGeometry(QRect(0, 0, 582, 22));
        menu = new QMenu(menubar);
        menu->setObjectName(QString::fromUtf8("menu"));
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName(QString::fromUtf8("statusbar"));
        MainWindow->setStatusBar(statusbar);

        menubar->addAction(menu->menuAction());
        menu->addAction(action_exit);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "Wolf catcher", nullptr));
        action_always_top->setText(QCoreApplication::translate("MainWindow", "\355\225\255\354\203\201\354\234\204", nullptr));
        action_clipboard_toggle->setText(QCoreApplication::translate("MainWindow", "\355\201\264\353\246\275\353\263\264\353\223\234\354\227\220\354\204\234 \354\266\224\352\260\200", nullptr));
        action_exit->setText(QCoreApplication::translate("MainWindow", "\354\242\205\353\243\214(&q)", nullptr));
        label->setText(QCoreApplication::translate("MainWindow", "\353\213\244\354\232\264\353\241\234\353\223\234 : ", nullptr));
        downloaded_label->setText(QCoreApplication::translate("MainWindow", "0", nullptr));
        label_3->setText(QCoreApplication::translate("MainWindow", "  /  \354\240\204\354\262\264 : ", nullptr));
        total_label->setText(QCoreApplication::translate("MainWindow", "0", nullptr));
        getButton->setText(QCoreApplication::translate("MainWindow", "\354\243\274\354\206\214 \354\227\205\353\215\260\354\235\264\355\212\270", nullptr));
        complete_delete_button->setText(QCoreApplication::translate("MainWindow", "\354\231\204\353\243\214 \354\202\255\354\240\234", nullptr));
        menu->setTitle(QCoreApplication::translate("MainWindow", "\354\236\221\354\227\205", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // MAINWINDOW_H
