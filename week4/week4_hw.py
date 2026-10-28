import tkinter as tk

from src.gamepkg1.game1 import start_game as game1
from src.gamepkg2.game2 import start_game as game2


def open_game1():
    menu.withdraw()

    try:
        game1(menu)
    except Exception:
        menu.deiconify()
        raise


def open_game2():
    menu.withdraw()

    try:
        game2(menu)
    except Exception:
        menu.deiconify()
        raise


def on_enter(event):
    event.widget.config(relief="raised", bd=6)


def on_leave(event):
    event.widget.config(relief="raised", bd=3)


# ==========================
# สร้างหน้าต่างหลัก
# ==========================

menu = tk.Tk()
menu.title("Game Launcher")
menu.geometry("900x650")
menu.configure(bg="#1E293B")
menu.resizable(False, False)

# ==========================
# หัวข้อ
# ==========================

title = tk.Label(
    menu,
    text="🎮 GAME COLLECTION 🎮",
    font=("Arial", 30, "bold"),
    fg="white",
    bg="#1E293B"
)

title.pack(pady=40)

subtitle = tk.Label(
    menu,
    text="Select a Game",
    font=("Arial", 16),
    fg="lightgray",
    bg="#1E293B"
)

subtitle.pack(pady=10)

# ==========================
# ปุ่มเกมที่ 1
# ==========================

btn1 = tk.Button(
    menu,
    text="🎲 Dodge Game",
    font=("Arial", 18, "bold"),
    bg="#10B981",
    fg="white",
    activebackground="#059669",
    activeforeground="white",
    width=22,
    height=2,
    bd=3,
    command=open_game1
)

btn1.pack(pady=25)

# ==========================
# ปุ่มเกมที่ 2
# ==========================

btn2 = tk.Button(
    menu,
    text="🚀 Space Escape",
    font=("Arial", 18, "bold"),
    bg="#3B82F6",
    fg="white",
    activebackground="#2563EB",
    activeforeground="white",
    width=22,
    height=2,
    bd=3,
    command=open_game2
)

btn2.pack(pady=25)

# ==========================
# ปุ่มออกจากโปรแกรม
# ==========================

exit_btn = tk.Button(
    menu,
    text="❌ Exit Program",
    font=("Arial", 16, "bold"),
    bg="#EF4444",
    fg="white",
    activebackground="#DC2626",
    activeforeground="white",
    width=18,
    height=1,
    bd=3,
    command=menu.destroy
)

exit_btn.pack(side="bottom", pady=40)

# ==========================
# เอฟเฟกต์เมื่อชี้เมาส์
# ==========================

for btn in (btn1, btn2, exit_btn):
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# ==========================
# เริ่มโปรแกรม
# ==========================

menu.mainloop()