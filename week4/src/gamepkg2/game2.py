import random
import tkinter as tk


WIDTH = 600
HEIGHT = 400
PLAYER_SIZE = 24
SURVIVAL_SECONDS = 30
FRAME_MS = 30


def start_game(parent):
    window = tk.Toplevel(parent)
    window.title("Space Escape")
    window.resizable(False, False)

    canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="#020617", highlightthickness=0)
    canvas.pack()
    state = {"active": True, "frames": 0, "after_id": None}
    pressed = set()
    meteors = {}
    player = canvas.create_polygon(
        WIDTH // 2,
        HEIGHT - 45,
        WIDTH // 2 - PLAYER_SIZE,
        HEIGHT - 10,
        WIDTH // 2 + PLAYER_SIZE,
        HEIGHT - 10,
        fill="#60A5FA",
        outline="white",
    )
    canvas.create_text(
        WIDTH // 2,
        18,
        text=f"Survive for {SURVIVAL_SECONDS} seconds! Move with the arrow keys",
        fill="white",
        font=("Arial", 12),
    )
    timer_label = canvas.create_text(55, 45, text="Time: 0", fill="white", font=("Arial", 14, "bold"))

    def close():
        state["active"] = False
        if state["after_id"] is not None:
            window.after_cancel(state["after_id"])
        window.destroy()
        parent.deiconify()

    def finish(escaped):
        state["active"] = False
        message = "You escaped!" if escaped else "Your ship was hit!"
        canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text=f"{message}\nPress Enter to play again",
            fill="white",
            font=("Arial", 20, "bold"),
            justify="center",
        )

    def restart(event=None):
        if state["active"]:
            return
        canvas.delete("all")
        meteors.clear()
        state.update(active=True, frames=0)
        nonlocal player, timer_label
        canvas.create_text(
            WIDTH // 2,
            18,
            text=f"Survive for {SURVIVAL_SECONDS} seconds! Move with the arrow keys",
            fill="white",
            font=("Arial", 12),
        )
        player = canvas.create_polygon(
            WIDTH // 2,
            HEIGHT - 45,
            WIDTH // 2 - PLAYER_SIZE,
            HEIGHT - 10,
            WIDTH // 2 + PLAYER_SIZE,
            HEIGHT - 10,
            fill="#60A5FA",
            outline="white",
        )
        timer_label = canvas.create_text(55, 45, text="Time: 0", fill="white", font=("Arial", 14, "bold"))
        tick()

    def on_key_down(event):
        pressed.add(event.keysym)

    def on_key_up(event):
        pressed.discard(event.keysym)

    def tick():
        if not state["active"]:
            return

        dx = ("Right" in pressed) - ("Left" in pressed)
        dy = ("Down" in pressed) - ("Up" in pressed)
        canvas.move(player, dx * 6, dy * 6)
        px1, py1, px2, py2 = canvas.bbox(player)
        if px1 < 0:
            canvas.move(player, -px1, 0)
        elif px2 > WIDTH:
            canvas.move(player, WIDTH - px2, 0)
        if py1 < 30:
            canvas.move(player, 0, 30 - py1)
        elif py2 > HEIGHT:
            canvas.move(player, 0, HEIGHT - py2)

        state["frames"] += 1
        elapsed = state["frames"] * FRAME_MS // 1000
        if elapsed >= SURVIVAL_SECONDS:
            finish(True)
            return

        if state["frames"] % 15 == 0:
            size = random.randint(18, 38)
            meteor_x = random.randint(size, WIDTH - size)
            meteor = canvas.create_oval(
                meteor_x - size,
                -size * 2,
                meteor_x + size,
                0,
                fill=random.choice(("#F97316", "#EF4444", "#A855F7")),
                outline="",
            )
            meteors[meteor] = size

        player_box = canvas.bbox(player)
        for meteor, size in list(meteors.items()):
            canvas.move(meteor, random.randint(-1, 1), 4 + elapsed // 8)
            meteor_box = canvas.bbox(meteor)
            if (
                meteor_box[0] < player_box[2]
                and meteor_box[2] > player_box[0]
                and meteor_box[1] < player_box[3]
                and meteor_box[3] > player_box[1]
            ):
                finish(False)
                return
            if meteor_box[1] > HEIGHT:
                canvas.delete(meteor)
                del meteors[meteor]

        canvas.itemconfigure(timer_label, text=f"Time: {elapsed}")
        state["after_id"] = window.after(FRAME_MS, tick)

    window.bind("<KeyPress>", on_key_down)
    window.bind("<KeyRelease>", on_key_up)
    window.bind("<Return>", restart)
    window.protocol("WM_DELETE_WINDOW", close)
    canvas.focus_set()
    tick()
