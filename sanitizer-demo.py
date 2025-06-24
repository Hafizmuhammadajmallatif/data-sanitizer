#!/usr/bin/env python3
"""
Safe demonstration of the Secure Data Sanitization Tool
Creates test files and shows how different deletion methods work
"""

import os
import sys
import tempfile
import subprocess
import hashlib
import time

def create_test_file(size_mb=1, content_type='sensitive'):
    """Create a test file with identifiable content"""
    temp_dir = tempfile.gettempdir()
    filename = f"test_sensitive_data_{int(time.time())}.txt"
    filepath = os.path.join(temp_dir, filename)
    
    print(f"[*] Creating test file: {filepath}")
    print(f"[*] Size: {size_mb} MB")
    
    with open(filepath, 'wb') as f:
        if content_type == 'sensitive':
            # Write identifiable pattern
            pattern = b"SENSITIVE_DATA_12345" * 50
            for _ in range(size_mb * 1024 * 1024 // len(pattern)):
                f.write(pattern)
        else:
            # Write random data
            for _ in range(size_mb):
                f.write(os.urandom(1024 * 1024))
    
    return filepath

def check_file_recovery_demo(filepath):
    """Demonstrate how deleted files might be recovered"""
    print("\n[DEMO] Standard Deletion vs Secure Deletion")
    print("=" * 60)
    
    # Read first 1KB of file
    with open(filepath, 'rb') as f:
        original_data = f.read(1024)
    
    print("Original file content (first 50 bytes):")
    print(f"  {original_data[:50]}")
    print(f"  MD5 hash: {hashlib.md5(original_data).hexdigest()}")
    
    print("\n[!] With standard deletion (os.remove):")
    print("  - File reference removed from file system")
    print("  - Data blocks marked as 'free'")
    print("  - Content remains on disk until overwritten")
    print("  - Recovery tools can easily restore the file")
    
    print("\n[✓] With secure deletion:")
    print("  - Data overwritten multiple times")
    print("  - Original content destroyed")
    print("  - File renamed to obscure metadata")
    print("  - Recovery becomes extremely difficult")
    print("=" * 60)

def demonstrate_overwrite_patterns():
    """Show what different overwrite patterns look like"""
    print("\n[DEMO] Overwrite Patterns Visualization")
    print("=" * 60)
    
    patterns = {
        'Original': b'SENSITIVE_DATA_12345',
        'Zeros': b'\x00' * 20,
        'Ones': b'\xFF' * 20,
        'Random': os.urandom(20),
        'DoD Pass 1': b'\x00' * 20,
        'DoD Pass 2': b'\xFF' * 20,
        'DoD Pass 3': os.urandom(20),
    }
    
    for name, pattern in patterns.items():
        hex_display = ' '.join(f'{b:02x}' for b in pattern[:20])
        ascii_display = ''.join(chr(b) if 32 <= b < 127 else '.' for b in pattern[:20])
        print(f"{name:12} | Hex: {hex_display}")
        print(f"{'':12} | ASCII: {ascii_display}")
        print()
    
    print("=" * 60)

def run_interactive_demo():
    """Run an interactive demonstration"""
    print("\n" + "=" * 60)
    print("SECURE DATA SANITIZATION TOOL - INTERACTIVE DEMO")
    print("=" * 60)
    
    print("\nThis demo will:")
    print("1. Create a test file with identifiable content")
    print("2. Show different overwrite patterns")
    print("3. Demonstrate secure deletion")
    print("4. Explain recovery prevention\n")
    
    input("Press Enter to continue...")
    
    # Create test file
    test_file = create_test_file(size_mb=1)
    
    # Show file recovery information
    check_file_recovery_demo(test_file)
    
    input("\nPress Enter to see overwrite patterns...")
    
    # Demonstrate patterns
    demonstrate_overwrite_patterns()
    
    # Ask if user wants to run actual deletion
    print("\n[?] Would you like to securely delete the test file?")
    print(f"    File: {test_file}")
    response = input("    Type 'yes' to proceed: ")
    
    if response.lower() == 'yes':
        print("\n[*] Running secure deletion with DoD 3-pass method...")
        try:
            # Run the secure delete tool
            cmd = [sys.executable, 'secure_delete.py', 'shred', test_file, '-m', 'dod3', '--confirm']
            subprocess.run(cmd, check=True)
            
            print("\n[✓] Secure deletion complete!")
            print("[*] The test file has been securely wiped")
            
            # Verify file is gone
            if not os.path.exists(test_file):
                print("[✓] File no longer exists in file system")
            
        except subprocess.CalledProcessError as e:
            print(f"[!] Error running secure delete: {e}")
        except FileNotFoundError:
            print("[!] secure_delete.py not found in current directory")
    else:
        # Clean up test file
        os.remove(test_file)
        print("\n[*] Test file removed (standard deletion)")
    
    print("\n[DEMO COMPLETE]")
    print("\nKey Takeaways:")
    print("- Standard deletion is not secure")
    print("- Multiple overwrite passes increase security")
    print("- Different storage types need different approaches")
    print("- Always backup important data before using security tools")
    print("\n" + "=" * 60)

def show_storage_type_info():
    """Display information about different storage types"""
    print("\n[INFO] Storage Type Considerations")
    print("=" * 60)
    
    storage_info = {
        "Hard Disk Drive (HDD)": {
            "How it works": "Magnetic storage on spinning platters",
            "Deletion": "Overwriting is effective",
            "Best method": "DoD 3-pass or 7-pass",
            "Notes": "Physical destruction most secure"
        },
        "Solid State Drive (SSD)": {
            "How it works": "Flash memory with wear leveling",
            "Deletion": "Overwriting may not reach all cells",
            "Best method": "Manufacturer secure erase command",
            "Notes": "TRIM complicates secure deletion"
        },
        "USB Flash Drive": {
            "How it works": "Flash memory similar to SSD",
            "Deletion": "Standard overwriting has limitations",
            "Best method": "Multiple overwrites + physical destruction",
            "Notes": "Cheap drives may have poor controllers"
        }
    }
    
    for storage_type, info in storage_info.items():
        print(f"\n{storage_type}:")
        for key, value in info.items():
            print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    print("Secure Data Sanitization Tool - Educational Demo")
    
    if len(sys.argv) > 1 and sys.argv[1] == '--info':
        show_storage_type_info()
    else:
        try:
            run_interactive_demo()
        except KeyboardInterrupt:
            print("\n\n[!] Demo interrupted by user")
        except Exception as e:
            print(f"\n[!] Error: {e}")
