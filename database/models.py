from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.types import (
    String, Integer, Text, DateTime, BigInteger, Boolean, Float
)
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash as hash
import database
from typing import Union
from flask_login import UserMixin
from datetime import datetime


Base = declarative_base()


GRUPO_FORNECEDOR = 1
GRUPO_COMPRADOR = 2
GRUPO_EMPRESA = 3
GRUPO_ADMIN = 4


empresa_categoria = Table(
    "empresa_categoria", Base.metadata,
    Column("empresa", ForeignKey("empresa.id"), primary_key=True),
    Column(
        "categoria_de_fornecedor",
        ForeignKey("categoria_de_fornecedor.id"),
        primary_key=True)
)


empresa_subcategoria = Table(
    "empresa_subcategoria", Base.metadata,
    Column("empresa", ForeignKey("empresa.id"), primary_key=True),
    Column(
        "subcategoria_de_fornecedor",
        ForeignKey("subcategoria_de_fornecedor.id"),
        primary_key=True
    )
)


class Usuario(Base, UserMixin):
    
    @classmethod
    def find_one(
        cls,
        id: Union[int, None] = None,
        email: Union[str, None] = None,
        token: Union[str, None] = None,
        username: Union[str, None] = None
    ):
        try:
            db = database.get_db()
            if id:
                user = db.query(Usuario).filter_by(id=id).first()
            elif email:
                user = db.query(Usuario).filter_by(email=email).first()
            elif token:
                user = db.query(Usuario).filter_by(token=token).first()
            elif username:
                user = db.query(Usuario).filter_by(username=username).first()
            user.grupo = user.grupo
            return user
        except:
            pass
        finally:
            db.close()
            
    @classmethod
    def all(cls):
        try:
            db = database.get_db()
            usuarios = db.query(Usuario).all()
            return usuarios
        finally:
            db.close()
            
    @classmethod
    def get_fornecedor(cls, usuario_id: int):
        fornecedores = Fornecedor.all()
        for fornecedor in fornecedores:
            if fornecedor.usuario.id == usuario_id:
                try:
                    db = database.get_db()
                    fornecedor = db.query(Fornecedor).filter_by(id=fornecedor.id).first()
                    fornecedor.empresa = fornecedor.empresa
                finally:
                    db.close()
                return fornecedor
            
    @classmethod
    def get_empresa(cls, usuario_id: int):
        empresas = Empresa.all()
        for empresa in empresas:
            if empresa.usuario.id == usuario_id:
                try:
                    db = database.get_db()
                    empresa = db.query(Empresa).filter_by(id=empresa.id).first()            
                    empresa.categorias_da_empresa = empresa.categorias.all()
                    empresa.subcategorias_da_empresa = empresa.subcategorias.all()
                    return empresa
                finally:
                    db.close()
            
    @classmethod
    def get_comprador(cls, usuario_id: int):
        compradores = Comprador.all()
        for comprador in compradores:
            if comprador.usuario.id == usuario_id:
                return comprador
    
    __tablename__ = "usuario"
    id = Column(BigInteger, primary_key=True, index=True)
    uuid = Column(String(100))
    username = Column(String(100))
    nome = Column(String(100))
    senha = Column(String(150))
    email = Column(String(100))
    ultimo_login = Column(DateTime)
    ativo = Column(Boolean)
    grupo_id = Column(Integer, ForeignKey("grupo.id"))
    grupo = relationship("Grupo", back_populates="usuarios")
    cadastrado_em = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    def __str__(self):
        return f'<Usuario: id:{self.id}; {self.username}>'
    
    def __repr__(self):
        return f'<Usuario: id:{self.id}; {self.username}>'
    
    def save(self):
        dictionary = self.__dict__
        del dictionary['_sa_instance_state']
        item = Usuario(**dictionary)
        item.senha = hash(item.senha)
        try:
            db = database.get_db()
            db.add(item)
            db.commit()
            db.refresh(item)
        finally:
            db.close()
        return item.id
    
    def atualizar_ultimo_login(self):
        self.update({'ultimo_login': datetime.now()})
        
    def update(self, item):
        if isinstance(item, Usuario):
            dictionary = item.__dict__
            del dictionary['_sa_instance_state']
        elif isinstance(item, dict):
            dictionary = item
        else:
            raise TypeError('O item precisa ser um objeto Usuario ou um dicionario.')

        usuario = Usuario.find_one(id=self.id)
        if usuario:
            try:
                db = database.get_db()
                usuario = db.query(Usuario).filter_by(id=Usuario.id)
                usuario.update(dictionary)
                db.commit()
            finally:
                db.close()
        else:
            item = Usuario(**dictionary)
            item.save()
            
    def update_password(self, password):
        try:
            db = database.get_db()
            db.query(Usuario).filter_by(email=self.email) \
                .update({'senha': hash(password)})
            db.commit()
        finally:
            db.close()


class Grupo(Base):
    __tablename__ = "grupo"
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    usuarios = relationship("Usuario", back_populates="grupo")
    cadastrado_em = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    def __str__(self):
        return f'<Grupo: {self.nome}>'
    def __repr__(self):
        return f'<Grupo: {self.nome}>'
    def save(self):
        dictionary = self.__dict__
        del dictionary['_sa_instance_state']
        item = Grupo(**dictionary)
        try:
            db = database.get_db()
            db.add(item)
            db.commit()
        finally:
            db.close()
    

class SMTP_Config(Base):
    __tablename__ = "smtp_config"
    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String(50))
    senha = Column(String(100))
    porta = Column(Integer)
    servidor = Column(String(50))
    empresa_id = Column(
        BigInteger, ForeignKey("empresa.id", ondelete='SET NULL'))
    empresa = relationship("Empresa", back_populates="smtp_config")
    tls = Column(Boolean)
    ssl = Column(Boolean)
    def __str__(self):
        return f'<SMTP_Config: id:{self.id}; {self.email}>'
    def __repr__(self):
        return f'<SMTP_Config: id:{self.id}; {self.email}>'


class Empresa(Base):
    @classmethod
    def find_one(
        cls,
        uuid: Union[int, None] = None,
        cnpj: Union[str, None] = None
    ):
        try:
            db = database.get_db()
            if uuid:
                empresa = db.query(Usuario).filter_by(uuid=uuid).first()
            elif cnpj:
                empresa = db.query(Usuario).filter_by(cnpj=cnpj).first()
            return empresa
        finally:
            db.close()
    @classmethod
    def all(cls):
        try:
            db = database.get_db()
            _all = db.query(Empresa).all()
            all = []
            for item in _all:
                item.usuario = item.usuario
                all.append(item)
            return all
        finally:
            db.close()
    __tablename__ = "empresa"
    id = Column(BigInteger, primary_key=True, index=True)
    uuid = Column(String(100))
    ativo = Column(Boolean)
    razao_social = Column(String(100))
    nome_fantasia = Column(String(100))
    cnpj = Column(String(100))
    responsavel = Column(String(100))
    abertura = Column(String(100))
    atividade_principal = Column(String(100))
    status = Column(String(100))
    tipo = Column(String(100))
    telefone = Column(String(100))
    natureza_juridica = Column(String(100))
    ultima_atualizacao = Column(DateTime)
    situacao = Column(String(100))
    porte = Column(String(100))
    email = Column(String(100))
    data_situacao = Column(DateTime)
    logradouro = Column(String(100))
    numero = Column(BigInteger)
    complemento = Column(String(100))
    bairro = Column(String(100))
    municipio = Column(String(100))
    uf = Column(String(100))
    cep = Column(String(100))
    
    #ACESSO À API
    url_erp = Column(String(100))
    token_erp = Column(Text)
    usr_erp = Column(String(100))
    senha_erp = Column(String(100))
    
    smtp_config = relationship("SMTP_Config", back_populates="empresa", uselist=False)
    cadastrado_em = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    usuario_id = Column(
        BigInteger, ForeignKey("usuario.id", ondelete='SET NULL'))
    usuario = relationship(
        "Usuario", backref="empresa", foreign_keys=[usuario_id])
    categorias = relationship(
        "CategoriaDeFornecedor",
        secondary=empresa_categoria,
        backref=backref('categorias', lazy='dynamic'),
        lazy='dynamic'
    )
    subcategorias = relationship(
        "SubcategoriaDeFornecedor",
        secondary=empresa_subcategoria,
        backref=backref('subcategorias', lazy='dynamic'),
        lazy='dynamic'
    )
    def __str__(self):
        return f'<Empresa: id:{self.id}; {self.nome_fantasia}>'
    def __repr__(self):
        return f'<Empresa: id:{self.id}; {self.nome_fantasia}>'
    def save(self):
        dictionary = self.__dict__
        del dictionary['_sa_instance_state']
        empresa = Empresa(**dictionary)
        try:
            db = database.get_db()
            db.add(empresa)
            db.commit()
        finally:
            db.close()


class Pergunta(Base):
    __tablename__ = "pergunta"
    id = Column(Integer, primary_key=True)
    peso = Column(Integer)
    empresa_id = Column(BigInteger, ForeignKey("empresa.id", ondelete='CASCADE'))
    empresa = relationship("Empresa", backref="perguntas", foreign_keys=[empresa_id])
    pergunta_descricao = Column(Text, nullable=False)
    tipo_de_resposta = Column(Text, nullable=False)
    def __str__(self):
        return f'<Pergunta: id:{self.id}>'
    def __repr__(self):
        return f'<Pergunta: id:{self.id}>'
    def save(self):
        dictionary = self.__dict__
        del dictionary['_sa_instance_state']
        item = Pergunta(**dictionary)
        try:
            db = database.get_db()
            db.add(item)
            db.commit()
        finally:
            db.close()


class OpcaoDeResposta(Base):
    __tablename__ = "opcoes_de_resposta"
    id = Column(Integer, primary_key=True)
    valor = Column(String(100))
    empresa_id = Column(BigInteger, ForeignKey("empresa.id", ondelete='CASCADE'))
    empresa = relationship("Empresa", backref="opcoes_de_resposta", foreign_keys=[empresa_id])
    def __str__(self):
        return f'<OpcaoDeResposta: id:{self.id}>'
    def __repr__(self):
        return f'<OpcaoDeResposta: id:{self.id}>'
    def save(self):
        dictionary = self.__dict__
        del dictionary['_sa_instance_state']
        item = OpcaoDeResposta(**dictionary)
        try:
            db = database.get_db()
            db.add(item)
            db.commit()
        finally:
            db.close()

class Resposta(Base):
    __tablename__ = "resposta"
    id = Column(Integer, primary_key=True)
    pergunta_id = Column(
        Integer, ForeignKey("pergunta.id", ondelete='CASCADE'))
    pergunta = relationship(
        "Pergunta", backref="resposta", foreign_keys=[pergunta_id])
    cotacao_id = Column(
        BigInteger, ForeignKey("cotacao.id", ondelete='CASCADE'))
    cotacao = relationship(
        "Cotacao", backref="resposta", foreign_keys=[cotacao_id])
    resposta_descricao = Column(Text, nullable=True)
    def __str__(self):
        return f'<Resposta: id:{self.id}>'
    def __repr__(self):
        return f'<Resposta: id:{self.id}>'
    def save(self):
        dictionary = self.__dict__
        del dictionary['_sa_instance_state']
        item = Resposta(**dictionary)
        try:
            db = database.get_db()
            db.add(item)
            db.commit()
        finally:
            db.close()


class Comprador(Base):
    
    @classmethod
    def find_one(
        cls,
        id: Union[int, None] = None,
        email: Union[str, None] = None
    ):
        try:
            db = database.get_db()
            if id:
                user = db.query(Comprador).filter_by(id=id).first()
            elif email:
                user = db.query(Comprador).filter_by(email=email).first()
            return user
        finally:
            db.close()
    @classmethod
    def all(cls):
        try:
            db = database.get_db()
            _all = db.query(Comprador).all()
            all = []
            for item in _all:
                item.usuario = item.usuario
                all.append(item)
        finally:
            db.close()
        return all
    
    __tablename__ = "comprador"
    id = Column(BigInteger, primary_key=True, index=True)
    nome = Column(String(100))
    telefone = Column(String(100))
    email = Column(String(100))
    cadastrado_em = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    empresa_id = Column(
        BigInteger, ForeignKey("empresa.id", ondelete='SET NULL'))
    empresa = relationship(
        "Empresa", backref="compradores", foreign_keys=[empresa_id])
    usuario_id = Column(
        BigInteger, ForeignKey("usuario.id", ondelete='SET NULL'))
    usuario = relationship(
        "Usuario", backref="comprador", foreign_keys=[usuario_id])
    ativo = Column(Boolean)
    def __str__(self):
        return f'<Comprador: id:{self.id}; {self.nome}>'
    def __repr__(self):
        return f'<Comprador: id:{self.id}; {self.nome}>'
    def save(self):
        dictionary = self.__dict__
        del dictionary['_sa_instance_state']
        item = Comprador(**dictionary)
        try:
            db = database.get_db()
            db.add(item)
            db.commit()
        finally:
            db.close()


class Fornecedor(Base):
    
    @classmethod
    def find_one(cls, cnpj=None, id=None):
        try:
            db = database.get_db()
            if id:
                fornecedor = db.query(Fornecedor).filter_by(id=id).first()
            elif cnpj:
                fornecedor = db.query(Fornecedor).filter_by(cnpj=cnpj).first()
            return fornecedor
        finally:
            db.close()
            
    @classmethod
    def all(cls):
        try:
            db = database.get_db()
            _all = db.query(Fornecedor).all()
            all = []
            for item in _all:
                item.usuario = item.usuario
                all.append(item)
        finally:
            db.close()
        return all
    
    __tablename__ = "fornecedor"
    
    id = Column(BigInteger, primary_key=True, index=True)
    # ------------ API ------------ #
    abertura = Column(String(100))
    atividade_principal = Column(String(100))
    status = Column(String(100))
    tipo = Column(String(100))
    telefone = Column(String(100))
    natureza_juridica = Column(String(100))
    ultima_atualizacao = Column(DateTime)
    situacao = Column(String(100))
    porte = Column(String(100))
    email_fornecedor = Column(String(100))
    email_solicitante = Column(String(100))
    data_situacao = Column(DateTime)
    logradouro = Column(String(100))
    numero = Column(BigInteger)
    complemento = Column(String(100))
    bairro = Column(String(100))
    municipio = Column(String(100))
    uf = Column(String(100))
    cep = Column(String(100))
    cnpj = Column(String(100))
    razao_social = Column(String(100))
    nome_fantasia = Column(String(100))
    # ------------ API ------------ #
    codigo_pes_uau = Column(Integer)
    apresentacao = Column(String(100))
    comentario = Column(String(200))
    avaliado = Column(Boolean)
    aprovado = Column(Boolean)
    cadastrado_em = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    empresa_id = Column(BigInteger, ForeignKey(
        "empresa.id", ondelete='SET NULL'))
    empresa = relationship(
        "Empresa", backref="fornecedores", foreign_keys=[empresa_id])
    usuario_id = Column(BigInteger, ForeignKey(
        "usuario.id", ondelete='SET NULL'))
    usuario = relationship(
        "Usuario", backref="fornecedores", foreign_keys=[usuario_id])
    ativo = Column(Boolean)
    avaliado = Column(Boolean)
    aprovado = Column(Boolean)
    
    def __str__(self):
        return f'<Fornecedor: id:{self.id}; {self.nome_fantasia}>'
    
    def __repr__(self):
        return f'<Fornecedor: id:{self.id}; {self.nome_fantasia}>'
    
    def save(self):
        dictionary = self.__dict__
        del dictionary['_sa_instance_state']
        item = Fornecedor(**dictionary)
        try:
            db = database.get_db()
            db.add(item)
            db.commit()
        finally:
            db.close()


class TipoDePrestacao(Base):
    @classmethod
    def all(cls):
        try:
            db = database.get_db()
            _all = db.query(TipoDePrestacao).all()
            all = []
            for item in _all:
                item.categoria = item.categoria
                item.subcategoria = item.subcategoria
                all.append(item)
            return all
        finally:
            db.close()
    __tablename__ = "tipo_de_prestacao"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(100))
    categoria_id = Column(BigInteger, ForeignKey(
        "categoria_de_fornecedor.id", ondelete='SET NULL'))
    categoria = relationship(
        "CategoriaDeFornecedor", backref="tipo_de_prestacao", foreign_keys=[categoria_id])
    subcategoria_id = Column(BigInteger, ForeignKey(
        "subcategoria_de_fornecedor.id", ondelete='SET NULL'))
    subcategoria = relationship(
        "SubcategoriaDeFornecedor", backref="tipo_de_prestacao", foreign_keys=[subcategoria_id])
    descricao = Column(String(100))
    cadastrado_em = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    fornecedor_id = Column(BigInteger, ForeignKey(
        "fornecedor.id", ondelete='SET NULL'))
    fornecedor = relationship(
        "Fornecedor", backref="tipos_de_prestacao", foreign_keys=[fornecedor_id])
    def __str__(self):
        return f'<TipoDePrestacao: id:{self.id}; {self.tipo}>'
    def __repr__(self):
        return f'<TipoDePrestacao: id:{self.id}; {self.tipo}>'
    def save(self):
        dictionary = self.__dict__
        del dictionary['_sa_instance_state']
        item = TipoDePrestacao(**dictionary)
        try:
            db = database.get_db()
            db.add(item)
            db.commit()
        finally:
            db.close()


class ContatoComercial(Base):
    __tablename__ = "contato_comercial"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))
    telefone = Column(String(100))
    ramal = Column(String(100))
    celular = Column(String(100))
    email = Column(String(100))
    cadastrado_em = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    fornecedor_id = Column(BigInteger, ForeignKey(
        "fornecedor.id", ondelete='SET NULL'))
    fornecedor = relationship(
        "Fornecedor", backref="contatos", foreign_keys=[fornecedor_id])
    def __str__(self):
        return f'<ContatoComercial: id:{self.id}; {self.nome}>'
    def __repr__(self):
        return f'<ContatoComercial: id:{self.id}; {self.nome}>'
    def save(self):
        dictionary = self.__dict__
        del dictionary['_sa_instance_state']
        item = ContatoComercial(**dictionary)
        try:
            db = database.get_db()
            db.add(item)
            db.commit()
        finally:
            db.close()


class Cotacao(Base):
    @classmethod
    def find_one(
        cls,
        id=None,
        codigo_empresa=None,
        codigo_obra=None,
        codigo_cotacao=None,
        codigo_fornecedor=None,
        versao=None
    ):
        try:
            db = database.get_db()
            if id:
                cotacao = db.query(Cotacao).filter_by(id=id).first()
            else:
                cotacao = db.query(Cotacao).filter_by(
                    codigo_empresa=codigo_empresa,
                    codigo_obra=codigo_obra,
                    codigo_cotacao=codigo_cotacao,
                    codigo_fornecedor=codigo_fornecedor,
                    versao=versao
                ).first()
            return cotacao
        finally:
            db.close()
    
    __tablename__ = "cotacao"
    
    id = Column(BigInteger, primary_key=True, index=True)
    uuid = Column(String(100))
    preenchida = Column(Boolean, nullable=False)  # Participando
    
    entrega_dos_insumos = Column(String(100))
    entrega_dos_materiais = Column(String(100))
    prazo_de_pagamento = Column(Integer)
    quantidade_de_parcelas = Column(Integer)
    intervalo_parcela = Column(Integer)
    intervalo_entrega = Column(Integer)
    quantidade_entrega = Column(Integer)
    cnpj_do_frete = Column(String(100))
    valor_do_frete = Column(Float)
    tipo_de_frete = Column(String(100))
    observacoes = Column(Text)
    
    total_impostos = Column(Float)
    total_itens = Column(Float)
    total_geral = Column(Float)
    desconto = Column(Float)
    total_liquido = Column(Float)
    
    obra = Column(Integer)
    numero_cotacao = Column(Integer)
    numero_fornecedor = Column(Integer)
    cnpj_fornecedor = Column(String(100))
    cnpj_empresa = Column(String(100))
    
    categoria = Column(String(100))
    codigo_empresa = Column(Integer, nullable=False)
    codigo_obra = Column(Integer, nullable=False)
    codigo_cotacao = Column(Integer, nullable=False)
    codigo_fornecedor = Column(Integer, nullable=False)
    
    contraproposta = Column(Text)
    
    versao = Column(Integer)
    status = Column(Integer) #0: em aberta, 1: em negociacao, 2: finalizado
    
    categoria = Column(String(100))
    
    cadastrado_em = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    empresa_id = Column(
        BigInteger, ForeignKey("empresa.id", ondelete='SET NULL'))
    empresa = relationship(
        "Empresa", backref="compras", foreign_keys=[empresa_id])
    fornecedor_id = Column(
        BigInteger, ForeignKey("fornecedor.id", ondelete='SET NULL'))
    fornecedor = relationship(
        "Fornecedor", backref="vendas", foreign_keys=[fornecedor_id])
    
    def __str__(self):
        return f'<Cotacao: id:{self.id}; {self.categoria}>'
    def __repr__(self):
        return f'<Cotacao: id:{self.id}; {self.categoria}>'
    def save(self):
        dictionary = self.__dict__
        del dictionary['_sa_instance_state']
        item = Cotacao(**dictionary)
        try:
            db = database.get_db()
            db.add(item)
            db.commit()
            db.refresh(item)
        finally:
            db.close()
        return item.id
            
    def update(self, item):
        if isinstance(item, Cotacao):
            dictionary = item.__dict__
            del dictionary['_sa_instance_state']
        elif isinstance(item, dict):
            dictionary = item
        else:
            raise TypeError('O item precisa ser um objeto Cotacao ou um dicionario.')

        cotacao = Cotacao.find_one(id=self.id)
        if cotacao:
            try:
                db = database.get_db()
                cotacao = db.query(Cotacao).filter_by(id=cotacao.id)
                cotacao.update(dictionary)
                db.commit()
            finally:
                db.close()
        else:
            item = Cotacao(**dictionary)
            item.save()


class ItemDeCotacao(Base):
    __tablename__ = 'item_de_cotacao'
    id = Column(BigInteger, primary_key=True, index=True)
    uuid = Column(String(100))
    insumo = Column(String(100))
    descricao = Column(String(100))
    unidade = Column(String(10))
    quantidade = Column(Float)
    preco = Column(Float)
    porcentagem_ipi = Column(Float)
    valor_ipi = Column(Float)
    marca = Column(String(50))
    porcentagem_icms = Column(Float)
    valor_icms = Column(Float)
    cotacao_id = Column(
        BigInteger, ForeignKey("cotacao.id", ondelete='SET NULL'))
    cotacao = relationship(
        "Cotacao", backref="itens", foreign_keys=[cotacao_id])
    def __str__(self):
        return f'<Cotacao: id:{self.id}; {self.descricao}>'
    def __repr__(self):
        return f'<Cotacao: id:{self.id}; {self.descricao}>'
    def save(self):
        dictionary = self.__dict__
        del dictionary['_sa_instance_state']
        item = ItemDeCotacao(**dictionary)
        try:
            db = database.get_db()
            db.add(item)
            db.commit()
        finally:
            db.close()

    def update(self, item):
        if isinstance(item, ItemDeCotacao):
            dictionary = item.__dict__
            del dictionary['_sa_instance_state']
        elif isinstance(item, dict):
            dictionary = item
        else:
            raise TypeError('O item precisa ser um objeto Cotacao ou um dicionario.')

        cotacao = Cotacao.find_one(id=self.id)
        if cotacao:
            try:
                db = database.get_db()
                cotacao = db.query(Cotacao).filter_by(id=cotacao.id)
                cotacao.update(dictionary)
                db.commit()
            finally:
                db.close()
        else:
            item = Cotacao(**dictionary)
            item.save()
    

class CategoriaDeFornecedor(Base):
    
    @classmethod
    def find_one(cls, id):
        try:
            db = database.get_db()
            categoria = db.query(CategoriaDeFornecedor).filter_by(id=id).first()
            return categoria
        finally:
            db.close()
            
    @classmethod
    def all(cls):
        try:
            db = database.get_db()
            all = db.query(CategoriaDeFornecedor).all()
        finally:
            db.close()
        return all
    
    @classmethod
    def get_subcategorias(cls, id):
        try:
            db = database.get_db()
            _subcategorias = db.query(SubcategoriaDeFornecedor).all()
            subcategorias = []
            for subcategoria in _subcategorias:
                if subcategoria.categoria_id == id:
                    subcategorias.append(subcategoria)
                    
            return subcategorias
        finally:
            db.close()
    
    __tablename__ = "categoria_de_fornecedor"
    id = Column(BigInteger, primary_key=True, index=True)
    nome = Column(String(100))
    cadastrado_em = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    def __str__(self):
        return f'<CategoriaDeFornecedor: id:{self.id}; {self.nome}>'
    def __repr__(self):
        return f'<CategoriaDeFornecedor: id:{self.id}; {self.nome}>'
    def save(self):
        dictionary = self.__dict__
        del dictionary['_sa_instance_state']
        item = CategoriaDeFornecedor(**dictionary)
        
        try:
            db = database.get_db()
            db.add(item)
            db.commit()
            db.refresh(item)
        finally:
            db.close()
        return item.id


class SubcategoriaDeFornecedor(Base):
    
    @classmethod
    def all(cls):
        try:
            db = database.get_db()
            all = db.query(SubcategoriaDeFornecedor).all()
        finally:
            db.close()
        return all
    
    __tablename__ = "subcategoria_de_fornecedor"
    id = Column(BigInteger, primary_key=True, index=True)
    nome = Column(String(100))
    categoria_id = Column(BigInteger, ForeignKey(
        "categoria_de_fornecedor.id", ondelete='CASCADE'))
    categoria = relationship("CategoriaDeFornecedor", backref="subcategorias")
    cadastrado_em = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    def __str__(self):
        return f'<SubcategoriaDeFornecedor: id:{self.id}; {self.nome}>'
    def __repr__(self):
        return f'<SubcategoriaDeFornecedor: id:{self.id}; {self.nome}>'
    def save(self):
        dictionary = self.__dict__
        del dictionary['_sa_instance_state']
        item = SubcategoriaDeFornecedor(**dictionary)
        try:
            db = database.get_db()
            db.add(item)
            db.commit()
            db.refresh(item)
        finally:
            db.close()
        return item.id
