import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import os
import re

# ─────────────────────────────────────────────
#  Data file path
# ─────────────────────────────────────────────
DATA_FILE = "contacts.json"

# ─────────────────────────────────────────────
#  Colour palette
# ─────────────────────────────────────────────
BG_DARK      = "#1e1e2e"
BG_CARD      = "#2a2a3e"
BG_ENTRY     = "#32324a"
ACCENT       = "#7c6aff"
ACCENT_LIGHT = "#a594ff"
ACCENT_HOVER = "#9d8fff"
TEXT_WHITE   = "#f0f0f8"
TEXT_GREY    = "#9898b0"
BTN_RED      = "#e05c6a"
BTN_RED_H    = "#f07080"
BTN_GREEN    = "#4caf7d"
BTN_GREEN_H  = "#5dc990"
BTN_BLUE     = "#4a90d9"
BTN_BLUE_H   = "#5aa8f0"
BORDER       = "#3c3c58"


# ─────────────────────────────────────────────
#  Persistence helpers
# ─────────────────────────────────────────────
def load_contacts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_contacts(contacts):
    with open(DATA_FILE, "w") as f:
        json.dump(contacts, f, indent=4)


# ─────────────────────────────────────────────
#  Validation helpers
# ─────────────────────────────────────────────
def validate_phone(phone):
    return re.fullmatch(r"[\d\s\-\+\(\)]{7,15}", phone) is not None


def validate_email(email):
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) is not None


# ─────────────────────────────────────────────
#  Rounded button helper
# ─────────────────────────────────────────────
def make_button(parent, text, command, bg, hover_bg, width=14):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=TEXT_WHITE,
        activebackground=hover_bg,
        activeforeground=TEXT_WHITE,
        font=("Segoe UI", 10, "bold"),
        bd=0,
        padx=12,
        pady=8,
        cursor="hand2",
        width=width,
        relief="flat",
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn


# ═════════════════════════════════════════════
#  Main Application
# ═════════════════════════════════════════════
class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📒  Contact Book")
        self.root.geometry("1050x680")
        self.root.minsize(900, 580)
        self.root.configure(bg=BG_DARK)

        self.contacts = load_contacts()
        self.selected_index = None   # index into self.contacts for the highlighted row

        self._build_ui()
        self._refresh_list()

    # ─── UI skeleton ──────────────────────────
    def _build_ui(self):
        # ── Header bar ──────────────────────
        header = tk.Frame(self.root, bg=ACCENT, height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📒  Contact Book",
            bg=ACCENT,
            fg=TEXT_WHITE,
            font=("Segoe UI", 18, "bold"),
        ).pack(side="left", padx=24, pady=10)

        tk.Label(
            header,
            text="Manage your contacts easily",
            bg=ACCENT,
            fg="#d0ccff",
            font=("Segoe UI", 10),
        ).pack(side="left", pady=10)

        # ── Body frame ──────────────────────
        body = tk.Frame(self.root, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=18, pady=14)

        # Left panel: list + search
        self._build_left_panel(body)

        # Right panel: form
        self._build_right_panel(body)

    # ─── Left panel ───────────────────────────
    def _build_left_panel(self, parent):
        left = tk.Frame(parent, bg=BG_CARD, bd=0, relief="flat")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Search bar
        search_frame = tk.Frame(left, bg=BG_CARD)
        search_frame.pack(fill="x", padx=14, pady=(14, 8))

        tk.Label(
            search_frame,
            text="🔍  Search",
            bg=BG_CARD,
            fg=TEXT_GREY,
            font=("Segoe UI", 10),
        ).pack(anchor="w")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._refresh_list())

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            bg=BG_ENTRY,
            fg=TEXT_WHITE,
            insertbackground=TEXT_WHITE,
            font=("Segoe UI", 11),
            bd=0,
            relief="flat",
        )
        search_entry.pack(fill="x", ipady=7, pady=(4, 0))
        tk.Frame(search_frame, bg=ACCENT, height=2).pack(fill="x")

        # Contact count label
        self.count_var = tk.StringVar(value="0 contacts")
        tk.Label(
            left,
            textvariable=self.count_var,
            bg=BG_CARD,
            fg=TEXT_GREY,
            font=("Segoe UI", 9),
        ).pack(anchor="w", padx=14)

        # Treeview
        tree_frame = tk.Frame(left, bg=BG_CARD)
        tree_frame.pack(fill="both", expand=True, padx=14, pady=(6, 10))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.Treeview",
            background=BG_ENTRY,
            foreground=TEXT_WHITE,
            rowheight=36,
            fieldbackground=BG_ENTRY,
            bordercolor=BORDER,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Custom.Treeview.Heading",
            background=ACCENT,
            foreground=TEXT_WHITE,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
        )
        style.map(
            "Custom.Treeview",
            background=[("selected", ACCENT)],
            foreground=[("selected", TEXT_WHITE)],
        )

        columns = ("Name", "Phone")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            selectmode="browse",
        )
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.column("Name", width=180, anchor="w")
        self.tree.column("Phone", width=140, anchor="w")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        # Bottom buttons under the list
        btn_row = tk.Frame(left, bg=BG_CARD)
        btn_row.pack(fill="x", padx=14, pady=(0, 12))

        make_button(btn_row, "➕  Add New", self._clear_form, BTN_GREEN, BTN_GREEN_H, 13).pack(side="left", padx=(0, 6))
        make_button(btn_row, "🗑  Delete", self._delete_contact, BTN_RED, BTN_RED_H, 13).pack(side="left")

    # ─── Right panel ──────────────────────────
    def _build_right_panel(self, parent):
        right = tk.Frame(parent, bg=BG_CARD, width=340)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        tk.Label(
            right,
            text="Contact Details",
            bg=BG_CARD,
            fg=ACCENT_LIGHT,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=20, pady=(18, 4))

        tk.Frame(right, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(0, 14))

        self.fields = {}
        field_defs = [
            ("Full Name *",    "name",    "👤"),
            ("Phone Number *", "phone",   "📞"),
            ("Email Address",  "email",   "📧"),
            ("Address",        "address", "🏠"),
        ]

        for label_text, key, icon in field_defs:
            self._build_field(right, label_text, key, icon)

        # Action buttons
        btn_frame = tk.Frame(right, bg=BG_CARD)
        btn_frame.pack(fill="x", padx=20, pady=(18, 0))

        make_button(btn_frame, "💾  Save Contact", self._save_contact, ACCENT, ACCENT_HOVER, 16).pack(fill="x", pady=(0, 8))
        make_button(btn_frame, "✏️  Update",       self._update_contact, BTN_BLUE, BTN_BLUE_H, 16).pack(fill="x", pady=(0, 8))
        make_button(btn_frame, "🔄  Clear Form",   self._clear_form,    BG_ENTRY, BORDER, 16).pack(fill="x")

        # Status bar
        self.status_var = tk.StringVar(value="Ready  ✔")
        tk.Label(
            right,
            textvariable=self.status_var,
            bg=BG_CARD,
            fg=BTN_GREEN,
            font=("Segoe UI", 9, "italic"),
        ).pack(anchor="w", padx=20, pady=(16, 0))

    def _build_field(self, parent, label_text, key, icon):
        frame = tk.Frame(parent, bg=BG_CARD)
        frame.pack(fill="x", padx=20, pady=(0, 12))

        tk.Label(
            frame,
            text=f"{icon}  {label_text}",
            bg=BG_CARD,
            fg=TEXT_GREY,
            font=("Segoe UI", 9),
        ).pack(anchor="w")

        entry = tk.Entry(
            frame,
            bg=BG_ENTRY,
            fg=TEXT_WHITE,
            insertbackground=TEXT_WHITE,
            font=("Segoe UI", 11),
            bd=0,
            relief="flat",
        )
        entry.pack(fill="x", ipady=7, pady=(3, 0))
        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x")
        entry.bind("<FocusIn>",  lambda e, f=frame: f.winfo_children()[-1].config(bg=ACCENT))
        entry.bind("<FocusOut>", lambda e, f=frame: f.winfo_children()[-1].config(bg=BORDER))

        self.fields[key] = entry

    # ─── Refresh list ─────────────────────────
    def _refresh_list(self):
        query = self.search_var.get().strip().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)

        shown = 0
        for i, c in enumerate(self.contacts):
            if query and query not in c["name"].lower() and query not in c["phone"]:
                continue
            tag = "even" if shown % 2 == 0 else "odd"
            self.tree.insert("", "end", iid=str(i), values=(c["name"], c["phone"]), tags=(tag,))
            shown += 1

        self.tree.tag_configure("even", background=BG_ENTRY)
        self.tree.tag_configure("odd",  background="#2e2e46")
        self.count_var.set(f"{shown} contact{'s' if shown != 1 else ''}")

    # ─── Tree selection ───────────────────────
    def _on_select(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        self.selected_index = int(sel[0])
        c = self.contacts[self.selected_index]
        for key in ("name", "phone", "email", "address"):
            self.fields[key].delete(0, "end")
            self.fields[key].insert(0, c.get(key, ""))
        self._set_status("Contact loaded  ✔", BTN_GREEN)

    # ─── Form helpers ─────────────────────────
    def _get_form_data(self):
        return {k: v.get().strip() for k, v in self.fields.items()}

    def _clear_form(self):
        for entry in self.fields.values():
            entry.delete(0, "end")
        self.selected_index = None
        self.tree.selection_remove(self.tree.selection())
        self._set_status("Form cleared", TEXT_GREY)

    def _set_status(self, msg, colour=BTN_GREEN):
        self.status_var.set(msg)
        # find the status label and recolour it
        for widget in self.root.winfo_children():
            self._recolour_label(widget, self.status_var, colour)

    def _recolour_label(self, widget, var, colour):
        if isinstance(widget, tk.Label) and widget.cget("textvariable") == str(var):
            widget.config(fg=colour)
        for child in widget.winfo_children():
            self._recolour_label(child, var, colour)

    # ─── CRUD operations ──────────────────────
    def _save_contact(self):
        data = self._get_form_data()

        if not data["name"]:
            messagebox.showwarning("Missing Field", "Please enter the contact's name.")
            return
        if not data["phone"]:
            messagebox.showwarning("Missing Field", "Please enter the phone number.")
            return
        if not validate_phone(data["phone"]):
            messagebox.showwarning("Invalid Phone", "Phone number contains invalid characters.\nUse digits, spaces, +, -, or parentheses (7–15 chars).")
            return
        if data["email"] and not validate_email(data["email"]):
            messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
            return

        # Check for duplicate phone
        for c in self.contacts:
            if c["phone"] == data["phone"]:
                messagebox.showwarning("Duplicate", f"A contact with phone {data['phone']} already exists.")
                return

        self.contacts.append(data)
        save_contacts(self.contacts)
        self._refresh_list()
        self._clear_form()
        self._set_status(f"'{data['name']}' saved  ✔", BTN_GREEN)

    def _update_contact(self):
        if self.selected_index is None:
            messagebox.showinfo("No Selection", "Please select a contact from the list first.")
            return

        data = self._get_form_data()
        if not data["name"]:
            messagebox.showwarning("Missing Field", "Name cannot be empty.")
            return
        if not data["phone"]:
            messagebox.showwarning("Missing Field", "Phone number cannot be empty.")
            return
        if not validate_phone(data["phone"]):
            messagebox.showwarning("Invalid Phone", "Phone number contains invalid characters.")
            return
        if data["email"] and not validate_email(data["email"]):
            messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
            return

        # Check duplicate phone (skip current contact)
        for i, c in enumerate(self.contacts):
            if i != self.selected_index and c["phone"] == data["phone"]:
                messagebox.showwarning("Duplicate", f"Another contact already uses {data['phone']}.")
                return

        self.contacts[self.selected_index] = data
        save_contacts(self.contacts)
        self._refresh_list()
        self._set_status(f"'{data['name']}' updated  ✔", BTN_BLUE)

    def _delete_contact(self):
        if self.selected_index is None:
            messagebox.showinfo("No Selection", "Please select a contact to delete.")
            return

        name = self.contacts[self.selected_index]["name"]
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete  '{name}'?\nThis action cannot be undone.",
        )
        if not confirm:
            return

        self.contacts.pop(self.selected_index)
        save_contacts(self.contacts)
        self._clear_form()
        self._refresh_list()
        self._set_status(f"'{name}' deleted", BTN_RED)


# ═════════════════════════════════════════════
#  Entry point
# ═════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
