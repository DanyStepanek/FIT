/********************************************************************************
** Form generated from reading UI file 'loaddialog.ui'
**
** Created by: Qt User Interface Compiler version 5.9.5
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_LOADDIALOG_H
#define UI_LOADDIALOG_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QDialog>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QTreeView>

QT_BEGIN_NAMESPACE

class Ui_LoadDialog
{
public:
    QGridLayout *gridLayout;
    QTreeView *treeView;
    QHBoxLayout *horizontalLayout;
    QSpacerItem *horizontalSpacer;
    QPushButton *cancelButton;
    QPushButton *loadButton;

    void setupUi(QDialog *LoadDialog)
    {
        if (LoadDialog->objectName().isEmpty())
            LoadDialog->setObjectName(QStringLiteral("LoadDialog"));
        LoadDialog->resize(380, 500);
        gridLayout = new QGridLayout(LoadDialog);
        gridLayout->setObjectName(QStringLiteral("gridLayout"));
        treeView = new QTreeView(LoadDialog);
        treeView->setObjectName(QStringLiteral("treeView"));
        treeView->setAutoFillBackground(false);

        gridLayout->addWidget(treeView, 0, 0, 1, 1);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setObjectName(QStringLiteral("horizontalLayout"));
        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer);

        cancelButton = new QPushButton(LoadDialog);
        cancelButton->setObjectName(QStringLiteral("cancelButton"));

        horizontalLayout->addWidget(cancelButton);

        loadButton = new QPushButton(LoadDialog);
        loadButton->setObjectName(QStringLiteral("loadButton"));

        horizontalLayout->addWidget(loadButton);


        gridLayout->addLayout(horizontalLayout, 1, 0, 1, 1);


        retranslateUi(LoadDialog);
        QObject::connect(cancelButton, SIGNAL(clicked()), LoadDialog, SLOT(reject()));
        QObject::connect(loadButton, SIGNAL(clicked()), LoadDialog, SLOT(accept()));

        QMetaObject::connectSlotsByName(LoadDialog);
    } // setupUi

    void retranslateUi(QDialog *LoadDialog)
    {
        LoadDialog->setWindowTitle(QApplication::translate("LoadDialog", "File Manager", Q_NULLPTR));
        cancelButton->setText(QApplication::translate("LoadDialog", "Cancel", Q_NULLPTR));
        loadButton->setText(QApplication::translate("LoadDialog", "Load", Q_NULLPTR));
    } // retranslateUi

};

namespace Ui {
    class LoadDialog: public Ui_LoadDialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_LOADDIALOG_H
