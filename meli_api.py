import requests
from database import get_db_conn
from psycopg2.extras import execute_values

# categorias - já definidas para o MVP
CATEGORIAS = {
    "eletronicos": "MLB1000",
    "academia": "MLB1276",
    "cosmeticos": "MLB1227",
    "sexshop": "MLB29285",
    "moda_praia": "MLB1430"
}

def salvar_produtos(produtos):
    conn = get_db_conn()
    cur = conn.cursor()
    query = """
        INSERT INTO produtos (ml_id, titulo, preco, imagem, link, categoria)
        VALUES %s
        ON CONFLICT (ml_id) DO NOTHING;
    """
    values = [(p['id'], p['title'], p['price'], p['thumbnail'], p['permalink'], p['categoria']) for p in produtos]
    execute_values(cur, query, values)
    conn.commit()
    cur.close()
    conn.close()

def coletar_produtos(limit=10):
    todos = []
    for nome, cat_id in CATEGORIAS.items():
        url = f"https://api.mercadolibre.com/sites/MLB/search?category={cat_id}&limit={limit}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        for item in data.get('results', []):
            todos.append({
                'id': item.get('id'),
                'title': item.get('title'),
                'price': item.get('price'),
                'thumbnail': item.get('thumbnail'),
                'permalink': item.get('permalink'),
                'categoria': nome
            })
    salvar_produtos(todos)
    return len(todos)
