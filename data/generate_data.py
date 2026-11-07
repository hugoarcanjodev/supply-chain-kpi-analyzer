import os
import sqlite3
import random
from datetime import datetime, timedelta

def criar_banco_dados():
    # Garante que a pasta data exista
    os.makedirs('data', exist_ok=True)
    db_path = os.path.join('data', 'supply_chain_data.db')
    
    # Conecta ou cria o banco SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("--- Criando as tabelas no SQLite ---")
    
    # 1. Tabela de Fornecedores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tb_fornecedores (
            id_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_fornecedor TEXT NOT NULL,
            regiao TEXT NOT NULL
        )
    ''')
    
    # 2. Tabela de Estoque (SKUs)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tb_estoque (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT NOT NULL UNIQUE,
            categoria TEXT NOT NULL,
            estoque_atual INTEGER NOT NULL,
            estoque_seguranca INTEGER NOT NULL,
            custo_unitario REAL NOT NULL
        )
    ''')
    
    # 3. Tabela de Pedidos de Compra
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tb_pedidos_compra (
            id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
            id_produto INTEGER,
            id_fornecedor INTEGER,
            data_pedido TEXT NOT NULL,
            data_entrega_prometida TEXT NOT NULL,
            data_entrega_real TEXT,
            quantidade_pedida INTEGER NOT NULL,
            FOREIGN KEY (id_produto) REFERENCES tb_estoque(id_produto),
            FOREIGN KEY (id_fornecedor) REFERENCES tb_fornecedores(id_fornecedor)
        )
    ''')
    
    # 4. Tabela de Desvios Logísticos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tb_desvios_logisticos (
            id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pedido INTEGER,
            tipo_desvio TEXT NOT NULL,
            data_evento TEXT NOT NULL,
            custo_prejuizo REAL NOT NULL,
            FOREIGN KEY (id_pedido) REFERENCES tb_pedidos_compra(id_pedido)
        )
    ''')
    
    print("--- Populando tabelas com dados realistas ---")
    
    # Inserindo Fornecedores
    fornecedores = [
        (1, 'XYZ Logistics', 'Sudeste'),
        (2, 'Alpha Fast Shippers', 'Sul'),
        (3, 'Global Components Co.', 'Nordeste'),
        (4, 'Beta Supply Chain', 'Sudeste')
    ]
    cursor.executemany('INSERT OR IGNORE INTO tb_fornecedores VALUES (?, ?, ?)', fornecedores)
    
    # Inserindo Produtos (SKUs) - Simulando itens para Curva ABC
    # Itens de alto custo (Classe A), médio (Classe B) e baixo custo com muito volume (Classe C)
    categorias = ['Eletrônicos', 'Mecânicos', 'Embalagens', 'Químicos']
    produtos = []
    
    # Gerando 30 SKUs fictícios
    random.seed(42) # Mantém os dados consistentes a cada execução
    for i in range(1, 31):
        sku = f"SKU-{1000 + i}"
        cat = random.choice(categorias)
        
        if i <= 5: # Classe A simulada (Alto custo)
            custo = round(random.uniform(500.0, 1500.0), 2)
            est_atual = random.randint(20, 50)
            est_seg = random.randint(15, 25)
        elif i <= 15: # Classe B simulada
            custo = round(random.uniform(50.0, 200.0), 2)
            est_atual = random.randint(100, 300)
            est_seg = random.randint(50, 100)
        else: # Classe C simulada (Baixo custo, muito estoque em excesso)
            custo = round(random.uniform(1.0, 20.0), 2)
            # Forçando distorção: estoque atual muito maior que o de segurança para simular o Insight 2
            est_seg = random.randint(100, 200)
            est_atual = est_seg * random.randint(2, 4) if i in [16, 17, 18, 19, 20] else random.randint(150, 400)
            
        produtos.append((i, sku, cat, est_atual, est_seg, custo))
        
    cursor.executemany('INSERT OR IGNORE INTO tb_estoque VALUES (?, ?, ?, ?, ?, ?)', produtos)
    
    # Gerando Pedidos de Compra (Histórico de 1 ano)
    data_inicial = datetime(2025, 1, 1)
    pedidos = []
    desvios = []
    
    id_pedido = 1
    id_desvio = 1
    
    for _ in range(500): # 500 pedidos no ano
        id_prod = random.randint(1, 30)
        id_forn = random.randint(1, 4)
        qtd = random.randint(50, 500)
        
        # Datas do fluxo logístico
        dias_aleatorios = random.randint(0, 340)
        dt_pedido = data_inicial + timedelta(days=dias_aleatorios)
        
        # Prazo acordado padrão no contrato de 7 dias
        prazo_contrato = 7
        dt_prometida = dt_pedido + timedelta(days=prazo_contrato)
        
        # Regras de negócio customizadas para os Insights do README:
        if id_forn == 1: # XYZ Logistics: instável (Lead time alto e variável)
            lead_time_real = int(random.normalvariative(12, 4)) # Média 12, desvio padrão simulado
            lead_time_real = max(3, lead_time_real) # Evita lead times negativos ou bizarros
        else: # Outros fornecedores são mais estáveis e rápidos
            lead_time_real = random.randint(5, 8)
            
        dt_real = dt_pedido + timedelta(days=lead_time_real)
        
        pedidos.append((
            id_pedido, id_prod, id_forn, 
            dt_pedido.strftime('%Y-%m-%d'), 
            dt_prometida.strftime('%Y-%m-%d'), 
            dt_real.strftime('%Y-%m-%d'), 
            qtd
        ))
        
        # Gerando Desvios Logísticos Propositalmente
        # Tipos: 'Damage during transit', 'Invoice Error', 'Short Shipment'
        if random.random() < 0.15: # 15% de chance de dar algum problema no pedido
            # Sorteia o tipo do problema
            sorteio_desvio = random.choice(['Damage during transit', 'Invoice Error', 'Short Shipment', 'Short Shipment'])
            
            # Simula a regra do Insight 3 (Avaria em transporte é rara mas muito cara)
            if sorteio_desvio == 'Damage during transit':
                # Prejuízo alto baseado no custo do produto
                custo_produto = [p[5] for p in produtos if p[0] == id_prod][0]
                prejuizo = round((qtd * custo_produto) * random.uniform(0.3, 0.7), 2)
            else:
                # Erros administrativos geram prejuízos menores/fixos de reprocesso
                prejuizo = round(random.uniform(100.0, 500.0), 2)
                
            desvios.append((
                id_desvio, id_pedido, sorteio_desvio, 
                dt_real.strftime('%Y-%m-%d'), prejuizo
            ))
            id_desvio += 1
            
        id_pedido += 1

    cursor.executemany('INSERT OR IGNORE INTO tb_pedidos_compra VALUES (?, ?, ?, ?, ?, ?, ?)', pedidos)
    cursor.executemany('INSERT OR IGNORE INTO tb_desvios_logisticos VALUES (?, ?, ?, ?, ?)', desvios)
    
    conn.commit()
    conn.close()
    print(f"✅ Banco de dados criado com sucesso em: {db_path}!")

if __name__ == "__main__":
    criar_banco_dados()
