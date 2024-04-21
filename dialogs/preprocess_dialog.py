import customtkinter as ctk
from customtkinter import E, N, ON, S
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import pandas as pd
import re
import demoji
from PIL import Image, ImageTk

class PreprocessDialog(simpledialog.Dialog):

    def body(self, master):
        ctk.CTkLabel(master, text='Load dataset:').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.file_path_var = tk.StringVar()
        self.file_path_entry = ctk.CTkEntry(master, textvariable=self.file_path_var, state='readonly')
        self.file_path_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Load browse image
        browse_img = ImageTk.PhotoImage(Image.open("assets/browse.png").resize((18, 18), Image.ANTIALIAS))
        
        # Create browse button with image
        self.browse_button = ctk.CTkButton(master, image=browse_img, command=self.load_dataset, text="Browse", compound="left", text_color="#000", fg_color="#F9F9F9", hover_color="#D0D0D0")
        self.browse_button.image = browse_img
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        self.clean_text_var = tk.BooleanVar()
        self.remove_duplicates_var = tk.BooleanVar()
        self.remove_numeric_var = tk.BooleanVar()  # Checkbox variable for removing numeric values
        
        # TODO: Checkbox for custom regex with input field
        
        # Checkboxes
        ctk.CTkCheckBox(master, text='Clean Text', variable=self.clean_text_var).grid(row=1, column=0, columnspan=3, sticky='w', padx=5, pady=5)
        ctk.CTkCheckBox(master, text='Remove Duplicates', variable=self.remove_duplicates_var).grid(row=2, column=0, columnspan=3, sticky='w', padx=5, pady=5)
        ctk.CTkCheckBox(master, text='Remove Numeric Values', variable=self.remove_numeric_var).grid(row=3, column=0, columnspan=3, sticky='w', padx=5, pady=5)
        
        return master

    def load_dataset(self):
        file_types = [('CSV files', '*.csv')]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            self.file_path_var.set(file_path)

    def apply(self):
        file_path = self.file_path_var.get()
        if not file_path:
            messagebox.showerror('Error', 'Please select a dataset.')
            return
        df = pd.read_csv(file_path) if file_path.endswith('.csv') else None
        if df is None:
            messagebox.showerror('Error', 'Unsupported file format.')
            return
        
        # Apply preprocessing steps
        if self.clean_text_var.get():
            df = df.applymap(lambda x: self.clean_text(x) if isinstance(x, str) else x)
        if self.remove_duplicates_var.get():
            df.drop_duplicates(inplace=True)
        if self.remove_numeric_var.get():
            df = df.applymap(lambda x: self.remove_numeric(x) if isinstance(x, str) else x)
        
        # Prompt user for save location
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not save_path:
            messagebox.showinfo('Info', 'Preprocessing completed but no file was saved.')
            return
        
        df.to_csv(save_path, index=False)
        
        messagebox.showinfo('Success', 'Preprocessing completed. File saved at: {}'.format(save_path))

    def clean_text(self, text):
        if pd.isnull(text):
            return text
        text = text.lower()
        text = re.sub('http[s]?://\\S+', '', text)
        text = re.sub('@\\w+', '', text)
        text = re.sub('#\\w+', '', text)
        text = re.sub('\\s+', ' ', text).strip()
        text = self.remove_emojis(text)
        return text

    def remove_numeric(self, text):
        if pd.isnull(text):
            return text
        # Remove numeric values
        text = re.sub(r'\d+', '', text)
        return text

    def remove_emojis(self, text):
        return demoji.replace(text, '')
