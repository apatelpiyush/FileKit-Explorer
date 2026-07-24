import winreg
import ctypes
import shutil
from pathlib import Path
import os

launcher = shutil.which("filekit.exe") or shutil.which("filekit")

if launcher is None:
    raise RuntimeError("filekit executable not found. Please install the package first.")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def create_entry(root, base, name, action):

    cmd = f'"{launcher}" {action} "%1"'

    with winreg.CreateKey(root, rf"{base}\shell\{name}\command") as key:
        winreg.SetValueEx(
            key,
            "",
            0,
            winreg.REG_SZ,
            cmd
        )


def install(root, base):

    with winreg.CreateKey(root, base) as menu:

        # Display text
        winreg.SetValueEx(
            menu,
            "MUIVerb",
            0,
            winreg.REG_SZ,
            "Converter"
        )

        # Make it a cascading menu
        winreg.SetValueEx(
            menu,
            "SubCommands",
            0,
            winreg.REG_SZ,
            ""
        )

        # Optional icon
        winreg.SetValueEx(
            menu,
            "Icon",
            0,
            winreg.REG_SZ,
            "shell32.dll,-152"
        )

    #create_entry(root, base, "Merge PDF", "merge")
    create_entry(root, base, "Image To PDF", "img2pdf")
    create_entry(root, base, "DOC To PDF", "doc2pdf")
    create_entry(root, base, "PPT To PDF", "ppt2pdf")
    create_entry(root, base, "Compress PDF", "compress")

def install_user():

    install(
        winreg.HKEY_CURRENT_USER,
        r"Software\Classes\AllFilesystemObjects\shell\Converter"
    )


def install_system():

    install(
        winreg.HKEY_CLASSES_ROOT,
        r"AllFilesystemObjects\shell\Converter"
    )
def install_sendto():
    import win32com.client

    sendto = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "SendTo"
    old_bat = sendto / "Merge-PDF.bat"
    old_bat.unlink(missing_ok=True)
    shortcut_path = sendto / "Merge-PDF.lnk"

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(shortcut_path))
    shortcut.TargetPath = launcher
    shortcut.Arguments = "merge"
    shortcut.WorkingDirectory = str(Path.home())
    shortcut.IconLocation = "shell32.dll,-152"
    shortcut.save()

    print("Installed SendTo shortcut")


if __name__ == "__main__":
    
    if is_admin():
        install_system()
        print("Installed system-wide")

    else:
        install_user()
        print("Installed for current user")
    install_sendto()