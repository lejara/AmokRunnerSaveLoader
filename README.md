# AmokRunnerSaveLoader
Allows you to load checkpoint saves using a GUI

# How to Use
1. Unzip "AmokSaveLoader.zip"
2. Run "AmokSaveLoader.exe"
3. Click on a save
4. in-game "Load The Last Checkpoint"

# How does it work?
It simply replaces your save folder with the chosen save

## Compile To Exe Command
This is the command i use to compile to exe. For those who like to vet this tool.
```
pyinstaller --noconfirm --onedir --windowed --icon "./Scirpt/icon.ico" --add-data "./Saves;Saves/" "./Scirpt/AmokSaveLoader.py"
```
