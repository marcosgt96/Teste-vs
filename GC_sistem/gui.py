import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
from models import (
    add_product,
    list_products,
    update_product_quantity,
    add_seller,
    list_sellers,
    record_sale,
    get_full_report,
    export_sales_csv,
    export_full_report_csv,
)


class ProductTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # título
        title = tk.Label(self, text="📦 Produtos", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # treeview products
        cols = ("id", "name", "cat", "unit", "cost", "sell", "qty")
        self.tree = ttk.Treeview(self, columns=cols, show='headings', height=8)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=80)
        self.tree.pack(fill='both', expand=True, padx=5, pady=5)

        frm = ttk.Frame(self)
        frm.pack(fill='x', pady=10, padx=5)
        
        # linha 1: nome, categoria
        row1 = ttk.Frame(frm)
        row1.pack(fill='x', pady=5)
        ttk.Label(row1, text="Nome:", font=("Arial", 10)).pack(side='left')
        self.name_var = tk.StringVar()
        ttk.Entry(row1, textvariable=self.name_var, width=15).pack(side='left', padx=5)
        ttk.Label(row1, text="Categoria:", font=("Arial", 10)).pack(side='left')
        self.cat_var = tk.StringVar()
        ttk.Entry(row1, textvariable=self.cat_var, width=15).pack(side='left', padx=5)
        
        # linha 2: unidade, custo
        row2 = ttk.Frame(frm)
        row2.pack(fill='x', pady=5)
        ttk.Label(row2, text="Unidade:", font=("Arial", 10)).pack(side='left')
        self.unit_var = tk.StringVar()
        ttk.Entry(row2, textvariable=self.unit_var, width=15).pack(side='left', padx=5)
        ttk.Label(row2, text="Custo:", font=("Arial", 10)).pack(side='left')
        self.cost_var = tk.StringVar()
        ttk.Entry(row2, textvariable=self.cost_var, width=15).pack(side='left', padx=5)
        
        # linha 3: venda, quantidade
        row3 = ttk.Frame(frm)
        row3.pack(fill='x', pady=5)
        ttk.Label(row3, text="Venda:", font=("Arial", 10)).pack(side='left')
        self.sell_var = tk.StringVar()
        ttk.Entry(row3, textvariable=self.sell_var, width=15).pack(side='left', padx=5)
        ttk.Label(row3, text="Qtde:", font=("Arial", 10)).pack(side='left')
        self.qty_var = tk.StringVar()
        ttk.Entry(row3, textvariable=self.qty_var, width=15).pack(side='left', padx=5)
        
        # botões
        btn_frm = ttk.Frame(frm)
        btn_frm.pack(fill='x', pady=10)
        ttk.Button(btn_frm, text="➕ Adicionar Produto", command=self.add_product).pack(side='left', padx=5)
        ttk.Button(btn_frm, text="📝 Atualizar Estoque", command=self.update_stock).pack(side='left', padx=5)
        ttk.Button(btn_frm, text="🔄 Recarregar", command=self.load_products).pack(side='left', padx=5)
        self.load_products()

    def load_products(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for p in list_products():
            self.tree.insert('', 'end', values=p)

    def add_product(self):
        try:
            add_product(
                self.name_var.get(),
                self.cat_var.get(),
                self.unit_var.get(),
                float(self.cost_var.get() or 0),
                float(self.sell_var.get() or 0),
                int(self.qty_var.get() or 0),
            )
            messagebox.showinfo("✅ Sucesso", "Produto adicionado!")
            self.name_var.set("")
            self.cat_var.set("")
            self.unit_var.set("")
            self.cost_var.set("")
            self.sell_var.set("")
            self.qty_var.set("")
            self.load_products()
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Falha: {str(e)}")

    def update_stock(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um produto na lista")
            return
        prod_id = self.tree.item(sel)['values'][0]
        delta = simpledialog.askinteger("Estoque", "Quantidade (+/-):", parent=self)
        if delta is None:
            return
        ok = update_product_quantity(prod_id, delta)
        if ok:
            messagebox.showinfo("✅ Sucesso", "Estoque atualizado!")
            self.load_products()
        else:
            messagebox.showerror("❌ Erro", "Estoque insuficiente para redução")


class SellerTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # título
        title = tk.Label(self, text="👤 Vendedores", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        self.tree = ttk.Treeview(self, columns=("id","name"), show='headings', height=10)
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Nome')
        self.tree.column('id', width=50)
        self.tree.column('name', width=250)
        self.tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        frm = ttk.Frame(self)
        frm.pack(fill='x', pady=10, padx=5)
        ttk.Label(frm, text="Nome:", font=("Arial", 10)).pack(side='left')
        self.name_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.name_var, width=30).pack(side='left', padx=5)
        ttk.Button(frm, text="➕ Adicionar", command=self.add_seller).pack(side='left', padx=5)
        ttk.Button(frm, text="🔄 Recarregar", command=self.load_sellers).pack(side='left', padx=5)
        self.load_sellers()

    def load_sellers(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for s in list_sellers():
            self.tree.insert('', 'end', values=s)

    def add_seller(self):
        try:
            add_seller(self.name_var.get())
            messagebox.showinfo("✅ Sucesso", "Vendedor adicionado!")
            self.name_var.set("")
            self.load_sellers()
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Falha: {str(e)}")


class SaleTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # título
        title = tk.Label(self, text="💰 Registrar Venda", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # seleção de vendedor
        sel_frm = ttk.Frame(self)
        sel_frm.pack(fill='x', padx=5, pady=5)
        ttk.Label(sel_frm, text="Vendedor:", font=("Arial", 10, "bold")).pack(side='left')
        self.seller_cb = ttk.Combobox(sel_frm, state='readonly', width=40)
        self.seller_cb.pack(side='left', padx=5)
        
        # produtos disponíveis
        ttk.Label(self, text="Produtos Disponíveis", font=("Arial", 11, "bold")).pack(pady=(10,5))
        self.prod_tree = ttk.Treeview(self, columns=("id","name","qty"), show='headings', height=6)
        for c in ("id","name","qty"):
            self.prod_tree.heading(c, text=c)
        self.prod_tree.column('id', width=50)
        self.prod_tree.column('name', width=150)
        self.prod_tree.column('qty', width=80)
        self.prod_tree.pack(fill='both', padx=5, pady=5)
        
        # adicionar itens à venda
        add_frm = ttk.Frame(self)
        add_frm.pack(fill='x', padx=5, pady=5)
        ttk.Label(add_frm, text="Produto ID:", font=("Arial", 9)).pack(side='left')
        self.prod_id = tk.StringVar()
        ttk.Entry(add_frm, textvariable=self.prod_id, width=10).pack(side='left', padx=3)
        ttk.Label(add_frm, text="Qtd:", font=("Arial", 9)).pack(side='left')
        self.qty = tk.StringVar()
        ttk.Entry(add_frm, textvariable=self.qty, width=10).pack(side='left', padx=3)
        ttk.Button(add_frm, text="➕ Adicionar Item", command=self.add_item).pack(side='left', padx=5)
        
        # itens selecionados
        ttk.Label(self, text="Itens da Venda", font=("Arial", 11, "bold")).pack(pady=(10,5))
        self.items = []
        self.items_tree = ttk.Treeview(self, columns=("pid","qty"), show='headings', height=5)
        self.items_tree.heading('pid',text='Produto ID')
        self.items_tree.heading('qty',text='Quantidade')
        self.items_tree.column('pid', width=100)
        self.items_tree.column('qty', width=100)
        self.items_tree.pack(fill='both', padx=5, pady=5)
        
        # botão finalizar venda
        ttk.Button(self, text="✅ Registrar Venda", command=self.finish_sale).pack(pady=10)
        self.load_sellers_and_products()

    def load_sellers_and_products(self):
        self.seller_cb['values'] = [f"{s[0]}: {s[1]}" for s in list_sellers()]
        for r in self.prod_tree.get_children():
            self.prod_tree.delete(r)
        for p in list_products():
            self.prod_tree.insert('', 'end', values=(p[0], p[1], p[6]))

    def add_item(self):
        try:
            pid = int(self.prod_id.get())
            qty = int(self.qty.get())
        except ValueError:
            messagebox.showerror("❌ Erro","Informe números válidos")
            return
        self.items.append((pid, qty))
        self.items_tree.insert('', 'end', values=(pid, qty))
        self.prod_id.set("")
        self.qty.set("")

    def finish_sale(self):
        if not self.items:
            messagebox.showwarning("⚠️ Aviso","Nenhum item adicionado")
            return
        sel = self.seller_cb.get()
        if not sel:
            messagebox.showwarning("⚠️ Aviso","Selecione vendedor")
            return
        seller_id = int(sel.split(':')[0])
        res = record_sale(seller_id, self.items)
        if res:
            messagebox.showinfo("✅ Venda Registrada", f"ID: {res}")
            self.items = []
            for r in self.items_tree.get_children():
                self.items_tree.delete(r)
            self.load_sellers_and_products()
        else:
            messagebox.showerror("❌ Erro","Estoque insuficiente")


class ReportTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # título
        title = tk.Label(self, text="📊 Relatórios", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # info text
        info = tk.Label(self, text="Relatório completo: Entradas de estoque + Vendas (cronológico)", 
                       font=("Arial", 9, "italic"))
        info.pack()
        
        # texto com scroll
        self.txt = scrolledtext.ScrolledText(self, wrap='word', font=("Courier", 9), height=15)
        self.txt.pack(fill='both', expand=True, padx=5, pady=5)
        
        # botões
        btn_frm = ttk.Frame(self)
        btn_frm.pack(fill='x', padx=5, pady=10)
        ttk.Button(btn_frm, text="🔄 Atualizar", command=self.load_report).pack(side='left', padx=5)
        ttk.Button(btn_frm, text="💾 Exportar Vendas (CSV)", command=self.export_sales).pack(side='left', padx=5)
        ttk.Button(btn_frm, text="💾 Exportar Relatório Completo", command=self.export_full).pack(side='left', padx=5)
        self.load_report()

    def load_report(self):
        self.txt.delete('1.0','end')
        for row in get_full_report():
            self.txt.insert('end', str(row)+"\n")

    def export_sales(self):
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV", "*.csv")])
        if not path:
            return
        try:
            export_sales_csv(path)
            messagebox.showinfo("✅ Sucesso",f"Vendas exportadas!")
        except Exception as e:
            messagebox.showerror("❌ Erro", str(e))

    def export_full(self):
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV", "*.csv")])
        if not path:
            return
        try:
            export_full_report_csv(path)
            messagebox.showinfo("✅ Sucesso",f"Relatório exportado!")
        except Exception as e:
            messagebox.showerror("❌ Erro", str(e))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🛒 Sistema de Vendas - Frutas e Legumes")
        self.geometry("1200x700")
        
        # criar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # cores
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0')
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', padding=[20,10])
        style.map('TNotebook.Tab', background=[('selected', '#ffffff'), ('active', '#e0e0e0')])
        
        # header
        header = tk.Frame(self, bg='#2c3e50', height=60)
        header.pack(fill='x')
        ttk.Label(header, text="🛒 Sistema de Vendas - Frutas e Legumes 🥕🍎", 
                 font=("Arial", 16, "bold")).pack(pady=10)
        
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        notebook.add(ProductTab(notebook), text="📦 Produtos")
        notebook.add(SellerTab(notebook), text="👤 Vendedores")
        notebook.add(SaleTab(notebook), text="💰 Vendas")
        notebook.add(ReportTab(notebook), text="📊 Relatórios")


def main():
    import db
    db.init_db()
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
