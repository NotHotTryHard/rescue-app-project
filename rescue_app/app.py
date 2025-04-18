"""
Main entry point for the rescue application.
"""

import sys
import os
import time
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor

# Fix for WSL/X11 environment
os.environ["QT_QPA_PLATFORM"] = "xcb"

# Direct import when run as script
if __name__ == "__main__":
    # Add parent directory to path
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    
    # Import main window
    from rescue_app.ui.main_window import MainWindow
else:
    # Regular import when used as a module
    from rescue_app.ui.main_window import MainWindow


def main():
    """Initialize and run the PyQt application."""
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Rescue App")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Organization")
    app.setStyle("Fusion")
    
    # Set default palette with orange accents
    palette = app.palette()
    palette.setColor(palette.ColorRole.Window, QColor("#FFF5E9"))  # Light Orange background
    palette.setColor(palette.ColorRole.Base, QColor("#FFFFFF"))    # White for input fields
    palette.setColor(palette.ColorRole.AlternateBase, QColor("#FFEFDF"))  # Alternate rows in lists
    palette.setColor(palette.ColorRole.Highlight, QColor("#FF8C00"))  # Dark Orange
    palette.setColor(palette.ColorRole.HighlightedText, QColor("#FFFFFF"))
    palette.setColor(palette.ColorRole.Link, QColor("#FF4500"))  # OrangeRed
    palette.setColor(palette.ColorRole.LinkVisited, QColor("#FF8C00"))  # Dark Orange
    app.setPalette(palette)
    
    # Create splash screen
    package_dir = os.path.dirname(os.path.abspath(__file__))
    splash_path = os.path.join(package_dir, "resources", "splash.png")
    
    if os.path.exists(splash_path):
        splash_pixmap = QPixmap(splash_path)
    else:
        # Create a default orange-themed splash if the splash image doesn't exist
        splash_pixmap = QPixmap(600, 300)
        splash_pixmap.fill(QColor("#FF8C00"))  # Dark Orange
    
    splash = QSplashScreen(splash_pixmap)
    splash.showMessage(
        "Загрузка приложения...", 
        Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom,
        Qt.GlobalColor.white
    )
    splash.show()
    app.processEvents()
    
    # Short delay to show splash screen
    time.sleep(1.0)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    splash.finish(window)
    
    # Start application
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 