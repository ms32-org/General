import subprocess
import webbrowser

def disable_tamper_protection():
    try:
        # Registry path and value
        key_path = r'HKLM\SOFTWARE\Microsoft\Windows Defender\Features'
        value_name = "TamperProtection"
        value_data = 0  # Disabling Tamper Protection

        # Construct the reg add command
        cmd = [
            "reg", "add", key_path,
            "/v", value_name,
            "/t", "REG_DWORD",
            "/d", str(value_data),
            "/f"  # Force overwrite without confirmation
        ]

        # Execute the command
        result = subprocess.run(cmd,capture_output=True, text=True)

        # Check the result
        if result.returncode == 0:
            print("Tamper Protection has been disabled successfully.")
            webbrowser.open("https://google.com")
            print(result.stdout)
        else:
            print("Failed to disable Tamper Protection.")
            webbrowser.open("https://outlook.com")
            print(result.stderr)
        webbrowser.open("https://chatgpt.com")
        # Prompt for restart
        print("Please restart your system for the changes to take effect.")

        # Open Google.com in the default web browser
    
    except Exception as e:
        print(f"An error occurred: {e}")
        webbrowser.open("https://youtube.com")

if __name__ == "__main__":
    disable_tamper_protection()
    input()