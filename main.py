import argparse
import tkinter as tk
from game_rules import BOARD_SIZE, STARTING_CHANCES, STAGES, STEP, Puzzle

CELL = 76
LEFT = 42
TOP = 92
COLORS = {"↑": "#7c4dff", "↓": "#ff5c8a", "←": "#00a9a5", "→": "#f5a623"}


class OneArrowGame:
    def __init__(self, demo=None):
        self.root = tk.Tk()
        self.root.title("一箭又一箭")
        self.root.resizable(False, False)
        self.root.configure(bg="#f3f7ff")
        if demo:
            self.root.attributes("-topmost", True)
        self.level = 0
        self.puzzle = None
        self.busy = False
        self.page = tk.Frame(self.root, bg="#f3f7ff", padx=24, pady=24)
        self.page.pack()
        if demo == "game":
            self.level = 1
            self.show_game()
        elif demo == "blocked":
            self.show_game()
            arrow = self.puzzle.arrow_at(0, 0)
            self.puzzle.choose(0, 0)
            self.collide(arrow, None)
            self.update_panel()
        elif demo == "pass":
            self.level = 2
            self.show_result(True)
        else:
            self.show_home()

    def clear_page(self):
        for child in self.page.winfo_children():
            child.destroy()

    def make_button(self, parent, label, command, color="#3856d4"):
        return tk.Button(parent, text=label, command=command, bg=color, fg="white",
                         font=("Arial", 12, "bold"), relief="flat", padx=20, pady=9,
                         activebackground=color, activeforeground="white", cursor="hand2")

    def show_home(self):
        self.clear_page()
        card = tk.Frame(self.page, bg="white", padx=46, pady=34)
        card.pack()
        tk.Label(card, text="一箭又一箭", bg="white", fg="#26376f", font=("Arial", 34, "bold")).pack()
        tk.Label(card, text="Python 箭头益智小游戏", bg="white", fg="#8792ac", font=("Arial", 13)).pack(pady=(0, 20))
        tk.Label(card, text="让每一支箭沿着自己的方向离开棋盘", bg="white", fg="#3d4a68", font=("Arial", 12)).pack(anchor="w")
        tk.Label(card, text="前方没有箭头：可以离开", bg="white", fg="#3d4a68", font=("Arial", 12)).pack(anchor="w", pady=(12, 0))
        tk.Label(card, text="前方有箭头：碰撞并失去一次机会", bg="white", fg="#3d4a68", font=("Arial", 12)).pack(anchor="w")
        tk.Label(card, text="共有 3 次机会，清空关卡即可继续前进", bg="white", fg="#3d4a68", font=("Arial", 12)).pack(anchor="w", pady=(0, 20))
        self.make_button(card, "开始游戏", self.start).pack()

    def start(self):
        self.level = 0
        self.show_game()

    def show_game(self):
        self.clear_page()
        self.puzzle = Puzzle(STAGES[self.level], STARTING_CHANCES)
        self.busy = False
        header = tk.Frame(self.page, bg="#f3f7ff")
        header.pack(fill="x", pady=(0, 10))
        tk.Label(header, text=f"第 {self.level + 1} / {len(STAGES)} 关", bg="#f3f7ff", fg="#26376f", font=("Arial", 16, "bold")).pack(side="left")
        self.status = tk.Label(header, text="选择一支箭头", bg="#f3f7ff", fg="#6d7898", font=("Arial", 11))
        self.status.pack(side="right")
        layout = tk.Frame(self.page, bg="#f3f7ff")
        layout.pack()
        self.canvas = tk.Canvas(layout, width=LEFT * 2 + CELL * BOARD_SIZE,
                                height=TOP + CELL * BOARD_SIZE + 18,
                                bg="white", highlightthickness=0)
        self.canvas.pack(side="left")
        panel = tk.Frame(layout, bg="white", padx=18, pady=18)
        panel.pack(side="left", fill="y", padx=(14, 0))
        tk.Label(panel, text="本关信息", bg="white", fg="#26376f", font=("Arial", 15, "bold")).pack(anchor="w")
        self.remaining = tk.Label(panel, bg="white", fg="#3d4a68", font=("Arial", 12))
        self.remaining.pack(anchor="w", pady=(24, 8))
        self.chances = tk.Label(panel, bg="white", fg="#3d4a68", font=("Arial", 12))
        self.chances.pack(anchor="w", pady=(0, 22))
        tk.Label(panel, text="先找前方没有障碍的箭头", bg="white", fg="#8792ac", font=("Arial", 10), wraplength=135, justify="left").pack(anchor="w", pady=(0, 18))
        self.make_button(panel, "重新本关", self.show_game, "#71809e").pack(anchor="w")
        self.make_button(panel, "回到首页", self.show_home, "#71809e").pack(anchor="w", pady=(10, 0))
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        self.canvas.create_text(LEFT, 38, text="让箭头找到出口", anchor="w", fill="#26376f", font=("Arial", 17, "bold"))
        self.canvas.create_text(LEFT, 62, text="点击后它会朝箭头方向前进", anchor="w", fill="#8792ac", font=("Arial", 10))
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                x = LEFT + column * CELL
                y = TOP + row * CELL
                self.canvas.create_rectangle(x, y, x + CELL, y + CELL, fill="#f7f9ff", outline="#dce4f5")
        for arrow in self.puzzle.arrows:
            self.draw_arrow(arrow)
        self.update_panel()

    def tag(self, arrow):
        return f"arrow-{arrow.row}-{arrow.column}"

    def draw_arrow(self, arrow):
        x = LEFT + arrow.column * CELL + CELL // 2
        y = TOP + arrow.row * CELL + CELL // 2
        tag = self.tag(arrow)
        self.canvas.create_oval(x - 25, y - 25, x + 25, y + 25, fill=COLORS[arrow.symbol], outline="", tags=tag)
        self.canvas.create_text(x, y - 1, text=arrow.symbol, fill="white", font=("Arial", 26, "bold"), tags=tag)

    def update_panel(self):
        self.remaining.config(text=f"剩余箭头：{len(self.puzzle.arrows)}")
        self.chances.config(text=f"剩余机会：{self.puzzle.chances} / {STARTING_CHANCES}")

    def on_click(self, event):
        if self.busy:
            return
        row = (event.y - TOP) // CELL
        column = (event.x - LEFT) // CELL
        if not 0 <= row < BOARD_SIZE or not 0 <= column < BOARD_SIZE:
            return
        result = self.puzzle.choose(row, column)
        if result is None:
            self.status.config(text="这里没有箭头")
        elif result.status == "blocked":
            self.collide(result.arrow)
            self.update_panel()
            if self.puzzle.is_lost:
                self.root.after(700, lambda: self.show_result(False))
        else:
            self.status.config(text="路线畅通，正在离场", fg="#16836d")
            self.fly(result.arrow)

    def collide(self, arrow, duration=650):
        self.status.config(text="前方被挡住了，少一次机会", fg="#d4475a")
        x = LEFT + arrow.column * CELL + 5
        y = TOP + arrow.row * CELL + 5
        border = self.canvas.create_rectangle(x, y, x + CELL - 10, y + CELL - 10, outline="#ef5f72", width=4)
        cross = self.canvas.create_text(x + CELL // 2 - 5, y + CELL // 2 - 2, text="×", fill="#ef5f72", font=("Arial", 32, "bold"))
        if duration is not None:
            self.root.after(duration, lambda: self.canvas.delete(border, cross))

    def fly(self, arrow):
        self.busy = True
        dr, dc = STEP[arrow.symbol]
        tag = self.tag(arrow)
        def animate(frame=0):
            if frame < 17:
                self.canvas.move(tag, dc * 12, dr * 12)
                self.root.after(20, lambda: animate(frame + 1))
                return
            self.canvas.delete(tag)
            self.update_panel()
            self.busy = False
            if self.puzzle.is_cleared:
                self.show_result(True)
        animate()

    def show_result(self, won):
        self.clear_page()
        card = tk.Frame(self.page, bg="white", padx=52, pady=36)
        card.pack()
        title = "本关完成！" if won else "本关暂停"
        color = "#16836d" if won else "#d4475a"
        detail = "全部箭头已经离开棋盘。" if won else "三次机会已经用完，重新观察路线吧。"
        tk.Label(card, text=title, bg="white", fg=color, font=("Arial", 29, "bold")).pack()
        tk.Label(card, text=detail, bg="white", fg="#596681", font=("Arial", 12)).pack(pady=(14, 24))
        box = tk.Frame(card, bg="white")
        box.pack()
        if won and self.level < len(STAGES) - 1:
            self.make_button(box, "下一关", self.next_level).pack(side="left", padx=5)
        elif won:
            self.make_button(box, "完成全部关卡", self.show_home).pack(side="left", padx=5)
        self.make_button(box, "再试一次", self.show_game, "#71809e").pack(side="left", padx=5)

    def next_level(self):
        self.level += 1
        self.show_game()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", choices=["welcome", "game", "blocked", "pass"])
    OneArrowGame(parser.parse_args().demo).run()
