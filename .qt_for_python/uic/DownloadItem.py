/********************************************************************************
** Form generated from reading UI file 'DownloadItem.ui'
**
** Created by: Qt User Interface Compiler version 6.3.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef DOWNLOADITEM_H
#define DOWNLOADITEM_H

#include <QtCore/QVariant>
#include <QtGui/QIcon>
#include <QtWidgets/QApplication>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QProgressBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_DownloadItem
{
public:
    QHBoxLayout *horizontalLayout;
    QLabel *image_label;
    QVBoxLayout *verticalLayout;
    QHBoxLayout *horizontalLayout_2;
    QLabel *title_label;
    QSpacerItem *horizontalSpacer;
    QPushButton *folder_open_button;
    QPushButton *cancel_button;
    QPushButton *delete_button;
    QHBoxLayout *horizontalLayout_4;
    QLabel *tag_label;
    QLabel *id_label;
    QHBoxLayout *horizontalLayout_3;
    QLabel *status_label;
    QSpacerItem *horizontalSpacer_2;
    QProgressBar *progress_bar;

    void setupUi(QWidget *DownloadItem)
    {
        if (DownloadItem->objectName().isEmpty())
            DownloadItem->setObjectName(QString::fromUtf8("DownloadItem"));
        DownloadItem->resize(592, 70);
        DownloadItem->setStyleSheet(QString::fromUtf8(""));
        horizontalLayout = new QHBoxLayout(DownloadItem);
        horizontalLayout->setSpacing(5);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        horizontalLayout->setContentsMargins(5, 5, 5, 5);
        image_label = new QLabel(DownloadItem);
        image_label->setObjectName(QString::fromUtf8("image_label"));
        image_label->setMinimumSize(QSize(60, 60));
        image_label->setMaximumSize(QSize(60, 60));
        image_label->setAutoFillBackground(false);
        image_label->setStyleSheet(QString::fromUtf8("#image_label {\n"
" background-color: #eee;\n"
"}"));

        horizontalLayout->addWidget(image_label);

        verticalLayout = new QVBoxLayout();
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        title_label = new QLabel(DownloadItem);
        title_label->setObjectName(QString::fromUtf8("title_label"));
        QFont font;
        font.setPointSize(11);
        font.setBold(true);
        title_label->setFont(font);

        horizontalLayout_2->addWidget(title_label);

        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer);

        folder_open_button = new QPushButton(DownloadItem);
        folder_open_button->setObjectName(QString::fromUtf8("folder_open_button"));
        QIcon icon;
        icon.addFile(QString::fromUtf8(":/icon/icons/folder-open.png"), QSize(), QIcon::Normal, QIcon::Off);
        folder_open_button->setIcon(icon);
        folder_open_button->setFlat(true);

        horizontalLayout_2->addWidget(folder_open_button);

        cancel_button = new QPushButton(DownloadItem);
        cancel_button->setObjectName(QString::fromUtf8("cancel_button"));
        cancel_button->setEnabled(true);
        QIcon icon1;
        icon1.addFile(QString::fromUtf8(":/icon/icons/stop.png"), QSize(), QIcon::Normal, QIcon::Off);
        cancel_button->setIcon(icon1);
        cancel_button->setFlat(true);

        horizontalLayout_2->addWidget(cancel_button);

        delete_button = new QPushButton(DownloadItem);
        delete_button->setObjectName(QString::fromUtf8("delete_button"));
        delete_button->setLayoutDirection(Qt::LeftToRight);
        delete_button->setAutoFillBackground(false);
        QIcon icon2;
        icon2.addFile(QString::fromUtf8(":/icon/icons/trash-delete-bin.png"), QSize(), QIcon::Normal, QIcon::Off);
        delete_button->setIcon(icon2);
        delete_button->setFlat(true);

        horizontalLayout_2->addWidget(delete_button);


        verticalLayout->addLayout(horizontalLayout_2);

        horizontalLayout_4 = new QHBoxLayout();
        horizontalLayout_4->setObjectName(QString::fromUtf8("horizontalLayout_4"));
        tag_label = new QLabel(DownloadItem);
        tag_label->setObjectName(QString::fromUtf8("tag_label"));
        QFont font1;
        font1.setBold(true);
        tag_label->setFont(font1);
        tag_label->setStyleSheet(QString::fromUtf8("color: #777777;"));

        horizontalLayout_4->addWidget(tag_label);

        id_label = new QLabel(DownloadItem);
        id_label->setObjectName(QString::fromUtf8("id_label"));
        id_label->setMaximumSize(QSize(100, 16777215));
        id_label->setFont(font1);
        id_label->setAlignment(Qt::AlignCenter);

        horizontalLayout_4->addWidget(id_label);


        verticalLayout->addLayout(horizontalLayout_4);

        horizontalLayout_3 = new QHBoxLayout();
        horizontalLayout_3->setObjectName(QString::fromUtf8("horizontalLayout_3"));
        status_label = new QLabel(DownloadItem);
        status_label->setObjectName(QString::fromUtf8("status_label"));

        horizontalLayout_3->addWidget(status_label);

        horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_3->addItem(horizontalSpacer_2);

        progress_bar = new QProgressBar(DownloadItem);
        progress_bar->setObjectName(QString::fromUtf8("progress_bar"));
        QSizePolicy sizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(progress_bar->sizePolicy().hasHeightForWidth());
        progress_bar->setSizePolicy(sizePolicy);
        progress_bar->setMaximumSize(QSize(150, 15));
        progress_bar->setValue(0);

        horizontalLayout_3->addWidget(progress_bar);


        verticalLayout->addLayout(horizontalLayout_3);


        horizontalLayout->addLayout(verticalLayout);

        horizontalLayout->setStretch(1, 1);

        retranslateUi(DownloadItem);

        QMetaObject::connectSlotsByName(DownloadItem);
    } // setupUi

    void retranslateUi(QWidget *DownloadItem)
    {
        DownloadItem->setWindowTitle(QCoreApplication::translate("DownloadItem", "Form", nullptr));
        image_label->setText(QString());
        title_label->setText(QCoreApplication::translate("DownloadItem", "Loading", nullptr));
        folder_open_button->setText(QString());
        cancel_button->setText(QString());
        delete_button->setText(QString());
        tag_label->setText(QString());
        id_label->setText(QCoreApplication::translate("DownloadItem", "0", nullptr));
        status_label->setText(QString());
    } // retranslateUi

};

namespace Ui {
    class DownloadItem: public Ui_DownloadItem {};
} // namespace Ui

QT_END_NAMESPACE

#endif // DOWNLOADITEM_H
