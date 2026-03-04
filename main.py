#!/usr/bin/env python3
"""
PDF for Linh - Entry point.
"""

import tkinter as tk

from pdf_for_linh.app import PDFToolApp


def main():
    root = tk.Tk()
    try:
        root.iconbitmap('icon.ico')
    except Exception:
        pass
    PDFToolApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
