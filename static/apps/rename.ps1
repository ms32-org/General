param(
    [string]$NewName = "MS32",
    [string]$Folder = "C:\Temp"
)

# Find currently connected Wi-Fi profile
$wlanInfo = netsh wlan show interfaces
$ssid = ($wlanInfo | Select-String "SSID" | Select-Object -First 1).ToString().Split(":")[1].Trim()

if (-not $ssid) {
    Write-Error "No Wi-Fi currently connected."
    exit
}

Write-Host "Currently connected Wi-Fi: $ssid"

# Create folder if not exists
if (!(Test-Path $Folder)) {
    New-Item -ItemType Directory -Path $Folder | Out-Null
}

# Export profile with password
Write-Host "Exporting profile '$ssid' with password..."
netsh wlan export profile name="$ssid" folder="$Folder" key=clear | Out-Null

# Locate exported XML
$xmlFile = Get-ChildItem -Path $Folder -Filter "Wi-Fi-$ssid.xml" | Select-Object -First 1
if (-not $xmlFile) {
    Write-Error "Could not find exported XML for '$ssid'"
    exit
}

# Rename inside XML
Write-Host "Renaming profile to '$NewName'..."
(Get-Content $xmlFile.FullName) -replace "<name>$ssid</name>", "<name>$NewName</name>" |
    Set-Content "$Folder\Wi-Fi-$NewName.xml"

# Import new profile with password intact
Write-Host "Adding new profile '$NewName'..."
netsh wlan add profile filename="$Folder\Wi-Fi-$NewName.xml" user=current | Out-Null

# Delete old profile
Write-Host "Deleting old profile '$ssid'..."
netsh wlan delete profile name="$ssid" | Out-Null

# Reconnect to new profile
Write-Host "Reconnecting to '$NewName'..."
netsh wlan connect name="$NewName" | Out-Null

Write-Host "✅ Done! Your current Wi-Fi has been renamed to '$NewName' and you are reconnected."
