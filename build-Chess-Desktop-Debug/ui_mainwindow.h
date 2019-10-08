/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.9.5
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTabWidget>
#include <QtWidgets/QToolButton>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QAction *actionNew_Tab;
    QAction *actionLoad;
    QAction *actionSave;
    QAction *actionClose_Tab;
    QAction *actionAbout;
    QAction *actionExit;
    QWidget *centralWidget;
    QTabWidget *tabWidget;
    QWidget *formLayoutWidget;
    QFormLayout *formLayout_3;
    QToolButton *playButton;
    QToolButton *stopButton;
    QToolButton *restartButton;
    QToolButton *forwardButton;
    QToolButton *backwardButton;
    QToolButton *addButton;
    QMenuBar *menuBar;
    QMenu *menuFile;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(1000, 750);
        MainWindow->setMinimumSize(QSize(1000, 750));
        MainWindow->setMaximumSize(QSize(1000, 750));
        QIcon icon;
        icon.addFile(QStringLiteral("assets/king.png"), QSize(), QIcon::Normal, QIcon::Off);
        MainWindow->setWindowIcon(icon);
        MainWindow->setDocumentMode(false);
        MainWindow->setDockNestingEnabled(false);
        actionNew_Tab = new QAction(MainWindow);
        actionNew_Tab->setObjectName(QStringLiteral("actionNew_Tab"));
        actionLoad = new QAction(MainWindow);
        actionLoad->setObjectName(QStringLiteral("actionLoad"));
        actionSave = new QAction(MainWindow);
        actionSave->setObjectName(QStringLiteral("actionSave"));
        actionClose_Tab = new QAction(MainWindow);
        actionClose_Tab->setObjectName(QStringLiteral("actionClose_Tab"));
        actionAbout = new QAction(MainWindow);
        actionAbout->setObjectName(QStringLiteral("actionAbout"));
        actionExit = new QAction(MainWindow);
        actionExit->setObjectName(QStringLiteral("actionExit"));
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        tabWidget = new QTabWidget(centralWidget);
        tabWidget->setObjectName(QStringLiteral("tabWidget"));
        tabWidget->setGeometry(QRect(40, 0, 950, 710));
        tabWidget->setAutoFillBackground(false);
        tabWidget->setTabPosition(QTabWidget::North);
        tabWidget->setTabShape(QTabWidget::Rounded);
        tabWidget->setDocumentMode(false);
        tabWidget->setTabsClosable(false);
        tabWidget->setMovable(true);
        formLayoutWidget = new QWidget(centralWidget);
        formLayoutWidget->setObjectName(QStringLiteral("formLayoutWidget"));
        formLayoutWidget->setGeometry(QRect(10, 50, 32, 551));
        formLayout_3 = new QFormLayout(formLayoutWidget);
        formLayout_3->setSpacing(6);
        formLayout_3->setContentsMargins(11, 11, 11, 11);
        formLayout_3->setObjectName(QStringLiteral("formLayout_3"));
        formLayout_3->setContentsMargins(0, 0, 0, 0);
        playButton = new QToolButton(formLayoutWidget);
        playButton->setObjectName(QStringLiteral("playButton"));
        playButton->setEnabled(true);
        playButton->setMaximumSize(QSize(80, 16777215));
        QIcon icon1;
        icon1.addFile(QStringLiteral("assets/icons8-play-24.png"), QSize(), QIcon::Normal, QIcon::Off);
        playButton->setIcon(icon1);

        formLayout_3->setWidget(1, QFormLayout::LabelRole, playButton);

        stopButton = new QToolButton(formLayoutWidget);
        stopButton->setObjectName(QStringLiteral("stopButton"));
        stopButton->setMaximumSize(QSize(80, 16777215));
        QIcon icon2;
        icon2.addFile(QStringLiteral("assets/icons8-stop-24.png"), QSize(), QIcon::Normal, QIcon::Off);
        stopButton->setIcon(icon2);

        formLayout_3->setWidget(2, QFormLayout::LabelRole, stopButton);

        restartButton = new QToolButton(formLayoutWidget);
        restartButton->setObjectName(QStringLiteral("restartButton"));
        restartButton->setMaximumSize(QSize(80, 16777215));
        QIcon icon3;
        icon3.addFile(QStringLiteral("assets/icons8-restart-24.png"), QSize(), QIcon::Normal, QIcon::Off);
        restartButton->setIcon(icon3);

        formLayout_3->setWidget(3, QFormLayout::LabelRole, restartButton);

        forwardButton = new QToolButton(formLayoutWidget);
        forwardButton->setObjectName(QStringLiteral("forwardButton"));
        forwardButton->setMaximumSize(QSize(80, 16777215));
        QIcon icon4;
        icon4.addFile(QStringLiteral("assets/icons8-fast-forward-24.png"), QSize(), QIcon::Normal, QIcon::Off);
        forwardButton->setIcon(icon4);

        formLayout_3->setWidget(5, QFormLayout::LabelRole, forwardButton);

        backwardButton = new QToolButton(formLayoutWidget);
        backwardButton->setObjectName(QStringLiteral("backwardButton"));
        backwardButton->setMaximumSize(QSize(80, 16777215));
        QIcon icon5;
        icon5.addFile(QStringLiteral("assets/icons8-rewind-24.png"), QSize(), QIcon::Normal, QIcon::Off);
        backwardButton->setIcon(icon5);

        formLayout_3->setWidget(6, QFormLayout::LabelRole, backwardButton);

        addButton = new QToolButton(centralWidget);
        addButton->setObjectName(QStringLiteral("addButton"));
        addButton->setGeometry(QRect(10, 10, 31, 31));
        QIcon icon6;
        icon6.addFile(QStringLiteral("assets/icons8-plus-math-24.png"), QSize(), QIcon::Normal, QIcon::Off);
        addButton->setIcon(icon6);
        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 1000, 22));
        menuFile = new QMenu(menuBar);
        menuFile->setObjectName(QStringLiteral("menuFile"));
        MainWindow->setMenuBar(menuBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        MainWindow->setStatusBar(statusBar);

        menuBar->addAction(menuFile->menuAction());
        menuFile->addAction(actionLoad);
        menuFile->addAction(actionSave);
        menuFile->addSeparator();
        menuFile->addAction(actionNew_Tab);
        menuFile->addAction(actionClose_Tab);
        menuFile->addSeparator();
        menuFile->addAction(actionAbout);
        menuFile->addAction(actionExit);

        retranslateUi(MainWindow);

        tabWidget->setCurrentIndex(-1);


        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "Chess", Q_NULLPTR));
        actionNew_Tab->setText(QApplication::translate("MainWindow", "New Tab", Q_NULLPTR));
#ifndef QT_NO_SHORTCUT
        actionNew_Tab->setShortcut(QApplication::translate("MainWindow", "Ctrl+N", Q_NULLPTR));
#endif // QT_NO_SHORTCUT
        actionLoad->setText(QApplication::translate("MainWindow", "Load..", Q_NULLPTR));
        actionSave->setText(QApplication::translate("MainWindow", "Save..", Q_NULLPTR));
#ifndef QT_NO_SHORTCUT
        actionSave->setShortcut(QApplication::translate("MainWindow", "Ctrl+S", Q_NULLPTR));
#endif // QT_NO_SHORTCUT
        actionClose_Tab->setText(QApplication::translate("MainWindow", "Close Tab", Q_NULLPTR));
#ifndef QT_NO_SHORTCUT
        actionClose_Tab->setShortcut(QApplication::translate("MainWindow", "Del", Q_NULLPTR));
#endif // QT_NO_SHORTCUT
        actionAbout->setText(QApplication::translate("MainWindow", "About..", Q_NULLPTR));
#ifndef QT_NO_SHORTCUT
        actionAbout->setShortcut(QApplication::translate("MainWindow", "F1", Q_NULLPTR));
#endif // QT_NO_SHORTCUT
        actionExit->setText(QApplication::translate("MainWindow", "Exit", Q_NULLPTR));
#ifndef QT_NO_SHORTCUT
        actionExit->setShortcut(QApplication::translate("MainWindow", "Ctrl+Esc", Q_NULLPTR));
#endif // QT_NO_SHORTCUT
        playButton->setText(QApplication::translate("MainWindow", "Auto", Q_NULLPTR));
#ifndef QT_NO_SHORTCUT
        playButton->setShortcut(QApplication::translate("MainWindow", "F5", Q_NULLPTR));
#endif // QT_NO_SHORTCUT
        stopButton->setText(QApplication::translate("MainWindow", "Stop", Q_NULLPTR));
#ifndef QT_NO_SHORTCUT
        stopButton->setShortcut(QApplication::translate("MainWindow", "F4", Q_NULLPTR));
#endif // QT_NO_SHORTCUT
        restartButton->setText(QApplication::translate("MainWindow", "Restart", Q_NULLPTR));
#ifndef QT_NO_SHORTCUT
        restartButton->setShortcut(QApplication::translate("MainWindow", "F6", Q_NULLPTR));
#endif // QT_NO_SHORTCUT
        forwardButton->setText(QApplication::translate("MainWindow", "Forward", Q_NULLPTR));
#ifndef QT_NO_SHORTCUT
        forwardButton->setShortcut(QApplication::translate("MainWindow", "F10", Q_NULLPTR));
#endif // QT_NO_SHORTCUT
        backwardButton->setText(QApplication::translate("MainWindow", "Backward", Q_NULLPTR));
        addButton->setText(QApplication::translate("MainWindow", "+", Q_NULLPTR));
#ifndef QT_NO_SHORTCUT
        addButton->setShortcut(QApplication::translate("MainWindow", "Ctrl+N", Q_NULLPTR));
#endif // QT_NO_SHORTCUT
        menuFile->setTitle(QApplication::translate("MainWindow", "File", Q_NULLPTR));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
