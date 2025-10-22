# supplier_gui.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from tkinter.scrolledtext import ScrolledText
import csv
import os

CSV_FILE = "supplier.csv"
FIELDS = ["id", "name", "address", "phone", "email", "about"]

def ensure_csv_exists():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # opcional: não escrever header para manter o mesmo formato antigo
            # writer.writerow(FIELDS)
            pass

def add_record(values):
    # values: list com 6 strings
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(values)

def read_all_text():
    if not os.path.exists(CSV_FILE):
        return ""
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
        return f.read()

def search_records(term):
    results = []
    if not os.path.exists(CSV_FILE):
        return results
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            line = ",".join(row)
            if term.lower() in line.lower():
                results.append(line)
    return results

# --- GUI ---
class SupplierGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Supplier Manager")
        self.geometry("800x600")
        # fundo amarelo suave
        self.configure(bg="#FFFF00")  # amarelo claro

        self.create_menu()
        self.create_main_widgets()
        ensure_csv_exists()

    def create_menu(self):
        menubar = tk.Menu(self)
        # File menu
        filemenu = tk.Menu(menubar, tearoff=0,bg="#FFFF00")
        filemenu.add_command(label="Add", command=self.open_add_dialog)
        filemenu.add_command(label="List", command=self.show_list)
        filemenu.add_command(label="Report (Search)", command=self.open_search_dialog)
        filemenu.add_separator()
        filemenu.add_command(label="Open CSV (Explorer)", command=self.open_csv_location)
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        # Help menu
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        menubar.configure(bg="#FFFF00")
        self.config(menu=menubar)
        self.configure(bg="#FFFF00")
    def create_main_widgets(self):
        frame = ttk.Frame(self)
        frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        # Title label
        title = tk.Label(frame, text="Supplier Manager", font=("Segoe UI", 16, "bold"))
        title.pack(pady=(6, 4))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=6)
        ttk.Button(btn_frame, text="Add", command=self.open_add_dialog).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="List", command=self.show_list).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Report (Search)", command=self.open_search_dialog).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Refresh", command=self.show_list).pack(side="left", padx=4)
        # Text area for list / output
        self.text = ScrolledText(frame, wrap="none", height=25,bg="#FFFF00")
        self.text.pack(fill="both", expand=True, pady=(6,0))
        self.text.configure(font=("Courier New", 10))

        # show existing on start
        self.show_list()

    def open_add_dialog(self):
        dlg = AddDialog(self)
        self.wait_window(dlg)
        if dlg.values:
            # write to CSV (use values sanitized)
            add_record(dlg.values)
            messagebox.showinfo("Saved", "Registo gravado em: " + CSV_FILE)
            self.show_list()

    def show_list(self):
        content = read_all_text()
        # mostrar tal como no txt: cada linha com virgulas (compatível Excel)
        self.text.delete("1.0", tk.END)
        if content.strip() == "":
            self.text.insert(tk.END, "(ficheiro vazio)\n")
        else:
            self.text.insert(tk.END, content)

    def open_search_dialog(self):
        term = simpledialog.askstring("Search / Report", "Find what?")
        if term is None:
            return
        results = search_records(term)
        self.text.delete("1.0", tk.END)
        if not results:
            self.text.insert(tk.END, "Nenhum resultado encontrado.\n")
        else:
            for r in results:
                self.text.insert(tk.END, r + "\n")

    def open_csv_location(self):
        # abrir a pasta que contém o CSV
        path = os.path.abspath(CSV_FILE)
        folder = os.path.dirname(path)
        try:
            if os.name == "nt":
                os.startfile(folder)
            elif os.name == "posix":
                import subprocess
                subprocess.Popen(["xdg-open", folder])
            else:
                messagebox.showinfo("Info", f"CSV está em: {path}")
        except Exception:
            messagebox.showinfo("Info", f"CSV está em: {path}")

    def show_about(self):
        messagebox.showinfo("About", "Supplier GUI\nFormato CSV compatível com Excel.\nCampos por linha: id,name,address,phone,email,about")

class AddDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add supplier")
        self.transient(parent)
        self.resizable(False, False)
        self.values = None

        body = ttk.Frame(self, padding=8)
        body.pack(fill="both", expand=True)

        self.entries = {}
        for i, field in enumerate(FIELDS):
            lbl = ttk.Label(body, text=field.capitalize()+":")
            lbl.grid(row=i, column=0, sticky="e", padx=4, pady=4)
            ent = ttk.Entry(body, width=60)
            ent.grid(row=i, column=1, sticky="w", padx=4, pady=4)
            self.entries[field] = ent

        # About can be a larger text
        self.entries["about"].destroy()
        about_txt = tk.Text(body, width=60, height=5)
        about_txt.grid(row=5, column=1, padx=4, pady=4)
        self.entries["about"] = about_txt

        btn_frame = ttk.Frame(body)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=(6,0))
        ttk.Button(btn_frame, text="Save", command=self.on_save).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="left", padx=6)

    def on_save(self):
        vals = []
        for f in FIELDS:
            widget = self.entries[f]
            if isinstance(widget, tk.Text):
                v = widget.get("1.0", tk.END).strip()
            else:
                v = widget.get().strip()
            # NÃO substituir vírgulas: usamos csv quoting, manter vírgulas se o user quiser
            # Mas remover novas linhas dentro do campo about para manter cada registo numa linha
            v = v.replace("\r", " ").replace("\n", " ")
            vals.append(v)
        # validação simples: id não vazio
        if not vals[0]:
            messagebox.showwarning("Validation", "id não pode ficar vazio.")
            return
        self.values = vals
        self.destroy()

if __name__ == "__main__":
    app = SupplierGUI()
    app.mainloop()

