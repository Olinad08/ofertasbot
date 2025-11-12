-- SQL para criar a tabela produtos (use no psql ou pgAdmin se preferir)
CREATE TABLE IF NOT EXISTS produtos (
    id SERIAL PRIMARY KEY,
    ml_id VARCHAR(80) UNIQUE,
    titulo TEXT,
    preco NUMERIC,
    imagem TEXT,
    link TEXT,
    categoria TEXT,
    criado_em TIMESTAMP DEFAULT NOW()
);
