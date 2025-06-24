#!/usr/bin/env python3
"""
Secure Data Sanitization Tool
Educational tool for demonstrating secure file deletion techniques
WARNING: This tool permanently destroys data. Use with extreme caution!
"""

import os
import sys
import random
import hashlib
import argparse
import time
from pathlib import Path
import struct
import platform

class SecureDelete:
    """Main class for secure file deletion operations"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.patterns = {
            'zeros': [b'\x00'],
            'ones': [b'\xFF'],
            'random': ['random'],
            'dod3': [b'\x00', b'\xFF', 'random'],  # DoD 5220.22-M (3 passes)
            'dod7': [b'\xF6', b'\x00', b'\xFF', 'random', b'\x00', b'\xFF', 'random'],  # DoD 5220.22-M (7 passes)
            'gutmann': self._generate_gutmann_patterns(),  # 35-pass Gutmann method
        }
    
    def _generate_gutmann_patterns(self):
        """Generate the 35-pass Gutmann overwrite patterns"""
        patterns = []
        # Random passes
        for _ in range(4):
            patterns.append('random')
        
        # Fixed patterns (simplified version)
        fixed_patterns = [
            b'\x55\x55\x55', b'\xAA\xAA\xAA', b'\x92\x49\x24', b'\x49\x24\x92',
            b'\x24\x92\x49', b'\x00\x00\x00', b'\x11\x11\x11', b'\x22\x22\x22',
            b'\x33\x33\x33', b'\x44\x44\x44', b'\x55\x55\x55', b'\x66\x66\x66',
            b'\x77\x77\x77', b'\x88\x88\x88', b'\x99\x99\x99', b'\xAA\xAA\xAA',
            b'\xBB\xBB\xBB', b'\xCC\xCC\xCC', b'\xDD\xDD\xDD', b'\xEE\xEE\xEE',
            b'\xFF\xFF\xFF', b'\x92\x49\x24', b'\x49\x24\x92', b'\x24\x92\x49',
            b'\x6D\xB6\xDB', b'\xB6\xDB\x6D', b'\xDB\x6D\xB6'
        ]
        
        patterns.extend(fixed_patterns)
        
        # Final random passes
        for _ in range(4):
            patterns.append('random')
            
        return patterns
    
    def _get_random_data(self, size):
        """Generate cryptographically secure random data"""
        return os.urandom(size)
    
    def _overwrite_file(self, filepath, pattern):
        """Overwrite file with specified pattern"""
        file_size = os.path.getsize(filepath)
        
        with open(filepath, 'rb+') as f:
            f.seek(0)
            
            if pattern == 'random':
                # Write random data in chunks
                chunk_size = 1024 * 1024  # 1MB chunks
                written = 0
                
                while written < file_size:
                    chunk = min(chunk_size, file_size - written)
                    f.write(self._get_random_data(chunk))
                    written += chunk
            else:
                # Write pattern data
                pattern_data = pattern * (file_size // len(pattern) + 1)
                f.write(pattern_data[:file_size])
            
            # Force write to disk
            f.flush()
            os.fsync(f.fileno())
    
    def _secure_rename(self, filepath):
        """Rename file to random name to obscure metadata"""
        directory = os.path.dirname(filepath)
        random_name = hashlib.sha256(os.urandom(32)).hexdigest()[:16]
        new_path = os.path.join(directory, random_name)
        
        try:
            os.rename(filepath, new_path)
            return new_path
        except:
            return filepath
    
    def shred_file(self, filepath, method='dod3'):
        """Securely delete a file using specified method"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        if method not in self.patterns:
            raise ValueError(f"Unknown method: {method}. Available: {list(self.patterns.keys())}")
        
        patterns = self.patterns[method]
        file_size = os.path.getsize(filepath)
        
        print(f"\n[*] Shredding: {filepath}")
        print(f"[*] Size: {file_size:,} bytes")
        print(f"[*] Method: {method} ({len(patterns)} passes)")
        
        # Overwrite with each pattern
        for i, pattern in enumerate(patterns, 1):
            if self.verbose:
                pattern_name = 'random' if pattern == 'random' else f"0x{pattern.hex()}"
                print(f"[*] Pass {i}/{len(patterns)}: Writing {pattern_name}")
            else:
                print(f"[*] Pass {i}/{len(patterns)}...", end='\r')
            
            self._overwrite_file(filepath, pattern)
        
        print(f"\n[*] Overwriting complete")
        
        # Rename file to obscure metadata
        if self.verbose:
            print("[*] Renaming file to obscure metadata...")
        filepath = self._secure_rename(filepath)
        
        # Delete the file
        os.remove(filepath)
        print("[✓] File securely deleted\n")
    
    def wipe_free_space(self, directory, passes=1):
        """Wipe free space on a drive (simplified version)"""
        print(f"\n[*] Wiping free space in: {directory}")
        print("[!] This is a simplified demonstration")
        
        # Create temporary file to fill free space
        temp_file = os.path.join(directory, f".wipe_{int(time.time())}")
        
        try:
            with open(temp_file, 'wb') as f:
                chunk_size = 1024 * 1024 * 10  # 10MB chunks
                written = 0
                
                print("[*] Filling free space with random data...")
                while True:
                    try:
                        f.write(self._get_random_data(chunk_size))
                        written += chunk_size
                        print(f"[*] Written: {written // (1024*1024)} MB", end='\r')
                    except (OSError, IOError):
                        # Disk full
                        break
                
                f.flush()
                os.fsync(f.fileno())
            
            print(f"\n[*] Filled {written // (1024*1024)} MB of free space")
            
        finally:
            # Remove temporary file
            if os.path.exists(temp_file):
                os.remove(temp_file)
                print("[✓] Free space wipe complete\n")

class FileRecoveryChecker:
    """Educational component to check if files can be recovered"""
    
    @staticmethod
    def check_file_recovery(filepath):
        """Check if a deleted file might be recoverable"""
        print("\n[Educational Information]")
        print("=" * 50)
        print("File Recovery Prevention:")
        print("- Standard deletion only removes file system references")
        print("- Data remains on disk until overwritten")
        print("- SSD TRIM commands may complicate secure deletion")
        print("- Multiple overwrite passes increase security")
        print("\nFactors affecting recovery:")
        
        # Check file system
        if platform.system() == 'Windows':
            print("- Windows: NTFS may keep file in Recycle Bin")
        elif platform.system() == 'Darwin':
            print("- macOS: APFS uses copy-on-write, complicating deletion")
        else:
            print("- Linux: ext4 journals may retain file metadata")
        
        # Check if SSD
        print("\nStorage considerations:")
        print("- HDDs: Overwriting is generally effective")
        print("- SSDs: Wear leveling may leave data copies")
        print("- Use manufacturer's secure erase for SSDs when possible")
        print("=" * 50)

def main():
    parser = argparse.ArgumentParser(
        description='Secure Data Sanitization Tool - Educational Purpose Only',
        epilog='WARNING: This tool permanently destroys data. Always backup important files!'
    )
    
    parser.add_argument('action', choices=['shred', 'wipe', 'info'],
                       help='Action to perform')
    parser.add_argument('target', nargs='?',
                       help='File to shred or directory for free space wipe')
    parser.add_argument('-m', '--method', default='dod3',
                       choices=['zeros', 'ones', 'random', 'dod3', 'dod7', 'gutmann'],
                       help='Overwrite method (default: dod3)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    parser.add_argument('--confirm', action='store_true',
                       help='Skip confirmation prompt')
    
    args = parser.parse_args()
    
    # Show educational info
    if args.action == 'info':
        print("\nSecure Data Sanitization Methods:")
        print("=" * 50)
        print("zeros    : Single pass with zeros")
        print("ones     : Single pass with ones")
        print("random   : Single pass with random data")
        print("dod3     : DoD 5220.22-M 3-pass standard")
        print("dod7     : DoD 5220.22-M 7-pass standard")
        print("gutmann  : 35-pass Gutmann method")
        print("\nNotes:")
        print("- More passes = more secure but slower")
        print("- Modern drives may need manufacturer tools")
        print("- Physical destruction is most secure")
        print("=" * 50)
        
        if args.target and os.path.exists(args.target):
            FileRecoveryChecker.check_file_recovery(args.target)
        
        return
    
    if not args.target:
        parser.error(f"Target required for {args.action} action")
    
    # Initialize secure delete
    shredder = SecureDelete(verbose=args.verbose)
    
    # Confirmation prompt
    if not args.confirm:
        print("\n" + "!" * 60)
        print("WARNING: This tool PERMANENTLY DESTROYS data!")
        print("The deleted data CANNOT be recovered!")
        print("!" * 60)
        
        if args.action == 'shred':
            print(f"\nTarget file: {args.target}")
        else:
            print(f"\nTarget directory: {args.target}")
        
        confirm = input("\nType 'YES' to continue: ")
        if confirm != 'YES':
            print("Operation cancelled.")
            sys.exit(0)
    
    try:
        if args.action == 'shred':
            # Shred file
            shredder.shred_file(args.target, method=args.method)
            
            # Show educational info
            FileRecoveryChecker.check_file_recovery(args.target)
            
        elif args.action == 'wipe':
            # Wipe free space
            if not os.path.isdir(args.target):
                print(f"Error: {args.target} is not a directory")
                sys.exit(1)
            
            shredder.wipe_free_space(args.target)
    
    except KeyboardInterrupt:
        print("\n\n[!] Operation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
