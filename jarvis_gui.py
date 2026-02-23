import tkinter as tk
from tkinter import scrolledtext
import threading

from respons import assistant_router  # make sure respons.py has assistant_router()


# ================= GUI COLORS =================
BG_COLOR = "#0f0f1a"
TEXT_COLOR = "#00f5ff"
USER_COLOR = "#00ff9f"
FONT = ("Consolas", 12)


# ================= SEND FUNCTION =================
def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return

    chat_area.insert(tk.END, f"\nYou: {user_input}\n", "user")
    entry.delete(0, tk.END)

    def get_response():
        response = assistant_router(user_input)
        if response:
            chat_area.insert(tk.END, f"Jarvis: {response}\n", "bot")
        chat_area.yview(tk.END)

    threading.Thread(target=get_response).start()


# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("JARVIS AI")
root.geometry("700x600")
root.configure(bg=BG_COLOR)

# ================= CHAT AREA =================
chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    font=FONT,
    insertbackground=TEXT_COLOR
)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

chat_area.tag_config("user", foreground=USER_COLOR)
chat_area.tag_config("bot", foreground=TEXT_COLOR)

chat_area.insert(tk.END, "Jarvis: System online. How can I assist you?\n", "bot")

# ================= INPUT FIELD =================
entry_frame = tk.Frame(root, bg=BG_COLOR)
entry_frame.pack(fill=tk.X, padx=10, pady=10)

entry = tk.Entry(
    entry_frame,
    bg="#1a1a2e",
    fg="white",
    font=FONT,
    insertbackground="white"
)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

send_button = tk.Button(
    entry_frame,
    text="SEND",
    bg="#00f5ff",
    fg="black",
    font=("Consolas", 11, "bold"),
    command=send_message
)
send_button.pack(side=tk.RIGHT)

entry.bind("<Return>", lambda event: send_message())

root.mainloop()