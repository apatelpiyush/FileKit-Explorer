# 📁 FileKit-Explorer

[![PyPI](https://img.shields.io/pypi/v/filekit-explorer)](https://pypi.org/project/filekit-explorer/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-success.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/filekit-explorer)](https://pypi.org/project/filekit-explorer/)

**FileKit-Explorer** is a cross-platform file conversion toolkit for **Windows** and **Linux**. It integrates directly into your file manager, allowing you to convert and manipulate files through the **right-click context menu** or from the **command line**.

---

## ✨ Features

- 📄 Merge multiple PDF files
- 🖼 Convert Images to PDF
- 📝 Convert Microsoft Word documents (.doc/.docx) to PDF
- 📊 Convert Microsoft PowerPoint presentations (.ppt/.pptx) to PDF
- 📦 Compress PDF files
- 🖱 Windows Explorer Context Menu Integration
- 🐧 Nautilus (GNOME Files) Integration
- 💻 Command-Line Interface (`filekit`)
- ⚡ Cross-platform support (Windows & Linux)

---

# 🚀 Quick Start

Install directly from **PyPI**

```bash
pip install filekit-explorer
```

Enable the right-click context menu.

### Windows

```powershell
python -m filekit.install_windows
```

### Linux (GNOME / Nautilus)

```bash
python -m filekit.install_linux
```

You're ready to start converting files directly from your file manager.

---

# 📥 Installation

## Install from PyPI (Recommended)

```bash
pip install filekit-explorer
```

Verify installation

```bash
filekit --help
```

---

## Install from Source (Developers)

```bash
git clone https://github.com/apatelpiyush/FileKit-Explorer.git

cd FileKit-Explorer

pip install -e .
```

---

# 🖥 Supported Platforms

| Platform | Status |
|----------|--------|
| Windows 10 / 11 | ✅ |
| Ubuntu / Debian (GNOME) | ✅ |
| Other Linux Distributions | ⚠️ Supported if Nautilus is installed |

---

# ⚙ External Requirements

Some features require additional software.

## Windows

| Software | Required For |
|----------|--------------|
| Microsoft Word | DOC/DOCX → PDF |
| Microsoft PowerPoint | PPT/PPTX → PDF |
| Ghostscript | PDF Compression |

### Install Ghostscript

Download from

https://ghostscript.com/releases/

After installation, ensure the **Ghostscript `bin` folder** is added to your system **PATH**.

Example

```
C:\Program Files\gs\gs10.xx.x\bin
```

---

## Linux

### LibreOffice

Required for

- DOC → PDF
- PPT → PDF

Install

```bash
sudo apt install libreoffice
```

---

### Ghostscript

Required for

- PDF Compression

Install

```bash
sudo apt install ghostscript
```

---

# 🖱 Installing Context Menu

## Windows

```powershell
python -m filekit.install_windows
```

Installs

- Converter Context Menu
- Send To → Merge PDF

---

## Linux

```bash
python -m filekit.install_linux
```

Restart Nautilus

```bash
nautilus -q
nautilus &
```

---

# 💻 Command Line Usage

### Merge PDFs

```bash
filekit merge file1.pdf file2.pdf
```

### Images → PDF

```bash
filekit img2pdf image1.jpg image2.png
```

### Word → PDF

```bash
filekit doc2pdf document.docx
```

### PowerPoint → PDF

```bash
filekit ppt2pdf presentation.pptx
```

### Compress PDF

```bash
filekit compress report.pdf
```

---

# 📂 Project Structure

```
File-Kit/
│
├── filekit/
│   ├── __init__.py
│   ├── controller.py
│   ├── conversion.py
│   ├── install_linux.py
│   └── install_windows.py
│
├── README.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
└── .gitignore
```

---

# 📦 Python Dependencies

All Python dependencies are installed automatically when installing File-Kit.

```bash
pip install filekit-explorer
```

For the complete list of dependencies, see:

➡️ **[requirements.txt](requirements.txt)**

---

# 🔨 Building from Source

Create a distributable wheel

```bash
python -m build
```

Output

```
dist/
├── filekit_explorer-x.x.x-py3-none-any.whl
└── filekit_explorer-x.x.x.tar.gz
```

---

# ❓ Troubleshooting

### `filekit` command not found

Reinstall the package

```bash
pip install --force-reinstall filekit-explorer
```

Ensure the Python **Scripts** directory is added to your system **PATH**.

---

### DOC/PPT conversion fails

Verify that

- Microsoft Office (Windows)

or

- LibreOffice (Linux)

is installed.

---

### PDF Compression fails

Verify Ghostscript installation

Linux

```bash
gs --version
```

Windows

```powershell
gswin64c -version
```

---

# 🛣 Roadmap

Planned features

- OCR Support
- EPUB Conversion
- PDF Encryption / Decryption
- Image Optimization
- Support Additional File Formats
- Additional Desktop Environment Support

---

# 🤝 Contributing

Contributions are welcome.

If you'd like to contribute:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

Bug reports and feature requests are always appreciated.

---

# 👨‍💻 Author

**Piyush Patel**

GitHub: https://github.com/apatelpiyush

---

# 📄 License

This project is licensed under the **MIT License**.

See **[LICENSE](LICENSE)** for complete details.

---

## 📚 Additional Files

- 📄 **[LICENSE](LICENSE)** — Project License
- 📦 **[requirements.txt](requirements.txt)** — Python Dependencies
- ⚙ **[pyproject.toml](pyproject.toml)** — Package Configuration