# Amok Runner Save Loader

Allows you to load any of the checkpoints in the game [Amok Runner](https://store.steampowered.com/app/2077650/Amok_Runner/) using a GUI

![Screenshot](https://i.imgur.com/ZiCQFKX.jpeg)

# How to Use

1. Download Zip [Here](https://github.com/lejara/AmokRunnerSaveLoader/releases)
2. Unzip "AmokSaveLoader.zip"
3. Run "AmokSaveLoader.exe"
4. Click on a save
5. in-game "Load The Last Checkpoint"

# How does it work?

It simply replaces your save folder with the chosen save

# Known Issues
 - Missing `AmokSaveLoader.exe`
 
 On some windows defender versions and/or any antivirus. It will detect a false postive and remove the exe. Simply recover the file in your antivirus.
 If you have issues doing so, you can run the tool from the source.
 
 
# Run from source

0. Download [python](https://www.python.org/downloads/)
1. Download/Extract this repo
2. Open Command Prompt and `cd` to the extacted repo directory
2. In Command Prompt enter `pip install PyQt6-Qt6`. This is its only dependency
4. Then enter `python Script/AmokSaveLoader.py`. To run the tool

## Compile To Exe Command

This is the command i use to compile to exe. For those who like to vet this tool.

```
pyinstaller --noconfirm --onedir --windowed --icon "./Script/icon.ico" --add-data "./Saves;Saves/" "./Script/AmokSaveLoader.py"
```
