import pathlib
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog, messagebox
from pdf_upload_manager import PDFUploadManager
from pdf_merge_logic import PDFMerger


class PDFMergerApp:
    """
    Tkinter GUI for uploading, rearranging, and merging PDFs.
    """

    def __init__(self, root: tk.Tk):
        self.root: tk.Tk = root
        self.root.title("PDF Merger")

        # Make window resizable
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        screen_width: int = self.root.winfo_screenwidth()
        screen_height: int = self.root.winfo_screenheight()
        app_width, app_height = int(screen_width * 0.5), int(screen_height * 0.5)
        self.root.geometry(f"{app_width}x{app_height}")
        self.font: tkFont.Font =  tkFont.Font(family="Arial", size=14)

        self.is_dark_mode = False

        # Generate UI components
        self.create_widgets()

        # Drag-and-drop data
        self.drag_data = {"widget": None, "index": None}
        
        self.pdf_upload_manager = PDFUploadManager()

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
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf")]
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
                "Insufficient PDF Files", "Please upload at least two PDFs.")
            return

        save_path = filedialog.asksaveasfilename(
            title="Save merged PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        if save_path:
            try:
                merger = PDFMerger(self.pdf_upload_manager.get_ordered_files())
                merger.merge(pathlib.Path(save_path).parent,
                             pathlib.Path(save_path).name)
                messagebox.showinfo("Success", "PDFs merged successfully!")
                self.listbox.delete(0, tk.END)
                self.pdf_upload_manager.pdf_files.clear()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def toggle_theme(self):
        """Switch between dark and light mode."""
        self.is_dark_mode = not self.is_dark_mode
        self.__apply_theme()

    def __create_app_window(self) -> tk.Frame:
        main_frame = tk.Frame(self.root)
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

        self.upload_btn = tk.Button(
            btn_frame, text="Upload File", font=self.font, command=self.upload_files)
        self.upload_btn.grid(row=0, column=0, padx=5, sticky="ew")

        self.remove_btn = tk.Button(
            btn_frame, text="Remove File", font=self.font, command=self.remove_selected_file)
        self.remove_btn.grid(row=0, column=1, padx=5, sticky="ew")

        self.merge_btn = tk.Button(
            btn_frame, text="Merge Files", font=self.font, command=self.merge_pdfs)
        self.merge_btn.grid(row=0, column=2, padx=5, sticky="ew")

        self.theme_btn = tk.Button(
            btn_frame, text="Toggle Theme", font=self.font, command=self.toggle_theme)
        self.theme_btn.grid(row=0, column=3, padx=5, sticky="ew")

    def __create_listbox(self, main_frame: tk.Frame) -> tk.Listbox:
        # Frame for listbox and scrollbar
        listbox_frame = tk.Frame(main_frame)
        listbox_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        listbox_frame.rowconfigure(0, weight=1)
        listbox_frame.columnconfigure(0, weight=1)

        # Listbox
        listbox = tk.Listbox(listbox_frame, width=50,
                             height=20, font=self.font)
        listbox.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        scrollbar = tk.Scrollbar(
            listbox_frame, orient="vertical", command=listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        listbox.config(yscrollcommand=scrollbar.set)

        return listbox

    def __apply_theme(self):
        """Apply dark or light mode theme."""
        if self.is_dark_mode:
            bg_color = "#2E2E2E"
            fg_color = "#FFFFFF"
            btn_bg = "#444444"
            btn_fg = "#FFFFFF"
        else:
            bg_color = "#FFFFFF"
            fg_color = "#000000"
            btn_bg = "#E0E0E0"
            btn_fg = "#000000"

        # Apply to root
        self.root.configure(bg=bg_color)

        # Apply to listbox and scrollbar
        self.listbox.configure(
            bg=bg_color, fg=fg_color, selectbackground="#888888", selectforeground="#FFFFFF")

        self.__refresh_listbox()

        # Apply to buttons
        for btn in [self.upload_btn, self.remove_btn, self.merge_btn, self.theme_btn]:
            btn.configure(bg=btn_bg, fg=btn_fg,
                          activebackground="#666666", activeforeground="#FFFFFF")

    def __refresh_listbox(self) -> None:
        """Refresh the listbox display to match upload_manager.pdf_files with zebra striping."""
        self.listbox.delete(0, tk.END)
        for idx, pdf in enumerate(self.pdf_upload_manager.pdf_files):
            self.listbox.insert(tk.END, pdf.name)

            if not self.is_dark_mode:
                if idx % 2 == 0:
                    self.listbox.itemconfig(idx, background="#CACACA")
                else:
                    self.listbox.itemconfig(idx, background="#FFFFFF")
            else:
                if idx % 2 == 0:
                    self.listbox.itemconfig(idx, background="#888888")

    def __on_drag_start(self, event) -> None:
        """Remember the item being dragged."""
        widget = event.widget
        index = widget.nearest(event.y)
        if index >= 0:
            self.drag_data["widget"] = widget
            self.drag_data["index"] = index

    def __on_drag_motion(self, event) -> None:
        """Visual feedback during drag."""
        widget = self.drag_data["widget"]
        if widget:
            widget.selection_clear(0, tk.END)
            widget.selection_set(widget.nearest(event.y))

    def __on_drag_release(self, event) -> None:
        """Reorder listbox + backend list when dropped."""
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
