# -*- coding: utf-8 -*-
"""
Sistema de Biblioteca - Paradigma ESTRUTURADO (Python)

Neste programa NAO sao usadas classes. Os dados ficam em listas de
dicionarios (registros) e toda a logica e dividida em funcoes
(modularizacao), seguindo as tres estruturas basicas da programacao
estruturada: sequencia, decisao (if/elif/else) e repeticao (while/for).
"""

# CONSTANTES (por convencao, nomes em maiusculo nao sao alterados)
PRAZO_DIAS = 7            # prazo de devolucao, em dias
MULTA_POR_DIA = 2.00      # valor da multa por dia de atraso (R$)
LIMITE_EMPRESTIMOS = 2    # maximo de livros por usuario ao mesmo tempo

# dados globais

livros = []      # ex.: {"codigo": 1, "titulo": "...", "autor": "...", "disponivel": True}
usuarios = []    # ex.: {"matricula": 1, "nome": "...", "emprestimos": [1, 3]}
proximo_codigo = 1
proxima_matricula = 1



# auxilio de entrada

def ler_inteiro(mensagem):
    """Le um numero inteiro do teclado, repetindo ate ser valido."""
    while True:                          # estrutura de repeticao
        valor = input(mensagem).strip()
        if valor.isdigit():              # estrutura de decisao
            return int(valor)            # retorno da funcao
        print("  Valor invalido. Digite um numero inteiro.")


def ler_texto(mensagem):
    """Le um texto que nao pode ficar vazio."""
    texto = input(mensagem).strip()
    while texto == "":
        print("  O campo nao pode ficar vazio.")
        texto = input(mensagem).strip()
    return texto


# F. busca
def buscar_livro(codigo):
    """Percorre a lista de livros e devolve o registro encontrado ou None."""
    for livro in livros:
        if livro["codigo"] == codigo:
            return livro
    return None


def buscar_usuario(matricula):
    """Percorre a lista de usuarios e devolve o registro encontrado ou None."""
    for usuario in usuarios:
        if usuario["matricula"] == matricula:
            return usuario
    return None


# F. cadastro
def cadastrar_livro():
    """Cria um novo registro de livro e o adiciona a lista."""
    global proximo_codigo                # altera variavel de escopo global
    titulo = ler_texto("Titulo do livro: ")
    autor = ler_texto("Autor: ")
    livro = {"codigo": proximo_codigo, "titulo": titulo,
             "autor": autor, "disponivel": True}
    livros.append(livro)
    print(f"  Livro cadastrado com codigo {proximo_codigo}.")
    proximo_codigo += 1


def cadastrar_usuario():
    """Cria um novo registro de usuario e o adiciona a lista."""
    global proxima_matricula
    nome = ler_texto("Nome do usuario: ")
    usuario = {"matricula": proxima_matricula, "nome": nome, "emprestimos": []}
    usuarios.append(usuario)
    print(f"  Usuario cadastrado com matricula {proxima_matricula}.")
    proxima_matricula += 1


# F. Regra de negocio
def calcular_multa(dias):
    """Funcao pura: recebe os dias de emprestimo e retorna a multa."""
    atraso = dias - PRAZO_DIAS
    if atraso > 0:
        return atraso * MULTA_POR_DIA
    return 0.0


def emprestar_livro():
    """Registra o emprestimo de um livro para um usuario."""
    matricula = ler_inteiro("Matricula do usuario: ")
    usuario = buscar_usuario(matricula)
    if usuario is None:
        print("  Usuario nao encontrado.")
        return
    if len(usuario["emprestimos"]) >= LIMITE_EMPRESTIMOS:
        print(f"  Limite de {LIMITE_EMPRESTIMOS} emprestimos atingido.")
        return

    codigo = ler_inteiro("Codigo do livro: ")
    livro = buscar_livro(codigo)
    if livro is None:
        print("  Livro nao encontrado.")
    elif not livro["disponivel"]:
        print("  Livro ja esta emprestado.")
    else:
        livro["disponivel"] = False
        usuario["emprestimos"].append(codigo)
        print(f"  Emprestimo realizado: '{livro['titulo']}' para {usuario['nome']}.")


def devolver_livro():
    """Registra a devolucao e calcula a multa por atraso."""
    codigo = ler_inteiro("Codigo do livro: ")
    livro = buscar_livro(codigo)
    if livro is None or livro["disponivel"]:
        print("  Este livro nao esta emprestado.")
        return

    dias = ler_inteiro("Quantos dias o livro ficou com o usuario? ")
    # procura qual usuario esta com o livro
    for usuario in usuarios:
        if codigo in usuario["emprestimos"]:
            usuario["emprestimos"].remove(codigo)
            break
    livro["disponivel"] = True

    multa = calcular_multa(dias)
    if multa > 0:
        print(f"  Devolucao com atraso. Multa: R$ {multa:.2f}")
    else:
        print("  Devolucao no prazo. Sem multa.")


# F. Relatorio
def listar_livros():
    """Mostra todos os livros e a situacao de cada um."""
    if len(livros) == 0:
        print("  Nenhum livro cadastrado.")
        return
    print("  COD | TITULO                         | AUTOR                | SITUACAO")
    for livro in livros:
        situacao = "Disponivel" if livro["disponivel"] else "Emprestado"
        print(f"  {livro['codigo']:>3} | {livro['titulo']:<30} | "
              f"{livro['autor']:<20} | {situacao}")


def listar_usuarios():
    """Mostra os usuarios e quantos livros cada um tem emprestado."""
    if len(usuarios) == 0:
        print("  Nenhum usuario cadastrado.")
        return
    for usuario in usuarios:
        qtd = len(usuario["emprestimos"])
        print(f"  {usuario['matricula']:>3} - {usuario['nome']} "
              f"({qtd} livro(s) emprestado(s))")


# Menu e principal
def exibir_menu():
    """Mostra as opcoes do menu de forma compacta."""
    print("\n===== BIBLIOTECA (ESTRUTURADO) =====")
    print("1-Cad. livro  2-Cad. usuario  3-Emprestar  4-Devolver")
    print("5-Listar livros  6-Listar usuarios  0-Sair")


def main():
    """Funcao principal: laco do menu com selecao de opcoes."""
    opcao = -1
    while opcao != 0:
        exibir_menu()
        opcao = ler_inteiro("Opcao: ")
        if opcao == 1:
            cadastrar_livro()
        elif opcao == 2:
            cadastrar_usuario()
        elif opcao == 3:
            emprestar_livro()
        elif opcao == 4:
            devolver_livro()
        elif opcao == 5:
            listar_livros()
        elif opcao == 6:
            listar_usuarios()
        elif opcao == 0:
            print("Encerrando o sistema...")
        else:
            print("  Opcao invalida.")


# Ponto de entrada do programa
if __name__ == "__main__":
    main()
