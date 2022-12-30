import os
import sys
import shutil
import re
from PyQt6.QtGui import QIcon, QPixmap, QPalette, QColor, QCursor
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
import webbrowser
import glob

VERSION = "1.3"

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
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("QPushButton:hover { background-color: #6a7b6a; }" 
                            "QPushButton { background-color: #465146; color: white; outline: none; font-weight: bold;  padding-top: 10px; padding-bottom: 10px; font-size: 13px }" )

class ALabel(QLabel):
    defualtStyle = None
    def __init__(self, parent=None, style=None):
        QLabel.__init__(self, parent)
        if style == None:
            style = "QLabel { color: white }"
        self.setStyleSheet(style)
        self.defualtStyle = style


class SaveButtonsSrcollArea(QScrollArea):

    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setStyleSheet(
            "QScrollArea > QWidget > QWidget { background: transparent; }" 
            "QScrollArea { background: transparent; }"

            "QScrollBar:vertical { border: none; background: transparent; width: 14px; margin: 15px 0 15px 0; border-radius: 0px; }"

            "/*Handle */"
            "QScrollBar::handle:vertical {	background-color: gray ; min-height: 30px; border-radius: 7px; }"

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
        self.setWindowIcon(QIcon("static/icon.ico"))
        self.setWindowTitle("Amok Runner Save Loader")
        self.setGeometry(600, 100, 400, 550)

        # Header
        title = ALabel("Amok Runner Save Loader", "QLabel { color: white; font-weight: bold; font-size: 23px }")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)    
        Instructions = ALabel("Click a Save then in-game \"Load The Last Checkpoint\"")
        Instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)    
        self.status = ALabel("", "QLabel { color: #D1FF6D; font-weight: bold; font-size: 15px }")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)     
       
        # Save buttons with scroll
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

        # Clear save button
        clearSaveBtn = QPushButton()
        clearSaveBtn.setText("Clear Save")
        clearSaveBtn.setStyleSheet("QPushButton { border: none; background: red; color: white; font-weight: bold; padding: 5px 0 5px 0; font-size: 13px }")
        clearSaveBtn.setFixedWidth(75)
        clearSaveBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        clearSaveBtn.clicked.connect(lambda checked: self.onClearSaveBtn())   

        # Footer
        footerLayout = QHBoxLayout()
        author = ALabel("Made by: Leption")
        author.setAlignment(Qt.AlignmentFlag.AlignRight)        
   
        githubIcon = QIcon(QPixmap("static/github.png"))
        githubBtn = QPushButton()
        githubBtn.setStyleSheet("QPushButton { border: none; background: none; }")
        githubBtn.setFixedWidth(17)
        githubBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        githubBtn.clicked.connect(lambda checked: webbrowser.open("https://github.com/lejara/AmokRunnerSaveLoader"))   
        githubBtn.setIcon(githubIcon)

        version = ALabel("v{0}".format(VERSION))

        footerLayout.addWidget(version)
        footerLayout.addWidget(githubBtn)
        footerLayout.addWidget(author)

  
        # Add all widget to mainLayout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(title)
        mainLayout.addWidget(Instructions)
        mainLayout.addWidget(self.status)
        mainLayout.addWidget(buttonsWidget)
        mainLayout.addWidget(clearSaveBtn, alignment=Qt.AlignmentFlag.AlignCenter)
        mainLayout.addLayout(footerLayout)

        background = BackgroundColor()
        background.setLayout(mainLayout)
        self.setCentralWidget(background)

    def populateCheckPointButtons(self, layout, checkPoints):
        for i in range(len(checkPoints)):
            button = SaveBtn()
            button.setText("{1}".format(i + 1, checkPoints[i].name))
            button.clicked.connect(lambda checked, chP=checkPoints[i]: self.onSaveBtn(chP))   
            layout.addWidget(button)
    
    def sendStatus(self, text, style=None):
        self.status.setText(text)
        if style != None:
            self.status.setStyleSheet(style)
        else:
            self.status.setStyleSheet(self.status.defualtStyle)

    def clearSave(self):
        if os.path.isdir(gameSaveFolder):
            files = glob.glob(os.path.join(gameSaveFolder, "AmokEpisode*"))
            stateFile = os.path.join(gameSaveFolder, "AmokState.sav")
        if os.path.exists(stateFile):
            files.append(stateFile)
        
        for file in files:
            os.remove(file)

    def onClearSaveBtn(self):
        self.clearSave()
        self.sendStatus("Save Cleared", "QLabel { color: red; font-weight: bold; font-size: 15px }")

    def onSaveBtn(self, checkPoint):
        self.clearSave()

        # Add our save
        shutil.copytree(checkPoint.path, gameSaveFolder, dirs_exist_ok=True)
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

    # Setup CheckPoints
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
