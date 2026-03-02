Sistema simples de vendas de frutas e legumes

Descrição
- CLI em Python para gerenciar produtos, estoque, vendedores e vendas.

Como usar
1. Crie um ambiente virtual (opcional):

```bash
python -m venv .venv
.venv\\Scripts\\activate
```

2. Instale dependências (não há dependências externas por enquanto):

```bash
pip install -r requirements.txt
```

3. Inicialize o banco de dados e rode o programa:

```bash
python main.py
```

Estrutura
- `main.py` - ponto de entrada para CLI
- `gui.py` - interface gráfica usando Tkinter (execute com `python gui.py`)
- `db.py` - inicialização do SQLite e helper de conexão
- `models.py` - operações de CRUD e lógica de vendas/estoque (inclui relatórios e exportação CSV)
- `cli.py` - interface de linha de comando

Relatórios e exportação
- `get_full_report()` retorna entradas de estoque e vendas ordenados por data.
- `export_sales_csv(path)` gera CSV das vendas.
- `export_full_report_csv(path)` gera CSV do relatório completo (entradas + vendas).


Nota
- Projeto simples para aprendizado; sinta-se à vontade para pedir melhorias (relatórios, GUI, exportar CSV, autenticação, etc.).

Testes
- Há um conjunto básico de testes em `tests/test_models.py`. Rode com:

```bash
pytest
```
