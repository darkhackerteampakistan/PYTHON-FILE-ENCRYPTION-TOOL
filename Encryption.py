import os
import time
import base64
from pathlib import Path

try:
    from cryptography.fernet import Fernet
except ImportError:
    print("Installing required package...")
    os.system("pip install cryptography")
    from cryptography.fernet import Fernet


# =========================
# COLOR UI
# =========================
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
B = "\033[94m"
C = "\033[96m"
W = "\033[0m"


# =========================
# ANIMATION
# =========================
def slow(text, delay=0.01):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()


def loading(msg="Processing"):
    for _ in range(3):
        print(f"{Y}{msg}.{W}", end="\r")
        time.sleep(0.25)
        print(f"{Y}{msg}..{W}", end="\r")
        time.sleep(0.25)
        print(f"{Y}{msg}...{W}", end="\r")
        time.sleep(0.25)
    print(" " * 50, end="\r")


# =========================
# FIND PYTHON FILES
# =========================
def find_python_files():
    search_paths = [
        "/sdcard",
        str(Path.home())
    ]

    py_files = []

    for base in search_paths:
        if os.path.exists(base):
            for root, dirs, files in os.walk(base):

                # Skip unnecessary folders
                dirs[:] = [
                    d for d in dirs
                    if d not in [
                        "Android",
                        ".thumbnails",
                        "__pycache__"
                    ]
                ]

                for file in files:
                    if (
                        file.endswith(".py")
                        and not file.startswith(".trashed")
                    ):
                        full_path = os.path.join(root, file)

                        # Skip this tool itself
                        if os.path.abspath(full_path) != os.path.abspath(__file__):
                            py_files.append(full_path)

    return sorted(set(py_files))


# =========================
# PROTECT FILE
# =========================
def protect_python_file(file_path):
    with open(file_path, "rb") as f:
        content = f.read()

    # Generate encryption key
    key = Fernet.generate_key()
    cipher = Fernet(key)

    encrypted = cipher.encrypt(content)

    base_name = os.path.splitext(
        os.path.basename(file_path)
    )[0]

    save_dir = os.path.dirname(file_path)

    # Folder create
    folder_name = f"{base_name}_encrypted_folder"
    folder_path = os.path.join(save_dir, folder_name)

    os.makedirs(folder_path, exist_ok=True)

    # Save protected file
    output_name = f"{base_name}_protected.pyenc"
    output_path = os.path.join(folder_path, output_name)

    with open(output_path, "wb") as f:
        f.write(encrypted)

    # Save key
    key_path = os.path.join(folder_path, "secret.key")

    with open(key_path, "wb") as f:
        f.write(key)

    return output_path, folder_path, key_path


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    os.system("clear")

    slow(f"{C}===================================={W}")
    slow(f"{G}   🔐 PYTHON FILE PROTECTION TOOL{W}")
    slow(f"{B}   Developer: Molla Mohammad Rifat Osama{W}")
    slow(f"{C}===================================={W}\n")

    loading("Scanning device")

    py_files = find_python_files()

    if not py_files:
        slow(f"{R}❌ No Python files found{W}")
        exit()

    slow(f"{G}✅ Total Python Files Found: {len(py_files)}{W}\n")

    for i, file in enumerate(py_files, 1):
        print(f"{C}[{i}] {G}{file}{W}")

    while True:
        try:
            choice = int(
                input(
                    f"\n{Y}Select file number ➤ {W}"
                )
            )

            if 1 <= choice <= len(py_files):
                selected_file = py_files[choice - 1]
                break
            else:
                slow(f"{R}❌ Invalid choice!{W}")

        except ValueError:
            slow(f"{R}❌ Enter valid number!{W}")

    print(f"\n{C}Selected:{W}")
    print(selected_file)

    loading("Protecting file")

    output_path, folder_path, key_path = protect_python_file(
        selected_file
    )

    slow(f"\n{G}✅ Done Successfully!{W}")
    slow(f"{C}📂 Folder Created:{W}")
    print(folder_path)

    slow(f"\n{Y}🔐 Protected File:{W}")
    print(output_path)

    slow(f"\n{B}🗝 Secret Key Saved:{W}")
    print(key_path)
