from db import init_db
from models import (
    add_seller,
    list_sellers,
    add_product,
    list_products,
    record_sale,
    get_sales_by_seller,
    update_product_quantity,
    get_full_report,
    export_sales_csv,
    export_full_report_csv,
)
import sqlite3
import subprocess
import sys


def safe_add_seller(name):
    try:
        add_seller(name)
        print(f"Vendedor '{name}' adicionado")
    except sqlite3.IntegrityError:
        print(f"Vendedor '{name}' já existe (ignorado)")


def safe_add_product(name, category, unit, cost, sell, qty):
    try:
        add_product(name, category, unit, cost, sell, qty)
        print(f"Produto '{name}' adicionado")
    except sqlite3.IntegrityError:
        print(f"Produto '{name}' já existe (ignorado)")
    except sqlite3.OperationalError as e:
        print(f"Erro de banco ao adicionar produto '{name}': {e}")


def main():
    init_db()
    print("Banco inicializado")

    # Adicionar vendedor e produto (exemplo)
    safe_add_seller("Maria")
    safe_add_product("Maca", "Frutas", "kg", 2.0, 4.5, 10)

    print("\nVendedores cadastrados:")
    sellers = list_sellers()
    for s in sellers:
        print(s)

    print("\nProdutos cadastrados:")
    products = list_products()
    for p in products:
        print(p)

    # demonstrar entrada de estoque
    if products:
        pid = products[0][0]
        print(f"\nAdicionando 5 unidades ao produto id={pid}")
        update_product_quantity(pid, 5)
        print("Estoque ajustado com entrada.")

    if not sellers or not products:
        print("Necessário ao menos 1 vendedor e 1 produto para registrar venda")
        return

    seller_id = sellers[0][0]
    product_id = products[0][0]

    print(f"\nRegistrando venda: vendedor_id={seller_id}, produto_id={product_id}, qtde=3")
    # executar registro de venda em subprocesso para evitar bloqueio do DB no processo atual
    try:
        cmd = [sys.executable, "-c", f"from models import record_sale; print(record_sale({seller_id}, [({product_id}, 3)]))"]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        out = res.stdout.strip()
        if out:
            print(f"Venda registrada com id: {out}")
        else:
            print("Falha ao registrar venda (verifique estoque/erros).")
        if res.stderr:
            print("Stderr:", res.stderr)
    except subprocess.TimeoutExpired:
        print("Tempo esgotado ao registrar venda (subprocesso travou).")
    except Exception as e:
        print(f"Erro ao registrar venda via subprocesso: {e}")

    print(f"\nVendas do vendedor {seller_id}:")
    sales = get_sales_by_seller(seller_id)
    for s in sales:
        print(s)

    print("\nProdutos após venda:")
    for p in list_products():
        print(p)

    # relatório completo e exports
    print("\nRelatório completo (entradas e vendas):")
    for row in get_full_report():
        print(row)
    export_sales_csv("sales.csv")
    export_full_report_csv("full_report.csv")
    print("Arquivos sales.csv e full_report.csv gerados.")


if __name__ == '__main__':
    main()
