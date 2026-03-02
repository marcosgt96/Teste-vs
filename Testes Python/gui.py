import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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
        # treeview products
        cols = ("id", "name", "cat", "unit", "cost", "sell", "qty")
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        for c in cols:
            self.tree.heading(c, text=c)
        self.tree.pack(fill='both', expand=True)

        frm = ttk.Frame(self)
        frm.pack(fill='x', pady=5)
        ttk.Label(frm, text="Nome").grid(row=0, column=0)
        self.name_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.name_var).grid(row=0, column=1)
        ttk.Label(frm, text="Categoria").grid(row=0, column=2)
        self.cat_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.cat_var).grid(row=0, column=3)
        ttk.Label(frm, text="Unidade").grid(row=1, column=0)
        self.unit_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.unit_var).grid(row=1, column=1)
        ttk.Label(frm, text="Custo").grid(row=1, column=2)
        self.cost_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.cost_var).grid(row=1, column=3)
        ttk.Label(frm, text="Venda").grid(row=2, column=0)
        self.sell_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.sell_var).grid(row=2, column=1)
        ttk.Label(frm, text="Qtde").grid(row=2, column=2)
        self.qty_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.qty_var).grid(row=2, column=3)
        ttk.Button(frm, text="Adicionar", command=self.add_product).grid(row=3, column=0, columnspan=2)
        ttk.Button(frm, text="Atualizar estoque", command=self.update_stock).grid(row=3, column=2, columnspan=2)
        ttk.Button(frm, text="Recarregar", command=self.load_products).grid(row=4, column=0, columnspan=4)
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
            messagebox.showinfo("Ok", "Produto adicionado")
            self.load_products()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def update_stock(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um produto na lista")
            return
        prod_id = self.tree.item(sel)['values'][0]
        delta = tk.simpledialog.askinteger("Quantidade", "Quantidade (+/-):")
        if delta is None:
            return
        ok = update_product_quantity(prod_id, delta)
        if ok:
            messagebox.showinfo("Ok", "Estoque atualizado")
            self.load_products()
        else:
            messagebox.showerror("Erro", "Falha ao atualizar estoque")


class SellerTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.tree = ttk.Treeview(self, columns=("id","name"), show='headings')
        self.tree.heading('id', text='id')
        self.tree.heading('name', text='name')
        self.tree.pack(fill='both', expand=True)
        frm = ttk.Frame(self)
        frm.pack(fill='x', pady=5)
        ttk.Label(frm, text="Nome").grid(row=0, column=0)
        self.name_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.name_var).grid(row=0, column=1)
        ttk.Button(frm, text="Adicionar", command=self.add_seller).grid(row=0, column=2)
        ttk.Button(frm, text="Recarregar", command=self.load_sellers).grid(row=1, column=0, columnspan=3)
        self.load_sellers()

    def load_sellers(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for s in list_sellers():
            self.tree.insert('', 'end', values=s)

    def add_seller(self):
        try:
            add_seller(self.name_var.get())
            messagebox.showinfo("Ok", "Vendedor adicionado")
            self.load_sellers()
        except Exception as e:
            messagebox.showerror("Erro", str(e))


class SaleTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.seller_cb = ttk.Combobox(self, state='readonly')
        self.seller_cb.pack(fill='x', padx=5, pady=5)
        self.prod_tree = ttk.Treeview(self, columns=("id","name","qty"), show='headings')
        for c in ("id","name","qty"):
            self.prod_tree.heading(c, text=c)
        self.prod_tree.pack(fill='both', expand=True)
        frm = ttk.Frame(self)
        frm.pack(fill='x', pady=5)
        ttk.Label(frm, text="Produto ID").grid(row=0,column=0)
        self.prod_id = tk.StringVar()
        ttk.Entry(frm, textvariable=self.prod_id).grid(row=0,column=1)
        ttk.Label(frm, text="Qtd").grid(row=0,column=2)
        self.qty = tk.StringVar()
        ttk.Entry(frm, textvariable=self.qty).grid(row=0,column=3)
        ttk.Button(frm, text="Adicionar item", command=self.add_item).grid(row=1,column=0,columnspan=4)
        self.items = []
        self.items_tree = ttk.Treeview(self, columns=("pid","qty"), show='headings')
        self.items_tree.heading('pid',text='produto')
        self.items_tree.heading('qty',text='qtd')
        self.items_tree.pack(fill='both', expand=True)
        ttk.Button(self, text="Registrar venda", command=self.finish_sale).pack(pady=5)
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
            messagebox.showerror("Erro","Informe números válidos")
            return
        self.items.append((pid, qty))
        self.items_tree.insert('', 'end', values=(pid, qty))

    def finish_sale(self):
        if not self.items:
            messagebox.showwarning("Aviso","Nenhum item adicionado")
            return
        sel = self.seller_cb.get()
        if not sel:
            messagebox.showwarning("Aviso","Selecione vendedor")
            return
        seller_id = int(sel.split(':')[0])
        res = record_sale(seller_id, self.items)
        if res:
            messagebox.showinfo("Sucesso", f"Venda registrada ID {res}")
            self.items = []
            for r in self.items_tree.get_children():
                self.items_tree.delete(r)
            self.load_sellers_and_products()
        else:
            messagebox.showerror("Erro","Falha no registro (estoque?)")


class ReportTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.txt = tk.Text(self, wrap='none')
        self.txt.pack(fill='both', expand=True)
        frm = ttk.Frame(self)
        frm.pack(fill='x')
        ttk.Button(frm, text="Atualizar", command=self.load_report).pack(side='left')
        ttk.Button(frm, text="Exportar vendas CSV", command=self.export_sales).pack(side='left')
        ttk.Button(frm, text="Exportar relatório completo", command=self.export_full).pack(side='left')
        self.load_report()

    def load_report(self):
        self.txt.delete('1.0','end')
        for row in get_full_report():
            self.txt.insert('end', str(row)+"\n")

    def export_sales(self):
        path = filedialog.asksaveasfilename(defaultextension='.csv')
        if not path:
            return
        try:
            export_sales_csv(path)
            messagebox.showinfo("Ok","Exportado")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def export_full(self):
        path = filedialog.asksaveasfilename(defaultextension='.csv')
        if not path:
            return
        try:
            export_full_report_csv(path)
            messagebox.showinfo("Ok","Exportado")
        except Exception as e:
            messagebox.showerror("Erro", str(e))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Vendas - GUI")
        self.geometry("800x600")
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)
        notebook.add(ProductTab(notebook), text="Produtos")
        notebook.add(SellerTab(notebook), text="Vendedores")
        notebook.add(SaleTab(notebook), text="Vendas")
        notebook.add(ReportTab(notebook), text="Relatórios")


def main():
    import db
    db.init_db()
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
