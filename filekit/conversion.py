import os
from pathlib import Path
import tempfile
import subprocess
import platform
import shutil
from concurrent.futures import ThreadPoolExecutor

def doc2pdf(file_path):
    q = Path(file_path)

    libreoffice = None

    if os.name == "nt":
        candidates = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        ]
        for exe in candidates:
            if os.path.exists(exe):
                libreoffice = exe
                break

    if libreoffice is None:
        libreoffice = shutil.which("libreoffice") or shutil.which("soffice")

    if libreoffice:
        # unique profile dir per call, cross-platform
        profile_dir = Path(tempfile.gettempdir()) / f"lo_profile_{os.getpid()}_{id(q)}"
        profile_uri = profile_dir.as_uri()  # gives correct file:// format on both OSes

        subprocess.run(
            [
                libreoffice,
                "--headless",
                f"-env:UserInstallation={profile_uri}",
                "--convert-to", "pdf",
                str(q),
                "--outdir", str(q.parent)
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        )

        output_path = q.with_suffix(".pdf")
        if not output_path.exists():
            raise RuntimeError("DOC to PDF conversion failed")
        return str(output_path)

    if platform.system() == "Windows":
        from docx2pdf import convert
        output_path = q.with_suffix(".pdf")
        convert(str(q), str(output_path))
        return str(output_path)

    raise RuntimeError("Neither LibreOffice nor Microsoft Word is installed.")

def img2pdf(image_files):
    from PIL import Image
    if not image_files:
        raise ValueError("No image files provided")

    paths = [Path(f) for f in image_files]
    output = paths[0].parent / (paths[0].stem + "_temp.pdf")

    images = []
    for p in paths:
        with Image.open(p) as img:
            images.append(img.convert("RGB"))

    images[0].save(
        output,
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=images[1:]
    )

    return str(output)


def convert_to_pdf(p: Path):
    suffix = p.suffix.lower()

    if suffix in [".jpg", ".jpeg", ".png", ".bmp"]:
        pdf = Path(img2pdf([str(p)]))
        return pdf, True

    elif suffix in [".doc", ".docx", ".odt"]:
        pdf = Path(doc2pdf(str(p)))
        return pdf, True

    elif suffix in [".ppt", ".pptx", ".odp"]:
        pdf = Path(ppt2pdf(str(p)))
        return pdf, True

    elif suffix == ".pdf":
        return p, False

    raise ValueError(f"Unsupported file: {p}")


def pdf_merge(files):
    from pypdf import PdfMerger
    if not files:
        raise ValueError("No files provided")

    paths = []

    for f in files:
        p = Path(f).expanduser().resolve()

        if not p.is_file():
            print(f"Skipping: {p}")
            continue

        paths.append(p)

    if not paths:
        raise ValueError("No valid files provided")
    # Number of worker threads
    workers = min(os.cpu_count() or 4, len(paths))

    pdf_list = [None] * len(paths)
    temp_files = []

    # ---------- CONVERT FILES IN PARALLEL ----------
    with ThreadPoolExecutor(max_workers=workers) as executor:

        futures = {
            executor.submit(convert_to_pdf, p): index
            for index, p in enumerate(paths)
        }

        for future in futures:
            index = futures[future]

            try:
                pdf_path, is_temp = future.result()
            except Exception:
                import traceback
                traceback.print_exc()
                raise

            if not pdf_path.exists():
                raise RuntimeError(f"Conversion failed:\n{pdf_path}")

            pdf_list[index] = pdf_path

            if is_temp:
                temp_files.append(pdf_path)
    
    # ---------- MERGE ----------
    output = paths[0].parent / (paths[0].stem + "_merged.pdf")
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(str(pdf))
    merger.write(str(output))
    merger.close()

    temp_files.append(output)
    # ---------- COMPRESS ----------
    final_output = Path(pdf_compress(output))
    # ---------- CLEANUP ----------
    for f in temp_files:
        if f != final_output:
            f.unlink(missing_ok=True)
    return str(final_output)


def pdf_compress(input_pdf, quality="ebook"):
    input_path = Path(input_pdf)
    output_path = input_path.with_name(input_path.stem + "_compressed.pdf")

    gs_command = "gswin64c" if os.name == "nt" else "gs"

    command = [
        gs_command,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{quality}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        str(input_path)
        
    ]
    if shutil.which(gs_command) is None:
        raise RuntimeError("Ghostscript not installed")
    subprocess.run(
    command,
    check=True,
    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
)

    return str(output_path)


def ppt2pdf(file_path):
    p = Path(file_path)

    if p.suffix.lower() not in [".ppt", ".pptx", ".odp"]:
        raise ValueError("Only PPT/PPTX/ODP files are supported")

    libreoffice = None

    # ---------- Find LibreOffice ----------
    if os.name == "nt":
        candidates = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        ]

        for exe in candidates:
            if os.path.exists(exe):
                libreoffice = exe
                break

    if libreoffice is None:
        libreoffice = shutil.which("libreoffice") or shutil.which("soffice")

    # ---------- Prefer LibreOffice ----------
    if libreoffice:
        profile_dir = Path(tempfile.gettempdir()) / f"lo_profile_{os.getpid()}_{id(p)}"
        profile_uri = profile_dir.as_uri()

        subprocess.run(
            [
                libreoffice,
                "--headless",
                f"-env:UserInstallation={profile_uri}",
                "--convert-to", "pdf",
                str(p),
                "--outdir", str(p.parent)
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        )

        output_path = p.with_suffix(".pdf")
        if not output_path.exists():
            raise RuntimeError("PPT to PDF conversion failed")
        return str(output_path)

    # ---------- Fallback to Microsoft PowerPoint ----------
    if platform.system() == "Windows":
        import win32com.client

        powerpoint = None
        presentation = None

        try:
            powerpoint = win32com.client.Dispatch("PowerPoint.Application")

            presentation = powerpoint.Presentations.Open(str(p.resolve()))

            output_path = p.with_suffix(".pdf")
            presentation.SaveAs(str(output_path), 32)

            return str(output_path)

        finally:
            if presentation:
                presentation.Close()
            if powerpoint:
                powerpoint.Quit()

    raise RuntimeError("Neither LibreOffice nor Microsoft PowerPoint is available.")
if __name__ == "__main__":

    print("This module is not intended to be run directly. Please use the controller script.")