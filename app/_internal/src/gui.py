import pathlib
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog, messagebox
from tkinter import ttk
from .pdf_upload_manager import PDFUploadManager
from .pdf_merge_logic import PDFMerger


class PDFMergerApp:
    """
    Tkinter GUI (ttk-styled) for uploading, rearranging, and merging PDFs.
    """

    def __init__(self, root: tk.Tk):
        self.root: tk.Tk = root
        self.root.title("PDF Merger")

        # Make window resizable
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        screen_width: int = self.root.winfo_screenwidth()
        screen_height: int = self.root.winfo_screenheight()
        app_width, app_height = int(
            screen_width * 0.5), int(screen_height * 0.5)
        self.root.geometry(f"{app_width}x{app_height}")
        self.font: tkFont.Font = tkFont.Font(family="Arial", size=13)

        # ttk styling
        self.style = ttk.Style(self.root)
        self.style.configure("TButton", font=("Arial", 13), padding=6)
        self.style.configure("TLabel", font=("Arial", 13))
        self.style.configure("TListbox", font=("Arial", 13))

        self.is_dark_mode = False

        # Drag-and-drop data
        self.drag_data = {"widget": None, "index": None}

        # Backend manager
        self.pdf_upload_manager = PDFUploadManager()

        # Generate UI components
        self.create_widgets()

        # Apply default theme
        self.__apply_theme()

    def create_widgets(self):
        main_window = self.__create_app_window()
        self.__create_buttons(main_window)
        self.listbox = self.__create_listbox(main_window)

        # Bind drag-and-drop
        self.listbox.bind("<Button-1>", self.__on_drag_start)
        self.listbox.bind("<B1-Motion>", self.__on_drag_motion)
        self.listbox.bind("<ButtonRelease-1>", self.__on_drag_release)

    def upload_files(self):
        """Open file dialog to select PDFs and add them to the list."""
        file_paths = filedialog.askopenfilenames(
            title="Select PDF files", filetypes=[("PDF files", "*.pdf")]
        )
        if file_paths:
            try:
                pdfs = [pathlib.Path(file) for file in file_paths]
                self.pdf_upload_manager.add_files(pdfs)
                self.__refresh_listbox()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def remove_selected_file(self):
        """Remove the selected file from the list."""
        selection = self.listbox.curselection()
        if not selection:
            return
        index = selection[0]
        pdf = self.pdf_upload_manager.pdf_files[index]
        self.pdf_upload_manager.remove_file(pdf)
        self.__refresh_listbox()

    def merge_pdfs(self):
        """Trigger merging process and save the merged file."""
        if len(self.pdf_upload_manager.pdf_files) < 2:
            messagebox.showwarning(
                "Insufficient PDF Files", "Please upload at least two PDFs."
            )
            return

        output_file_path = filedialog.asksaveasfilename(
            title="Save merged PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
        )

        if output_file_path:
            try:
                merger = PDFMerger(self.pdf_upload_manager.get_ordered_files())
                merger.merge(pathlib.Path(output_file_path))
                messagebox.showinfo("Success", "PDFs merged successfully!")
                self.listbox.delete(0, tk.END)
                self.pdf_upload_manager.pdf_files.clear()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def toggle_theme(self):
        """Switch between dark and light mode."""
        self.is_dark_mode = not self.is_dark_mode
        self.__apply_theme()

    def __create_app_window(self) -> ttk.Frame:
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure root to expand main_frame
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Configure grid rows/cols in main_frame
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=0)
        main_frame.columnconfigure(0, weight=1)

        return main_frame

    def __create_buttons(self, main_frame: tk.Frame):
        # Button frame
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        btn_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.upload_btn = ttk.Button(
            btn_frame, text="Upload File", command=self.upload_files
        )
        self.upload_btn.grid(row=0, column=0, padx=5, sticky="ew")

        self.remove_btn = ttk.Button(
            btn_frame, text="Remove File", command=self.remove_selected_file
        )
        self.remove_btn.grid(row=0, column=1, padx=5, sticky="ew")

        self.merge_btn = ttk.Button(
            btn_frame, text="Merge Files", command=self.merge_pdfs
        )
        self.merge_btn.grid(row=0, column=2, padx=5, sticky="ew")

        self.theme_btn = ttk.Button(
            btn_frame, text="Toggle Theme", command=self.toggle_theme
        )
        self.theme_btn.grid(row=0, column=3, padx=5, sticky="ew")

    def __create_listbox(self, main_frame: ttk.Frame) -> tk.Listbox:
        # Frame for listbox and scrollbar
        listbox_frame = ttk.Frame(main_frame)
        listbox_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        listbox_frame.rowconfigure(0, weight=1)
        listbox_frame.columnconfigure(0, weight=1)

        # Listbox
        listbox = tk.Listbox(
            listbox_frame, width=50, height=20, font=self.font, relief="flat", bd=2
        )
        listbox.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            listbox_frame, orient="vertical", command=listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        listbox.config(yscrollcommand=scrollbar.set)

        return listbox

    def __apply_theme(self):
        if self.is_dark_mode:
            bg_color = "#2E2E2E"
            fg_color = "#FFFFFF"
            listbox_bg = "#3C3C3C"
        else:
            bg_color = "#F8F8F8"
            fg_color = "#000000"
            listbox_bg = "#FFFFFF"

        # Apply to root
        self.root.configure(bg=bg_color)

        # Apply to listbox and scrollbar
        self.listbox.configure(
            bg=listbox_bg,
            fg=fg_color,
            selectbackground="#6666CC",
            selectforeground="#FFFFFF",
        )
        self.__refresh_listbox()

    def __refresh_listbox(self):
        """Refresh the listbox display to show the uploaded pdf files."""
        self.listbox.delete(0, tk.END)
        for idx, pdf in enumerate(self.pdf_upload_manager.pdf_files):
            self.listbox.insert(tk.END, pdf.name)
            if not self.is_dark_mode:
                if idx % 2 == 0:
                    self.listbox.itemconfig(idx, background="#ECECEC")
            else:
                if idx % 2 == 0:
                    self.listbox.itemconfig(idx, background="#444444")

    def __on_drag_start(self, event):
        """Remembers the item being dragged."""
        widget = event.widget
        index = widget.nearest(event.y)
        if index >= 0:
            self.drag_data["widget"] = widget
            self.drag_data["index"] = index

    def __on_drag_motion(self, event):
        """Visual feedback during drag."""
        widget = self.drag_data["widget"]
        if widget:
            widget.selection_clear(0, tk.END)
            widget.selection_set(widget.nearest(event.y))

    def __on_drag_release(self, event):
        """Reorders listbox and the backend list when releasing the dragged PDF."""
        widget = self.drag_data["widget"]
        if widget:
            from_index = self.drag_data["index"]
            to_index = widget.nearest(event.y)
            if from_index != to_index:
                pdf = self.pdf_upload_manager.pdf_files[from_index]
                self.pdf_upload_manager.rearrange_pdf(pdf, to_index)
                self.__refresh_listbox()
                widget.selection_set(to_index)
        self.drag_data = {"widget": None, "index": None}
