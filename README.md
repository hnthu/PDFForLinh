# PDF Split & Join Tool

Ứng dụng đơn giản để chia nhỏ và gộp file PDF với giao diện đồ họa.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows-lightgrey)

## Tính năng

### Split PDF (Chia file)
- **Mỗi trang 1 file**: Tách từng trang thành file riêng biệt
- **Theo khoảng trang**: Chia theo khoảng tùy chọn (VD: 1-3, 4-6, 7-10)
- **Theo số trang**: Chia file với số trang cố định mỗi file

### Join PDFs (Gộp file)
- Gộp nhiều file PDF thành một
- Sắp xếp thứ tự file trước khi gộp
- Thêm/xóa file dễ dàng

## Cài đặt

### Tải app đã build sẵn
1. Vào tab **Actions** của repo này
2. Chọn workflow **Build macOS App** mới nhất
3. Tải **PDF-Tool-macOS-DMG** hoặc **PDF-Tool-Windows**

### Chạy từ source code

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# Cài dependencies
pip install -r requirements.txt

# Chạy app
python pdf_tool.py
```

## Build app

### Build trên máy local

```bash
# Cài PyInstaller
pip install pyinstaller

# Build cho macOS
pyinstaller --onefile --windowed --name "PDF Tool" pdf_tool.py

# App sẽ ở thư mục dist/
```

### Build tự động với GitHub Actions

Push code lên GitHub, app sẽ được build tự động. Tải từ tab Actions.

## Cấu trúc project

```
├── pdf_tool.py              # Code chính
├── requirements.txt         # Dependencies
├── README.md               # File này
└── .github/
    └── workflows/
        └── build.yml       # GitHub Actions workflow
```

## Yêu cầu hệ thống

- **macOS**: 10.15 (Catalina) trở lên
- **Windows**: Windows 10 trở lên
- **Python**: 3.9+ (nếu chạy từ source)

## License

MIT License
