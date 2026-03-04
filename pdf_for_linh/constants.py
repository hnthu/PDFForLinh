"""
constants.py

UI theme constants for PDF for Linh.
Update values here to restyle the entire application.
"""

from typing import Final

COLORS: Final[dict[str, str]] = {
    "bg":     "#FFF0F5",  # Lavender blush
    "pink":   "#FFB6C1",  # Light pink
    "purple": "#DDA0DD",  # Plum
    "yellow": "#FFFACD",  # Lemon chiffon
    "button": "#FF69B4",  # Hot pink
    "text":   "#8B4513",  # Saddle brown
}

# Fonts: (family, size[, weight])
FONT_TITLE      = ("Arial Rounded MT Bold", 20, "bold")
FONT_SUBTITLE   = ("Arial Rounded MT Bold", 11)
FONT_LABEL      = ("Arial Rounded MT Bold", 12)
FONT_LABEL_BOLD = ("Arial Rounded MT Bold", 12, "bold")
FONT_BTN        = ("Arial Rounded MT Bold", 11, "bold")
FONT_BTN_BIG    = ("Arial Rounded MT Bold", 13, "bold")
FONT_ENTRY      = ("Arial", 11)
FONT_ENTRY_LG   = ("Arial", 12)
FONT_HINT       = ("Arial", 10)
