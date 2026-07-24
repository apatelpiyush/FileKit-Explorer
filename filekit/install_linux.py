from pathlib import Path
import os
import shutil

FILEKIT = shutil.which("filekit")

if FILEKIT is None:
    raise RuntimeError("filekit executable not found. Install File-Kit first.")

SCRIPT_DIR = (
    Path.home()
    / ".local/share/nautilus/scripts/Converter"
)

SCRIPT_DIR.mkdir(parents=True, exist_ok=True)


def create_script(name, action):
    script_path = SCRIPT_DIR / name

    content = f"""#!/usr/bin/env bash

files=()

while IFS= read -r file; do
    [[ -n "$file" ]] && files+=("$file")
done <<< "$NAUTILUS_SCRIPT_SELECTED_FILE_PATHS"

"{FILEKIT}" {action} "${{files[@]}}"
"""

    script_path.write_text(content)
    os.chmod(script_path, 0o755)


# Create the Nautilus scripts
create_script("Merge PDF", "merge")
create_script("Image To PDF", "img2pdf")
create_script("DOC To PDF", "doc2pdf")
create_script("PPT To PDF", "ppt2pdf")
create_script("Compress PDF", "compress")

print("✓ File-Kit Nautilus scripts installed successfully.")