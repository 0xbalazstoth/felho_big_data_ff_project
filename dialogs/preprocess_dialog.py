import customtkinter as ctk
from customtkinter import E, N, ON, S
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import pandas as pd
import re
import demoji

class PreprocessDialog(simpledialog.Dialog):

    def body(self, master):
        ctk.CTkLabel(master, text='Load dataset:').grid(row=0)
        self.file_path_var = tk.StringVar()
        self.file_path_entry = ctk.CTkEntry(master, textvariable=self.file_path_var, state='readonly')
        self.file_path_entry.grid(row=0, column=1)
        ctk.CTkButton(master, text='Browse...', command=self.load_dataset).grid(row=0, column=2)
        self.clean_text_var = tk.BooleanVar()
        self.tokenization_var = tk.BooleanVar()
        self.lemmatization_var = tk.BooleanVar()
        ctk.CTkCheckBox(master, text='Clean Text', variable=self.clean_text_var).grid(row=1, column=0, sticky='w')
        info_button = ctk.CTkButton(master, text='i')
        info_button.grid(row=1, column=1, sticky='w')
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
        if self.clean_text_var.get():
            df = df.applymap(lambda x: self.clean_text(x) if isinstance(x, str) else x)
        
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
        text = re.sub('\\d+', '', text)
        text = re.sub('\\s+', ' ', text).strip()
        text = self.remove_emojis(text)
        return text

    def remove_emojis(self, text):
        return demoji.replace(text, '')