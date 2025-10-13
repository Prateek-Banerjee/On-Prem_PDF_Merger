import pathlib
from tkinterdnd2 import TkinterDnD as tk
from src.gui import PDFMergerApp


def main():
    root = tk.Tk()
    icon_path = pathlib.Path.cwd().joinpath("App_Icon.ico")
    root.iconbitmap(icon_path)
    PDFMergerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
