import os
import sys
import shutil
import re
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *

# TODO: add instructions

VERSION = "1.1"

# Locators
gameSavePath = "{0}\Amok\Saved".format(os.getenv('LOCALAPPDATA'))
gameSaveFolder = "{0}\SaveGames".format(gameSavePath)
chPSavesPath = ".\Saves\\"

# Window 
class LoaderWindow(QWidget):

    def __init__(self, checkPoints):
        super().__init__()        
        self.setWindowIcon(QIcon("./icon.png"))
        self.setWindowTitle("Amok Runner Save Loader v{0}".format(VERSION))
        self.setMinimumWidth(500)

        layout = QVBoxLayout()

        Instructions = QLabel("Instructions: Click a Save then in-game \"Load The Last Checkpoint\"")
        layout.addWidget(Instructions)

        self.note = QLabel("")
        self.populateCheckPointButtons(layout, checkPoints)
        layout.addWidget(self.note)

        # Footer
        h_layout = QHBoxLayout()
        author = QLabel("Made by: Leption")        
        spacelabel = QLabel("")
        version = QLabel("v{0}".format(VERSION))
        h_layout.addWidget(version)
        h_layout.addWidget(spacelabel)
        h_layout.addWidget(author)
        layout.addLayout(h_layout)

        self.setLayout(layout)

    def populateCheckPointButtons(self, layout, checkPoints):
        for i in range(len(checkPoints)):
            button = QPushButton()
            button.setText("{1}".format(i + 1, checkPoints[i].name))
            layout.addWidget(button)
            button.clicked.connect(lambda checked, chP=checkPoints[i]: self.loadSave(chP))   
    
    def sendStatus(self, text):
        self.note.setText(text)
        
    def loadSave(self, checkPoint):
        # Remove Current Game Save
        if os.path.isdir(gameSaveFolder):
            shutil.rmtree(gameSaveFolder)

        # Add our save
        shutil.copytree(checkPoint.path, gameSaveFolder)
        self.sendStatus("Loaded Save: {0}".format(checkPoint.index))


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
        (See Toothy's implementation in the comments)
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
