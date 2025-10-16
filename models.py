# models.py
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Numeric, CheckConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# ===== MODELS =====
class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    telefone = Column(String(20))

    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cliente id={self.id} nome={self.nome!r} email={self.email!r}>"

class Produto(Base):
    __tablename__ = "produtos"

    id_produto = Column(Integer, primary_key=True)
    nome_produto = Column(String(160), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    estoque = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        CheckConstraint("preco >= 0", name="ck_produto_preco"),
        CheckConstraint("estoque >= 0", name="ck_produto_estoque"),
    )

    itens = relationship("ItemPedido", back_populates="produto")

    def __repr__(self):
        return f"<Produto id={self.id} nome_produto={self.nome_produto!r} preco={self.preco!r} estoque={self.estoque}>"
    
class Pedido (Base):
    __tablename__ = "pedido"
    
     #id_pedido = Column(Integer, primary_key = true)
    id = Column(Integer, primary_key = True)
    id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)
     #quant_produtos = Column(Integer, nullable=)
     #preco_total = Column(numeric(10,2), nullable=false)
     #nome_cliente = Column(varchar(100), nullable=false)
    data_criacao = Column(DateTime, nullable = False, default=datetime.utcnow)
    status = Column(String(120), nullable=False, default="Aberto")
    
    cliente = relationship("Cliente", back_populates="pedidos")
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")
    
    def total(self):
        return sum((it.quantidade * it.preco_unitario) for it in self.itens)

    def __repr__(self):
        return"<Pedido ID: {self.id} | Cliente ID: {self.cliente_id} | status: {self.status}"

class pedido_item (Base):
    __tablename__ = "pedido_item"
    
    id_cliente = Column(Integer, primary_key = True)
    id_produto = Column(Integer, primary_key = True)
    loc = Column(String(100))

# CONEXÕES E SESSOES 
def get_engine(db_url: str = "sqlite:///loja_jogos.db"):
    return create_engine (db_url, echo= False, future= True)

def create_session(db_url: str = "sqlite:///loja_jogos.db"):
    engine = get_engine(db_url)
    Base.metadata.create_All(engine)
    Sessionlocal = sessionmaker(bind= engine, autoflush=False, autocommit= False, future= True)
    return SessionLocal()   

# Comentario para teste !