import random
import tkinter as tk


WIDTH = 600
HEIGHT = 400
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 18


def start_game(parent):
    window = tk.Toplevel(parent)
    window.title("Dodge Game")
    window.resizable(False, False)

    canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="#0F172A", highlightthickness=0)
    canvas.pack()
    canvas.create_text(
        WIDTH // 2,
        18,
        text="Move with the arrow keys and avoid the falling blocks",
        fill="white",
        font=("Arial", 12),
    )

    state = {"active": True, "score": 0, "frames": 0, "after_id": None}
    pressed = set()
    obstacles = {}
    player = canvas.create_rectangle(
        WIDTH // 2 - PLAYER_WIDTH // 2,
        HEIGHT - 45,
        WIDTH // 2 + PLAYER_WIDTH // 2,
        HEIGHT - 45 + PLAYER_HEIGHT,
        fill="#34D399",
        outline="",
    )
    score_label = canvas.create_text(55, 45, text="Score: 0", fill="white", font=("Arial", 14, "bold"))

    def close():
        state["active"] = False
        if state["after_id"] is not None:
            window.after_cancel(state["after_id"])
        window.destroy()
        parent.deiconify()

    def finish():
        state["active"] = False
        canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text=f"Game over! Score: {state['score']}\nPress Enter to play again",
            fill="white",
            font=("Arial", 20, "bold"),
            justify="center",
        )

    def restart(event=None):
        if state["active"]:
            return
        canvas.delete("all")
        obstacles.clear()
        state.update(active=True, score=0, frames=0)
        nonlocal player, score_label
        canvas.create_text(
            WIDTH // 2,
            18,
            text="Move with the arrow keys and avoid the falling blocks",
            fill="white",
            font=("Arial", 12),
        )
        player = canvas.create_rectangle(
            WIDTH // 2 - PLAYER_WIDTH // 2,
            HEIGHT - 45,
            WIDTH // 2 + PLAYER_WIDTH // 2,
            HEIGHT - 45 + PLAYER_HEIGHT,
            fill="#34D399",
            outline="",
        )
        score_label = canvas.create_text(55, 45, text="Score: 0", fill="white", font=("Arial", 14, "bold"))
        tick()

    def on_key_down(event):
        pressed.add(event.keysym)

    def on_key_up(event):
        pressed.discard(event.keysym)

    def tick():
        if not state["active"]:
            return

        x1, y1, x2, y2 = canvas.coords(player)
        dx = ("Right" in pressed) - ("Left" in pressed)
        canvas.move(player, dx * 7, 0)
        x1, y1, x2, y2 = canvas.coords(player)
        if x1 < 0:
            canvas.move(player, -x1, 0)
        elif x2 > WIDTH:
            canvas.move(player, WIDTH - x2, 0)

        state["frames"] += 1
        if state["frames"] % 18 == 0:
            block_width = random.randint(30, 75)
            block_x = random.randint(0, WIDTH - block_width)
            block = canvas.create_rectangle(
                block_x,
                -25,
                block_x + block_width,
                0,
                fill="#F87171",
                outline="",
            )
            obstacles[block] = block_width

        for block, block_width in list(obstacles.items()):
            canvas.move(block, 0, 4 + min(state["score"] // 5, 5))
            bx1, by1, bx2, by2 = canvas.coords(block)
            px1, py1, px2, py2 = canvas.coords(player)
            if bx1 < px2 and bx2 > px1 and by1 < py2 and by2 > py1:
                finish()
                return
            if by1 > HEIGHT:
                canvas.delete(block)
                del obstacles[block]
                state["score"] += 1

        canvas.itemconfigure(score_label, text=f"Score: {state['score']}")
        state["after_id"] = window.after(30, tick)

    window.bind("<KeyPress>", on_key_down)
    window.bind("<KeyRelease>", on_key_up)
    window.bind("<Return>", restart)
    window.protocol("WM_DELETE_WINDOW", close)
    canvas.focus_set()
    tick()
