import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

class StockGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Stock")
        self.root.configure(bg='yellow')
        self.files = "stock.csv"
        
        # Criar ficheiro se não existir
        if not os.path.exists(self.files):
            with open(self.files, "w") as f:
                f.write("")
        
        self.setup_gui()
    
    def setup_gui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar expansão
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="SISTEMA DE GESTÃO DE STOCK", 
                               font=('Arial', 16, 'bold'), background='yellow')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Botões do menu
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=1, column=0, sticky=(tk.W, tk.N), padx=(0, 10))
        
        self.add_btn = ttk.Button(buttons_frame, text="0 - Adicionar Item", 
                                 command=self.adds, width=20)
        self.add_btn.grid(row=0, column=0, pady=5)
        
        self.list_btn = ttk.Button(buttons_frame, text="1 - Listar Stock", 
                                  command=self.lists, width=20)
        self.list_btn.grid(row=1, column=0, pady=5)
        
        self.report_btn = ttk.Button(buttons_frame, text="2 - Procurar", 
                                    command=self.reports, width=20)
        self.report_btn.grid(row=2, column=0, pady=5)
        
        self.exit_btn = ttk.Button(buttons_frame, text="3 - Sair", 
                                  command=self.root.quit, width=20)
        self.exit_btn.grid(row=3, column=0, pady=5)
        
        # Área de texto para exibir dados
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.text_area = tk.Text(text_frame, width=60, height=20, wrap=tk.WORD,bg='yellow')
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def adds(self):
        """Adicionar novo item ao stock"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Adicionar Item")
        add_window.transient(self.root)
        add_window.grab_set()
        
        # Frame para os campos
        form_frame = ttk.Frame(add_window, padding="10")
        form_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Campos de entrada
        ttk.Label(form_frame, text="ID do Número de Entrada:").grid(row=0, column=0, sticky=tk.W, pady=5)
        id_entry = ttk.Entry(form_frame, width=30)
        id_entry.grid(row=0, column=1, pady=5, padx=(5, 0))
        
        ttk.Label(form_frame, text="ID do Produto:").grid(row=1, column=0, sticky=tk.W, pady=5)
        product_entry = ttk.Entry(form_frame, width=30)
        product_entry.grid(row=1, column=1, pady=5, padx=(5, 0))
        
        ttk.Label(form_frame, text="Unidades:").grid(row=2, column=0, sticky=tk.W, pady=5)
        units_entry = ttk.Entry(form_frame, width=30)
        units_entry.grid(row=2, column=1, pady=5, padx=(5, 0))
        
        def save_entry():
            id_val = id_entry.get().replace(",", ";").strip()
            product_val = product_entry.get().replace(",", ";").strip()
            units_val = units_entry.get().replace(",", ";").strip()
            
            if not all([id_val, product_val, units_val]):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
            
            # Escrever no ficheiro CSV
            line = f"{id_val},{product_val},{units_val}\n"
            try:
                with open(self.files, "a") as f:
                    f.write(line)
                self.status_var.set("Item adicionado com sucesso!")
                add_window.destroy()
                self.lists()  # Atualizar a lista
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao guardar: {str(e)}")
        
        # Botões
        button_frame = ttk.Frame(add_window, padding="10")
        button_frame.grid(row=1, column=0, sticky=(tk.E, tk.W))
        
        ttk.Button(button_frame, text="Guardar", command=save_entry).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="Cancelar", command=add_window.destroy).grid(row=0, column=1)
        
        # Focar no primeiro campo
        id_entry.focus()
    
    def lists(self):
        """Listar todo o stock"""
        try:
            with open(self.files, "r") as f:
                content = f.read()
            
            self.text_area.delete(1.0, tk.END)
            if content.strip():
                self.text_area.insert(1.0, content)
            else:
                self.text_area.insert(1.0, "Nenhum item em stock.")
            
            self.status_var.set("Stock listado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler ficheiro: {str(e)}")
    
    def reports(self):
        """Procurar itens no stock"""
        search_term = simpledialog.askstring("Procurar", "Encontrar o quê?")
        
        if search_term is None:  # Usuário cancelou
            return
        
        if not search_term.strip():
            messagebox.showwarning("Aviso", "Por favor, insira um termo de pesquisa.")
            return
        
        try:
            with open(self.files, "r") as f:
                lines = f.readlines()
            
            self.text_area.delete(1.0, tk.END)
            
            found_items = []
            for line in lines:
                if search_term.lower() in line.lower():
                    found_items.append(line.strip())
            
            if found_items:
                result = "\n".join(found_items)
                self.text_area.insert(1.0, result)
                self.status_var.set(f"Encontrados {len(found_items)} itens com '{search_term}'")
            else:
                self.text_area.insert(1.0, f"Nenhum item encontrado com '{search_term}'")
                self.status_var.set(f"Nenhum resultado para '{search_term}'")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na pesquisa: {str(e)}")

def main():
    root = tk.Tk()
    root.configure(bg='yellow')
    app = StockGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
