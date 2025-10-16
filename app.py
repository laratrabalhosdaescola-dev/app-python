#app.py

from decimal import Decimal
from models import create_session, Cliente, Produto, Pedido, pedido_item

DB_URL = "sqlite:///loja_jogos.db"
session = create_session(DB_URL)

def cadastrar_cliente():
    nome=input("Nome do cliente: ").strip()
    email = input ("Email do cliente: ").strip()
    telefone = input ("telefone do cliente: ").strip() or None
    cliente = Cliente(nome=nome, email=email, telefone=telefone)
    session.add(cliente)
    session.comit()
    print(f"Cliente Cadrastro: {cliente}")

def cadastrar_produto():
    nome_produto = input("Nome do produto").strip()
    preco = Decimal(input ("preço do produto(ex: 199.99):")). replace(".", ".")
    estoque = int(input("estoque: "))

    produto = Produto(nome_produto=nome_produto, preco=preco, estoque=estoque)
    session.add(produto)
    session.comit()
    print(f"Produto Cadrastro: {nome_produto}")

def criar_pedido():
    cliente_id = int(input("Digite o ID do cliente: "))
    pedido = Pedido(cliente_id=cliente_id)  
    session.add(pedido)
    session.flush() # garante o id do pedido antes de inserir itens

    print ("Adicione itens (Enter em produto_ID para finalizar).")  
    while True:
        val: input ("Produto ID (Enter para sair):").strip()
        if not val: 
            break
        produto_id = int(val)
        quantidade = int(input("quantidade : "))

        #buscar produto para pegar preço e validar o estoque
        produto = session.get(Produto, produto.id)
        if produto is None: 
            print("Produto não encontrado")
            continue
        if produto.estoque < quantidade :
            print(f"estoque insuficiente. Quantidade Disponivel : {produto.estoque}")

            
            # debita do estoque 
            produto.estoque -= quantidade

            item=ItemPedido(
                pedido_id = pedido.id,
                produto_id= produto_id,
                quantidade = quantidade,
                preco_unit = produto.preco
            )
            session.add(item)
            
            
            session.comit()



