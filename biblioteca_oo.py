# -*- coding: utf-8 -*-
"""
Sistema de Biblioteca - Paradigma ORIENTADO A OBJETOS (Python)

Conceitos aplicados:
  - Classe e objeto
  - Construtor (__init__) e atributos de instancia
  - Encapsulamento (atributos "privados" com _ e acesso por @property)
  - Abstracao (classe abstrata com ABC e @abstractmethod)
  - Heranca (Livro e Revista herdam de ItemAcervo)
  - Polimorfismo (cada item calcula prazo e multa do seu jeito)
  - Associacao / composicao (Biblioteca contem itens, usuarios e emprestimos)
  - Excecoes personalizadas (classes de erro proprias)
  - Metodos especiais (__str__)
"""

from abc import ABC, abstractmethod


# E. personalizadas (heranca da classe Exception)
class BibliotecaErro(Exception):
    """Erro base do sistema de biblioteca."""


class ItemIndisponivelErro(BibliotecaErro):
    """Lancado quando se tenta emprestar um item que ja esta emprestado."""


class LimiteEmprestimosErro(BibliotecaErro):
    """Lancado quando o usuario ja atingiu o limite de emprestimos."""


class NaoEncontradoErro(BibliotecaErro):
    """Lancado quando um codigo ou matricula nao existe."""


# C. abstrata
class ItemAcervo(ABC):
    """Representa qualquer item do acervo. Nao pode ser instanciada."""

    def __init__(self, codigo, titulo):
        self._codigo = codigo          # atributo protegido (encapsulamento)
        self._titulo = titulo
        self._disponivel = True

    # propriedades: acesso controlado aos atributos 
    @property
    def codigo(self):
        return self._codigo

    @property
    def titulo(self):
        return self._titulo

    @property
    def disponivel(self):
        return self._disponivel

    def marcar_emprestado(self):
        if not self._disponivel:
            raise ItemIndisponivelErro(f"'{self._titulo}' ja esta emprestado.")
        self._disponivel = False

    def marcar_devolvido(self):
        self._disponivel = True

    # metodos abstratos: cada subclasse DEVE implementar 
    @abstractmethod
    def prazo_dias(self):
        """Prazo de devolucao em dias."""

    @abstractmethod
    def multa_por_dia(self):
        """Valor da multa por dia de atraso."""

    @abstractmethod
    def tipo(self):
        """Nome do tipo do item."""

    # metodo concreto que usa os abstratos (Template Method) 
    def calcular_multa(self, dias):
        atraso = dias - self.prazo_dias()
        return atraso * self.multa_por_dia() if atraso > 0 else 0.0

    def __str__(self):
        situacao = "Disponivel" if self._disponivel else "Emprestado"
        return f"[{self._codigo}] {self.tipo():<7} {self._titulo:<28} {situacao}"


# subclasses
class Livro(ItemAcervo):
    def __init__(self, codigo, titulo, autor):
        super().__init__(codigo, titulo)   # chama o construtor da superclasse
        self._autor = autor

    @property
    def autor(self):
        return self._autor

    def prazo_dias(self):
        return 7

    def multa_por_dia(self):
        return 2.00

    def tipo(self):
        return "Livro"


class Revista(ItemAcervo):
    def __init__(self, codigo, titulo, edicao):
        super().__init__(codigo, titulo)
        self._edicao = edicao

    def prazo_dias(self):
        return 3                            # revistas tem prazo menor

    def multa_por_dia(self):
        return 1.00                         # e multa menor

    def tipo(self):
        return "Revista"


# C- Usuario
class Usuario:
    LIMITE = 2                              # atributo de classe

    def __init__(self, matricula, nome):
        self._matricula = matricula
        self._nome = nome
        self._itens = []                    # itens em posse do usuario

    @property
    def matricula(self):
        return self._matricula

    @property
    def nome(self):
        return self._nome

    def pode_emprestar(self):
        return len(self._itens) < Usuario.LIMITE

    def adicionar_item(self, item):
        if not self.pode_emprestar():
            raise LimiteEmprestimosErro(
                f"{self._nome} ja atingiu o limite de {Usuario.LIMITE} emprestimos.")
        self._itens.append(item)

    def remover_item(self, item):
        self._itens.remove(item)

    def possui(self, item):
        return item in self._itens

    def __str__(self):
        return f"{self._matricula:>3} - {self._nome} ({len(self._itens)} item(ns) emprestado(s))"


# C. blibioteca
class Biblioteca:
    def __init__(self, nome):
        self._nome = nome
        self._acervo = {}                   # codigo -> ItemAcervo
        self._usuarios = {}                 # matricula -> Usuario
        self._prox_codigo = 1
        self._prox_matricula = 1

    # cadastro 
    def cadastrar_livro(self, titulo, autor):
        item = Livro(self._prox_codigo, titulo, autor)
        return self._registrar(item)

    def cadastrar_revista(self, titulo, edicao):
        item = Revista(self._prox_codigo, titulo, edicao)
        return self._registrar(item)

    def _registrar(self, item):             # metodo "privado" de apoio
        self._acervo[item.codigo] = item
        self._prox_codigo += 1
        return item

    def cadastrar_usuario(self, nome):
        usuario = Usuario(self._prox_matricula, nome)
        self._usuarios[usuario.matricula] = usuario
        self._prox_matricula += 1
        return usuario

    # buscas 
    def buscar_item(self, codigo):
        if codigo not in self._acervo:
            raise NaoEncontradoErro(f"Item {codigo} nao encontrado.")
        return self._acervo[codigo]

    def buscar_usuario(self, matricula):
        if matricula not in self._usuarios:
            raise NaoEncontradoErro(f"Usuario {matricula} nao encontrado.")
        return self._usuarios[matricula]

    # regras de negocio 
    def emprestar(self, matricula, codigo):
        usuario = self.buscar_usuario(matricula)
        item = self.buscar_item(codigo)
        if not usuario.pode_emprestar():
            raise LimiteEmprestimosErro(
                f"{usuario.nome} ja atingiu o limite de {Usuario.LIMITE} emprestimos.")
        item.marcar_emprestado()            # pode lancar ItemIndisponivelErro
        usuario.adicionar_item(item)
        return item, usuario

    def devolver(self, codigo, dias):
        item = self.buscar_item(codigo)
        if item.disponivel:
            raise BibliotecaErro("Este item nao esta emprestado.")
        for usuario in self._usuarios.values():
            if usuario.possui(item):
                usuario.remover_item(item)
                break
        item.marcar_devolvido()
        return item.calcular_multa(dias)    # chamada polimorfica

    def itens(self):
        return list(self._acervo.values())

    def usuarios(self):
        return list(self._usuarios.values())


# INTERFACE COM O USUARIO (menu de texto)

class Menu:
    def __init__(self, biblioteca):
        self._bib = biblioteca

    @staticmethod
    def ler_inteiro(msg):
        while True:
            valor = input(msg).strip()
            if valor.isdigit():
                return int(valor)
            print("  Valor invalido. Digite um numero inteiro.")

    @staticmethod
    def ler_texto(msg):
        texto = input(msg).strip()
        while not texto:
            print("  O campo nao pode ficar vazio.")
            texto = input(msg).strip()
        return texto

    def exibir(self):
        print("\n===== BIBLIOTECA (ORIENTADO A OBJETOS) =====")
        print("1-Cad. livro  2-Cad. revista  3-Cad. usuario  4-Emprestar")
        print("5-Devolver  6-Listar acervo  7-Listar usuarios  0-Sair")

    def executar(self):
        # dicionario de opcoes -> metodos (evita longa cadeia de if/elif)
        acoes = {1: self._livro, 2: self._revista, 3: self._usuario,
                 4: self._emprestar, 5: self._devolver,
                 6: self._listar_acervo, 7: self._listar_usuarios}
        while True:
            self.exibir()
            opcao = self.ler_inteiro("Opcao: ")
            if opcao == 0:
                print("Encerrando o sistema...")
                break
            acao = acoes.get(opcao)
            if acao is None:
                print("  Opcao invalida.")
                continue
            try:
                acao()
            except BibliotecaErro as erro:   # tratamento de excecoes
                print(f"  ERRO: {erro}")

    # ---------- acoes do menu ----------
    def _livro(self):
        item = self._bib.cadastrar_livro(self.ler_texto("Titulo: "),
                                         self.ler_texto("Autor: "))
        print(f"  Livro cadastrado com codigo {item.codigo}.")

    def _revista(self):
        item = self._bib.cadastrar_revista(self.ler_texto("Titulo: "),
                                           self.ler_inteiro("Edicao: "))
        print(f"  Revista cadastrada com codigo {item.codigo}.")

    def _usuario(self):
        u = self._bib.cadastrar_usuario(self.ler_texto("Nome: "))
        print(f"  Usuario cadastrado com matricula {u.matricula}.")

    def _emprestar(self):
        item, usuario = self._bib.emprestar(self.ler_inteiro("Matricula: "),
                                            self.ler_inteiro("Codigo do item: "))
        print(f"  Emprestimo realizado: '{item.titulo}' para {usuario.nome} "
              f"(prazo: {item.prazo_dias()} dias).")

    def _devolver(self):
        codigo = self.ler_inteiro("Codigo do item: ")
        dias = self.ler_inteiro("Dias com o usuario: ")
        multa = self._bib.devolver(codigo, dias)
        if multa > 0:
            print(f"  Devolucao com atraso. Multa: R$ {multa:.2f}")
        else:
            print("  Devolucao no prazo. Sem multa.")

    def _listar_acervo(self):
        itens = self._bib.itens()
        if not itens:
            print("  Acervo vazio.")
        for item in itens:                  # cada objeto usa seu proprio __str__
            print(f"  {item}")

    def _listar_usuarios(self):
        usuarios = self._bib.usuarios()
        if not usuarios:
            print("  Nenhum usuario cadastrado.")
        for u in usuarios:
            print(f"  {u}")


# programa principal
if __name__ == "__main__":
    biblioteca = Biblioteca("Biblioteca Central")   # criacao do objeto
    Menu(biblioteca).executar()
