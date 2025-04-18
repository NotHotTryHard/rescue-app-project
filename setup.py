"""
Setup script for the rescue application.
"""

from setuptools import setup, find_packages

setup(
    name="rescue-app",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyqt6",
        "numpy",
        "pandas",
        "matplotlib",
        "scipy",
        "networkx",
        "geopy",
    ],
    entry_points={
        "console_scripts": [
            "rescue-app=rescue_app.app:main",
        ],
    },
    author="User",
    author_email="user@example.com",
    description="Application for rescue station management and emergency response analysis",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 