# 🌸 PDF for Linh 🌸

Ứng dụng chia nhỏ và gộp file PDF với giao diện dễ thương 💕

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows-lightgrey)

## ✨ Tính năng

### ✂️ Chia PDF (Split)
- Chia theo khoảng trang tùy chọn (VD: `1-3, 4-6, 7-10`)
- Chia từng trang riêng lẻ (VD: `1, 3, 5, 7`)
- Kết hợp cả hai cách (VD: `1-3, 5, 7-10`)
- **Tự động lưu** cùng thư mục với file gốc

### 📎 Gộp PDF (Join)
- Gộp nhiều file PDF thành một
- Sắp xếp thứ tự file trước khi gộp (lên/xuống)
- **Tự động đặt tên** file (Merged_PDF_timestamp.pdf)
- **Tự động lưu** cùng thư mục với file đầu tiên

### 🎀 Giao diện dễ thương
- Màu pastel hồng, tím, vàng nhạt
- Icon emoji cute
- Font tròn dễ đọc
- Nút bấm đổi màu khi hover
- Thông báo vui vẻ 💕

## 📥 Cài đặt

### Cách 1: Tải app đã build sẵn (Khuyên dùng)

1. Vào tab **[Actions](../../actions)** của repo này
2. Click vào workflow **Build macOS App** mới nhất ✅
3. Kéo xuống phần **Artifacts**
4. Tải về:
   - **PDF-for-Linh-macOS-DMG** (cho macOS)
   - **PDF-for-Linh-Windows** (cho Windows)

#### 🍎 Mở app trên macOS lần đầu
Vì app chưa có chữ ký Apple, macOS sẽ chặn. Làm theo cách này:
1. Click chuột phải vào app
2. Chọn **Open**
3. Click **Open** trong popup

### Cách 2: Chạy từ source code

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# Cài thư viện
pip3 install PyPDF2

# Chạy app
python3 pdf_tool.py
```

### Cách 3: Tự build app trên máy

```bash
# Cài PyInstaller
pip3 install pyinstaller PyPDF2

# Build app
pyinstaller --onefile --windowed --name "PDF for Linh" pdf_tool.py

# App nằm trong thư mục dist/
```

## 🖥️ Yêu cầu hệ thống

| Hệ điều hành | Phiên bản |
|--------------|-----------|
| macOS | 10.15 (Catalina) trở lên |
| Windows | Windows 10 trở lên |
| Python | 3.9+ (nếu chạy từ source) |

## 📁 Cấu trúc project

```
├── pdf_tool.py              # Code chính
├── requirements.txt         # Dependencies
├── README.md                # File này
├── .gitignore              # Ignore files
└── .github/
    └── workflows/
        └── build.yml        # GitHub Actions workflow
```

## 🐛 Lỗi thường gặp

| Lỗi | Cách sửa |
|-----|----------|
| "App can't be opened" | Click chuột phải → Open |
| "Python not found" | Cài Python: `brew install python` |
| "No module named PyPDF2" | Chạy: `pip3 install PyPDF2` |
| "tkinter not found" | Chạy: `brew install python-tk` |

## 📝 Cách sử dụng

### Chia PDF
1. Mở app → Tab **✂️ Chia PDF**
2. Click **🔍 Chọn file** → chọn file PDF
3. Nhập khoảng trang (VD: `1-5, 6-10`)
4. Click **✂️ CHIA FILE ✂️**
5. File mới sẽ lưu cùng thư mục với file gốc 🎉

### Gộp PDF
1. Mở app → Tab **📎 Gộp PDF**
2. Click **➕ Thêm** → chọn các file PDF
3. Dùng **⬆️ ⬇️** để sắp xếp thứ tự
4. Click **📎 GỘP FILE 📎**
5. File mới sẽ lưu cùng thư mục với file đầu tiên 🎉

## 💕 Credit

Made with love for Linh ✨

## 📄 License

MIT License