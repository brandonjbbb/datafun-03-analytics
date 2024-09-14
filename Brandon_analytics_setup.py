"""
Brandon's Analytics Setup Script
This script sets up the environment for the analytics project.
"""

import os
import subprocess
import sys

# Define the necessary directories for your project
required_directories = [
    "data-txt",  # Folder for text data files
    "logs",  # Folder for log files
    "output",  # Folder for output files
]

# Define the necessary Python packages (add more if needed)
required_packages = [
    "requests",  # For making HTTP requests
    "urllib3",  # For handling HTTP connections with custom SSL settings
]


def create_directories():
    """Create necessary directories for the project."""
    for directory in required_directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"Directory '{directory}' is ready.")
        except Exception as e:
            print(f"Error creating directory '{directory}': {e}")


def install_packages():
    """Install required Python packages."""
    try:
        for package in required_packages:
            print(f"Installing package '{package}'...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Package '{package}' installed successfully.")
    except Exception as e:
        print(f"Error installing packages: {e}")


def main():
    """Run all setup tasks."""
    print("Setting up the project environment...")
    create_directories()
    install_packages()
    print("Setup completed successfully.")


if __name__ == "__main__":
    main()
