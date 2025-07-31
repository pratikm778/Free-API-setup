#!/usr/bin/env python3
"""
Setup script for Cascading AI API Flow
"""
import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("[ERROR] Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"[OK] Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("[INFO] Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("[OK] Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to install dependencies: {e}")
        return False

def setup_env_file():
    """Set up environment file"""
    env_path = Path(".env")
    env_example_path = Path(".env.example")

    if env_path.exists():
        print("[OK] .env file already exists")
        return True

    if env_example_path.exists():
        try:
            # Copy .env.example to .env
            with open(env_example_path, 'r') as src:
                content = src.read()
            with open(env_path, 'w') as dst:
                dst.write(content)
            print("[OK] Created .env file from template")
            print("[INFO] Please edit .env and add your API keys")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to create .env file: {e}")
            return False
    else:
        print("[WARN] .env.example not found")
        return False

def run_tests():
    """Run basic tests"""
    print("[INFO] Running setup tests...")
    try:
        # Import test to check if modules work
        from cascade import CascadingAPIClient
        from providers import get_available_providers

        providers = get_available_providers()
        if providers:
            print(f"[OK] Found {len(providers)} configured providers")
        else:
            print("[WARN] No API keys configured yet")
            print("   Edit .env file and add your API keys")

        return True
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False
    except Exception as e:
        print(f"[WARN] Setup test warning: {e}")
        return True  # Non-critical

def main():
    """Main setup function"""
    print("Cascading AI API Flow - Setup")
    print("=" * 40)

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Install dependencies
    if not install_dependencies():
        sys.exit(1)

    # Setup environment file
    if not setup_env_file():
        print("[WARN] Could not set up .env file")
        print("   Please manually copy .env.example to .env")

    # Run basic tests
    run_tests()

    print("\n[INFO] Setup completed!")
    print("\n[INFO] Next steps:")
    print("   1. Edit .env file and add your API keys")
    print("   2. Run: python test_providers.py")
    print("   3. Run: python example.py")
    print("\n[INFO] Documentation:")
    print("   - README.md - Quick overview")
    print("   - setup_guide.md - Detailed setup instructions")


if __name__ == "__main__":
    main()