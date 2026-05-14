# 📒 Contact Book — Python Desktop App

A clean, dark-themed contact management application built entirely
with Python's standard library (tkinter + json).  No third-party
packages are required.

---

## Features
| # | Feature | Details |
|---|---------|---------|
| 1 | Contact Information | Name, Phone, Email, Address |
| 2 | Add Contact | Form on the right panel → "Save Contact" |
| 3 | View Contact List | Scrollable table on the left panel |
| 4 | Search Contact | Live search bar (name or phone) |
| 5 | Update Contact | Select a row → edit fields → "Update" |
| 6 | Delete Contact | Select a row → "Delete" button |
| 7 | User Interface | Dark themed, colour-coded buttons, status bar |

---

## Requirements
- Python 3.8 or newer (tkinter is bundled with Python on Windows & macOS)
- Linux users: `sudo apt install python3-tk`

---

## How to Run
```
python contact_book.py
```
That's it — no pip installs needed.

---

## File Structure
```
contact_book/
├── contact_book.py   ← entire application source code
├── contacts.json     ← auto-created on first save
└── README.md
```

---

## Usage Guide
1. **Add a contact** — fill in the right-side form and click **💾 Save Contact**.
2. **View contacts** — all saved contacts appear in the left list.
3. **Search** — type any part of a name or phone number in the search box.
4. **Edit a contact** — click a row, change details in the form, click **✏️ Update**.
5. **Delete a contact** — click a row, then click **🗑 Delete** and confirm.
6. **Clear form** — click **🔄 Clear Form** to reset all fields.

---

## Data Storage
Contacts are saved locally in `contacts.json` in the same folder as
the script.  The file is created automatically on the first save.
