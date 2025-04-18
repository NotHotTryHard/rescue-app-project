#!/usr/bin/env python3
"""
Entry point runner for the rescue application.
"""

import sys
import os
import time
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

# Add the project directory to sys.path if it's not already there
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

from rescue_app.ui.main_window import MainWindow


def main():
    """Run the rescue application."""
    # Create application with proper metadata
    app = QApplication(sys.argv)
    app.setApplicationName("Rescue App")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Organization")
    
    # Set application style
    app.setStyle("Fusion")  # Use Fusion style for consistent look across platforms
    
    # Create and show splash screen
    package_dir = os.path.dirname(os.path.abspath(__file__))
    splash_path = os.path.join(package_dir, "rescue_app", "resources", "splash.png")
    
    # If splash image exists, show it
    if os.path.exists(splash_path):
        splash_pixmap = QPixmap(splash_path)
    else:
        # Create a simple splash screen programmatically
        splash_pixmap = QPixmap(600, 300)
        splash_pixmap.fill(Qt.GlobalColor.white)
    
    splash = QSplashScreen(splash_pixmap)
    
    # Add text to splash screen
    splash.showMessage(
        "Загрузка приложения...", 
        Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom,
        Qt.GlobalColor.darkBlue
    )
    splash.show()
    
    # Make sure splash screen is displayed while loading
    app.processEvents()
    
    # Simulate some startup time (replace with actual initialization tasks if needed)
    time.sleep(1.5)  # Short delay to show splash screen
    
    # Create the main window
    window = MainWindow()
    
    # Show the main window
    window.show()
    
    # Close splash screen once main window is ready
    splash.finish(window)
    
    # Start the application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 