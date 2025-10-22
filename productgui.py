"""
GUI Product Manager
- Janela amarela com menus (Tkinter)
- Mantém o mesmo formato CSV usado no script original (linhas: id,name,supplier id,about) para integrar no Excel
- Substitui vírgulas por `;` nos campos para não quebrar o CSV
- Menu: File -> Open CSV, Exit
- Actions -> Add, List, Report

Guardar como: gui_product_manager.py
Executar: python gui_product_manager.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import csv
import os

DEFAULT_FILE = "product.csv"

class ProductGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Product CSV Manager")
        self.geometry("800x600")
        # Janela amarela
        self.configure(bg="#FFFF00")

        self.csvfile = DEFAULT_FILE

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open CSV...", command=self.open_csv)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.on_exit)
        menubar.add_cascade(label="File", menu=filemenu)

        actions = tk.Menu(menubar, tearoff=0)
        actions.add_command(label="Add", command=self.add_item)
        actions.add_command(label="List", command=self.list_items)
        actions.add_command(label="Report (search)", command=self.report_items)
        menubar.add_cascade(label="Actions", menu=actions)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.config(menu=menubar)

    def create_widgets(self):
        # Top frame with current file label and basic buttons
        top = tk.Frame(self, bg="#FFF9A8")
        top.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)

        self.file_label = tk.Label(top, text=f"CSV: {self.csvfile}", bg="#FFF9A8")
        self.file_label.pack(side=tk.LEFT)

        btn_add = tk.Button(top, text="Add", command=self.add_item,bg="#FFFF00")
        btn_add.pack(side=tk.RIGHT, padx=4)
        btn_list = tk.Button(top, text="List", command=self.list_items,bg="#FFFF00")
        btn_list.pack(side=tk.RIGHT, padx=4)

        # Text area to show CSV contents or results
        self.text = tk.Text(self, wrap=tk.NONE,bg="#FFFF00")
        self.text.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0,8))

        # Add horizontal and vertical scrollbars
        xscroll = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.text.xview)
        xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        yscroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.configure(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)

    def open_csv(self):
        f = filedialog.askopenfilename(title="Open CSV file", filetypes=[("CSV files","*.csv"), ("All files","*.*")])
        if f:
            self.csvfile = f
            self.file_label.config(text=f"CSV: {self.csvfile}")
            self.list_items()

    def on_exit(self):
        self.destroy()

    def show_about(self):
        messagebox.showinfo("About", "Product CSV Manager\nJanela amarela com menus\nMantem formato CSV para integrar no Excel")

    def ensure_file(self):
        # Create file if it doesn't exist
        if not os.path.exists(self.csvfile):
            with open(self.csvfile, "w", newline='', encoding='utf-8-sig') as fh:
                # no header by design (keeps behavior of original script)
                pass

    def sanitize(self, s: str) -> str:
        # Replace commas so they don't break CSV columns (original script replaced with ';')
        return s.replace(",", ";")

    def add_item(self):
        # Simple form in a modal dialog
        dlg = tk.Toplevel(self)
        dlg.title("Add product")
        dlg.transient(self)
        dlg.grab_set()
        dlg.configure(bg="#FFF9A8")

        labels = ["id number", "name", "supplier id", "about"]
        entries = []
        for i, lab in enumerate(labels):
            tk.Label(dlg, text=lab + ":", bg="#FFF9A8").grid(row=i, column=0, sticky=tk.W, padx=8, pady=6)
            e = tk.Entry(dlg, width=60)
            e.grid(row=i, column=1, padx=8, pady=6)
            entries.append(e)

        def on_save():
            vals = [self.sanitize(e.get().strip()) for e in entries]
            if not vals[0]:
                messagebox.showwarning("Validation", "id number is required")
                return
            line = ",".join(vals)
            try:
                with open(self.csvfile, "a", newline='', encoding='utf-8-sig') as fh:
                    fh.write(line + "\n")
                dlg.destroy()
                messagebox.showinfo("Saved", "Linha adicionada ao CSV")
                self.list_items()
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        btn_frame = tk.Frame(dlg, bg="#FFF9A8")
        btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=8)
        tk.Button(btn_frame, text="Save", command=on_save).pack(side=tk.LEFT, padx=6)
        tk.Button(btn_frame, text="Cancel", command=dlg.destroy).pack(side=tk.LEFT, padx=6)

        # Center dialog
        dlg.update_idletasks()
        w = dlg.winfo_width(); h = dlg.winfo_height()
        x = self.winfo_x() + (self.winfo_width() - w)//2
        y = self.winfo_y() + (self.winfo_height() - h)//2
        dlg.geometry(f"+{x}+{y}")

    def list_items(self):
        self.ensure_file()
        try:
            with open(self.csvfile, "r", encoding='utf-8-sig') as fh:
                data = fh.read()
        except Exception as ex:
            data = f"Erro a ler ficheiro: {ex}"
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, data)

    def report_items(self):
        self.ensure_file()
        q = simpledialog.askstring("Find what?", "Texto a procurar:", parent=self)
        if q is None:
            return
        q = q.strip()
        results = []
        try:
            with open(self.csvfile, "r", encoding='utf-8-sig') as fh:
                for line in fh:
                    if q.lower() in line.lower():
                        results.append(line.rstrip('\n'))
        except Exception as ex:
            messagebox.showerror("Error", str(ex))
            return
        self.text.delete(1.0, tk.END)
        if results:
            self.text.insert(tk.END, "\n".join(results))
        else:
            self.text.insert(tk.END, "(no matches)")

if __name__ == '__main__':
    app = ProductGUI()
    app.list_items()
    app.mainloop()

