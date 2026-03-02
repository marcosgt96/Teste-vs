import sqlite3
import os
from contextlib import closing


DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")


def get_connection():
    # aumentar timeout para evitar erros "database is locked" em acessos concorrentes
    return sqlite3.connect(DB_PATH, timeout=10)


def init_db():
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            category TEXT,
            unit TEXT,
            cost_price REAL DEFAULT 0,
            selling_price REAL DEFAULT 0,
            quantity INTEGER DEFAULT 0
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS sellers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seller_id INTEGER,
            date TEXT DEFAULT (datetime('now')),
            total REAL,
            FOREIGN KEY(seller_id) REFERENCES sellers(id)
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            unit_price REAL,
            subtotal REAL,
            FOREIGN KEY(sale_id) REFERENCES sales(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
        """)

        # tabela para registrar entradas/saídas de estoque (além de vendas)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS stock_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            delta INTEGER,
            date TEXT DEFAULT (datetime('now')),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
        """)

        conn.commit()


if __name__ == "__main__":
    init_db()
    print(f"Banco inicializado em: {DB_PATH}")
