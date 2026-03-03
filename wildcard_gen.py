import tkinter as tk
from tkinter import filedialog, messagebox
import random
import os
import shutil

WILDCARD_DIR = "wild card text"


class WildcardGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wildcard Tag Generator")
        self.root.geometry("600x500")

        os.makedirs(WILDCARD_DIR, exist_ok=True)

        self.wildcard_files = []

        frame_top = tk.Frame(root, pady=10)
        frame_top.pack(fill="x", padx=10)

        self.btn_add = tk.Button(
            frame_top,
            text="Add Wildcard Files (.txt)",
            command=self.add_files,
            bg="#dddddd"
        )
        self.btn_add.pack(side="left", padx=5)

        self.btn_save = tk.Button(
            frame_top,
            text="Save Wildcards",
            command=self.save_files,
            bg="#cce5ff"
        )
        self.btn_save.pack(side="left", padx=5)

        self.btn_clear_list = tk.Button(
            frame_top,
            text="Clear File List",
            command=self.clear_files,
            bg="#ffcccc"
        )
        self.btn_clear_list.pack(side="right", padx=5)

        self.lbl_info = tk.Label(
            root,
            text="Loaded Wildcards (1 tag will be pulled from each):"
        )
        self.lbl_info.pack(anchor="w", padx=15)

        self.listbox = tk.Listbox(root, height=8, selectmode="extended")
        self.listbox.pack(fill="x", padx=10, pady=5)

        frame_action = tk.Frame(root, pady=10)
        frame_action.pack(fill="x")

        tk.Label(frame_action, text="Separator:").pack(side="left", padx=(15, 5))
        self.ent_separator = tk.Entry(frame_action, width=5)
        self.ent_separator.insert(0, ", ")
        self.ent_separator.pack(side="left")

        self.btn_generate = tk.Button(
            frame_action,
            text="GENERATE PROMPT",
            command=self.generate,
            bg="#ccffcc",
            font=("Arial", 10, "bold")
        )
        self.btn_generate.pack(side="right", padx=15)

        tk.Label(root, text="Generated Result:").pack(anchor="w", padx=15)
        self.txt_output = tk.Text(root, height=8, font=("Segoe UI", 10))
        self.txt_output.pack(fill="both", expand=True, padx=10, pady=5)

        frame_bottom = tk.Frame(root, pady=10)
        frame_bottom.pack(fill="x")

        self.btn_copy = tk.Button(
            frame_bottom,
            text="Copy to Clipboard",
            command=self.copy_to_clipboard
        )
        self.btn_copy.pack(side="right", padx=15)

        self.lbl_credit = tk.Label(
            frame_bottom,
            text="BY KOOKIE PUM",
            fg="#777777",
            font=("Segoe UI", 9)
        )
        self.lbl_credit.pack(side="left", padx=15)

        self.load_saved_files()

    def get_unique_filename(self, filename):
        base, ext = os.path.splitext(filename)
        counter = 1
        new_name = filename

        existing = {
            os.path.basename(f) for f in self.wildcard_files
        }

        while new_name in existing:
            new_name = f"{base} ({counter}){ext}"
            counter += 1

        return new_name

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select Wildcard Text Files",
            filetypes=(("Text Files", "*.txt"),)
        )

        for src in files:
            filename = os.path.basename(src)
            unique_name = self.get_unique_filename(filename)
            dest = os.path.join(WILDCARD_DIR, unique_name)

            shutil.copy(src, dest)
            self.wildcard_files.append(dest)
            self.listbox.insert("end", f"[{unique_name}] - Ready")

    def save_files(self):
        if not self.wildcard_files:
            messagebox.showinfo("Nothing to Save", "No wildcard files to save.")
            return

        messagebox.showinfo(
            "Saved",
            f"Wildcard files saved to:\n{WILDCARD_DIR}"
        )

    def load_saved_files(self):
        self.clear_files()
        for file in sorted(os.listdir(WILDCARD_DIR)):
            if file.lower().endswith(".txt"):
                path = os.path.join(WILDCARD_DIR, file)
                self.wildcard_files.append(path)
                self.listbox.insert("end", f"[{file}] - Loaded")

    def clear_files(self):
        self.wildcard_files = []
        self.listbox.delete(0, "end")

    def generate(self):
        if not self.wildcard_files:
            messagebox.showwarning("No Files", "Please add at least one text file first.")
            return

        selected_tags = []

        for file_path in self.wildcard_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = [line.strip() for line in f if line.strip()]
                    selected_tags.append(random.choice(lines) if lines else "MISSING_DATA")
            except Exception:
                selected_tags.append("ERROR")

        result = self.ent_separator.get().join(selected_tags)
        self.txt_output.delete("1.0", "end")
        self.txt_output.insert("end", result)

    def copy_to_clipboard(self):
        content = self.txt_output.get("1.0", "end-1c")
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = WildcardGeneratorApp(root)
    root.mainloop()