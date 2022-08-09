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

class Ui_Form
{
public:
    QHBoxLayout *horizontalLayout;
    QLabel *image_label;
    QVBoxLayout *verticalLayout;
    QHBoxLayout *horizontalLayout_2;
    QLabel *label;
    QSpacerItem *horizontalSpacer;
    QPushButton *folder_open_button;
    QPushButton *delete_button;
    QPushButton *cancel_button;
    QHBoxLayout *horizontalLayout_3;
    QProgressBar *progress_bar;
    QSpacerItem *horizontalSpacer_2;
    QLabel *status_label;

    void setupUi(QWidget *Form)
    {
        if (Form->objectName().isEmpty())
            Form->setObjectName(QString::fromUtf8("Form"));
        Form->resize(592, 70);
        horizontalLayout = new QHBoxLayout(Form);
        horizontalLayout->setSpacing(5);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        horizontalLayout->setContentsMargins(5, 5, 5, 5);
        image_label = new QLabel(Form);
        image_label->setObjectName(QString::fromUtf8("image_label"));
        image_label->setMinimumSize(QSize(60, 60));
        image_label->setMaximumSize(QSize(60, 60));
        image_label->setAutoFillBackground(true);

        horizontalLayout->addWidget(image_label);

        verticalLayout = new QVBoxLayout();
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        label = new QLabel(Form);
        label->setObjectName(QString::fromUtf8("label"));
        QFont font;
        font.setPointSize(11);
        font.setBold(true);
        label->setFont(font);

        horizontalLayout_2->addWidget(label);

        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer);

        folder_open_button = new QPushButton(Form);
        folder_open_button->setObjectName(QString::fromUtf8("folder_open_button"));
        QIcon icon;
        icon.addFile(QString::fromUtf8(":/icon/icons/folder-open.png"), QSize(), QIcon::Normal, QIcon::Off);
        folder_open_button->setIcon(icon);
        folder_open_button->setFlat(true);

        horizontalLayout_2->addWidget(folder_open_button);

        delete_button = new QPushButton(Form);
        delete_button->setObjectName(QString::fromUtf8("delete_button"));
        delete_button->setLayoutDirection(Qt::LeftToRight);
        delete_button->setAutoFillBackground(false);
        QIcon icon1;
        icon1.addFile(QString::fromUtf8(":/icon/icons/trash-delete-bin.png"), QSize(), QIcon::Normal, QIcon::Off);
        delete_button->setIcon(icon1);
        delete_button->setFlat(true);

        horizontalLayout_2->addWidget(delete_button);

        cancel_button = new QPushButton(Form);
        cancel_button->setObjectName(QString::fromUtf8("cancel_button"));
        cancel_button->setEnabled(true);
        QIcon icon2;
        icon2.addFile(QString::fromUtf8(":/icon/icons/cancel.png"), QSize(), QIcon::Normal, QIcon::Off);
        cancel_button->setIcon(icon2);
        cancel_button->setFlat(true);

        horizontalLayout_2->addWidget(cancel_button);


        verticalLayout->addLayout(horizontalLayout_2);

        horizontalLayout_3 = new QHBoxLayout();
        horizontalLayout_3->setObjectName(QString::fromUtf8("horizontalLayout_3"));
        progress_bar = new QProgressBar(Form);
        progress_bar->setObjectName(QString::fromUtf8("progress_bar"));
        QSizePolicy sizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(progress_bar->sizePolicy().hasHeightForWidth());
        progress_bar->setSizePolicy(sizePolicy);
        progress_bar->setMaximumSize(QSize(150, 15));
        progress_bar->setValue(24);

        horizontalLayout_3->addWidget(progress_bar);

        horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_3->addItem(horizontalSpacer_2);

        status_label = new QLabel(Form);
        status_label->setObjectName(QString::fromUtf8("status_label"));

        horizontalLayout_3->addWidget(status_label);


        verticalLayout->addLayout(horizontalLayout_3);


        horizontalLayout->addLayout(verticalLayout);

        horizontalLayout->setStretch(1, 1);

        retranslateUi(Form);

        QMetaObject::connectSlotsByName(Form);
    } // setupUi

    void retranslateUi(QWidget *Form)
    {
        Form->setWindowTitle(QCoreApplication::translate("Form", "Form", nullptr));
        image_label->setText(QString());
        label->setText(QCoreApplication::translate("Form", "TextLabel", nullptr));
        folder_open_button->setText(QString());
        delete_button->setText(QString());
        cancel_button->setText(QString());
        status_label->setText(QCoreApplication::translate("Form", "TextLabel", nullptr));
    } // retranslateUi

};

namespace Ui {
    class Form: public Ui_Form {};
} // namespace Ui

QT_END_NAMESPACE

#endif // DOWNLOADITEM_H
