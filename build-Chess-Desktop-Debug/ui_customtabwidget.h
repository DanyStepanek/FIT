/********************************************************************************
** Form generated from reading UI file 'customtabwidget.ui'
**
** Created by: Qt User Interface Compiler version 5.9.5
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_CUSTOMTABWIDGET_H
#define UI_CUSTOMTABWIDGET_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QGraphicsView>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_CustomTabWidget
{
public:
    QWidget *gridLayoutWidget_2;
    QGridLayout *gridLayout_2;
    QListWidget *moveslistWidget;
    QWidget *gridLayoutWidget;
    QGridLayout *gridLayout;
    QGraphicsView *chessboardView;

    void setupUi(QWidget *CustomTabWidget)
    {
        if (CustomTabWidget->objectName().isEmpty())
            CustomTabWidget->setObjectName(QStringLiteral("CustomTabWidget"));
        CustomTabWidget->resize(953, 620);
        gridLayoutWidget_2 = new QWidget(CustomTabWidget);
        gridLayoutWidget_2->setObjectName(QStringLiteral("gridLayoutWidget_2"));
        gridLayoutWidget_2->setGeometry(QRect(670, 10, 261, 600));
        gridLayout_2 = new QGridLayout(gridLayoutWidget_2);
        gridLayout_2->setObjectName(QStringLiteral("gridLayout_2"));
        gridLayout_2->setContentsMargins(0, 0, 0, 0);
        moveslistWidget = new QListWidget(gridLayoutWidget_2);
        moveslistWidget->setObjectName(QStringLiteral("moveslistWidget"));

        gridLayout_2->addWidget(moveslistWidget, 0, 0, 1, 1);

        gridLayoutWidget = new QWidget(CustomTabWidget);
        gridLayoutWidget->setObjectName(QStringLiteral("gridLayoutWidget"));
        gridLayoutWidget->setGeometry(QRect(10, 10, 600, 600));
        gridLayout = new QGridLayout(gridLayoutWidget);
        gridLayout->setObjectName(QStringLiteral("gridLayout"));
        gridLayout->setContentsMargins(0, 0, 0, 0);
        chessboardView = new QGraphicsView(gridLayoutWidget);
        chessboardView->setObjectName(QStringLiteral("chessboardView"));

        gridLayout->addWidget(chessboardView, 0, 0, 1, 1);


        retranslateUi(CustomTabWidget);

        QMetaObject::connectSlotsByName(CustomTabWidget);
    } // setupUi

    void retranslateUi(QWidget *CustomTabWidget)
    {
        CustomTabWidget->setWindowTitle(QApplication::translate("CustomTabWidget", "Form", Q_NULLPTR));
    } // retranslateUi

};

namespace Ui {
    class CustomTabWidget: public Ui_CustomTabWidget {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_CUSTOMTABWIDGET_H
