"""
app.py

PDFToolApp — main application window for PDF for Linh.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from pdf_for_linh import pdf_ops
from pdf_for_linh.constants import (
    COLORS,
    FONT_BTN, FONT_BTN_BIG, FONT_ENTRY, FONT_ENTRY_LG,
    FONT_HINT, FONT_LABEL, FONT_LABEL_BOLD, FONT_SUBTITLE, FONT_TITLE,
)

_PDF_FILTER = [("PDF files", "*.pdf")]


class PDFToolApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("🌸 PDF for Linh 🌸")
        self.root.geometry("580x520")
        self.root.resizable(True, True)
        self.root.configure(bg=COLORS["bg"])

        self._files_to_join: list[str] = []

        self._setup_styles()
        self._setup_ui()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _setup_styles(self) -> None:
        style = ttk.Style()
        style.configure("Cute.TNotebook", background=COLORS["bg"])
        style.configure("Cute.TNotebook.Tab", font=FONT_LABEL_BOLD, padding=(20, 10))

    def _setup_ui(self) -> None:
        header = tk.Frame(self.root, bg=COLORS["pink"], pady=10)
        header.pack(fill=tk.X)
        tk.Label(header, text="✨ PDF for Linh ✨", font=FONT_TITLE,
                 bg=COLORS["pink"], fg="#FFFFFF").pack()
        tk.Label(header, text="🎀 Chia & Gộp PDF dễ dàng 🎀", font=FONT_SUBTITLE,
                 bg=COLORS["pink"], fg="#FFFFFF").pack()

        notebook = ttk.Notebook(self.root, style="Cute.TNotebook")
        notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        split_frame = tk.Frame(notebook, bg=COLORS["bg"], padx=20, pady=20)
        notebook.add(split_frame, text="  ✂️ Chia PDF  ")
        self._setup_split_tab(split_frame)

        join_frame = tk.Frame(notebook, bg=COLORS["bg"], padx=20, pady=20)
        notebook.add(join_frame, text="  📎 Gộp PDF  ")
        self._setup_join_tab(join_frame)

    def _make_button(
        self, parent: tk.Widget, text: str, command: Callable, big: bool = False
    ) -> tk.Button:
        base_color = COLORS["button"] if big else COLORS["purple"]
        btn = tk.Button(
            parent, text=text, command=command,
            font=FONT_BTN_BIG if big else FONT_BTN,
            bg=base_color, fg="white",
            activebackground=COLORS["pink"], activeforeground="white",
            relief=tk.FLAT,
            padx=20 if big else 15, pady=10 if big else 6,
            cursor="heart" if big else "hand2",
            borderwidth=0,
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=COLORS["pink"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=base_color))
        return btn

    # ------------------------------------------------------------------
    # Split tab
    # ------------------------------------------------------------------

    def _setup_split_tab(self, parent: tk.Frame) -> None:
        tk.Label(parent, text="📁 Chọn file PDF để chia:", font=FONT_LABEL,
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor=tk.W)

        file_frame = tk.Frame(parent, bg=COLORS["bg"])
        file_frame.pack(fill=tk.X, pady=(8, 15))

        self._split_file_var = tk.StringVar()
        tk.Entry(
            file_frame, textvariable=self._split_file_var, state="readonly",
            font=FONT_ENTRY, relief=tk.FLAT,
            bg=COLORS["yellow"], fg=COLORS["text"],
            readonlybackground=COLORS["yellow"],
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        self._make_button(
            file_frame, "🔍 Chọn file", self._select_split_file
        ).pack(side=tk.RIGHT, padx=(10, 0))

        self._page_info_var = tk.StringVar()
        tk.Label(parent, textvariable=self._page_info_var, font=FONT_LABEL_BOLD,
                 bg=COLORS["bg"], fg="#9370DB").pack(anchor=tk.W, pady=(0, 10))

        tk.Label(parent, text="📝 Nhập trang cần chia:", font=FONT_LABEL,
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor=tk.W, pady=(10, 5))

        self._range_entry = tk.Entry(
            parent, font=FONT_ENTRY_LG, relief=tk.FLAT,
            bg=COLORS["yellow"], fg=COLORS["text"],
            insertbackground=COLORS["button"],
        )
        self._range_entry.pack(fill=tk.X, ipady=10, pady=(0, 5))

        tk.Label(parent, text="💡 VD: 1-3, 4-6, 7-10  hoặc  1, 3, 5",
                 font=FONT_HINT, bg=COLORS["bg"], fg="#B0B0B0").pack(anchor=tk.W)

        btn_frame = tk.Frame(parent, bg=COLORS["bg"])
        btn_frame.pack(pady=25)
        self._make_button(btn_frame, "✂️ CHIA FILE ✂️", self._do_split, big=True).pack()

        self._split_status = tk.StringVar()
        tk.Label(parent, textvariable=self._split_status, font=FONT_LABEL_BOLD,
                 bg=COLORS["bg"], fg="#32CD32").pack()

    def _select_split_file(self) -> None:
        file = filedialog.askopenfilename(title="🔍 Chọn file PDF", filetypes=_PDF_FILTER)
        if file:
            self._split_file_var.set(file)
            try:
                count = pdf_ops.get_page_count(file)
                self._page_info_var.set(f"📄 File có {count} trang")
            except Exception:
                self._page_info_var.set("")

    def _do_split(self) -> None:
        input_file = self._split_file_var.get()
        if not input_file:
            messagebox.showerror("🙈 Ối!", "Linh ơi chọn file PDF đi nè!")
            return

        ranges = self._range_entry.get().strip()
        if not ranges:
            messagebox.showerror("🙈 Ối!", "Linh ơi nhập số trang đi nè!")
            return

        try:
            outputs = pdf_ops.split_pdf(input_file, ranges)
            self._split_status.set(f"✨ Đã chia thành {len(outputs)} file! ✨")
            messagebox.showinfo("🎉 Yay!", "Chia file thành công rồi nè!\n\n✨ Linh Cảm Ơn ✨\n💕💕💕")
        except ValueError as exc:
            messagebox.showerror(
                "🙈 Ối!",
                f"Linh ơi nhập sai rồi!\n{exc}\nNhập kiểu: 1-3, 4-6 hoặc 1, 3, 5 nha 💕",
            )
        except Exception as exc:
            messagebox.showerror("🙈 Ối!", f"Có lỗi rồi: {exc}")

    # ------------------------------------------------------------------
    # Join tab
    # ------------------------------------------------------------------

    def _setup_join_tab(self, parent: tk.Frame) -> None:
        tk.Label(parent, text="📚 Danh sách file PDF để gộp:", font=FONT_LABEL,
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor=tk.W)

        list_frame = tk.Frame(parent, bg=COLORS["yellow"], relief=tk.FLAT)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(8, 10))

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._file_listbox = tk.Listbox(
            list_frame, yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE, font=FONT_ENTRY, relief=tk.FLAT,
            bg=COLORS["yellow"], fg=COLORS["text"],
            selectbackground=COLORS["pink"], selectforeground="white",
            highlightthickness=0,
        )
        self._file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self._file_listbox.yview)

        btn_frame = tk.Frame(parent, bg=COLORS["bg"])
        btn_frame.pack(fill=tk.X, pady=10)
        self._make_button(btn_frame, "➕ Thêm",    self._add_files).pack(side=tk.LEFT, padx=(0, 5))
        self._make_button(btn_frame, "➖ Xóa",     self._remove_file).pack(side=tk.LEFT, padx=5)
        self._make_button(btn_frame, "⬆️",         self._move_up).pack(side=tk.LEFT, padx=5)
        self._make_button(btn_frame, "⬇️",         self._move_down).pack(side=tk.LEFT, padx=5)
        self._make_button(btn_frame, "🗑️ Xóa hết", self._clear_files).pack(side=tk.RIGHT)

        join_btn_frame = tk.Frame(parent, bg=COLORS["bg"])
        join_btn_frame.pack(pady=15)
        self._make_button(join_btn_frame, "📎 GỘP FILE 📎", self._do_join, big=True).pack()

        self._join_status = tk.StringVar()
        tk.Label(parent, textvariable=self._join_status, font=FONT_LABEL_BOLD,
                 bg=COLORS["bg"], fg="#32CD32").pack()

    def _add_files(self) -> None:
        files = filedialog.askopenfilenames(title="📁 Chọn file PDF", filetypes=_PDF_FILTER)
        for file in files:
            if file not in self._files_to_join:
                self._files_to_join.append(file)
                self._file_listbox.insert(tk.END, f"📄 {Path(file).name}")

    def _remove_file(self) -> None:
        selection = self._file_listbox.curselection()
        if selection:
            idx = selection[0]
            self._file_listbox.delete(idx)
            del self._files_to_join[idx]

    def _move_up(self) -> None:
        selection = self._file_listbox.curselection()
        if selection and selection[0] > 0:
            idx = selection[0]
            self._files_to_join[idx], self._files_to_join[idx - 1] = (
                self._files_to_join[idx - 1], self._files_to_join[idx]
            )
            text = self._file_listbox.get(idx)
            self._file_listbox.delete(idx)
            self._file_listbox.insert(idx - 1, text)
            self._file_listbox.selection_set(idx - 1)

    def _move_down(self) -> None:
        selection = self._file_listbox.curselection()
        if selection and selection[0] < len(self._files_to_join) - 1:
            idx = selection[0]
            self._files_to_join[idx], self._files_to_join[idx + 1] = (
                self._files_to_join[idx + 1], self._files_to_join[idx]
            )
            text = self._file_listbox.get(idx)
            self._file_listbox.delete(idx)
            self._file_listbox.insert(idx + 1, text)
            self._file_listbox.selection_set(idx + 1)

    def _clear_files(self) -> None:
        self._file_listbox.delete(0, tk.END)
        self._files_to_join.clear()

    def _do_join(self) -> None:
        if len(self._files_to_join) < 2:
            messagebox.showerror("🙈 Ối!", "Linh ơi thêm ít nhất 2 file nha!")
            return
        try:
            output_folder = Path(self._files_to_join[0]).parent
            output_file = pdf_ops.join_pdfs(self._files_to_join, output_folder)
            self._join_status.set(f"✨ Đã gộp {len(self._files_to_join)} file! ✨")
            messagebox.showinfo(
                "🎉 Yay!",
                f"Gộp file thành công rồi nè!\n\n📄 {output_file.name}"
                "\n\n✨ Linh Cảm Ơn ✨\n💕💕💕",
            )
        except Exception as exc:
            messagebox.showerror("🙈 Ối!", f"Có lỗi rồi: {exc}")
