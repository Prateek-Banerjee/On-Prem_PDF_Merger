import tkinter as tk
from gui import PDFMergerApp


def main():
    root = tk.Tk()
    root.iconbitmap("App_Icon.ico")
    PDFMergerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
