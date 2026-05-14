import os
import base64
import zlib
import marshal
import hashlib
import random
import string
import time

# =========================
# UI COLORS
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
        time.sleep(0.2)
        print(f"{Y}{msg}..{W}", end="\r")
        time.sleep(0.2)
        print(f"{Y}{msg}...{W}", end="\r")
        time.sleep(0.2)
    print(" " * 40, end="\r")

# =========================
# KEY GENERATION
# =========================
K1 = "dark_team"
K2 = "rifat_osama"
K3 = "secure_key"

def get_key():
    data = (K1 + K2 + K3).encode()
    return hashlib.sha256(data).digest()

# =========================
# ENCRYPT FUNCTION
# =========================
def encrypt_code(code):
    key = get_key()

    compiled = compile(code, "<enc>", "exec")
    marshaled = marshal.dumps(compiled)
    compressed = zlib.compress(marshaled)

    # simple XOR encryption (no external library)
    encrypted = bytearray()
    for i, b in enumerate(compressed):
        encrypted.append(b ^ key[i % len(key)])

    return base64.b64encode(encrypted).decode()

# =========================
# LOADER BUILDER
# =========================
def build_loader(enc_data):
    return f"""
import base64, zlib, marshal, hashlib

K1="dark_team"
K2="rifat_osama"
K3="secure_key"

def key():
    return hashlib.sha256((K1+K2+K3).encode()).digest()

data = base64.b64decode("{enc_data}")

key_bytes = key()

# XOR DECRYPT
raw = bytearray()
for i,b in enumerate(data):
    raw.append(b ^ key_bytes[i % len(key_bytes)])

code = marshal.loads(zlib.decompress(raw))
exec(code)
"""

# =========================
# FILE SEARCH
# =========================
def find_py_files():
    paths = ["/sdcard", os.getcwd()]
    files = []

    for p in paths:
        if os.path.exists(p):
            for r, d, f in os.walk(p):
                d[:] = [x for x in d if x not in ["Android", "__pycache__", ".thumbnails"]]

                for file in f:
                    if file.endswith(".py") and not file.startswith(".trashed"):
                        full = os.path.join(r, file)
                        if full != os.path.abspath(__file__):
                            files.append(full)

    return sorted(set(files))

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    os.system("clear")

    slow(f"{C}===================================={W}")
    slow(f"{G}   🔐 PYTHON ENCRYPTION TOOL{W}")
    slow(f"{B}   No External Library Version{W}")
    slow(f"{C}===================================={W}\n")

    loading("Scanning device")

    py_files = find_py_files()

    if not py_files:
        slow(f"{R}❌ No Python files found{W}")
        exit()

    slow(f"{G}📂 Found Files: {len(py_files)}{W}\n")

    for i, f in enumerate(py_files, 1):
        print(f"{C}[{i}] {G}{f}{W}")

    choice = int(input(f"\n{Y}Select file ➤ {W}"))

    selected = py_files[choice - 1]

    slow(f"\n{B}Encrypting...{W}")
    loading("Encrypting")

    with open(selected, "r", encoding="utf-8") as f:
        code = f.read()

    enc = encrypt_code(code)
    loader = build_loader(enc)

    name = os.path.splitext(os.path.basename(selected))[0]

    folder = os.path.join(os.path.dirname(selected), name + "_encrypted")
    os.makedirs(folder, exist_ok=True)

    out = os.path.join(folder, name + "_protected.py")

    with open(out, "w") as f:
        f.write(loader)

    slow(f"\n{G}✅ DONE!{W}")
    print(f"{C}Folder: {folder}{W}")
    print(f"{C}File: {out}{W}")
