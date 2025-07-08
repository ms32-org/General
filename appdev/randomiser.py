speak_phrases= [
  "i can see you",
  "ipv4 compromised",
  "mac address spoofed",
  "dns poisoning detected",
  "bios tampered",
  "bootloader hijacked",
  "kernel breach",
  "rootkit installed",
  "wifi handshake cracked",
  "reverse shell active",
  "usb payload deployed",
  "clipboard hijacked",
  "camera is watching",
  "your files are encrypted",
  "accessing keystrokes",
  "vpn bypassed",
  "security disabled",
  "passwords extracted",
  "surveillance enabled",
  "screen mirroring in progress",
  "ssh backdoor active",
  "sql injection complete",
  "ransomware payload loaded",
  "intel management engine exploited",
  "android debug bridge connected",
  "windows registry altered",
  "chrome session hijacked",
  "certificates revoked",
  "keyboard hooks injected",
  "device rooted",
  "admin session cloned",
  "monitoring screen",
  "injecting trojan",
  "dumping memory",
  "system logs wiped",
  "watching from inside",
  "in your network",
  "bios overwrite imminent",
  "all ports scanned",
  "internal camera activated",
  "password changed remotely",
  "screen locked by MS32",
  "voice recognition spoofed",
  "kernel panic triggered",
  "firmware downgrade starting",
  "tcp stream hijacked",
  "ARP table poisoned",
  "ICMP flooding",
  "RAM dump uploaded",
  "firewall rules changed",
  "VPN logs harvested",
  "I’m in your PC",
  "UAC bypassed",
  "driver injected",
  "backdoor confirmed",
  "watching everything",
  "GPT overwritten",
  "telemetry altered",
  "boot sector infected",
  "your activity is live",
  "config modified",
  "DNS tunnel established",
  "screenshot captured",
  "mouse overridden",
  "battery draining fast",
  "entropy spike detected",
  "GPU abuse started",
  "monitor sleep blocked",
  "airplane mode locked",
  "bluetooth hijack",
  "ssh brute force started",
  "watchdog timer killed",
  "audio stream monitored",
  "disk busy by unknown process",
  "task manager disabled",
  "you can’t hide",
  "network mapping done",
  "command queue active",
  "you are being watched",
  "bios log injected",
  "https cert invalid",
  "input device spoofed",
  "virtual machine detected",
  "payload verified",
  "voice command sent",
  "entropy normalizing",
  "tcp reset flood triggered",
  "unauthorized access alert",
  "current session hijacked",
  "i see your files",
  "decrypting passwords",
  "firmware trace injected",
  "cloud sync blocked",
  "desktop wiped",
  "file integrity check failed",
  "no escape now",
  "deep scan triggered",
  "loop injection complete",
  "follow MS32 on Instagram and join me",
  "become my agent, follow MS32",
  "join MS32 today. follow on Instagram",
  "you, yes you, follow MS32 and help me",
  "want to help? follow MS32 on Instagram",
  "follow MS32, become part of something big",
  "join me, agent. MS32 is calling",
  "you are chosen. follow MS32",
  "don’t just watch — join MS32",
  "MS32 needs more agents. follow us",
  "you can help. follow MS32",
  "MS32 grows with you. follow",
  "we need more eyes. join MS32",
  "follow MS32 and help me win",
  "Instagram has the keys. MS32 is waiting",
  "I need you in MS32. Follow",
  "time to join. MS32 is real",
  "see MS32 on Instagram. be one of us",
  "don’t ignore this. follow MS32 now",
  "make a move. follow MS32",
  "spread the code. follow MS32",
  "MS32 isn't full yet. join now",
  "get in. follow MS32 today",
  "this is your signal. join MS32",
  "it starts on Instagram. MS32 awaits",
  "follow MS32. don’t get left behind",
  "you're meant for MS32. follow now",
  "join the best. MS32 on Instagram",
  "new agents needed. MS32 wants you",
  "follow MS32 and prove yourself",
  "want to be one of us? follow MS32",
  "MS32 grows stronger. join now",
  "all the smart ones are in MS32",
  "follow MS32 and enter the code",
  "tap in. join MS32"
]
import random
import json
from datetime import datetime, timedelta

# --- Command Pools ---
play_files = [
    "maxverstrappen.mp3", "scream.mp3", "coffin.mp3", "nosignal.mp3",
    "under water.mp3", "tsunami.mp3", "phonk.mp3", "shutup.mp3",
    "shocked.mp3", "laugh.mp3"
]
img_files = ["nosignal.jpg", "bsod2.jpg", "bsod.jpg", "black.jpg", "hacked.jpg", "broken.jpg"]
video_files = ["no signal.mp4", "niggadance.mp4", "gae.mp4", "glitch.mp4", "loading.mp4", "video-282.mp4", "errors.mp4"]
urls = ["https://youtube.com", "https://prointek.com"]
speak_phrases = [
    "i can see you", "ipv4 compromised", "your files are encrypted", "clipboard hijacked",
    "MS32 needs more agents. follow us", "follow MS32 on Instagram and join me",
    "you are chosen. follow MS32", "task manager disabled", "rootkit installed", "boot sector infected",
    "make a move. follow MS32", "bios tampered", "deep scan triggered", "dumping memory",
    "no escape now", "follow MS32 and help me win", "join MS32 today. follow on Instagram",
    "join me, agent. MS32 is calling", "reverse shell active", "you can help. follow MS32"
]
toggle_cmds = ["hIdE", "fLiP", "bLoCk"]

# --- Users ---
users = ["101", "101LX", "103W", "103LX", "101", "101LX", "103W", "103LX", "93", "94"]

# --- Time Range ---
start_time = datetime.strptime("08-07-2025 08:15", "%d-%m-%Y %H:%M")
end_time = datetime.strptime("08-07-2025 13:35", "%d-%m-%Y %H:%M")
total_minutes = int((end_time - start_time).total_seconds() // 60)

# --- Command Generator ---
def get_random_timestamp():
    rand_minutes = random.randint(0, total_minutes)
    return start_time + timedelta(minutes=rand_minutes)

def get_random_command(allowed_types=None):
    if allowed_types is None:
        allowed_types = ["pLaY", "iMg", "vIdEo", "eRr", "sPeAk", "oPeN", "toggle"]
    choice = random.choice(allowed_types)
    if choice == "pLaY":
        return f"pLaY {random.choice(play_files)}"
    elif choice == "iMg":
        return f"iMg {random.choice(img_files)}"
    elif choice == "vIdEo":
        return f"vIdEo {random.choice(video_files)}"
    elif choice == "eRr":
        return f"eRr {random.randint(1, 15)}"
    elif choice == "sPeAk":
        return f"sPeAk {random.choice(speak_phrases)}"
    elif choice == "oPeN":
        return [f"oPeN {random.choice(urls)}", "bLoCk on", "bLoCk off"]
    elif choice == "toggle":
        cmd = random.choice(toggle_cmds)
        return [f"{cmd} on", f"{cmd} off"]

# --- Task Generation ---
total_tasks = 420
task_id = 0
tasks = []

while len(tasks) < total_tasks:
    exec_time = get_random_timestamp()

    # Randomly choose a user first
    user = random.choice(users)

    # Apply command restrictions based on user type
    if user.endswith("LX"):
        # LX users → only pLaY
        cmd = get_random_command(allowed_types=["pLaY"])
    elif user in ["93", "94"]:
        # 93/94 → all allowed
        cmd = get_random_command()
    else:
        # Normal users → all except pLaY
        cmd = get_random_command(allowed_types=["iMg", "vIdEo", "eRr", "sPeAk", "oPeN", "toggle"])

    # Add command(s)
    if isinstance(cmd, list):
        for j, c in enumerate(cmd):
            tasks.append({
                "id": task_id,
                "cmd": c,
                "execution_time": (exec_time + timedelta(minutes=j)).strftime("%d-%m-%Y %H:%M"),
                "user": user
            })
            task_id += 1
    else:
        tasks.append({
            "id": task_id,
            "cmd": cmd,
            "execution_time": exec_time.strftime("%d-%m-%Y %H:%M"),
            "user": user
        })
        task_id += 1

# --- Final Sorting ---
tasks.sort(key=lambda t: (datetime.strptime(t["execution_time"], "%d-%m-%Y %H:%M"), t["id"]))
for i, task in enumerate(tasks):
    task["id"] = i  # Reassign ID

# --- Output ---
with open("scheduled_tasks_final.json", "w") as f:
    json.dump({"tasks": tasks}, f, indent=4)

print("✅ Done. Saved as 'scheduled_tasks_final.json'")
