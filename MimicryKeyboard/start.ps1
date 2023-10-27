# Define the path to the executable
$exePath = "C:\Users\%USERNAME%\MimicryKeyboard\dist\mimicry_keyboard\mimicry_keyboard.exe"

# Create a registry entry to run the executable on startup
$registryPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$registryName = "MimicryKeyboard"
$registryValue = "powershell -windowstyle hidden -command Start-Process -NoNewWindow -FilePath `'$exePath`'"

Set-ItemProperty -Path $registryPath -Name $registryName -Value $registryValue

Start-Process -WindowStyle Hidden -FilePath $exePath

Exit