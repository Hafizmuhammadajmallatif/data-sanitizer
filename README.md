# 🔐 Secure Data Sanitization Tool

An educational Python tool demonstrating secure file deletion techniques and data sanitization methods.

> ⚠️ **WARNING:**  
> This tool **PERMANENTLY DESTROYS** data. Deleted files **CANNOT** be recovered. Use with extreme caution and always maintain backups of important data.

---

## 🧭 Overview

This tool demonstrates various secure deletion algorithms used to prevent data recovery.  
It is designed for **educational purposes** to help understand:

- How secure deletion works
- Why standard file deletion isn't truly secure

---

## ✨ Features

### 🔁 Multiple Overwrite Methods
- `zeros`: Single pass (overwrite with zeros)
- `ones`: Single pass (overwrite with ones)
- `random`: Single pass (overwrite with random data)
- `dod3`: 3-pass DoD 5220.22-M method
- `dod7`: 7-pass DoD 5220.22-M extended
- `gutmann`: 35-pass Gutmann method

### 🔐 Security Features
- Cryptographically secure random data generation
- File system cache flushing
- Metadata obscuration (renaming before deletion)
- Free space wiping

### 📚 Educational Focus
- Explanations for each deletion method
- Why recovery prevention matters
- Platform-specific considerations

---

## 🛠 Installation & Usage

### 🔽 Clone the Repository

```bash
git clone https://github.com/yourusername/secure-data-sanitizer.git
cd secure-data-sanitizer

💻 Make Executable (Linux/macOS)
bash
Copy
Edit
chmod +x secure_delete.py
✅ No external dependencies required — uses only Python standard library.

🚀 Commands
Command	Description
python secure_delete.py info	Show details about all deletion methods
python secure_delete.py shred sensitive_file.txt	Securely delete a file (default DoD 3-pass)
python secure_delete.py shred sensitive_file.txt -m gutmann	Use a specific method (e.g., Gutmann)
python secure_delete.py wipe /path/to/dir	Wipe free space in a directory
python secure_delete.py shred file.txt -v	Verbose mode (detailed output)
python secure_delete.py shred file.txt --confirm	Skip confirmation prompt (dangerous!)

🧠 How It Works
❌ Standard File Deletion
Only removes file system references

Data remains on disk until overwritten

Easily recoverable with undelete tools

✅ Secure Overwriting
Writes patterns over original data multiple times

Reduces or eliminates chance of recovery

🕵️ Metadata Obfuscation
Renames file before deletion

Obscures filename from file system journals

🔐 Security Considerations
Storage Type	Notes
HDDs	Overwriting generally effective. Multiple passes improve security.
SSDs	TRIM & wear leveling may prevent full sanitization. Use manufacturer tools.
File Systems	Journaling may retain metadata. Use full-disk encryption + secure erase when possible.

✅ Best Practices
Use full-disk encryption

Use manufacturer tools for SSDs

Physically destroy drives for maximum security

Consider the sensitivity of data before deletion

⚠ Limitations
❌ Not ideal for SSDs due to controller behaviors

❌ Cannot wipe slack space

❌ Does not clear RAM

❌ Simplified free space wiping logic

🎓 Educational Purpose
This tool is created to:

Demonstrate how secure deletion works

Educate about data persistence

Compare various overwriting algorithms

🧑‍⚖️ Ethical Use
Only use this tool on files and systems you own.

Respect privacy and data protection laws

Do not use to destroy evidence

Consider environmental impact of physical destruction

🤝 Contributing
Contributions are welcome!
If submitting a PR, please:

Add educational comments or docs

Include relevant warnings

Report vulnerabilities responsibly

📚 References
DoD 5220.22-M Standard

Gutmann Method

NIST SP 800-88 Guidelines

📄 License
MIT License — Free to use, modify, and share.

⚠ Disclaimer
This tool is provided for educational purposes only.
The authors are not responsible for any damage, misuse, or data loss.
Always back up your data before using any deletion tool.
