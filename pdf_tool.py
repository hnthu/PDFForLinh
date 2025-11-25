#!/usr/bin/env python3
"""
PDF Split & Join Tool
Ứng dụng để chia nhỏ và gộp file PDF
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PyPDF2 import PdfReader, PdfWriter


class PDFToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Split & Join Tool")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Danh sách file để join
        self.files_to_join = []
        
        self.setup_ui()
    
    def setup_ui(self):
        # Notebook (tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab Split
        split_frame = ttk.Frame(notebook, padding=20)
        notebook.add(split_frame, text="  Split PDF  ")
        self.setup_split_tab(split_frame)
        
        # Tab Join
        join_frame = ttk.Frame(notebook, padding=20)
        notebook.add(join_frame, text="  Join PDFs  ")
        self.setup_join_tab(join_frame)
    
    def setup_split_tab(self, parent):
        # File input
        ttk.Label(parent, text="Chọn file PDF để chia:").pack(anchor=tk.W)
        
        file_frame = ttk.Frame(parent)
        file_frame.pack(fill=tk.X, pady=(5, 15))
        
        self.split_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.split_file_var, state='readonly').pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Chọn file", command=self.select_split_file).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Split options
        ttk.Label(parent, text="Cách chia:").pack(anchor=tk.W, pady=(10, 5))
        
        self.split_mode = tk.StringVar(value="each")
        
        ttk.Radiobutton(parent, text="Mỗi trang thành 1 file", variable=self.split_mode, value="each").pack(anchor=tk.W)
        
        range_frame = ttk.Frame(parent)
        range_frame.pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(range_frame, text="Theo khoảng trang:", variable=self.split_mode, value="range").pack(side=tk.LEFT)
        self.range_entry = ttk.Entry(range_frame, width=20)
        self.range_entry.pack(side=tk.LEFT, padx=(10, 0))
        ttk.Label(range_frame, text="(VD: 1-3, 4-6, 7-10)").pack(side=tk.LEFT, padx=(5, 0))
        
        pages_frame = ttk.Frame(parent)
        pages_frame.pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(pages_frame, text="Mỗi file có số trang:", variable=self.split_mode, value="chunks").pack(side=tk.LEFT)
        self.chunks_entry = ttk.Entry(pages_frame, width=10)
        self.chunks_entry.pack(side=tk.LEFT, padx=(10, 0))
        self.chunks_entry.insert(0, "5")
        
        # Output folder
        ttk.Label(parent, text="Thư mục lưu:").pack(anchor=tk.W, pady=(15, 5))
        
        output_frame = ttk.Frame(parent)
        output_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.split_output_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.split_output_var, state='readonly').pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Chọn thư mục", command=self.select_split_output).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Split button
        ttk.Button(parent, text="SPLIT PDF", command=self.split_pdf, style='Accent.TButton').pack(pady=20)
        
        # Status
        self.split_status = tk.StringVar()
        ttk.Label(parent, textvariable=self.split_status, foreground='green').pack()
    
    def setup_join_tab(self, parent):
        # File list
        ttk.Label(parent, text="Danh sách file PDF để gộp:").pack(anchor=tk.W)
        
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        # Listbox with scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        
        # Buttons for list management
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Thêm file", command=self.add_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Xóa file", command=self.remove_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Lên ↑", command=self.move_up).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Xuống ↓", command=self.move_down).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Xóa tất cả", command=self.clear_files).pack(side=tk.RIGHT)
        
        # Output file
        ttk.Label(parent, text="Lưu file kết quả:").pack(anchor=tk.W, pady=(10, 5))
        
        output_frame = ttk.Frame(parent)
        output_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.join_output_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.join_output_var, state='readonly').pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Chọn vị trí", command=self.select_join_output).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Join button
        ttk.Button(parent, text="JOIN PDFs", command=self.join_pdfs, style='Accent.TButton').pack(pady=10)
        
        # Status
        self.join_status = tk.StringVar()
        ttk.Label(parent, textvariable=self.join_status, foreground='green').pack()
    
    # Split functions
    def select_split_file(self):
        file = filedialog.askopenfilename(
            title="Chọn file PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if file:
            self.split_file_var.set(file)
            # Auto set output folder
            self.split_output_var.set(os.path.dirname(file))
    
    def select_split_output(self):
        folder = filedialog.askdirectory(title="Chọn thư mục lưu")
        if folder:
            self.split_output_var.set(folder)
    
    def split_pdf(self):
        input_file = self.split_file_var.get()
        output_folder = self.split_output_var.get()
        
        if not input_file:
            messagebox.showerror("Lỗi", "Vui lòng chọn file PDF!")
            return
        if not output_folder:
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục lưu!")
            return
        
        try:
            reader = PdfReader(input_file)
            total_pages = len(reader.pages)
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            
            mode = self.split_mode.get()
            
            if mode == "each":
                # Mỗi trang 1 file
                for i in range(total_pages):
                    writer = PdfWriter()
                    writer.add_page(reader.pages[i])
                    output_path = os.path.join(output_folder, f"{base_name}_page_{i+1}.pdf")
                    with open(output_path, 'wb') as f:
                        writer.write(f)
                self.split_status.set(f"Đã chia thành {total_pages} file!")
            
            elif mode == "range":
                # Theo khoảng trang
                ranges = self.range_entry.get().strip()
                if not ranges:
                    messagebox.showerror("Lỗi", "Vui lòng nhập khoảng trang!")
                    return
                
                for idx, r in enumerate(ranges.split(',')):
                    r = r.strip()
                    if '-' in r:
                        start, end = map(int, r.split('-'))
                    else:
                        start = end = int(r)
                    
                    writer = PdfWriter()
                    for i in range(start - 1, min(end, total_pages)):
                        writer.add_page(reader.pages[i])
                    
                    output_path = os.path.join(output_folder, f"{base_name}_pages_{start}-{end}.pdf")
                    with open(output_path, 'wb') as f:
                        writer.write(f)
                
                self.split_status.set(f"Đã chia theo khoảng trang!")
            
            elif mode == "chunks":
                # Chia theo số trang mỗi file
                try:
                    chunk_size = int(self.chunks_entry.get())
                except ValueError:
                    messagebox.showerror("Lỗi", "Số trang không hợp lệ!")
                    return
                
                file_count = 0
                for i in range(0, total_pages, chunk_size):
                    writer = PdfWriter()
                    for j in range(i, min(i + chunk_size, total_pages)):
                        writer.add_page(reader.pages[j])
                    
                    file_count += 1
                    output_path = os.path.join(output_folder, f"{base_name}_part_{file_count}.pdf")
                    with open(output_path, 'wb') as f:
                        writer.write(f)
                
                self.split_status.set(f"Đã chia thành {file_count} file!")
            
            messagebox.showinfo("Thành công", "Chia file PDF thành công!")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
    
    # Join functions
    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Chọn file PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        for file in files:
            if file not in self.files_to_join:
                self.files_to_join.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))
    
    def remove_file(self):
        selection = self.file_listbox.curselection()
        if selection:
            idx = selection[0]
            self.file_listbox.delete(idx)
            del self.files_to_join[idx]
    
    def move_up(self):
        selection = self.file_listbox.curselection()
        if selection and selection[0] > 0:
            idx = selection[0]
            # Swap in list
            self.files_to_join[idx], self.files_to_join[idx-1] = self.files_to_join[idx-1], self.files_to_join[idx]
            # Update listbox
            text = self.file_listbox.get(idx)
            self.file_listbox.delete(idx)
            self.file_listbox.insert(idx-1, text)
            self.file_listbox.selection_set(idx-1)
    
    def move_down(self):
        selection = self.file_listbox.curselection()
        if selection and selection[0] < len(self.files_to_join) - 1:
            idx = selection[0]
            # Swap in list
            self.files_to_join[idx], self.files_to_join[idx+1] = self.files_to_join[idx+1], self.files_to_join[idx]
            # Update listbox
            text = self.file_listbox.get(idx)
            self.file_listbox.delete(idx)
            self.file_listbox.insert(idx+1, text)
            self.file_listbox.selection_set(idx+1)
    
    def clear_files(self):
        self.file_listbox.delete(0, tk.END)
        self.files_to_join.clear()
    
    def select_join_output(self):
        file = filedialog.asksaveasfilename(
            title="Lưu file PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        if file:
            self.join_output_var.set(file)
    
    def join_pdfs(self):
        if len(self.files_to_join) < 2:
            messagebox.showerror("Lỗi", "Vui lòng thêm ít nhất 2 file PDF!")
            return
        
        output_file = self.join_output_var.get()
        if not output_file:
            messagebox.showerror("Lỗi", "Vui lòng chọn vị trí lưu file!")
            return
        
        try:
            writer = PdfWriter()
            
            for pdf_file in self.files_to_join:
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    writer.add_page(page)
            
            with open(output_file, 'wb') as f:
                writer.write(f)
            
            self.join_status.set(f"Đã gộp {len(self.files_to_join)} file thành công!")
            messagebox.showinfo("Thành công", "Gộp file PDF thành công!")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")


def main():
    root = tk.Tk()
    
    # Style
    style = ttk.Style()
    if 'aqua' in style.theme_names():
        style.theme_use('aqua')  # macOS native look
    
    app = PDFToolApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
