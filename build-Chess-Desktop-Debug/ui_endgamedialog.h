/********************************************************************************
** Form generated from reading UI file 'endgamedialog.ui'
**
** Created by: Qt User Interface Compiler version 5.9.5
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_ENDGAMEDIALOG_H
#define UI_ENDGAMEDIALOG_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QDialog>
#include <QtWidgets/QHeaderView>

QT_BEGIN_NAMESPACE

class Ui_EndGameDialog
{
public:

    void setupUi(QDialog *EndGameDialog)
    {
        if (EndGameDialog->objectName().isEmpty())
            EndGameDialog->setObjectName(QStringLiteral("EndGameDialog"));
        EndGameDialog->resize(404, 484);

        retranslateUi(EndGameDialog);

        QMetaObject::connectSlotsByName(EndGameDialog);
    } // setupUi

    void retranslateUi(QDialog *EndGameDialog)
    {
        EndGameDialog->setWindowTitle(QApplication::translate("EndGameDialog", "Dialog", Q_NULLPTR));
    } // retranslateUi

};

namespace Ui {
    class EndGameDialog: public Ui_EndGameDialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_ENDGAMEDIALOG_H
