#!/usr/bin/env python3
"""
PDF for Linh
Ứng dụng để chia nhỏ và gộp file PDF
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter


class PDFToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF for Linh")
        self.root.geometry("550x450")
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
        
        # Hiển thị số trang
        self.page_info_var = tk.StringVar()
        ttk.Label(parent, textvariable=self.page_info_var, foreground='blue').pack(anchor=tk.W, pady=(0, 10))
        
        # Range input
        ttk.Label(parent, text="Nhập khoảng trang cần chia:").pack(anchor=tk.W, pady=(10, 5))
        
        range_frame = ttk.Frame(parent)
        range_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.range_entry = ttk.Entry(range_frame)
        self.range_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(parent, text="VD: 1-3, 4-6, 7-10  hoặc  1, 3, 5  hoặc  1-3, 5, 7-10", foreground='gray').pack(anchor=tk.W)
        
        # Split button
        ttk.Button(parent, text="SPLIT PDF", command=self.split_pdf).pack(pady=30)
        
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
        
        # Join button
        ttk.Button(parent, text="JOIN PDFs", command=self.join_pdfs).pack(pady=20)
        
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
            # Hiển thị số trang
            try:
                reader = PdfReader(file)
                total_pages = len(reader.pages)
                self.page_info_var.set(f"File có {total_pages} trang")
            except:
                self.page_info_var.set("")
    
    def split_pdf(self):
        input_file = self.split_file_var.get()
        
        if not input_file:
            messagebox.showerror("Lỗi", "Vui lòng chọn file PDF!")
            return
        
        ranges = self.range_entry.get().strip()
        if not ranges:
            messagebox.showerror("Lỗi", "Vui lòng nhập khoảng trang!")
            return
        
        try:
            reader = PdfReader(input_file)
            total_pages = len(reader.pages)
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_folder = os.path.dirname(input_file)
            
            file_count = 0
            for r in ranges.split(','):
                r = r.strip()
                if '-' in r:
                    start, end = map(int, r.split('-'))
                else:
                    start = end = int(r)
                
                # Kiểm tra trang hợp lệ
                if start < 1 or end > total_pages or start > end:
                    messagebox.showerror("Lỗi", f"Khoảng trang {r} không hợp lệ! File có {total_pages} trang.")
                    return
                
                writer = PdfWriter()
                for i in range(start - 1, end):
                    writer.add_page(reader.pages[i])
                
                if start == end:
                    output_path = os.path.join(output_folder, f"{base_name}_page_{start}.pdf")
                else:
                    output_path = os.path.join(output_folder, f"{base_name}_pages_{start}-{end}.pdf")
                
                with open(output_path, 'wb') as f:
                    writer.write(f)
                file_count += 1
            
            self.split_status.set(f"Đã chia thành {file_count} file!")
            messagebox.showinfo("Thành công", f"Chia file PDF thành công!\n\nLinh Cảm Ơn 💕")
            
        except ValueError:
            messagebox.showerror("Lỗi", "Định dạng khoảng trang không hợp lệ!\nVD: 1-3, 4-6 hoặc 1, 3, 5")
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
            self.files_to_join[idx], self.files_to_join[idx-1] = self.files_to_join[idx-1], self.files_to_join[idx]
            text = self.file_listbox.get(idx)
            self.file_listbox.delete(idx)
            self.file_listbox.insert(idx-1, text)
            self.file_listbox.selection_set(idx-1)
    
    def move_down(self):
        selection = self.file_listbox.curselection()
        if selection and selection[0] < len(self.files_to_join) - 1:
            idx = selection[0]
            self.files_to_join[idx], self.files_to_join[idx+1] = self.files_to_join[idx+1], self.files_to_join[idx]
            text = self.file_listbox.get(idx)
            self.file_listbox.delete(idx)
            self.file_listbox.insert(idx+1, text)
            self.file_listbox.selection_set(idx+1)
    
    def clear_files(self):
        self.file_listbox.delete(0, tk.END)
        self.files_to_join.clear()
    
    def join_pdfs(self):
        if len(self.files_to_join) < 2:
            messagebox.showerror("Lỗi", "Vui lòng thêm ít nhất 2 file PDF!")
            return
        
        try:
            writer = PdfWriter()
            
            for pdf_file in self.files_to_join:
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    writer.add_page(page)
            
            # Tự động đặt tên và lưu cùng thư mục với file đầu tiên
            output_folder = os.path.dirname(self.files_to_join[0])
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(output_folder, f"Merged_PDF_{timestamp}.pdf")
            
            with open(output_file, 'wb') as f:
                writer.write(f)
            
            self.join_status.set(f"Đã gộp {len(self.files_to_join)} file!")
            messagebox.showinfo("Thành công", f"Gộp file PDF thành công!\n\nFile đã lưu: {os.path.basename(output_file)}\n\nLinh Cảm Ơn 💕")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")


def main():
    root = tk.Tk()
    
    # Style
    style = ttk.Style()
    if 'aqua' in style.theme_names():
        style.theme_use('aqua')
    
    app = PDFToolApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()