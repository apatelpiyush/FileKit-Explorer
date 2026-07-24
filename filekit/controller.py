import sys
from filekit.conversion import *


def main():

    action = sys.argv[1]
    files = [f for f in sys.argv[2:] if f.strip()]

    try:

        if action == "merge":
            print(sys.argv)
            print(files)
            pdf_merge(files)

        elif action == "img2pdf":
            img2pdf(files)

        elif action == "doc2pdf":
            doc2pdf(files[0])

        elif action == "ppt2pdf":
            ppt2pdf(files[0])

        elif action == "compress":
            pdf_compress(files[0])

    except Exception as e:
        raise RuntimeError("Invalid Action") from e

if __name__ == "__main__":
    main()