import tkinter as tk
from tkinter import font
import random
import string
import pyperclip


# ──────────────────────────────────────────────
#  Colour palette  (matches the demo screenshot)
# ──────────────────────────────────────────────
BG_OUTER   = "#0a0a1a"   # almost-black starfield
BG_CARD    = "#1a1a3e"   # dark-navy card
BG_FIELD   = "#12122a"   # darker field inside card
BG_BTN     = "#7c3aed"   # purple generate button
BG_BTN_HOV = "#6d28d9"
ON_COLOR   = "#6366f1"   # indigo toggle ON
OFF_COLOR  = "#4b5563"   # grey toggle OFF
FG_WHITE   = "#ffffff"
FG_GREY    = "#9ca3af"
FG_LABEL   = "#cbd5e1"
SLIDER_ACT = "#6366f1"


# ──────────────────────────────────────────────
#  Custom Toggle Switch widget
# ──────────────────────────────────────────────
class ToggleSwitch(tk.Canvas):
    WIDTH  = 46
    HEIGHT = 24
    RADIUS = 12

    def __init__(self, parent, initial=True, command=None, **kwargs):
        super().__init__(
            parent,
            width=self.WIDTH,
            height=self.HEIGHT,
            bg=BG_CARD,
            highlightthickness=0,
            **kwargs
        )
        self._on      = initial
        self._command = command
        self._draw()
        self.bind("<Button-1>", self._toggle)

    # ── drawing ──────────────────────────────
    def _draw(self):
        self.delete("all")
        color = ON_COLOR if self._on else OFF_COLOR

        # track (rounded rectangle via arc + rectangle trick)
        r = self.RADIUS
        w = self.WIDTH
        h = self.HEIGHT
        self.create_arc(0, 0, h, h, start=90, extent=180, fill=color, outline=color)
        self.create_arc(w-h, 0, w, h, start=270, extent=180, fill=color, outline=color)
        self.create_rectangle(r, 0, w-r, h, fill=color, outline=color)

        # knob position
        if self._on:
            cx = w - r
        else:
            cx = r
        self.create_oval(cx-r+3, 3, cx+r-3, h-3, fill=FG_WHITE, outline=FG_WHITE)

    # ── interaction ──────────────────────────
    def _toggle(self, _event=None):
        self._on = not self._on
        self._draw()
        if self._command:
            self._command(self._on)

    def get(self):
        return self._on

    def set(self, value: bool):
        self._on = value
        self._draw()


# ──────────────────────────────────────────────
#  Main Application
# ──────────────────────────────────────────────
class PasswordGeneratorApp:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Password Generator")
        self.root.configure(bg=BG_OUTER)
        self.root.resizable(False, False)

        # ── fonts ────────────────────────────
        self.f_title  = font.Font(family="Segoe UI", size=20, weight="bold")
        self.f_sub    = font.Font(family="Segoe UI", size=11)
        self.f_card   = font.Font(family="Segoe UI", size=13, weight="bold")
        self.f_label  = font.Font(family="Segoe UI", size=10)
        self.f_btn    = font.Font(family="Segoe UI", size=11, weight="bold")
        self.f_pwd    = font.Font(family="Consolas",  size=12, weight="bold")
        self.f_tiny   = font.Font(family="Segoe UI", size=9)

        # ── state ────────────────────────────
        self.length_var  = tk.IntVar(value=16)
        self.password_var = tk.StringVar(value="")
        self.copied_var  = tk.StringVar(value="")

        self._build_ui()
        self._center_window(520, 660)

    # ── layout ───────────────────────────────
    def _build_ui(self):
        # outer wrapper (starfield feel via padding)
        outer = tk.Frame(self.root, bg=BG_OUTER, padx=30, pady=20)
        outer.pack(fill="both", expand=True)

        # page title
        tk.Label(
            outer, text="Password Generator",
            font=self.f_title, bg=BG_OUTER, fg=FG_WHITE
        ).pack(pady=(10, 20))

        # ── CARD ─────────────────────────────
        card = tk.Frame(outer, bg=BG_CARD, padx=24, pady=22,
                        relief="flat", bd=0)
        card.pack(fill="x", padx=0)

        tk.Label(
            card, text="Password Generator",
            font=self.f_card, bg=BG_CARD, fg=FG_WHITE
        ).pack(anchor="w", pady=(0, 12))

        # ── password output field ────────────
        field_frame = tk.Frame(card, bg=BG_FIELD, pady=10, padx=12)
        field_frame.pack(fill="x", pady=(0, 14))

        self.pwd_label = tk.Label(
            field_frame,
            textvariable=self.password_var,
            font=self.f_pwd,
            bg=BG_FIELD,
            fg=FG_WHITE,
            wraplength=380,
            justify="center",
            cursor="hand2"
        )
        self.pwd_label.pack(side="left", expand=True)
        self.pwd_label.bind("<Button-1>", self._copy_password)

        self.copy_hint = tk.Label(
            field_frame,
            textvariable=self.copied_var,
            font=self.f_tiny,
            bg=BG_FIELD,
            fg=ON_COLOR
        )
        self.copy_hint.pack(side="right", padx=(4, 0))

        # placeholder
        self.password_var.set("CLICK GENERATE")

        # ── length section ───────────────────
        len_row = tk.Frame(card, bg=BG_CARD)
        len_row.pack(fill="x", pady=(0, 4))

        tk.Label(
            len_row, text="LENGTH: ",
            font=self.f_label, bg=BG_CARD, fg=FG_GREY
        ).pack(side="left")

        self.len_display = tk.Label(
            len_row,
            textvariable=self.length_var,
            font=font.Font(family="Segoe UI", size=10, weight="bold"),
            bg=BG_CARD,
            fg=ON_COLOR
        )
        self.len_display.pack(side="left")

        # slider row
        slider_row = tk.Frame(card, bg=BG_CARD)
        slider_row.pack(fill="x", pady=(2, 14))

        tk.Label(slider_row, text="4",  font=self.f_label,
                 bg=BG_CARD, fg=FG_GREY).pack(side="left")

        self.slider = tk.Scale(
            slider_row,
            from_=4, to=32,
            orient="horizontal",
            variable=self.length_var,
            showvalue=False,
            bg=BG_CARD,
            fg=FG_WHITE,
            troughcolor=OFF_COLOR,
            activebackground=ON_COLOR,
            highlightthickness=0,
            bd=0,
            sliderrelief="flat",
            length=280
        )
        self.slider.pack(side="left", padx=8, expand=True, fill="x")

        tk.Label(slider_row, text="32", font=self.f_label,
                 bg=BG_CARD, fg=FG_GREY).pack(side="right")

        # ── settings section ─────────────────
        tk.Label(
            card, text="SETTINGS",
            font=self.f_tiny, bg=BG_CARD, fg=FG_GREY
        ).pack(anchor="w", pady=(4, 6))

        settings_box = tk.Frame(card, bg=BG_CARD)
        settings_box.pack(fill="x")

        self.toggle_upper  = self._setting_row(settings_box, "Include Uppercase",  True)
        self.toggle_lower  = self._setting_row(settings_box, "Include Lowercase",  True)
        self.toggle_digits = self._setting_row(settings_box, "Include Numbers",    True)
        self.toggle_symbols= self._setting_row(settings_box, "Include Symbols",    False)

        # ── generate button ──────────────────
        self.gen_btn = tk.Button(
            card,
            text="GENERATE PASSWORD",
            font=self.f_btn,
            bg=BG_BTN,
            fg=FG_WHITE,
            activebackground=BG_BTN_HOV,
            activeforeground=FG_WHITE,
            relief="flat",
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2",
            command=self.generate_password
        )
        self.gen_btn.pack(fill="x", pady=(18, 0))
        self.gen_btn.bind("<Enter>", lambda e: self.gen_btn.config(bg=BG_BTN_HOV))
        self.gen_btn.bind("<Leave>", lambda e: self.gen_btn.config(bg=BG_BTN))

        # ── bottom tagline ───────────────────
        tk.Label(
            outer,
            text="Generate random passwords with one click.",
            font=self.f_sub,
            bg=BG_OUTER,
            fg=FG_GREY
        ).pack(pady=(22, 6))

    # ── helper: one toggle row ────────────────
    def _setting_row(self, parent, label_text, default_on):
        row = tk.Frame(parent, bg="#23234a", pady=8, padx=12)
        row.pack(fill="x", pady=3)

        tk.Label(
            row, text=label_text,
            font=self.f_sub, bg="#23234a", fg=FG_LABEL
        ).pack(side="left")

        toggle = ToggleSwitch(row, initial=default_on)
        toggle.configure(bg="#23234a")
        toggle.pack(side="right")

        return toggle

    # ── password generation ───────────────────
    def generate_password(self):
        length = self.length_var.get()

        charset = ""
        guaranteed = []

        if self.toggle_upper.get():
            charset   += string.ascii_uppercase
            guaranteed.append(random.choice(string.ascii_uppercase))

        if self.toggle_lower.get():
            charset   += string.ascii_lowercase
            guaranteed.append(random.choice(string.ascii_lowercase))

        if self.toggle_digits.get():
            charset   += string.digits
            guaranteed.append(random.choice(string.digits))

        if self.toggle_symbols.get():
            symbols    = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            charset   += symbols
            guaranteed.append(random.choice(symbols))

        if not charset:
            self.password_var.set("Enable at least one option!")
            self.copied_var.set("")
            return

        # fill remaining positions randomly
        remaining = length - len(guaranteed)
        if remaining < 0:
            remaining = 0
            guaranteed = guaranteed[:length]

        password_chars = guaranteed + [random.choice(charset) for _ in range(remaining)]
        random.shuffle(password_chars)

        self.password_var.set("".join(password_chars))
        self.copied_var.set("")
        self._flash_btn()

    # ── copy on click ─────────────────────────
    def _copy_password(self, _event=None):
        pwd = self.password_var.get()
        if pwd and pwd != "CLICK GENERATE":
            try:
                pyperclip.copy(pwd)
                self.copied_var.set("✓ Copied!")
                self.root.after(2000, lambda: self.copied_var.set(""))
            except Exception:
                self.copied_var.set("(install pyperclip to copy)")

    # ── brief button flash animation ──────────
    def _flash_btn(self):
        self.gen_btn.config(bg="#4f46e5")
        self.root.after(150, lambda: self.gen_btn.config(bg=BG_BTN))

    # ── centre the window on screen ──────────
    def _center_window(self, w, h):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x  = (sw - w) // 2
        y  = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")


# ──────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = PasswordGeneratorApp(root)
    root.mainloop()
