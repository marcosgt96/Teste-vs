import os
import sqlite3
import pytest
from db import DB_PATH, init_db
from models import (
    add_product,
    list_products,
    update_product_quantity,
    add_seller,
    list_sellers,
    record_sale,
    get_full_report,
)


def setup_function(fn):
    # delete db before each test
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()


def test_product_lifecycle():
    add_product('Banana', 'Frutas', 'kg', 1.0, 2.0, 5)
    prods = list_products()
    assert len(prods) == 1
    pid = prods[0][0]
    assert update_product_quantity(pid, 3)
    assert list_products()[0][6] == 8
    assert not update_product_quantity(pid, -100)


def test_seller_and_sale():
    add_seller('Joao')
    sellers = list_sellers()
    assert sellers and sellers[0][1] == 'Joao'
    pid = add_product('Laranja', 'Frutas', 'kg', 1, 2, 10) or list_products()[0][0]
    sid = sellers[0][0]
    sale_id = record_sale(sid, [(1, 2)])
    assert sale_id is not None
    rpt = get_full_report()
    assert any(r[0] == 'sale' for r in rpt)
