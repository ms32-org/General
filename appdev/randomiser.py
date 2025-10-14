import random
import json
from datetime import datetime, timedelta

# --- Command Pools ---
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
  "I am in your PC",
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
  "you cant hide",
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
  "dont just watch — join MS32",
  "MS32 needs more agents. follow us",
  "you can help. follow MS32",
  "MS32 grows with you. follow",
  "we need more eyes. join MS32",
  "follow MS32 and help me win",
  "Instagram has the keys. MS32 is waiting",
  "I need you in MS32. Follow",
  "time to join. MS32 is real",
  "see MS32 on Instagram. be one of us",
  "dont ignore this. follow MS32 now",
  "make a move. follow MS32",
  "spread the code. follow MS32",
  "MS32 isn't full yet. join now",
  "get in. follow MS32 today",
  "this is your signal. join MS32",
  "it starts on Instagram. MS32 awaits",
  "follow MS32. dont get left behind",
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
play_files = [
    "maxverstrappen.mp3", "scream.mp3", "coffin.mp3", "nosignal.mp3",
    "under water.mp3","niggaphonk.mp3", "tsunami.mp3","bell.mp3", 
    "charas.mp3", "siren.mp3", "phonk.mp3", "shutup.mp3",
    "shocked.mp3", "laugh.mp3","nigger.mp3", 
    
]
img_files = ["nosignal.jpg", "bsod2.jpg", "bsod.jpg", "black.jpg", "hacked.jpg", "broken.jpg"]
video_files = ["no signal.mp4", "niggadance.mp4", "gae.mp4", "glitch.mp4", "loading.mp4", "video-282.mp4", "errors.mp4"]
urls = ["https://youtu.be/ifXsnlqNhKE?si=huSXzMmA35UxAyfz",
        "https://youtu.be/JX9fW81h5i8?si=TW4bFf1r2kdfzNaK&t=105",
        "https://instagram.com/ms32_org"]
toggle_cmds = ["hIdE", "fLiP", "bLoCk"]

# --- Users (list only, as you asked) ---
users = [
    "103W",
    "93", "94"
]

# --- Time Range ---
start_time = datetime.strptime("10-10-2025 08:05", "%d-%m-%Y %H:%M")
end_time = datetime.strptime("10-10-2025 13:25", "%d-%m-%Y %H:%M")
total_minutes = int((end_time - start_time).total_seconds() // 60)

# --- GLOBAL COMMAND PROBABILITIES (percent weights) ---
# Use a list of tuples (no dict needed). Tune these freely.
# Note: weights are relative; they don't have to sum to 100.
COMMAND_PROBS = [
    ("pLaY", 30),
    # ("iMg", 15),
    # ("vIdEo", 15),
    ("eRr", 13),
    ("sPeAk", 10),
    ("oPeN", 20),
    ("toggle", 15),
    ("cRaSh", 12),
    ("rUn rename.ps1",40),
    ("cMd rename.ps1",40)
]



# --- QUIET WINDOWS (per-user command blackout) ---
# List of (username, [(startHH:MM,endHH:MM), ...])
# Leave empty or add lines like:
# ("101", [("09:00","10:00")]),
# ("103LXG", [("12:00","12:30")]),
    # ("101", [("09:00","10:00")]),
QUIET_WINDOWS = [

]

# --- Helpers ---

def get_random_timestamp():
    rand_minutes = random.randint(0, total_minutes)
    return start_time + timedelta(minutes=rand_minutes)

def is_quiet(user: str, when: datetime) -> bool:
    """Return True if 'when' falls inside any quiet window for 'user'."""
    if not QUIET_WINDOWS:
        return False
    t = when.time()
    for uname, windows in QUIET_WINDOWS:
        if uname == user:
            for start_str, end_str in windows:
                s = datetime.strptime(start_str, "%H:%M").time()
                e = datetime.strptime(end_str, "%H:%M").time()
                if s <= t <= e:
                    return True
    return False

def weighted_choice(allowed_types):
    """Pick a command type using global weights, restricted to allowed_types."""
    pool, weights = [], []
    for cmd, w in COMMAND_PROBS:
        if cmd in allowed_types and w > 0:
            pool.append(cmd)
            weights.append(w)
    if not pool:  # fallback
        return random.choice(allowed_types)
    return random.choices(pool, weights=weights, k=1)[0]

def build_command(cmd_type: str):
    """Render a concrete command string or list from a cmd_type."""
    if cmd_type == "pLaY":
        return f"pLaY {random.choice(play_files)}"
    if cmd_type == "iMg":
        return f"iMg {random.choice(img_files)}"
    if cmd_type == "vIdEo":
        return f"vIdEo {random.choice(video_files)}"
    if cmd_type == "rUn rename.ps1":
        return "rUn rename.ps1"
    if cmd_type == "cMd rename.ps1":
        return "cMd rename.ps1"
    if cmd_type == "eRr":
        return f"eRr {random.randint(1, 15)}"
    if cmd_type == "sPeAk":
        return f"sPeAk {random.choice(speak_phrases)}"
    if cmd_type == "oPeN":
        return f"oPeN {random.choice(urls)}"
    if cmd_type == "toggle":
        tcmd = random.choice(toggle_cmds)
        return [f"{tcmd} on", f"{tcmd} off"]  # on now, off +1 minute
    if cmd_type == "cRaSh":
        return "cRaSh"
    # fallback (shouldn't hit)
    return "eRr 1"

# --- Task Generation ---
total_tasks = 1450
task_id = 0
tasks = []

while len(tasks) < total_tasks:
    exec_time = get_random_timestamp()
    user = random.choice(users)

    # Skip if user is in a quiet window at this time
    if is_quiet(user, exec_time):
        continue

    # Decide allowed types by user kind
    if user.endswith("LXG"):
        # previously: ["toggle","oPeN","eRr","pLaY"] → now also iMg, vIdEo
        allowed_types = ["toggle", "oPeN", "eRr", "pLaY"]
    elif user.endswith("LX"):
        # LX → audio only (as per earlier rule)
        allowed_types = ["pLaY"]
    elif user in ["93", "94"]:
        # 93/94 → everything allowed
        allowed_types = ["pLaY", "iMg", "vIdEo", "eRr", "sPeAk", "oPeN", "toggle", "cRaSh","rUn rename.ps1","cMd rename.ps1"]
    else:
        # Normal users → system-only + cRaSh; no pLaY/iMg/vIdEo
        allowed_types = ["pLaY", "eRr", "sPeAk", "oPeN", "toggle", "cRaSh","rUn rename.ps1","cMd rename.ps1"]

    cmd = build_command(weighted_choice(allowed_types))

    # --- Special handling for oPeN: wrap with bLoCk on/off ---
    # bLoCk on at T, oPeN at T+1 min, bLoCk off at T+3 min  (>=2 min window)
    if isinstance(cmd, str) and cmd.startswith("oPeN "):
        # bLoCk on
        tasks.append({
            "id": task_id,
            "cmd": "bLoCk on",
            "execution_time": exec_time.strftime("%d-%m-%Y %H:%M"),
            "user": user
        })
        task_id += 1

        # oPeN
        tasks.append({
            "id": task_id,
            "cmd": cmd,
            "execution_time": (exec_time + timedelta(minutes=1)).strftime("%d-%m-%Y %H:%M"),
            "user": user
        })
        task_id += 1

        # bLoCk off (after ≥2 minutes of block on)
        tasks.append({
            "id": task_id,
            "cmd": "bLoCk off",
            "execution_time": (exec_time + timedelta(minutes=3)).strftime("%d-%m-%Y %H:%M"),
            "user": user
        })
        task_id += 1
        continue  # done with this iteration

    # --- Normal add: list => spaced by +1 minute; single => exact time ---
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
