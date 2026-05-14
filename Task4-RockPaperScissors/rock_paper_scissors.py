"""
╔══════════════════════════════════════════════════╗
║      ROCK  PAPER  SCISSORS  —  GUI  Edition      ║
║      Built with Python + Tkinter                 ║
║      Internship Task 4                           ║
╚══════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import random


# ─────────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────────

CHOICES = ["Rock", "Paper", "Scissors"]

EMOJIS = {
    "Rock":     "🪨",
    "Paper":    "📄",
    "Scissors": "✂️"
}

RULES = {
    "Rock":     "Scissors",
    "Scissors": "Paper",
    "Paper":    "Rock"
}

# ── Palette ──
BG          = "#0f0e17"
CARD        = "#1a1830"
BORDER      = "#2a2840"
TEXT        = "#f0ede8"
DIM         = "#6b6880"
PURPLE      = "#c8b4f8"
PINK        = "#f8b4c8"
GREEN       = "#b4f8c8"
YELLOW      = "#f5f0a8"
BTN_ROCK    = "#c8b4f8"
BTN_PAPER   = "#a8d8f8"
BTN_SCISSOR = "#f8c8a8"


# ─────────────────────────────────────────────────
#  GAME LOGIC  (pure functions, no UI dependency)
# ─────────────────────────────────────────────────

def computer_pick():
    return random.choice(CHOICES)


def decide_winner(player, computer):
    """Return 'player', 'computer', or 'tie'."""
    if player == computer:
        return "tie"
    return "player" if RULES[player] == computer else "computer"


# ─────────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────────

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Rock · Paper · Scissors")
        self.geometry("500x750")
        self.resizable(False, False)
        self.configure(bg=BG)

        # scores
        self.p_score  = 0
        self.c_score  = 0
        self.ties     = 0
        self.rounds   = 0

        self._fonts()
        self._build()

    # ── fonts ──────────────────────────────────

    def _fonts(self):
        self.f_title  = tkfont.Font(family="Helvetica", size=20, weight="bold")
        self.f_sub    = tkfont.Font(family="Helvetica", size=10)
        self.f_emoji  = tkfont.Font(family="Helvetica", size=48)
        self.f_label  = tkfont.Font(family="Helvetica", size=9)
        self.f_score  = tkfont.Font(family="Helvetica", size=34, weight="bold")
        self.f_result = tkfont.Font(family="Helvetica", size=14, weight="bold")
        self.f_btn    = tkfont.Font(family="Helvetica", size=13, weight="bold")
        self.f_small  = tkfont.Font(family="Helvetica", size=10)

    # ── full UI build ───────────────────────────

    def _build(self):
        pad = dict(padx=20)

        # ── header ──
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", pady=(24, 0), **pad)

        tk.Label(header, text="ROCK · PAPER · SCISSORS",
                 font=self.f_title, bg=BG, fg=TEXT).pack()
        tk.Label(header, text="Choose your move and beat the computer",
                 font=self.f_sub, bg=BG, fg=DIM).pack(pady=(2, 0))

        self._divider()

        # ── scoreboard ──
        self._scoreboard()

        self._divider()

        # ── arena (emoji display) ──
        self._arena()

        # ── result banner ──
        self.result_var = tk.StringVar(value="Make your move below ↓")
        self.result_lbl = tk.Label(self, textvariable=self.result_var,
                                   font=self.f_result, bg=CARD, fg=DIM,
                                   pady=12, relief="flat")
        self.result_lbl.pack(fill="x", padx=20, pady=(0, 14))

        # ── choice buttons ──
        self._choice_buttons()

        self._divider()

        # ── action buttons ──
        self._action_buttons()

        # ── footer ──
        tk.Label(self, text="Rock beats Scissors  ·  Scissors beats Paper  ·  Paper beats Rock",
                 font=self.f_label, bg=BG, fg=DIM).pack(pady=(10, 4))

    # ── scoreboard section ──────────────────────

    def _scoreboard(self):
        frame = tk.Frame(self, bg=CARD, bd=0, relief="flat")
        frame.pack(fill="x", padx=20, pady=8)

        cols = [
            ("👤 YOU",      "p_score_var", PURPLE),
            ("🎮 ROUNDS",   "rounds_var",  DIM),
            ("🤖 COMPUTER", "c_score_var", PINK),
        ]

        for i, (label, var_name, color) in enumerate(cols):
            col = tk.Frame(frame, bg=CARD)
            col.grid(row=0, column=i, padx=10, pady=14, sticky="nsew")
            frame.columnconfigure(i, weight=1)

            var = tk.StringVar(value="0")
            setattr(self, var_name, var)

            tk.Label(col, text=label, font=self.f_label,
                     bg=CARD, fg=DIM).pack()
            tk.Label(col, textvariable=var, font=self.f_score,
                     bg=CARD, fg=color).pack()

        # ties row
        ties_frame = tk.Frame(frame, bg=CARD)
        ties_frame.grid(row=1, column=0, columnspan=3, pady=(0, 10))
        self.ties_var = tk.StringVar(value="Ties: 0")
        tk.Label(ties_frame, textvariable=self.ties_var,
                 font=self.f_label, bg=CARD, fg=DIM).pack()

    # ── arena ───────────────────────────────────

    def _arena(self):
        arena = tk.Frame(self, bg=BG)
        arena.pack(fill="x", padx=20, pady=6)
        arena.columnconfigure(0, weight=1)
        arena.columnconfigure(1, weight=0)
        arena.columnconfigure(2, weight=1)

        # player side
        self.p_card = tk.Frame(arena, bg=CARD, bd=0)
        self.p_card.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        tk.Label(self.p_card, text="YOU", font=self.f_label,
                 bg=CARD, fg=DIM).pack(pady=(10, 0))
        self.p_emoji = tk.Label(self.p_card, text="❓", font=self.f_emoji,
                                bg=CARD, fg=TEXT)
        self.p_emoji.pack(pady=6)
        self.p_name = tk.Label(self.p_card, text="—", font=self.f_small,
                               bg=CARD, fg=DIM)
        self.p_name.pack(pady=(0, 10))

        # vs
        tk.Label(arena, text="VS", font=self.f_btn,
                 bg=BG, fg=BORDER).grid(row=0, column=1, padx=6)

        # computer side
        self.c_card = tk.Frame(arena, bg=CARD, bd=0)
        self.c_card.grid(row=0, column=2, sticky="nsew", padx=(6, 0))
        tk.Label(self.c_card, text="COMPUTER", font=self.f_label,
                 bg=CARD, fg=DIM).pack(pady=(10, 0))
        self.c_emoji = tk.Label(self.c_card, text="❓", font=self.f_emoji,
                                bg=CARD, fg=TEXT)
        self.c_emoji.pack(pady=6)
        self.c_name = tk.Label(self.c_card, text="—", font=self.f_small,
                               bg=CARD, fg=DIM)
        self.c_name.pack(pady=(0, 10))

    # ── choice buttons ──────────────────────────

    def _choice_buttons(self):
        lbl = tk.Label(self, text="— SELECT YOUR MOVE —",
                       font=self.f_label, bg=BG, fg=DIM)
        lbl.pack(pady=(4, 8))

        frame = tk.Frame(self, bg=BG)
        frame.pack(padx=20, pady=(0, 6))

        colors = [BTN_ROCK, BTN_PAPER, BTN_SCISSOR]
        for i, choice in enumerate(CHOICES):
            btn = tk.Button(
                frame,
                text=f"{EMOJIS[choice]}\n{choice}",
                font=self.f_btn,
                bg=colors[i],
                fg="#1a1830",
                activebackground=colors[i],
                activeforeground="#1a1830",
                width=7,
                height=3,
                bd=0,
                cursor="hand2",
                relief="flat",
                command=lambda c=choice: self._play(c)
            )
            btn.grid(row=0, column=i, padx=8)
            btn.bind("<Enter>", lambda e, b=btn, col=colors[i]: b.config(bg=self._lighten(col)))
            btn.bind("<Leave>", lambda e, b=btn, col=colors[i]: b.config(bg=col))

    # ── action buttons ───────────────────────────

    def _action_buttons(self):
        frame = tk.Frame(self, bg=BG)
        frame.pack(pady=10, padx=20, fill="x")

        tk.Button(frame, text="🔄  Reset Scores",
                  font=self.f_small, bg=CARD, fg=DIM,
                  activebackground=BORDER, activeforeground=TEXT,
                  bd=0, cursor="hand2", relief="flat", padx=12, pady=8,
                  command=self._reset).pack(side="left", expand=True, fill="x", padx=(0, 6))

        tk.Button(frame, text="📊  View Stats",
                  font=self.f_small, bg=CARD, fg=DIM,
                  activebackground=BORDER, activeforeground=TEXT,
                  bd=0, cursor="hand2", relief="flat", padx=12, pady=8,
                  command=self._show_stats).pack(side="left", expand=True, fill="x", padx=(6, 0))

    # ── divider ─────────────────────────────────

    def _divider(self):
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=20, pady=6)

    # ─────────────────────────────────────────────
    #  GAME ACTIONS
    # ─────────────────────────────────────────────

    def _play(self, player_choice):
        """Run one full round."""
        cpu = computer_pick()
        winner = decide_winner(player_choice, cpu)

        self.rounds += 1

        # update arena display
        self.p_emoji.config(text=EMOJIS[player_choice])
        self.p_name.config(text=player_choice, fg=TEXT)
        self.c_emoji.config(text=EMOJIS[cpu])
        self.c_name.config(text=cpu, fg=TEXT)

        # highlight winner card
        self.p_card.config(bg=CARD)
        self.c_card.config(bg=CARD)

        if winner == "player":
            self.p_score += 1
            self.p_card.config(bg="#1e1a38")
            self._set_result(f"🏆  You WIN!  {EMOJIS[player_choice]} beats {EMOJIS[cpu]}", GREEN)
        elif winner == "computer":
            self.c_score += 1
            self.c_card.config(bg="#2a1a28")
            self._set_result(f"💻  Computer WINS!  {EMOJIS[cpu]} beats {EMOJIS[player_choice]}", PINK)
        else:
            self.ties += 1
            self._set_result(f"🤝  It's a TIE!  Both chose {EMOJIS[player_choice]}", YELLOW)

        self._refresh_scores()

    def _set_result(self, text, color):
        self.result_var.set(text)
        self.result_lbl.config(fg=color, bg=CARD)

    def _refresh_scores(self):
        self.p_score_var.set(str(self.p_score))
        self.c_score_var.set(str(self.c_score))
        self.rounds_var.set(str(self.rounds))
        self.ties_var.set(f"Ties: {self.ties}")

    def _reset(self):
        confirm = messagebox.askyesno(
            "Reset Scores",
            "Are you sure you want to reset all scores?",
            icon="warning"
        )
        if confirm:
            self.p_score = 0
            self.c_score = 0
            self.ties    = 0
            self.rounds  = 0
            self._refresh_scores()
            self.p_emoji.config(text="❓")
            self.p_name.config(text="—", fg=DIM)
            self.c_emoji.config(text="❓")
            self.c_name.config(text="—", fg=DIM)
            self.p_card.config(bg=CARD)
            self.c_card.config(bg=CARD)
            self.result_var.set("Make your move below ↓")
            self.result_lbl.config(fg=DIM, bg=CARD)

    def _show_stats(self):
        if self.rounds == 0:
            messagebox.showinfo("Stats", "No rounds played yet!\nMake a move first.")
            return

        win_rate = (self.p_score / self.rounds) * 100
        cpu_rate = (self.c_score / self.rounds) * 100

        if self.p_score > self.c_score:
            overall = "🥇 You are WINNING overall!"
        elif self.c_score > self.p_score:
            overall = "🤖 Computer is WINNING overall!"
        else:
            overall = "🤝 It's EVEN overall!"

        stats = (
            f"📊  GAME STATISTICS\n"
            f"{'─' * 30}\n"
            f"Total Rounds     :  {self.rounds}\n"
            f"Your Wins        :  {self.p_score}  ({win_rate:.1f}%)\n"
            f"Computer Wins    :  {self.c_score}  ({cpu_rate:.1f}%)\n"
            f"Ties             :  {self.ties}\n"
            f"{'─' * 30}\n"
            f"{overall}"
        )
        messagebox.showinfo("Game Statistics", stats)

    # ── helper ───────────────────────────────────

    def _lighten(self, hex_color):
        """Return a slightly lighter version of a hex color for hover effect."""
        r = min(255, int(hex_color[1:3], 16) + 20)
        g = min(255, int(hex_color[3:5], 16) + 20)
        b = min(255, int(hex_color[5:7], 16) + 20)
        return f"#{r:02x}{g:02x}{b:02x}"


# ─────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()
