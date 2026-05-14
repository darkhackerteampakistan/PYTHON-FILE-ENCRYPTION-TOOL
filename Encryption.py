import os
import time

# 🎨 Color codes
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
B = "\033[94m"
C = "\033[96m"
W = "\033[0m"

# ⏳ typing animation
def slow(text, delay=0.01):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

# 🔄 loading animation
def loading(msg="Scanning"):
    for _ in range(3):
        print(f"{Y}{msg}.{W}", end="\r")
        time.sleep(0.3)
        print(f"{Y}{msg}..{W}", end="\r")
        time.sleep(0.3)
        print(f"{Y}{msg}...{W}", end="\r")
        time.sleep(0.3)
    print(" " * 30, end="\r")

# 📂 Find all Python files
def find_python_files():
    search_paths = [
        "/sdcard",
        os.path.expanduser("~")
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
                    if file.endswith(".py"):
                        full_path = os.path.join(root, file)
                        py_files.append(full_path)

    return sorted(list(set(py_files)))

# 🚀 MAIN
if __name__ == "__main__":
    os.system("clear")

    slow(f"{C}===================================={W}")
    slow(f"{G}     🐍 PYTHON FILE FINDER TOOL{W}")
    slow(f"{B}     Developer: Molla Mohammad Rifat Osama{W}")
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
            choice = int(input(f"\n{Y}Select file number ➤ {W}"))

            if 1 <= choice <= len(py_files):
                selected_file = py_files[choice - 1]

                print(f"\n{G}✅ Selected File:{W}")
                print(f"{C}{selected_file}{W}")

                # File info
                size = os.path.getsize(selected_file) / 1024

                print(f"\n{Y}📄 File Name:{W} {os.path.basename(selected_file)}")
                print(f"{Y}📂 Folder:{W} {os.path.dirname(selected_file)}")
                print(f"{Y}📦 Size:{W} {size:.2f} KB")

                break
            else:
                slow(f"{R}❌ Invalid choice!{W}")

        except ValueError:
            slow(f"{R}❌ Enter a valid number!{W}")
