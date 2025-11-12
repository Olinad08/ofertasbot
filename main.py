import os
import asyncio
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from database import init_db, get_db_conn
from meli_api import coletar_produtos
from scheduler import start_scheduler

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# grupos por categoria (variáveis de ambiente)
GRUPOS = {
    "eletronicos": os.getenv("GRUPO_ELETRONICOS"),
    "academia": os.getenv("GRUPO_ACADEMIA"),
    "cosmeticos": os.getenv("GRUPO_COSMETICOS"),
    "sexshop": os.getenv("GRUPO_SEXSHOP"),
    "moda_praia": os.getenv("GRUPO_MODA")
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔄 Coletar Produtos (ML)", callback_data="coletar")],
        [InlineKeyboardButton("📤 Enviar Agora (manual)", callback_data="enviar")],
        [InlineKeyboardButton("📊 Ver Status", callback_data="status")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Escolha uma ação 👇", reply_markup=reply_markup)

async def botao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "coletar":
        await query.edit_message_text("⏳ Coletando produtos do Mercado Livre...")
        n = coletar_produtos(limit=10)
        await query.edit_message_text(f"✅ {n} produtos coletados e salvos no banco.")

    elif data == "enviar":
        await query.edit_message_text("⏳ Enviando ofertas para os grupos...")
        # chama a tarefa de postar uma vez
        await send_once(context)

        await query.edit_message_text("✅ Envio manual concluído.")

    elif data == "status":
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("SELECT categoria, COUNT(*) FROM produtos GROUP BY categoria")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        if rows:
            texto = "📊 Produtos por categoria:\n"
            for cat, cnt in rows:
                texto += f"• {cat}: {cnt}\n"
        else:
            texto = "Nenhum produto encontrado no banco."
        await query.edit_message_text(texto)

async def send_once(context):
    # envia uma rodada imediata por categoria
    conn = get_db_conn()
    cur = conn.cursor()
    for categoria, grupo in GRUPOS.items():
        cur.execute("SELECT titulo, preco, imagem, link FROM produtos WHERE categoria=%s ORDER BY RANDOM() LIMIT 5", (categoria,))
        items = cur.fetchall()
        for titulo, preco, imagem, link in items:
            msg = f"🔥 *{titulo}*\n💰 R$ {preco:.2f}\n📦 {categoria.capitalize()}"
            try:
                await context.bot.send_photo(
                    chat_id=grupo,
                    photo=imagem,
                    caption=msg,
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔗 Ver oferta', url=link)]])
                )
            except Exception as e:
                print('Erro enviando mensagem:', e)
            await asyncio.sleep(2)
    cur.close()
    conn.close()

async def main():
    # inicializa DB (cria tabela se não existir)
    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(botao))

    # start scheduler background
    start_scheduler(app)

    print('🤖 Bot rodando (ofertasbot) — aguardando eventos...')
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
