Secure Data Sanitization Tool
An educational Python tool demonstrating secure file deletion techniques and data sanitization
methods.
⚠ WARNING
This tool PERMANENTLY DESTROYS data. Deleted files CANNOT be recovered. Use with
extreme caution and always maintain backups of important data.
Overview
This tool demonstrates various secure deletion algorithms used to prevent data recovery. It's designed
for educational purposes to understand how secure deletion works and why standard file deletion isn't
secure.
Features
Multiple Overwrite Methods:
Single pass (zeros/ones/random)
DoD 5220.22-M (3-pass and 7-pass)
Gutmann 35-pass method
Security Features:
Cryptographically secure random data generation
File system cache flushing
Metadata obscuration through renaming
Free space wiping capability
Educational Components:
Detailed information about each deletion method
Recovery prevention explanations
Platform-specific considerations
Installation
Usage
Basic Commands
Available Methods
Method Passes Description
zeros 1 Overwrite with zeros
ones 1 Overwrite with ones
random 1 Overwrite with random data
dod3 3 DoD 5220.22-M standard
dod7 7 DoD 5220.22-M extended
gutmann 35 Gutmann method (most thorough)
How It Works
bash
# Clone the repository# Clone the repository
gitgit clone https://github.com/yourusername/secure-data-sanitizer.gitclone https://github.com/yourusername/secure-data-sanitizer.git
cdcd secure-data-sanitizersecure-data-sanitizer
# Make executable (Linux/macOS)# Make executable (Linux/macOS)
chmodchmod +x secure_delete.py+x secure_delete.py
# No external dependencies required - uses Python standard library only# No external dependencies required - uses Python standard library only
bash
# Show information about deletion methods# Show information about deletion methods
python secure_delete.py infopython secure_delete.py info
# Securely delete a file (default DoD 3-pass)# Securely delete a file (default DoD 3-pass)
python secure_delete.py shred sensitive_file.txtpython secure_delete.py shred sensitive_file.txt
# Use specific deletion method# Use specific deletion method
python secure_delete.py shred sensitive_file.txt -m gutmannpython secure_delete.py shred sensitive_file.txt -m gutmann
# Wipe free space in a directory# Wipe free space in a directory
python secure_delete.py wipe /path/to/directorypython secure_delete.py wipe /path/to/directory
# Verbose mode for detailed output# Verbose mode for detailed output
python secure_delete.py shred file.txt -vpython secure_delete.py shred file.txt -v
# Skip confirmation prompt (dangerous!)# Skip confirmation prompt (dangerous!)
python secure_delete.py shred file.txt --confirmpython secure_delete.py shred file.txt --confirm
1. Standard File Deletion (Insecure)
Operating system only removes file system references
Data remains on disk until overwritten
Can be easily recovered with undelete tools
2. Secure Overwriting
Writes patterns over the original data multiple times
Different patterns target various storage technologies
Makes data recovery extremely difficult or impossible
3. Metadata Removal
Renames file to random name before deletion
Obscures original filename from file system journals
Security Considerations
Hard Disk Drives (HDDs)
Overwriting is generally effective
Multiple passes increase security
Magnetic remnance theoretically possible but practically difficult
Solid State Drives (SSDs)
Wear leveling may leave data copies
TRIM commands complicate secure deletion
Controller may move data internally
Recommend using manufacturer's secure erase command
File Systems
NTFS (Windows): Shadow copies may retain data
APFS (macOS): Copy-on-write may preserve old versions
ext4 (Linux): Journal may contain file metadata
Best Practices
. Use full-disk encryption to protect data at rest
. For SSDs, use manufacturer secure erase tools when possible
. Physical destruction is the only 100% secure method
. Consider the sensitivity of data when choosing method
Limitations
. Not suitable for SSDs: Due to wear leveling and internal controller behavior
. Cannot wipe slack space: File system may store data in unreachable areas
. No memory wiping: RAM may contain sensitive data
. Limited free space wiping: Simplified implementation
Educational Purpose
This tool is designed to:
Demonstrate secure deletion concepts
Show why standard deletion is insecure
Educate about data persistence
Illustrate different overwriting algorithms
Ethical Use
Only use on files and systems you own
Respect privacy and data protection laws
Do not use to destroy evidence
Consider environmental impact of physical destruction
Contributing
Contributions welcome! Please ensure any PRs:
Include educational documentation
Add appropriate warnings
Follow responsible disclosure for any security issues
References
DoD 5220.22-M Standard
Gutmann Method
NIST SP 800-88 Guidelines for Media Sanitization
License
MIT License - See LICENSE file for details
Disclaimer
This tool is provided for educational purposes only. The authors are not responsible for any data loss or
misuse. Always ensure you have proper backups before using any data destruction tool.
