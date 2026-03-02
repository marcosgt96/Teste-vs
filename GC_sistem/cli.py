import sqlite3
from models import (
    add_product,
    list_products,
    update_product_quantity,
    add_seller,
    list_sellers,
    record_sale,
    get_sales_by_seller,
)


def _input_int(prompt, allow_empty=False, default=None):
    while True:
        v = input(prompt).strip()
        if v == "" and allow_empty:
            return default
        try:
            return int(v)
        except ValueError:
            print("Entrada inválida: digite um número inteiro.")


def _input_float(prompt, allow_empty=False, default=None):
    while True:
        v = input(prompt).strip()
        if v == "" and allow_empty:
            return default
        try:
            return float(v)
        except ValueError:
            print("Entrada inválida: digite um número (ex: 12.50).")


def _input_str(prompt, allow_empty=False, default=None):
    while True:
        v = input(prompt).strip()
        if v == "" and allow_empty:
            return default
        if v == "":
            print("Entrada vazia — por favor digite um valor.")
            continue
        return v


def menu():
    while True:
        print("\n=== Sistema de Vendas ===")
        print("1. Produtos")
        print("2. Vendedores")
        print("3. Vendas")
        print("4. Relatórios")
        print("0. Sair")
        opt = input("Escolha: ").strip()
        if opt == "1":
            produtos_menu()
        elif opt == "2":
            vendedores_menu()
        elif opt == "3":
            vendas_menu()
        elif opt == "4":
            relatorios_menu()
        elif opt == "0":
            break
        else:
            print("Opção inválida. Digite 0-4.")


def produtos_menu():
    while True:
        print("\n-- Produtos --")
        print("1. Adicionar produto")
        print("2. Listar produtos")
        print("3. Atualizar estoque")
        print("0. Voltar")
        o = input("Escolha: ").strip()
        if o == "1":
            name = _input_str("Nome: ")
            cat = _input_str("Categoria: ", allow_empty=True, default="")
            unit = _input_str("Unidade (ex: kg, un): ", allow_empty=True, default="un")
            cost = _input_float("Preço de custo: ", allow_empty=True, default=0.0)
            sell = _input_float("Preço de venda: ", allow_empty=True, default=0.0)
            qty = _input_int("Quantidade inicial: ", allow_empty=True, default=0)
            try:
                add_product(name, cat, unit, cost, sell, qty)
                print("Produto adicionado.")
            except sqlite3.IntegrityError:
                print("Já existe um produto com esse nome.")
        elif o == "2":
            rows = list_products()
            if not rows:
                print("Nenhum produto cadastrado.")
                continue
            print("ID | Nome | Categoria | Unidade | Custo | Venda | Qtde")
            for r in rows:
                print(" | ".join(map(str, r)))
        elif o == "3":
            rows = list_products()
            if not rows:
                print("Nenhum produto cadastrado.")
                continue
            for r in rows:
                print("ID:", r[0], "-", r[1], "(qtde:", r[6], ")")
            pid = _input_int("ID do produto: ")
            delta = _input_int("Quantidade (+ entrada, - saída): ")
            ok = update_product_quantity(pid, delta)
            print("Atualizado." if ok else "Falha: cheque ID/estoque.")
        elif o == "0":
            break
        else:
            print("Opção inválida.")


def vendedores_menu():
    while True:
        print("\n-- Vendedores --")
        print("1. Adicionar vendedor")
        print("2. Listar vendedores")
        print("0. Voltar")
        o = input("Escolha: ").strip()
        if o == "1":
            name = _input_str("Nome: ")
            try:
                add_seller(name)
                print("Vendedor adicionado.")
            except sqlite3.IntegrityError:
                print("Já existe um vendedor com esse nome.")
        elif o == "2":
            rows = list_sellers()
            if not rows:
                print("Nenhum vendedor cadastrado.")
            for r in rows:
                print(r)
        elif o == "0":
            break
        else:
            print("Opção inválida.")


def vendas_menu():
    print("\n-- Registrar Venda --")
    sellers = list_sellers()
    if not sellers:
        print("Nenhum vendedor cadastrado.")
        return
    print("Vendedores:")
    for s in sellers:
        print(s)
    sid = _input_int("ID do vendedor: ")
    # validar vendedor
    if not any(s[0] == sid for s in sellers):
        print("Vendedor não encontrado.")
        return
    items = []
    prods = list_products()
    if not prods:
        print("Nenhum produto cadastrado.")
        return
    print("Produtos disponíveis:")
    for p in prods:
        print(p)
    while True:
        pid_raw = input("ID do produto (enter para terminar): ").strip()
        if pid_raw == "":
            break
        try:
            pid = int(pid_raw)
        except ValueError:
            print("ID inválido.")
            continue
        if not any(p[0] == pid for p in prods):
            print("Produto não encontrado.")
            continue
        qty = _input_int("Quantidade: ")
        items.append((pid, qty))
    if not items:
        print("Nenhum item informado.")
        return
    sale_id = record_sale(sid, items)
    if sale_id:
        print(f"Venda registrada. ID: {sale_id}")
    else:
        print("Falha: estoque insuficiente ou dados inválidos.")


def relatorios_menu():
    while True:
        print("\n-- Relatórios --")
        print("1. Vendas por vendedor")
        print("0. Voltar")
        o = input("Escolha: ").strip()
        if o == "1":
            sellers = list_sellers()
            if not sellers:
                print("Nenhum vendedor cadastrado.")
                continue
            for s in sellers:
                print(s)
            sid = _input_int("ID do vendedor: ")
            if not any(s[0] == sid for s in sellers):
                print("Vendedor não encontrado.")
                continue
            sales = get_sales_by_seller(sid)
            if not sales:
                print("Nenhuma venda para esse vendedor.")
            for s in sales:
                print(s)
        elif o == "0":
            break
        else:
            print("Opção inválida.")
