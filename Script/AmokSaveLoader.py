import os
import sys
import shutil
import re
from PyQt6.QtGui import QIcon, QPixmap, QPalette, QColor
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *

VERSION = "1.2"

# Locators
gameSavePath = "{0}\Amok\Saved".format(os.getenv('LOCALAPPDATA'))
gameSaveFolder = "{0}\SaveGames".format(gameSavePath)
chPSavesPath = ".\Saves\\"

# Window 
class BackgroundColor(QWidget):
    def __init__(self):
        super(BackgroundColor, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1D211C"))
        self.setPalette(palette)

class SaveBtn(QPushButton):
    def __init__(self):
        super(SaveBtn, self).__init__()
        self.setAutoFillBackground(True)

        self.setStyleSheet("QPushButton:hover { background-color: #6a7b6a; }" 
                            "QPushButton { background-color: #465146; color: white; outline: none; font-weight: bold;  padding-top: 10px; padding-bottom: 10px; font-size: 13px }" )

class ALabel(QLabel):
    def __init__(self, parent=None, style=None):
        QLabel.__init__(self, parent)
        if style == None:
            style = "QLabel { color: white }"
        self.setStyleSheet(style)


class SaveButtonsSrcollArea(QScrollArea):

    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setStyleSheet(
            "QScrollArea > QWidget > QWidget { background: transparent; }" 
            "QScrollArea { background: transparent; }"

            "QScrollBar:vertical { border: none; background: transparent; width: 14px; margin: 15px 0 15px 0; border-radius: 0px; }"

            "/*Handle */"
            "QScrollBar::handle:vertical {	background-color: gray ; min-height: 30px; border-radius: 7px; }"
            "QScrollBar::handle:vertical:hover{	background-color: black }"

            "/* Buttons */"
            "QScrollBar::sub-line:vertical { border: none; background-color: transparent; height: 15px;border-top-left-radius: 7px;border-top-right-radius: 7px;subcontrol-position: top;subcontrol-origin: margin;} "
            "QScrollBar::add-line:vertical { border: none; background-color: transparent; height: 15px; border-bottom-left-radius: 7px; border-bottom-right-radius: 7px; subcontrol-position: bottom; subcontrol-origin: margin; }"

            "/* Arrows */"
            "QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical { background: none; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{ background: none; }"
        )

class LoaderWindow(QMainWindow):

    def __init__(self, checkPoints):
        super().__init__()        
        self.setWindowIcon(QIcon("./icon.png"))
        self.setWindowTitle("Amok Runner Save Loader v{0}".format(VERSION))
        # self.setMinimumWidth(500)
        self.setGeometry(600, 100, 400, 550)

        # main layout
        mainLayout = QVBoxLayout()

        title = ALabel("Amok Runner Save Loader", "QLabel { color: white; font-weight: bold; font-size: 23px }")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)    
        Instructions = ALabel("Click a Save then in-game \"Load The Last Checkpoint\"")
        Instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)    
        self.status = ALabel("", "QLabel { color: #AECF67; font-weight: bold; font-size: 15px }")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)     
       
        # save buttons layout with scroll
        buttonsWidget = QWidget()
        buttonsLayout = QVBoxLayout(buttonsWidget)  
        buttonsWidget.setLayout(buttonsLayout)

        buttonsScroll = SaveButtonsSrcollArea(buttonsWidget)        
        buttonsLayout.addWidget(buttonsScroll)
        buttonsScroll.setWidgetResizable(True)
        
        buttonsScrollContent = QWidget(buttonsScroll)
        scrollLayout = QVBoxLayout(buttonsScrollContent)
        buttonsScroll.setWidget(buttonsScrollContent)

        self.populateCheckPointButtons(scrollLayout, checkPoints)

        # Footer
        footerLayout = QHBoxLayout()
        author = ALabel("Made by: Leption")
        author.setAlignment(Qt.AlignmentFlag.AlignRight)        
        spacelabel = ALabel("")
        version = ALabel("v{0}".format(VERSION))
        footerLayout.addWidget(version)
        footerLayout.addWidget(spacelabel)
        footerLayout.addWidget(author)


        # Add all widget to mainLayout
        mainLayout.addWidget(title)
        mainLayout.addWidget(Instructions)
        mainLayout.addWidget(self.status)
        mainLayout.addWidget(buttonsWidget)
        mainLayout.addLayout(footerLayout)


        # init
        background = BackgroundColor()
        background.setLayout(mainLayout)
        self.setCentralWidget(background)

    def populateCheckPointButtons(self, layout, checkPoints):
        for i in range(len(checkPoints)):
            button = SaveBtn()
            button.setText("{1}".format(i + 1, checkPoints[i].name))
            button.clicked.connect(lambda checked, chP=checkPoints[i]: self.loadSave(chP))   
            layout.addWidget(button)
    
    def sendStatus(self, text):
        self.status.setText(text)
        
    def loadSave(self, checkPoint):
        # Remove Current Game Save
        if os.path.isdir(gameSaveFolder):
            shutil.rmtree(gameSaveFolder)

        # Add our save
        shutil.copytree(checkPoint.path, gameSaveFolder)
        self.sendStatus("Loaded: {0}".format(checkPoint.name))


if __name__ == "__main__":
    # Get Save Folder Names
    checkPointFolderNames = []
    for chFolder in os.listdir(chPSavesPath):
        checkPointFolderNames.append(chFolder)

    # Sort Save Folder Names
    def atoi(text):
        return int(text) if text.isdigit() else text

    def natural_keys(text):
        '''
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        '''
        return [ atoi(c) for c in re.split(r'(\d+)', text) ]

    checkPointFolderNames.sort(key=natural_keys)

    # Setup Check Point Metadata
    class CheckPointSave(object):
        path=None
        name=None
        index=None

    checkPoints = []
    for index in range(len(checkPointFolderNames)):
        newCheckPoint = CheckPointSave()
        newCheckPoint.path = "{0}{1}\\SaveGames".format(chPSavesPath, checkPointFolderNames[index])
        newCheckPoint.name = checkPointFolderNames[index]
        newCheckPoint.index = index + 1
        checkPoints.append(newCheckPoint)


    app = QApplication(sys.argv)
    window = LoaderWindow(checkPoints)
    window.show()
    app.exec()
