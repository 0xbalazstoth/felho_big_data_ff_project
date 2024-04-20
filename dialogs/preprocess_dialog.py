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
        self.create_tooltip(info_button, 'Convert to lowercase\n- Remove URLs, mentions, hashtags\n- Remove numbers\n- Normalize spaces\n- Remove emojis')
        return master

    def create_tooltip(self, widget, text):
        tooltip_window = None

        def on_enter(event):
            nonlocal tooltip_window
            x, y, cx, cy = widget.bbox('insert')
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 20
            tooltip_window = ctk.CTkToplevel(widget)
            tooltip_window.wm_overrideredirect(True)
            tooltip_window.wm_geometry('+%d+%d' % (x, y))
            label = ctk.CTkLabel(tooltip_window, text=text, justify='left', background='#ffffe0', relief='solid', foreground='black', borderwidth=1, font=('tahoma', '8', 'normal'))
            label.pack(ipadx=1)

        def on_leave(event):
            nonlocal tooltip_window
            if tooltip_window:
                tooltip_window.destroy()
                tooltip_window = None
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)

    def load_dataset(self):
        file_types = [('CSV files', '*.csv'), ('JSON files', '*.json')]
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
        messagebox.showinfo('Success', 'Preprocessing completed.')

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