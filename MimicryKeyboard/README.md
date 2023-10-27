# 😄 Mimicry Keyboard 😄

## Description

Welcome to the "Mimicry Keyboard" prank script! This script is designed to add a whimsical twist to your friends' typing experience by doubling each keystroke. 🎉 Imagine the hilarity as 'W' becomes 'WW,' and the laughter multiplies with each keypress. 😅

**Name:** Mimicry Keyboard
**Version:** 1.0

## How It Works

"Mimicry Keyboard" operates by intercepting keyboard input using system hooks. Every time a key is pressed, it swiftly captures the input and doubles the character as it makes its way to the application or text field. The doubling effect multiplies with each successive keypress, creating a comical and sometimes maddening typing experience. 🤣

## Prerequisites

Before you can start pranking, ensure that you have the following prerequisites:

- This prank script is written in Python.
- You'll need Python 3.x installed on your system.

## Setup and Usage

To set up and run the "Mimicry Keyboard" prank script, follow these detailed steps:

1. Install `pyinstaller` from pip if you haven't already. This tool is essential for converting the script into an executable file. 📦

```bash
pip install pyinstaller
```

2. Type the following command to convert the script to an executable file. This will create a `dist` folder with the executable file inside. 📦

```bash
pyinstaller --onefile mimicry_keyboard.py
```

3. Open the `start.ps1` script, and make sure to change the line `$exePath = "C:\Users\%USERNAME%\MimicryKeyboard\dist\main\mimicry_keyboard.exe"` to the path of the executable file you created. 📝 (_NOTE_: %USERNAME% retrieves the current username of your computer, so there's no need to change it unless necessary.)

4. Run the **start.ps1** script with caution. **NOTICE**: This prank script may disrupt normal computer use and could be quite frustrating for some users. It is advisable to run this script on a virtual machine or a computer you don't mind causing temporary mischief on. The script runs discreetly in the background, remaining invisible to the user. 👻. Do also remember that this script does run on startup.

5. To stop the prank, go to Task Manager, and look for the process named "mimicry_keyboard.exe." 🛑 If you can't find it in the Processes tab, check the Details tab, where you'll be able to locate and terminate the process. Then for the removing startup go into `HKCU:\Software\Microsoft\Windows\CurrentVersion\Run` in Regedit and delete the `MimicryKeyboard` key.

## Legal Responsibility

By running the "Mimicry Keyboard" prank script, you accept full responsibility for your actions. The author of these scripts and this repository cannot be held liable for any consequences that may arise from the use of these scripts. Remember, the goal is to create laughter, not fright. Enjoy "The Joy of Prankreation" responsibly and spread joy! 😁
