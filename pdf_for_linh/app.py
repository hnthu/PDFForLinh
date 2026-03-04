"""
app.py

PDFToolApp — main application window for PDF for Linh.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from pdf_for_linh import pdf_ops


class PDFToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 PDF for Linh 🌸")
        self.root.geometry("580x520")
        self.root.resizable(True, True)

        self.colors = {
            'bg':     '#FFF0F5',
            'pink':   '#FFB6C1',
            'purple': '#DDA0DD',
            'yellow': '#FFFACD',
            'button': '#FF69B4',
            'text':   '#8B4513',
        }
        self.root.configure(bg=self.colors['bg'])
        self.files_to_join = []

        self._setup_styles()
        self._setup_ui()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _setup_styles(self):
        style = ttk.Style()
        style.configure('Cute.TNotebook', background=self.colors['bg'])
        style.configure('Cute.TNotebook.Tab',
                        font=('Arial Rounded MT Bold', 12, 'bold'),
                        padding=(20, 10))

    def _setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.colors['pink'], pady=10)
        header.pack(fill=tk.X)
        tk.Label(header, text="✨ PDF for Linh ✨",
                 font=('Arial Rounded MT Bold', 20, 'bold'),
                 bg=self.colors['pink'], fg='#FFFFFF').pack()
        tk.Label(header, text="🎀 Chia & Gộp PDF dễ dàng 🎀",
                 font=('Arial Rounded MT Bold', 11),
                 bg=self.colors['pink'], fg='#FFFFFF').pack()

        # Tabs
        notebook = ttk.Notebook(self.root, style='Cute.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        split_frame = tk.Frame(notebook, bg=self.colors['bg'], padx=20, pady=20)
        notebook.add(split_frame, text="  ✂️ Chia PDF  ")
        self._setup_split_tab(split_frame)

        join_frame = tk.Frame(notebook, bg=self.colors['bg'], padx=20, pady=20)
        notebook.add(join_frame, text="  📎 Gộp PDF  ")
        self._setup_join_tab(join_frame)

    def _make_button(self, parent, text, command, big=False):
        base_color = self.colors['button'] if big else self.colors['purple']
        btn = tk.Button(parent, text=text, command=command,
                        font=('Arial Rounded MT Bold', 13 if big else 11, 'bold'),
                        bg=base_color, fg='white',
                        activebackground=self.colors['pink'], activeforeground='white',
                        relief=tk.FLAT,
                        padx=20 if big else 15, pady=10 if big else 6,
                        cursor='heart' if big else 'hand2',
                        borderwidth=0)
        btn.bind('<Enter>', lambda e: btn.config(bg=self.colors['pink']))
        btn.bind('<Leave>', lambda e: btn.config(bg=base_color))
        return btn

    # ------------------------------------------------------------------
    # Split tab
    # ------------------------------------------------------------------

    def _setup_split_tab(self, parent):
        tk.Label(parent, text="📁 Chọn file PDF để chia:",
                 font=('Arial Rounded MT Bold', 12),
                 bg=self.colors['bg'], fg=self.colors['text']).pack(anchor=tk.W)

        file_frame = tk.Frame(parent, bg=self.colors['bg'])
        file_frame.pack(fill=tk.X, pady=(8, 15))

        self.split_file_var = tk.StringVar()
        tk.Entry(file_frame, textvariable=self.split_file_var, state='readonly',
                 font=('Arial', 11), relief=tk.FLAT,
                 bg=self.colors['yellow'], fg=self.colors['text'],
                 readonlybackground=self.colors['yellow']
                 ).pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        self._make_button(file_frame, "🔍 Chọn file", self._select_split_file
                          ).pack(side=tk.RIGHT, padx=(10, 0))

        self.page_info_var = tk.StringVar()
        tk.Label(parent, textvariable=self.page_info_var,
                 font=('Arial Rounded MT Bold', 12, 'bold'),
                 bg=self.colors['bg'], fg='#9370DB').pack(anchor=tk.W, pady=(0, 10))

        tk.Label(parent, text="📝 Nhập trang cần chia:",
                 font=('Arial Rounded MT Bold', 12),
                 bg=self.colors['bg'], fg=self.colors['text']).pack(anchor=tk.W, pady=(10, 5))

        self.range_entry = tk.Entry(parent, font=('Arial', 12), relief=tk.FLAT,
                                    bg=self.colors['yellow'], fg=self.colors['text'],
                                    insertbackground=self.colors['button'])
        self.range_entry.pack(fill=tk.X, ipady=10, pady=(0, 5))

        tk.Label(parent, text="💡 VD: 1-3, 4-6, 7-10  hoặc  1, 3, 5",
                 font=('Arial', 10), bg=self.colors['bg'], fg='#B0B0B0').pack(anchor=tk.W)

        btn_frame = tk.Frame(parent, bg=self.colors['bg'])
        btn_frame.pack(pady=25)
        self._make_button(btn_frame, "✂️ CHIA FILE ✂️", self._split_pdf, big=True).pack()

        self.split_status = tk.StringVar()
        tk.Label(parent, textvariable=self.split_status,
                 font=('Arial Rounded MT Bold', 12, 'bold'),
                 bg=self.colors['bg'], fg='#32CD32').pack()

    def _select_split_file(self):
        file = filedialog.askopenfilename(title="🔍 Chọn file PDF",
                                          filetypes=[("PDF files", "*.pdf")])
        if file:
            self.split_file_var.set(file)
            try:
                count = pdf_ops.get_page_count(file)
                self.page_info_var.set(f"📄 File có {count} trang")
            except Exception:
                self.page_info_var.set("")

    def _split_pdf(self):
        input_file = self.split_file_var.get()
        if not input_file:
            messagebox.showerror("🙈 Ối!", "Linh ơi chọn file PDF đi nè!")
            return

        ranges = self.range_entry.get().strip()
        if not ranges:
            messagebox.showerror("🙈 Ối!", "Linh ơi nhập số trang đi nè!")
            return

        try:
            outputs = pdf_ops.split_pdf(input_file, ranges)
            self.split_status.set(f"✨ Đã chia thành {len(outputs)} file! ✨")
            messagebox.showinfo("🎉 Yay!", "Chia file thành công rồi nè!\n\n✨ Linh Cảm Ơn ✨\n💕💕💕")
        except ValueError as e:
            messagebox.showerror("🙈 Ối!", f"Linh ơi nhập sai rồi!\n{e}\nNhập kiểu: 1-3, 4-6 hoặc 1, 3, 5 nha 💕")
        except Exception as e:
            messagebox.showerror("🙈 Ối!", f"Có lỗi rồi: {str(e)}")

    # ------------------------------------------------------------------
    # Join tab
    # ------------------------------------------------------------------

    def _setup_join_tab(self, parent):
        tk.Label(parent, text="📚 Danh sách file PDF để gộp:",
                 font=('Arial Rounded MT Bold', 12),
                 bg=self.colors['bg'], fg=self.colors['text']).pack(anchor=tk.W)

        list_frame = tk.Frame(parent, bg=self.colors['yellow'], relief=tk.FLAT)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(8, 10))

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.file_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                       selectmode=tk.SINGLE,
                                       font=('Arial', 11), relief=tk.FLAT,
                                       bg=self.colors['yellow'], fg=self.colors['text'],
                                       selectbackground=self.colors['pink'],
                                       selectforeground='white',
                                       highlightthickness=0)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.file_listbox.yview)

        btn_frame = tk.Frame(parent, bg=self.colors['bg'])
        btn_frame.pack(fill=tk.X, pady=10)
        self._make_button(btn_frame, "➕ Thêm",   self._add_files).pack(side=tk.LEFT, padx=(0, 5))
        self._make_button(btn_frame, "➖ Xóa",    self._remove_file).pack(side=tk.LEFT, padx=5)
        self._make_button(btn_frame, "⬆️",        self._move_up).pack(side=tk.LEFT, padx=5)
        self._make_button(btn_frame, "⬇️",        self._move_down).pack(side=tk.LEFT, padx=5)
        self._make_button(btn_frame, "🗑️ Xóa hết", self._clear_files).pack(side=tk.RIGHT)

        join_btn_frame = tk.Frame(parent, bg=self.colors['bg'])
        join_btn_frame.pack(pady=15)
        self._make_button(join_btn_frame, "📎 GỘP FILE 📎", self._join_pdfs, big=True).pack()

        self.join_status = tk.StringVar()
        tk.Label(parent, textvariable=self.join_status,
                 font=('Arial Rounded MT Bold', 12, 'bold'),
                 bg=self.colors['bg'], fg='#32CD32').pack()

    def _add_files(self):
        files = filedialog.askopenfilenames(title="📁 Chọn file PDF",
                                            filetypes=[("PDF files", "*.pdf")])
        for file in files:
            if file not in self.files_to_join:
                self.files_to_join.append(file)
                self.file_listbox.insert(tk.END, f"📄 {os.path.basename(file)}")

    def _remove_file(self):
        selection = self.file_listbox.curselection()
        if selection:
            idx = selection[0]
            self.file_listbox.delete(idx)
            del self.files_to_join[idx]

    def _move_up(self):
        selection = self.file_listbox.curselection()
        if selection and selection[0] > 0:
            idx = selection[0]
            self.files_to_join[idx], self.files_to_join[idx - 1] = (
                self.files_to_join[idx - 1], self.files_to_join[idx])
            text = self.file_listbox.get(idx)
            self.file_listbox.delete(idx)
            self.file_listbox.insert(idx - 1, text)
            self.file_listbox.selection_set(idx - 1)

    def _move_down(self):
        selection = self.file_listbox.curselection()
        if selection and selection[0] < len(self.files_to_join) - 1:
            idx = selection[0]
            self.files_to_join[idx], self.files_to_join[idx + 1] = (
                self.files_to_join[idx + 1], self.files_to_join[idx])
            text = self.file_listbox.get(idx)
            self.file_listbox.delete(idx)
            self.file_listbox.insert(idx + 1, text)
            self.file_listbox.selection_set(idx + 1)

    def _clear_files(self):
        self.file_listbox.delete(0, tk.END)
        self.files_to_join.clear()

    def _join_pdfs(self):
        if len(self.files_to_join) < 2:
            messagebox.showerror("🙈 Ối!", "Linh ơi thêm ít nhất 2 file nha!")
            return
        try:
            output_folder = os.path.dirname(self.files_to_join[0])
            output_file = pdf_ops.join_pdfs(self.files_to_join, output_folder)
            self.join_status.set(f"✨ Đã gộp {len(self.files_to_join)} file! ✨")
            messagebox.showinfo("🎉 Yay!",
                                f"Gộp file thành công rồi nè!\n\n📄 {os.path.basename(output_file)}"
                                "\n\n✨ Linh Cảm Ơn ✨\n💕💕💕")
        except Exception as e:
            messagebox.showerror("🙈 Ối!", f"Có lỗi rồi: {str(e)}")
