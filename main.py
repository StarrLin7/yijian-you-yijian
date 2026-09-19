import argparse
import tkinter as tk

from game_rules import BOARD_SIZE, STARTING_CHANCES, STAGES, STEP, Puzzle

CELL = 76
BOARD_LEFT = 45
BOARD_TOP = 105
COLORS = {"↑": "#7c4dff", "↓": "#ff5c8a", "←": "#00a9a5", "→": "#f5a623"}


class GameApp:
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
        self.page = tk.Frame(self.root, bg="#f3f7ff", padx=28, pady=26)
        self.page.pack()
        if demo == "game":
            self.level = 1
            self.show_game()
        elif demo == "blocked":
            self.show_game()
            arrow = self.puzzle.arrow_at(0, 0)
            self.puzzle.choose(0, 0)
            self.show_collision(arrow, None)
            self.refresh_side()
        elif demo == "pass":
            self.level = 2
            self.show_result(True)
        else:
            self.show_home()

    def clean(self):
        for child in self.page.winfo_children():
            child.destroy()

    def button(self, parent, text, command, color="#3856d4"):
        return tk.Button(parent, text=text, command=command, font=("Arial", 12, "bold"),
                         bg=color, fg="white", activebackground=color, activeforeground="white",
                         relief="flat", padx=22, pady=10, cursor="hand2")

    def show_home(self):
        self.clean()
        card = tk.Frame(self.page, bg="white", padx=45, pady=36)
        card.pack()
        tk.Label(card, text="一箭又一箭", font=("Arial", 35, "bold"), bg="white", fg="#26376f").pack()
        tk.Label(card, text="Python 箭头益智小游戏", font=("Arial", 13), bg="white", fg="#8b96b8").pack(pady=(0, 20))
        rule = "让每一支箭沿着自己的方向离开棋盘

前方没有箭头：可以离开
前方有箭头：会碰撞并失去一次机会

共有 3 次机会，清空关卡即可继续前进。"
        tk.Label(card, text=rule, font=("Arial", 12), bg="white", fg="#3d4a68", justify="left").pack(pady=(0, 24))
        self.button(card, "开始游戏", self.start).pack()

    def start(self):
        self.level = 0
        self.show_game()

    def show_game(self):
        self.clean()
        self.puzzle = Puzzle(STAGES[self.level], STARTING_CHANCES)
        self.busy = False
        header = tk.Frame(self.page, bg="#f3f7ff")
        header.pack(fill="x", pady=(0, 12))
        tk.Label(header, text=f"第 {self.level + 1} / {len(STAGES)} 关", font=("Arial", 16, "bold"), bg="#f3f7ff", fg="#26376f").pack(side="left")
        self.message = tk.Label(header, text="选择一支箭头", font=("Arial", 11), bg="#f3f7ff", fg="#6d7898")
        self.message.pack(side="right")
        content = tk.Frame(self.page, bg="#f3f7ff")
        content.pack()
        width = BOARD_LEFT * 2 + CELL * BOARD_SIZE
        height = BOARD_TOP + CELL * BOARD_SIZE + 24
        self.canvas = tk.Canvas(content, width=width, height=height, bg="white", highlightthickness=0)
        self.canvas.pack(side="left")
        panel = tk.Frame(content, bg="white", padx=20, pady=18)
        panel.pack(side="left", fill="y", padx=(14, 0))
        tk.Label(panel, text="本关信息", font=("Arial", 15, "bold"), bg="white", fg="#26376f").pack(anchor="w")
        self.left_label = tk.Label(panel, font=("Arial", 12), bg="white", fg="#3d4a68")
        self.left_label.pack(anchor="w", pady=(26, 9))
        self.chance_label = tk.Label(panel, font=("Arial", 12), bg="white", fg="#3d4a68")
        self.chance_label.pack(anchor="w", pady=(0, 24))
        tk.Label(panel, text="提示：先找前方
没有障碍的箭头。", bg="white", fg="#8792ac", font=("Arial", 10), justify="left").pack(anchor="w", pady=(0, 20))
        self.button(panel, "重新本关", self.show_game, "#71809e").pack(anchor="w")
        self.button(panel, "回到首页", self.show_home, "#71809e").pack(anchor="w", pady=(10, 0))
        self.canvas.bind("<Button-1>", self.click_board)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        self.canvas.create_text(BOARD_LEFT, 52, text="让箭头找到出口", anchor="w", font=("Arial", 17, "bold"), fill="#26376f")
        self.canvas.create_text(BOARD_LEFT, 77, text="点击后它会朝箭头方向前进", anchor="w", font=("Arial", 10), fill="#8b96b8")
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                x = BOARD_LEFT + column * CELL
                y = BOARD_TOP + row * CELL
                self.canvas.create_rectangle(x, y, x + CELL, y + CELL, fill="#f7f9ff", outline="#dce4f5")
        for arrow in self.puzzle.arrows:
            self.draw_arrow(arrow)
        self.refresh_side()

    def draw_arrow(self, arrow):
        x = BOARD_LEFT + arrow.column * CELL + CELL // 2
        y = BOARD_TOP + arrow.row * CELL + CELL // 2
        tag = self.arrow_tag(arrow)
        self.canvas.create_oval(x - 25, y - 25, x + 25, y + 25, fill=COLORS[arrow.symbol], outline="", tags=tag)
        self.canvas.create_text(x, y - 1, text=arrow.symbol, fill="white", font=("Arial", 26, "bold"), tags=tag)

    def arrow_tag(self, arrow):
        return f"arrow-{arrow.row}-{arrow.column}"

    def refresh_side(self):
        self.left_label.config(text=f"剩余箭头：{len(self.puzzle.arrows)}")
        used = STARTING_CHANCES - self.puzzle.chances
        self.chance_label.config(text=f"剩余机会：{'● ' * self.puzzle.chances}{'○ ' * used}")

    def click_board(self, event):
        if self.busy:
            return
        column = (event.x - BOARD_LEFT) // CELL
        row = (event.y - BOARD_TOP) // CELL
        if not (0 <= row < BOARD_SIZE and 0 <= column < BOARD_SIZE):
            return
        result = self.puzzle.choose(row, column)
        if result is None:
            self.message.config(text="这里没有箭头")
        elif result.status == "blocked":
            self.show_collision(result.arrow)
            self.refresh_side()
            if self.puzzle.is_lost:
                self.root.after(720, lambda: self.show_result(False))
        else:
            self.message.config(text="路线畅通，正在离场！", fg="#16836d")
            self.fly_out(result.arrow)

    def show_collision(self, arrow, hide_after=650):
        self.message.config(text="前方被挡住了，少一次机会", fg="#d4475a")
        x = BOARD_LEFT + arrow.column * CELL + 5
        y = BOARD_TOP + arrow.row * CELL + 5
        border = self.canvas.create_rectangle(x, y, x + CELL - 10, y + CELL - 10, outline="#ef5f72", width=4)
        self.canvas.create_text(x + CELL // 2 - 5, y + CELL // 2 - 2, text="×", fill="#ef5f72", font=("Arial", 32, "bold"), tags="warning")
        if hide_after is not None:
            self.root.after(hide_after, lambda: self.canvas.delete(border, "warning"))

    def fly_out(self, arrow):
        self.busy = True
        tag = self.arrow_tag(arrow)
        dr, dc = STEP[arrow.symbol]
        def move(frame=0):
            if frame < 17:
                self.canvas.move(tag, dc * 12, dr * 12)
                self.root.after(20, lambda: move(frame + 1))
                return
            self.canvas.delete(tag)
            self.refresh_side()
            self.busy = False
            if self.puzzle.is_cleared:
                self.show_result(True)
            else:
                self.message.config(text="做得好，继续寻找出口", fg="#6d7898")
        move()

    def show_result(self, won):
        self.clean()
        card = tk.Frame(self.page, bg="white", padx=56, pady=38)
        card.pack()
        if won:
            title, color = "本关完成！", "#16836d"
            detail = f"你成功让第 {self.level + 1} 关的全部箭头离开棋盘。"
        else:
            title, color = "本关暂停", "#d4475a"
            detail = "三次机会都用完了，重新观察箭头前方的路线吧。"
        tk.Label(card, text=title, font=("Arial", 29, "bold"), bg="white", fg=color).pack()
        tk.Label(card, text=detail, font=("Arial", 12), bg="white", fg="#596681", wraplength=380).pack(pady=(14, 26))
        choices = tk.Frame(card, bg="white")
        choices.pack()
        if won and self.level < len(STAGES) - 1:
            self.button(choices, "下一关", self.next_level).pack(side="left", padx=5)
        elif won:
            self.button(choices, "完成全部关卡", self.show_home).pack(side="left", padx=5)
        self.button(choices, "再试一次", self.show_game, "#71809e").pack(side="left", padx=5)

    def next_level(self):
        self.level += 1
        self.show_game()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", choices=["welcome", "game", "blocked", "pass"])
    GameApp(parser.parse_args().demo).run()
