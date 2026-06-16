
from tkinter import *
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import os
import hashlib
from datetime import datetime

# ---------------- LOAD KEY ---------------- #

with open("keys/secret.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

# ---------------- HISTORY ---------------- #

history = []

# ---------------- HASH FUNCTION ---------------- #

def calculate_hash(filepath):

    sha256 = hashlib.sha256()

    with open(filepath, "rb") as file:

        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()

# ---------------- ENCRYPT FILE ---------------- #

def encrypt_file():

    filepath = filedialog.askopenfilename()

    if not filepath:
        return

    with open(filepath, "rb") as file:
        data = file.read()

    encrypted_data = fernet.encrypt(data)

    filename = os.path.basename(filepath)

    output_path = "encrypted_files/encrypted_" + filename

    with open(output_path, "wb") as enc_file:
        enc_file.write(encrypted_data)

    file_hash = calculate_hash(filepath)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    history.append(f"Encrypted: {filename} | {timestamp}")

    log_data = (
        f"\n[ENCRYPTED]\n"
        f"File: {filename}\n"
        f"SHA256: {file_hash}\n"
        f"Time: {timestamp}\n"
    )

    with open("logs/security_logs.txt", "a") as log:
        log.write(log_data)

    status_label.config(
        text=f"File Encrypted Successfully\nSaved To:\n{output_path}",
        fg="#d4af37"
    )

# ---------------- DECRYPT FILE ---------------- #

def decrypt_file():

    filepath = filedialog.askopenfilename()

    if not filepath:
        return

    with open(filepath, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    filename = os.path.basename(filepath)

    output_path = "decrypted_files/decrypted_" + filename

    with open(output_path, "wb") as dec_file:
        dec_file.write(decrypted_data)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    history.append(f"Decrypted: {filename} | {timestamp}")

    log_data = (
        f"\n[DECRYPTED]\n"
        f"File: {filename}\n"
        f"Time: {timestamp}\n"
    )

    with open("logs/security_logs.txt", "a") as log:
        log.write(log_data)

    status_label.config(
        text=f"File Decrypted Successfully\nSaved To:\n{output_path}",
        fg="#00ff99"
    )

# ---------------- SHOW HISTORY ---------------- #

def show_history():

    if len(history) == 0:
        messagebox.showinfo(
            "History",
            "No Activity Found"
        )
        return

    history_text = "\n".join(history)

    messagebox.showinfo(
        "Encryption History",
        history_text
    )

# ---------------- HOVER EFFECTS ---------------- #

def on_enter(e):

    e.widget['background'] = '#d4af37'
    e.widget['fg'] = 'black'

def on_leave(e):

    e.widget['background'] = '#111111'
    e.widget['fg'] = '#d4af37'

# ---------------- GUI WINDOW ---------------- #

root = Tk()

root.title("Secure File Storage System")

root.geometry("800x650")

root.config(bg="#0a0a0a")

root.resizable(False, False)

# ---------------- TITLE ---------------- #

title = Label(
    root,
    text="SECURE FILE STORAGE SYSTEM",
    font=("Arial", 26, "bold"),
    bg="#0a0a0a",
    fg="#d4af37"
)

title.pack(pady=30)

# ---------------- SUBTITLE ---------------- #

subtitle = Label(
    root,
    text="AES-256 File Encryption & Secure Storage",
    font=("Arial", 12),
    bg="#0a0a0a",
    fg="#c5a862"
)

subtitle.pack()

# ---------------- BUTTON STYLE ---------------- #

btn_style = {
    "font": ("Arial", 13, "bold"),
    "bg": "#111111",
    "fg": "#d4af37",
    "activebackground": "#d4af37",
    "activeforeground": "black",
    "relief": FLAT,
    "bd": 0,
    "width": 30,
    "height": 2,
    "cursor": "hand2"
}

# ---------------- ENCRYPT BUTTON ---------------- #

encrypt_btn = Button(
    root,
    text="Encrypt File",
    command=encrypt_file,
    **btn_style
)

encrypt_btn.pack(pady=25)

# ---------------- DECRYPT BUTTON ---------------- #

decrypt_btn = Button(
    root,
    text="Decrypt File",
    command=decrypt_file,
    **btn_style
)

decrypt_btn.pack(pady=15)

# ---------------- HISTORY BUTTON ---------------- #

history_btn = Button(
    root,
    text="Show Encryption History",
    command=show_history,
    **btn_style
)

history_btn.pack(pady=15)

# ---------------- STATUS LABEL ---------------- #

status_label = Label(
    root,
    text="No Activity Yet",
    font=("Arial", 12),
    bg="#111111",
    fg="white",
    width=60,
    height=8,
    wraplength=600
)

status_label.pack(pady=40)

# ---------------- HOVER EFFECTS ---------------- #

buttons = [
    encrypt_btn,
    decrypt_btn,
    history_btn
]

for btn in buttons:
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# ---------------- FOOTER ---------------- #

footer = Label(
    root,
    text="Cybersecurity Internship Project • AES Encryption Edition",
    font=("Arial", 10),
    bg="#0a0a0a",
    fg="#8b7355"
)

footer.pack(side=BOTTOM, pady=20)

# ---------------- RUN ---------------- #

root.mainloop()

