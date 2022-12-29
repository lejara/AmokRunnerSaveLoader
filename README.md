# Amok Runner Save Loader
Allows you to load any of the checkpoints in the game [Amok Runner](https://store.steampowered.com/app/2077650/Amok_Runner/) using a GUI

# How to Use
1. Download Zip [Here](https://github.com/lejara/AmokRunnerSaveLoader/releases)
2. Unzip "AmokSaveLoader.zip"
3. Run "AmokSaveLoader.exe"
4. Click on a save
5. in-game "Load The Last Checkpoint"

# How does it work?
It simply replaces your save folder with the chosen save

## Compile To Exe Command
This is the command i use to compile to exe. For those who like to vet this tool.
```
pyinstaller --noconfirm --onedir --windowed --icon "./Scirpt/icon.ico" --add-data "./Saves;Saves/" "./Scirpt/AmokSaveLoader.py"
```
