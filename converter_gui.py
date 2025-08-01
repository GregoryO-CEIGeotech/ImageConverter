import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
from pillow_heif import register_heif_opener
from pathlib import Path
import time

register_heif_opener()

SUPPORTED_FORMATS = ['JPEG', 'JPG', 'PNG', 'WEBP', 'GIF', 'BMP', 'ICO', 'TIFF', 'PPM', 'TGA']

# Function to convert a single image file
def convert_image(input_path, output_format, output_dir):
    try:
        image = Image.open(input_path)
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_file = os.path.join(output_dir, f"{base_name}.{output_format.lower()}")
        if output_format.upper() in ['JPEG', 'JPG'] and image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(output_file, output_format)
        return output_file
    except Exception as e:
        return str(e)

# GUI Application
class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Converter")
        self.root.geometry("1280x800")

        self.files = []

        self.root.grid_rowconfigure(7, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Drag-and-drop file area
        self.drop_label = tk.Label(root, text="Drag and drop files here or click 'Add Files'", relief=tk.SUNKEN, height=3)
        self.drop_label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        # Add, remove, and clear buttons
        self.add_button = tk.Button(root, text="Add Files", command=self.add_files)
        self.add_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.remove_button = tk.Button(root, text="Remove Selected", command=self.remove_selected)
        self.remove_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.clear_button = tk.Button(root, text="Clear All", command=self.clear_all)
        self.clear_button.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

        # File listbox with scrollbar
        self.file_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        self.file_listbox.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")
        self.root.grid_rowconfigure(2, weight=1)

        self.file_listbox.bind("<Button-3>", self.show_context_menu)
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Remove Selected", command=self.remove_selected)
        self.context_menu.add_command(label="Clear All", command=self.clear_all)

        # Format selection
        self.format_label = tk.Label(root, text="Select Output Format")
        self.format_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.format_var = tk.StringVar(value=SUPPORTED_FORMATS[0])
        self.format_menu = ttk.Combobox(root, textvariable=self.format_var, values=SUPPORTED_FORMATS)
        self.format_menu.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        # Output directory
        self.output_dir_button = tk.Button(root, text="Select Output Directory", command=self.select_output_directory)
        self.output_dir_button.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        self.output_dir = str(Path.home() / "Downloads")
        self.output_label = tk.Label(root, text=f"Output Dir: {self.output_dir}", wraplength=500, anchor="w", justify="left")
        self.output_label.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Convert button
        self.convert_button = tk.Button(root, text="Convert Images", command=self.convert_images)
        self.convert_button.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Results box
        self.result_box = tk.Text(root, height=10, wrap=tk.WORD)
        self.result_box.grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Time taken label
        self.time_label = tk.Label(root, text="")
        self.time_label.grid(row=8, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="ew")

    def add_files(self):
        new_files = filedialog.askopenfilenames(title="Select Image Files")
        for file in new_files:
            if file not in self.files:
                self.files.append(file)
                self.file_listbox.insert(tk.END, file)

    def remove_selected(self):
        selected_indices = self.file_listbox.curselection()
        selected_files = [self.file_listbox.get(i) for i in selected_indices]
        for file in selected_files:
            if file in self.files:
                self.files.remove(file)
        for i in reversed(selected_indices):
            self.file_listbox.delete(i)

    def clear_all(self):
        self.files.clear()
        self.file_listbox.delete(0, tk.END)

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def select_output_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir = directory
            self.output_label.config(text=f"Output Dir: {self.output_dir}")

    def convert_images(self):
        output_format = self.format_var.get()
        self.result_box.delete(1.0, tk.END)
        self.time_label.config(text="")
        if not self.files:
            messagebox.showwarning("No files", "Please add some image files to convert.")
            return

        start_time = time.time()

        for file_path in self.files:
            result = convert_image(file_path, output_format, self.output_dir)
            if os.path.exists(result):
                self.result_box.insert(tk.END, f"✔ Converted: {os.path.basename(result)}\n")
            else:
                self.result_box.insert(tk.END, f"✘ Failed: {file_path}\nReason: {result}\n")

        end_time = time.time()
        duration = end_time - start_time
        self.time_label.config(text=f"Conversion completed in {duration:.2f} seconds.")

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()
