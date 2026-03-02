from db import get_connection


def add_product(name, category, unit, cost_price, selling_price, quantity):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (name, category, unit, cost_price, selling_price, quantity) VALUES (?, ?, ?, ?, ?, ?)",
        (name, category, unit, cost_price, selling_price, quantity),
    )
    conn.commit()
    conn.close()


def list_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, category, unit, cost_price, selling_price, quantity FROM products ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return rows


def update_product_quantity(product_id, delta):
    """Adjust stock by delta; record entry/exit and prevent negative quantity."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT quantity FROM products WHERE id = ?", (product_id,))
    r = cur.fetchone()
    if not r:
        conn.close()
        return False
    new_q = r[0] + delta
    if new_q < 0:
        conn.close()
        return False
    cur.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_q, product_id))
    # registrar movimento
    cur.execute("INSERT INTO stock_entries (product_id, delta) VALUES (?, ?)", (product_id, delta))
    conn.commit()
    conn.close()
    return True


def add_seller(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO sellers (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()


def list_sellers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM sellers ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return rows


def record_sale(seller_id, items):
    """items: list of (product_id, quantity)
    Returns sale_id on success or None if stock insufficient.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Check stock
    for product_id, qty in items:
        cur.execute("SELECT quantity, selling_price FROM products WHERE id = ?", (product_id,))
        r = cur.fetchone()
        if not r or r[0] < qty:
            conn.close()
            return None

    # Compute total and update stock
    total = 0
    cur.execute("INSERT INTO sales (seller_id, total) VALUES (?, ?)", (seller_id, 0.0))
    sale_id = cur.lastrowid
    for product_id, qty in items:
        cur.execute("SELECT quantity, selling_price FROM products WHERE id = ?", (product_id,))
        q, price = cur.fetchone()
        subtotal = qty * price
        total += subtotal
        cur.execute("INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES (?, ?, ?, ?, ?)",
                    (sale_id, product_id, qty, price, subtotal))
        cur.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (qty, product_id))

    cur.execute("UPDATE sales SET total = ? WHERE id = ?", (total, sale_id))
    conn.commit()
    conn.close()
    return sale_id


def get_sales_by_seller(seller_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, date, total FROM sales WHERE seller_id = ? ORDER BY date DESC", (seller_id,))
    sales = cur.fetchall()
    conn.close()
    return sales


def list_stock_entries(product_id=None):
    conn = get_connection()
    cur = conn.cursor()
    if product_id:
        cur.execute("SELECT id, product_id, delta, date FROM stock_entries WHERE product_id = ? ORDER BY date DESC", (product_id,))
    else:
        cur.execute("SELECT id, product_id, delta, date FROM stock_entries ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_full_report():
    """Return combined list of stock entries and sales items ordered by date."""
    conn = get_connection()
    cur = conn.cursor()
    query = """
    SELECT 'entry' as type, e.date, p.name AS product, e.delta, NULL AS seller, NULL AS sale_total
      FROM stock_entries e
      JOIN products p ON e.product_id = p.id
    UNION
    SELECT 'sale' as type, s.date, p.name AS product, si.quantity, sel.name as seller, s.total as sale_total
      FROM sales s
      JOIN sale_items si ON si.sale_id = s.id
      JOIN products p ON si.product_id = p.id
      JOIN sellers sel ON s.seller_id = sel.id
    ORDER BY date
    """
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows


def export_sales_csv(path):
    import csv
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT s.id, s.date, sel.name as seller, p.name as product, si.quantity, si.unit_price, si.subtotal
        FROM sales s
          JOIN sellers sel ON s.seller_id = sel.id
          JOIN sale_items si ON si.sale_id = s.id
          JOIN products p ON si.product_id = p.id
        ORDER BY s.date
        """
    )
    rows = cur.fetchall()
    conn.close()
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['sale_id', 'date', 'seller', 'product', 'quantity', 'unit_price', 'subtotal'])
        writer.writerows(rows)


def export_full_report_csv(path):
    import csv
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT 'entry' as type, e.date, p.name, e.delta, NULL, NULL
          FROM stock_entries e JOIN products p ON e.product_id = p.id
        UNION
        SELECT 'sale' as type, s.date, p.name, si.quantity, sel.name, s.total
          FROM sales s
            JOIN sale_items si ON si.sale_id = s.id
            JOIN products p ON si.product_id = p.id
            JOIN sellers sel ON s.seller_id = sel.id
        ORDER BY date
        """
    )
    rows = cur.fetchall()
    conn.close()
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['type', 'date', 'product', 'quantity_or_delta', 'seller', 'sale_total'])
        writer.writerows(rows)
