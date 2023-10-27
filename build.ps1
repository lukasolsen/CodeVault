# Author: Lukas Olsen

# Define the source script path and PyInstaller command
$mimicry_originalPython = "C:\Users\lukma\Viruses\MimicryKeyboard\mimicry_keyboard.py"
$mimicry_finishedInternal = "C:\Users\lukma\Viruses\MimicryKeyboard\dist\mimicry_keyboard\_internal"
$mimicry_finishedPython = "C:\Users\lukma\Viruses\MimicryKeyboard\dist\mimicry_keyboard\mimicry_keyboard.exe"
$pyInstallerCommand = "pyinstaller $mimicry_originalPython"
$mimicry_originalReadme = "C:\Users\lukma\Viruses\MimicryKeyboard\README.md"
$mimicry_originalStart = "C:\Users\lukma\Viruses\MimicryKeyboard\start.ps1"

# Run the pyInstallers

cd "C:\Users\lukma\Viruses\MimicryKeyboard"
Invoke-Expression -Command $pyInstallerCommand
cd "C:\Users\lukma\Viruses"

# Create a ZIP FILES
$MimicryKeyboardZIP = "C:\Users\lukma\Viruses\MimicryKeyboardRelease"

New-Item -ItemType Directory -Force -Path $MimicryKeyboardZIP
Copy-Item -Path $mimicry_finishedInternal -Destination $MimicryKeyboardZIP -Recurse
Copy-Item -Path $mimicry_finishedPython -Destination $MimicryKeyboardZIP -Recurse
Copy-Item -Path $mimicry_originalReadme -Destination $MimicryKeyboardZIP -Recurse
Copy-Item -Path $mimicry_originalStart -Destination $MimicryKeyboardZIP -Recurse

# Create a ZIP FILE
Compress-Archive -Path $MimicryKeyboardZIP -DestinationPath "C:\Users\lukma\Viruses\MimicryKeyboard.zip"

# Delete
Remove-Item -Path $MimicryKeyboardZIP -Force -Recurse
