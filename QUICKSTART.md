# Quick Start Guide - Rescue Application

This is a simple guide to get the Rescue Application running on your computer with minimal setup.

## Windows Users (Easiest Method)

1. Make sure you have **Python 3.8 or newer** installed on your computer
   - You can download it from [python.org](https://www.python.org/downloads/)
   - Be sure to check "Add Python to PATH" during installation

2. **Double-click** the `run_program.bat` file
   - This will automatically set up everything and launch the application
   - The first run will take longer as it installs dependencies

## All Users (Manual Method)

1. **Install Python 3.8+** if you don't have it already
   - Windows: [python.org/downloads](https://www.python.org/downloads/)
   - macOS: `brew install python` (with Homebrew) or from python.org
   - Linux: `sudo apt install python3 python3-pip python3-venv` (Ubuntu/Debian)

2. **Open a terminal/command prompt** in the project directory

3. **Create a virtual environment:**
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```
   python run.py
   ```

## Troubleshooting

- **Nothing happens when I click run_program.bat**
  - Make sure Python is properly installed and added to your PATH
  - Try running the batch file as administrator

- **Missing dependencies errors**
  - Make sure you have an internet connection for the initial setup
  - If on Linux, you may need additional system packages:
    ```
    sudo apt-get install python3-tk libxcb-xinerama0
    ```

- **For additional help**
  - See the more detailed `README-INSTALL.md` file

## What's Next?

- Add rescue stations using the interface
- Run simulations to analyze rescue coverage
- Experiment with different station configurations 