#!/usr/bin/env python3
"""
PDF for Linh 💕
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
        self.root.title("🌸 PDF for Linh 🌸")
        self.root.geometry("580x520")
        self.root.resizable(True, True)
        
        # Màu pastel dễ thương
        self.colors = {
            'bg': '#FFF0F5',           # Lavender blush
            'pink': '#FFB6C1',          # Light pink
            'purple': '#DDA0DD',        # Plum
            'mint': '#98FB98',          # Pale green
            'yellow': '#FFFACD',        # Lemon chiffon
            'blue': '#E6E6FA',          # Lavender
            'button': '#FF69B4',        # Hot pink
            'button_text': '#FFFFFF',
            'text': '#8B4513',          # Saddle brown
        }
        
        # Set background color
        self.root.configure(bg=self.colors['bg'])
        
        # Danh sách file để join
        self.files_to_join = []
        
        self.setup_styles()
        self.setup_ui()
    
    def setup_styles(self):
        style = ttk.Style()
        
        # Frame style
        style.configure('Cute.TFrame', background=self.colors['bg'])
        
        # Label style
        style.configure('Cute.TLabel', 
                       background=self.colors['bg'], 
                       foreground=self.colors['text'],
                       font=('Arial Rounded MT Bold', 12))
        
        style.configure('Title.TLabel',
                       background=self.colors['bg'],
                       foreground='#FF1493',
                       font=('Arial Rounded MT Bold', 14, 'bold'))
        
        style.configure('Info.TLabel',
                       background=self.colors['bg'],
                       foreground='#9370DB',
                       font=('Arial Rounded MT Bold', 11))
        
        style.configure('Success.TLabel',
                       background=self.colors['bg'],
                       foreground='#32CD32',
                       font=('Arial Rounded MT Bold', 12, 'bold'))
        
        # Button style
        style.configure('Cute.TButton',
                       font=('Arial Rounded MT Bold', 11),
                       padding=(15, 8))
        
        style.configure('Big.TButton',
                       font=('Arial Rounded MT Bold', 13, 'bold'),
                       padding=(20, 12))
        
        # Entry style
        style.configure('Cute.TEntry',
                       font=('Arial', 11),
                       padding=8)
        
        # Notebook style
        style.configure('Cute.TNotebook', background=self.colors['bg'])
        style.configure('Cute.TNotebook.Tab', 
                       font=('Arial Rounded MT Bold', 12, 'bold'),
                       padding=(20, 10))
    
    def setup_ui(self):
        # Header dễ thương
        header_frame = tk.Frame(self.root, bg=self.colors['pink'], pady=10)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame, 
                              text="✨ PDF for Linh ✨",
                              font=('Arial Rounded MT Bold', 20, 'bold'),
                              bg=self.colors['pink'],
                              fg='#FFFFFF')
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame,
                                 text="🎀 Chia & Gộp PDF dễ dàng 🎀",
                                 font=('Arial Rounded MT Bold', 11),
                                 bg=self.colors['pink'],
                                 fg='#FFFFFF')
        subtitle_label.pack()
        
        # Notebook (tabs)
        notebook = ttk.Notebook(self.root, style='Cute.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Tab Split
        split_frame = tk.Frame(notebook, bg=self.colors['bg'], padx=20, pady=20)
        notebook.add(split_frame, text="  ✂️ Chia PDF  ")
        self.setup_split_tab(split_frame)
        
        # Tab Join
        join_frame = tk.Frame(notebook, bg=self.colors['bg'], padx=20, pady=20)
        notebook.add(join_frame, text="  📎 Gộp PDF  ")
        self.setup_join_tab(join_frame)
    
    def create_cute_button(self, parent, text, command, big=False):
        btn = tk.Button(parent,
                       text=text,
                       command=command,
                       font=('Arial Rounded MT Bold', 13 if big else 11, 'bold'),
                       bg=self.colors['button'] if big else self.colors['purple'],
                       fg='white',
                       activebackground=self.colors['pink'],
                       activeforeground='white',
                       relief=tk.FLAT,
                       padx=20 if big else 15,
                       pady=10 if big else 6,
                       cursor='heart' if big else 'hand2',
                       borderwidth=0)
        
        # Hover effect
        def on_enter(e):
            btn['bg'] = self.colors['pink']
        def on_leave(e):
            btn['bg'] = self.colors['button'] if big else self.colors['purple']
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def setup_split_tab(self, parent):
        # File input
        tk.Label(parent, 
                text="📁 Chọn file PDF để chia:",
                font=('Arial Rounded MT Bold', 12),
                bg=self.colors['bg'],
                fg=self.colors['text']).pack(anchor=tk.W)
        
        file_frame = tk.Frame(parent, bg=self.colors['bg'])
        file_frame.pack(fill=tk.X, pady=(8, 15))
        
        self.split_file_var = tk.StringVar()
        file_entry = tk.Entry(file_frame, 
                             textvariable=self.split_file_var,
                             state='readonly',
                             font=('Arial', 11),
                             bg=self.colors['yellow'],
                             fg=self.colors['text'],
                             relief=tk.FLAT,
                             readonlybackground=self.colors['yellow'])
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        
        self.create_cute_button(file_frame, "🔍 Chọn file", self.select_split_file).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Hiển thị số trang
        self.page_info_var = tk.StringVar()
        tk.Label(parent, 
                textvariable=self.page_info_var,
                font=('Arial Rounded MT Bold', 12, 'bold'),
                bg=self.colors['bg'],
                fg='#9370DB').pack(anchor=tk.W, pady=(0, 10))
        
        # Range input
        tk.Label(parent,
                text="📝 Nhập trang cần chia:",
                font=('Arial Rounded MT Bold', 12),
                bg=self.colors['bg'],
                fg=self.colors['text']).pack(anchor=tk.W, pady=(10, 5))
        
        self.range_entry = tk.Entry(parent,
                                   font=('Arial', 12),
                                   bg=self.colors['yellow'],
                                   fg=self.colors['text'],
                                   relief=tk.FLAT,
                                   insertbackground=self.colors['button'])
        self.range_entry.pack(fill=tk.X, ipady=10, pady=(0, 5))
        
        tk.Label(parent,
                text="💡 VD: 1-3, 4-6, 7-10  hoặc  1, 3, 5",
                font=('Arial', 10),
                bg=self.colors['bg'],
                fg='#B0B0B0').pack(anchor=tk.W)
        
        # Split button
        btn_frame = tk.Frame(parent, bg=self.colors['bg'])
        btn_frame.pack(pady=25)
        self.create_cute_button(btn_frame, "✂️ CHIA FILE ✂️", self.split_pdf, big=True).pack()
        
        # Status
        self.split_status = tk.StringVar()
        tk.Label(parent,
                textvariable=self.split_status,
                font=('Arial Rounded MT Bold', 12, 'bold'),
                bg=self.colors['bg'],
                fg='#32CD32').pack()
    
    def setup_join_tab(self, parent):
        # File list
        tk.Label(parent,
                text="📚 Danh sách file PDF để gộp:",
                font=('Arial Rounded MT Bold', 12),
                bg=self.colors['bg'],
                fg=self.colors['text']).pack(anchor=tk.W)
        
        list_frame = tk.Frame(parent, bg=self.colors['yellow'], relief=tk.FLAT)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(8, 10))
        
        # Listbox with scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_listbox = tk.Listbox(list_frame,
                                       yscrollcommand=scrollbar.set,
                                       selectmode=tk.SINGLE,
                                       font=('Arial', 11),
                                       bg=self.colors['yellow'],
                                       fg=self.colors['text'],
                                       selectbackground=self.colors['pink'],
                                       selectforeground='white',
                                       relief=tk.FLAT,
                                       highlightthickness=0)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.file_listbox.yview)
        
        # Buttons for list management
        btn_frame = tk.Frame(parent, bg=self.colors['bg'])
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.create_cute_button(btn_frame, "➕ Thêm", self.add_files).pack(side=tk.LEFT, padx=(0, 5))
        self.create_cute_button(btn_frame, "➖ Xóa", self.remove_file).pack(side=tk.LEFT, padx=5)
        self.create_cute_button(btn_frame, "⬆️", self.move_up).pack(side=tk.LEFT, padx=5)
        self.create_cute_button(btn_frame, "⬇️", self.move_down).pack(side=tk.LEFT, padx=5)
        self.create_cute_button(btn_frame, "🗑️ Xóa hết", self.clear_files).pack(side=tk.RIGHT)
        
        # Join button
        join_btn_frame = tk.Frame(parent, bg=self.colors['bg'])
        join_btn_frame.pack(pady=15)
        self.create_cute_button(join_btn_frame, "📎 GỘP FILE 📎", self.join_pdfs, big=True).pack()
        
        # Status
        self.join_status = tk.StringVar()
        tk.Label(parent,
                textvariable=self.join_status,
                font=('Arial Rounded MT Bold', 12, 'bold'),
                bg=self.colors['bg'],
                fg='#32CD32').pack()
    
    # Split functions
    def select_split_file(self):
        file = filedialog.askopenfilename(
            title="🔍 Chọn file PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if file:
            self.split_file_var.set(file)
            try:
                reader = PdfReader(file)
                total_pages = len(reader.pages)
                self.page_info_var.set(f"📄 File có {total_pages} trang")
            except:
                self.page_info_var.set("")
    
    def split_pdf(self):
        input_file = self.split_file_var.get()
        
        if not input_file:
            messagebox.showerror("🙈 Ối!", "Linh ơi chọn file PDF đi nè!")
            return
        
        ranges = self.range_entry.get().strip()
        if not ranges:
            messagebox.showerror("🙈 Ối!", "Linh ơi nhập số trang đi nè!")
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
                
                if start < 1 or end > total_pages or start > end:
                    messagebox.showerror("🙈 Ối!", f"Trang {r} không có nè!\nFile chỉ có {total_pages} trang thôi 💕")
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
            
            self.split_status.set(f"✨ Đã chia thành {file_count} file! ✨")
            messagebox.showinfo("🎉 Yay!", f"Chia file thành công rồi nè!\n\n✨ Linh Cảm Ơn ✨\n💕💕💕")
            
        except ValueError:
            messagebox.showerror("🙈 Ối!", "Linh ơi nhập sai rồi!\nNhập kiểu: 1-3, 4-6 hoặc 1, 3, 5 nha 💕")
        except Exception as e:
            messagebox.showerror("🙈 Ối!", f"Có lỗi rồi: {str(e)}")
    
    # Join functions
    def add_files(self):
        files = filedialog.askopenfilenames(
            title="📁 Chọn file PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        for file in files:
            if file not in self.files_to_join:
                self.files_to_join.append(file)
                self.file_listbox.insert(tk.END, f"📄 {os.path.basename(file)}")
    
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
            messagebox.showerror("🙈 Ối!", "Linh ơi thêm ít nhất 2 file nha!")
            return
        
        try:
            writer = PdfWriter()
            
            for pdf_file in self.files_to_join:
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    writer.add_page(page)
            
            output_folder = os.path.dirname(self.files_to_join[0])
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(output_folder, f"Merged_PDF_{timestamp}.pdf")
            
            with open(output_file, 'wb') as f:
                writer.write(f)
            
            self.join_status.set(f"✨ Đã gộp {len(self.files_to_join)} file! ✨")
            messagebox.showinfo("🎉 Yay!", f"Gộp file thành công rồi nè!\n\n📄 {os.path.basename(output_file)}\n\n✨ Linh Cảm Ơn ✨\n💕💕💕")
            
        except Exception as e:
            messagebox.showerror("🙈 Ối!", f"Có lỗi rồi: {str(e)}")


def main():
    root = tk.Tk()
    
    # Icon cho window (nếu có)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    app = PDFToolApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()