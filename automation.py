import webbrowser
import subprocess
import os




# ------------------ WEB APPS ------------------

WEB_APPS = {
    "youtube": "https://www.youtube.com/",
    "wikipedia": "https://www.wikipedia.org/",
    "instagram": "https://www.instagram.com/",
    "facebook": "https://www.facebook.com/",
    "twitter": "https://twitter.com/",
    "telegram": "https://telegram.me/",
}


# ------------------ OPEN WEB APP ------------------

def open_web_app(app_name):
    for name, url in WEB_APPS.items():
        if name in app_name:
            webbrowser.open(url)
            print(f"Opening {name}")
            return True
    return False


# ------------------ OPEN LOCAL APP ------------------

def open_local_app(app_name):
    try:
        subprocess.Popen(app_name, creationflags=subprocess.CREATE_NO_WINDOW)
        print(f"Opening {app_name}")
        return True
    except Exception:
        return False


# ------------------ CLOSE APP ------------------

def close_app(app_name):
    try:
        subprocess.run(
            f"taskkill /IM {app_name}.exe /F",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"Closing {app_name}")
        return True
    except Exception:
        return False


# ------------------ SYSTEM COMMANDS ------------------

def shutdown_system():
    print("Shutting down...")
    os.system("shutdown /s /t 5")


def restart_system():
    print("Restarting...")
    os.system("shutdown /r /t 5")


# ------------------ AUTOMATION ENGINE ------------------

def auto(command):
    command = command.lower()

    if not command:
        print("Empty command")
        return

    words = command.split()

    command = words[0]

    # ---------------- OPEN ----------------
    if command in ["open", "start", "launch"]:
        if len(words) < 2:
            print("Specify what to open.")
            return

        target = " ".join(words[1:])

        if open_local_app(target):
            return

        if open_web_app(target):
            return

        print("Application not found.")

    # ---------------- CLOSE ----------------
    elif command in ["close", "stop"]:
        if len(words) < 2:
            print("Specify what to close.")
            return

        target = words[1]
        close_app(target)

    # ---------------- SHUTDOWN ----------------
    elif command == "shutdown":
        shutdown_system()

    # ---------------- RESTART ----------------
    elif command == "restart":
        restart_system()

    else:
        print("Unknown command type.")


# ------------------ MAIN ------------------
# while True:
#     intent = input("Enter your intent: ")
#     automation(intent)
