import asyncio
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import get_db_conn
from dotenv import load_dotenv
load_dotenv()

GRUPOS = {
    "eletronicos": os.getenv("GRUPO_ELETRONICOS"),
    "academia": os.getenv("GRUPO_ACADEMIA"),
    "cosmeticos": os.getenv("GRUPO_COSMETICOS"),
    "sexshop": os.getenv("GRUPO_SEXSHOP"),
    "moda_praia": os.getenv("GRUPO_MODA")
}

async def postar_round(app):
    # envia uma rodada de posts (5 por categoria)
    conn = get_db_conn()
    cur = conn.cursor()
    for categoria, grupo in GRUPOS.items():
        cur.execute("SELECT titulo, preco, imagem, link FROM produtos WHERE categoria=%s ORDER BY RANDOM() LIMIT 5", (categoria,))
        items = cur.fetchall()
        for titulo, preco, imagem, link in items:
            msg = f"🔥 *{titulo}*\n💰 R$ {preco:.2f}\n📦 {categoria.capitalize()}"
            try:
                await app.bot.send_photo(
                    chat_id=grupo,
                    photo=imagem,
                    caption=msg,
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔗 Ver oferta', url=link)]])
                )
            except Exception as e:
                print('Erro ao enviar:', e)
            await asyncio.sleep(2)
    cur.close()
    conn.close()

def start_scheduler(app, interval_minutes=60):
    # cria tarefa que roda a cada interval_minutes
    async def loop():
        while True:
            print('Iniciando ciclo de postagem automática...')
            try:
                await postar_round(app)
            except Exception as e:
                print('Erro no ciclo automatico:', e)
            await asyncio.sleep(interval_minutes * 60)
    asyncio.create_task(loop())
