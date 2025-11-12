# ofertasbot

Bot Telegram que coleta produtos do Mercado Livre e publica automaticamente em grupos por categoria.

## Estrutura
- `main.py` - código principal (menu + agendamento)
- `database.py` - conexão com Postgres (suporta DATABASE_URL do Render)
- `meli_api.py` - integra com API do Mercado Livre
- `scheduler.py` - rotina de postagem automática (a cada 1h por padrão)
- `requirements.txt` - dependências
- `Procfile` - comando para Render
- `.env.example` - modelo de variáveis de ambiente
- `database.sql` - script SQL para criar tabela

## Configuração local (teste)
1. Crie e ative um virtualenv:
   ```bash
   python -m venv venv
   source venv/bin/activate  # mac/linux
   venv\Scripts\activate    # windows
   ```
2. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Copie `.env.example` para `.env` e preencha suas credenciais (BOT_TOKEN, DATABASE_URL ou DB_*)
4. Crie o banco (opcional) usando `database.sql` ou deixe que `init_db()` crie a tabela automaticamente.
5. Rode localmente:
   ```bash
   python main.py
   ```

## Deploy no Render (passo a passo)
1. Crie um novo repositório no GitHub e faça push do projeto.
2. No Render, crie um novo **Background Worker** apontando para seu repositório.
3. Build Command:
   ```
   pip install -r requirements.txt
   ```
4. Start Command:
   ```
   python main.py
   ```
5. Adicione as variáveis de ambiente (no painel do serviço) a partir do `.env.example`.
6. Se ainda não criou, crie um serviço **Postgres** no Render (Free tier) e copie o `DATABASE_URL` para as variáveis de ambiente.
7. Inicie o serviço. Verifique logs para confirmar que aparece:
   ```
   🤖 Bot rodando (ofertasbot) — aguardando eventos...
   ```

## Próximos passos sugeridos
- Adicionar links de afiliado (Admitad / Mercado Livre Affiliates) antes de publicar.
- Implementar controle de estoque / evitar repostagens usando timestamp.
- Adicionar painel web ou comandos adicionais no bot para gerenciar frequência e quantidade.
- Integrar Shopee quando sua afiliação estiver ativa.

## Observações legais
- Respeite os Termos de Uso do Mercado Livre (use API oficial quando possível).
- Peça consentimento para envio em listas privadas e siga as regras do Telegram.
