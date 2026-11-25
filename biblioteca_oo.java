import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

//  EXCEÇÕES PERSONALIZADAS
class BibliotecaErro extends Exception {
    public BibliotecaErro(String mensagem) {
        super(mensagem);
    }
}

class ItemIndisponivelErro extends BibliotecaErro {
    public ItemIndisponivelErro(String mensagem) {
        super(mensagem);
    }
}

class LimiteEmprestimosErro extends BibliotecaErro {
    public LimiteEmprestimosErro(String mensagem) {
        super(mensagem);
    }
}

class NaoEncontradoErro extends BibliotecaErro {
    public NaoEncontradoErro(String mensagem) {
        super(mensagem);
    }
}

// CLASSE ABSTRATA 
abstract class ItemAcervo {
    protected int codigo;
    protected String titulo;
    protected boolean disponivel;

    public ItemAcervo(int codigo, String titulo) {
        this.codigo = codigo;
        this.titulo = titulo;
        this.disponivel = true;
    }

    public int getCodigo() {
        return codigo;
    }

    public String getTitulo() {
        return titulo;
    }

    public boolean isDisponivel() {
        return disponivel;
    }

    public void marcarEmprestado() throws ItemIndisponivelErro {
        if (!disponivel) {
            throw new ItemIndisponivelErro("'" + titulo + "' ja esta emprestado.");
        }
        this.disponivel = false;
    }

    public void marcarDevolvido() {
        this.disponivel = true;
    }

    // Métodos abstratos
    public abstract int prazoDias();
    public abstract double multaPorDia();
    public abstract String tipo();

    // Template Method
    public double calcularMulta(int dias) {
        int atraso = dias - prazoDias();
        return atraso > 0 ? atraso * multaPorDia() : 0.0;
    }

    @Override
    public String toString() {
        String situacao = disponivel ? "Disponivel" : "Emprestado";
        return String.format("[%d] %-7s %-28s %s", codigo, tipo(), titulo, situacao);
    }
}

//  SUBCLASSES 
class Livro extends ItemAcervo {
    private String autor;

    public Livro(int codigo, String titulo, String autor) {
        super(codigo, titulo);
        this.autor = autor;
    }

    public String getAutor() {
        return autor;
    }

    @Override
    public int prazoDias() {
        return 7;
    }

    @Override
    public double multaPorDia() {
        return 2.00;
    }

    @Override
    public String tipo() {
        return "Livro";
    }
}

class Revista extends ItemAcervo {
    private int edicao;

    public Revista(int codigo, String titulo, int edicao) {
        super(codigo, titulo);
        this.edicao = edicao;
    }

    public int getEdicao() {
        return edicao;
    }

    @Override
    public int prazoDias() {
        return 3;
    }

    @Override
    public double multaPorDia() {
        return 1.00;
    }

    @Override
    public String tipo() {
        return "Revista";
    }
}

//  USUÁRIO
class Usuario {
    public static final int LIMITE = 2;

    private int matricula;
    private String nome;
    private List<ItemAcervo> itens;

    public Usuario(int matricula, String nome) {
        this.matricula = matricula;
        this.nome = nome;
        this.itens = new ArrayList<>();
    }

    public int getMatricula() {
        return matricula;
    }

    public String getNome() {
        return nome;
    }

    public boolean podeEmprestar() {
        return itens.size() < LIMITE;
    }

    public void adicionarItem(ItemAcervo item) throws LimiteEmprestimosErro {
        if (!podeEmprestar()) {
            throw new LimiteEmprestimosErro(
                nome + " ja atingiu o limite de " + LIMITE + " emprestimos."
            );
        }
        itens.add(item);
    }

    public void removerItem(ItemAcervo item) {
        itens.remove(item);
    }

    public boolean possui(ItemAcervo item) {
        return itens.contains(item);
    }

    @Override
    public String toString() {
        return String.format("%3d - %s (%d item(ns) emprestado(s))", matricula, nome, itens.size());
    }
}

// Classe auxiliar para retornar item + usuario no empréstimo
class Emprestimo {
    public final ItemAcervo item;
    public final Usuario usuario;

    public Emprestimo(ItemAcervo item, Usuario usuario) {
        this.item = item;
        this.usuario = usuario;
    }
}

// BIBLIOTECA 
class Biblioteca {
    private String nome;
    private Map<Integer, ItemAcervo> acervo;
    private Map<Integer, Usuario> usuarios;
    private int proxCodigo;
    private int proxMatricula;

    public Biblioteca(String nome) {
        this.nome = nome;
        this.acervo = new LinkedHashMap<>();
        this.usuarios = new LinkedHashMap<>();
        this.proxCodigo = 1;
        this.proxMatricula = 1;
    }

    public Livro cadastrarLivro(String titulo, String autor) {
        Livro item = new Livro(proxCodigo, titulo, autor);
        registrar(item);
        return item;
    }

    public Revista cadastrarRevista(String titulo, int edicao) {
        Revista item = new Revista(proxCodigo, titulo, edicao);
        registrar(item);
        return item;
    }

    private void registrar(ItemAcervo item) {
        acervo.put(item.getCodigo(), item);
        proxCodigo++;
    }

    public Usuario cadastrarUsuario(String nome) {
        Usuario usuario = new Usuario(proxMatricula, nome);
        usuarios.put(usuario.getMatricula(), usuario);
        proxMatricula++;
        return usuario;
    }

    public ItemAcervo buscarItem(int codigo) throws NaoEncontradoErro {
        ItemAcervo item = acervo.get(codigo);
        if (item == null) {
            throw new NaoEncontradoErro("Item " + codigo + " nao encontrado.");
        }
        return item;
    }

    public Usuario buscarUsuario(int matricula) throws NaoEncontradoErro {
        Usuario usuario = usuarios.get(matricula);
        if (usuario == null) {
            throw new NaoEncontradoErro("Usuario " + matricula + " nao encontrado.");
        }
        return usuario;
    }

    public Emprestimo emprestar(int matricula, int codigo) throws BibliotecaErro {
        Usuario usuario = buscarUsuario(matricula);
        ItemAcervo item = buscarItem(codigo);

        if (!usuario.podeEmprestar()) {
            throw new LimiteEmprestimosErro(
                usuario.getNome() + " ja atingiu o limite de " + Usuario.LIMITE + " emprestimos."
            );
        }

        item.marcarEmprestado();
        usuario.adicionarItem(item);
        return new Emprestimo(item, usuario);
    }

    public double devolver(int codigo, int dias) throws BibliotecaErro {
        ItemAcervo item = buscarItem(codigo);
        if (item.isDisponivel()) {
            throw new BibliotecaErro("Este item nao esta emprestado.");
        }

        for (Usuario usuario : usuarios.values()) {
            if (usuario.possui(item)) {
                usuario.removerItem(item);
                break;
            }
        }

        item.marcarDevolvido();
        return item.calcularMulta(dias);
    }

    public List<ItemAcervo> getItens() {
        return new ArrayList<>(acervo.values());
    }

    public List<Usuario> getUsuarios() {
        return new ArrayList<>(usuarios.values());
    }
}

// MENU (INTERFACE DE TEXTO) 
class Menu {
    private Biblioteca bib;
    private Scanner scanner;

    public Menu(Biblioteca biblioteca) {
        this.bib = biblioteca;
        this.scanner = new Scanner(System.in);
    }

    private int lerInteiro(String msg) {
        while (true) {
            System.out.print(msg);
            String valor = scanner.nextLine().trim();
            if (valor.matches("\\d+")) {
                return Integer.parseInt(valor);
            }
            System.out.println("  Valor invalido. Digite um numero inteiro.");
        }
    }

    private String lerTexto(String msg) {
        while (true) {
            System.out.print(msg);
            String texto = scanner.nextLine().trim();
            if (!texto.isEmpty()) {
                return texto;
            }
            System.out.println("  O campo nao pode ficar vazio.");
        }
    }

    private void exibir() {
        System.out.println("\n===== BIBLIOTECA (ORIENTADO A OBJETOS) =====");
        System.out.println("1-Cad. livro  2-Cad. revista  3-Cad. usuario  4-Emprestar");
        System.out.println("5-Devolver  6-Listar acervo  7-Listar usuarios  0-Sair");
    }

    public void executar() {
        while (true) {
            exibir();
            int opcao = lerInteiro("Opcao: ");

            if (opcao == 0) {
                System.out.println("Encerrando o sistema...");
                break;
            }

            try {
                switch (opcao) {
                    case 1: cadastrarLivro(); break;
                    case 2: cadastrarRevista(); break;
                    case 3: cadastrarUsuario(); break;
                    case 4: emprestar(); break;
                    case 5: devolver(); break;
                    case 6: listarAcervo(); break;
                    case 7: listarUsuarios(); break;
                    default: System.out.println("  Opcao invalida.");
                }
            } catch (BibliotecaErro erro) {
                System.out.println("  ERRO: " + erro.getMessage());
            }
        }
        scanner.close();
    }

    private void cadastrarLivro() {
        Livro item = bib.cadastrarLivro(lerTexto("Titulo: "), lerTexto("Autor: "));
        System.out.println("  Livro cadastrado com codigo " + item.getCodigo() + ".");
    }

    private void cadastrarRevista() {
        Revista item = bib.cadastrarRevista(lerTexto("Titulo: "), lerInteiro("Edicao: "));
        System.out.println("  Revista cadastrada com codigo " + item.getCodigo() + ".");
    }

    private void cadastrarUsuario() {
        Usuario u = bib.cadastrarUsuario(lerTexto("Nome: "));
        System.out.println("  Usuario cadastrado com matricula " + u.getMatricula() + ".");
    }

    private void emprestar() throws BibliotecaErro {
        int matricula = lerInteiro("Matricula: ");
        int codigo = lerInteiro("Codigo do item: ");
        Emprestimo emp = bib.emprestar(matricula, codigo);
        System.out.printf("  Emprestimo realizado: '%s' para %s (prazo: %d dias).%n",
                emp.item.getTitulo(), emp.usuario.getNome(), emp.item.prazoDias());
    }

    private void devolver() throws BibliotecaErro {
        int codigo = lerInteiro("Codigo do item: ");
        int dias = lerInteiro("Dias com o usuario: ");
        double multa = bib.devolver(codigo, dias);
        if (multa > 0) {
            System.out.printf("  Devolucao com atraso. Multa: R$ %.2f%n", multa);
        } else {
            System.out.println("  Devolucao no prazo. Sem multa.");
        }
    }

    private void listarAcervo() {
        List<ItemAcervo> itens = bib.getItens();
        if (itens.isEmpty()) {
            System.out.println("  Acervo vazio.");
            return;
        }
        for (ItemAcervo item : itens) {
            System.out.println("  " + item);
        }
    }

    private void listarUsuarios() {
        List<Usuario> usuarios = bib.getUsuarios();
        if (usuarios.isEmpty()) {
            System.out.println("  Nenhum usuario cadastrado.");
            return;
        }
        for (Usuario u : usuarios) {
            System.out.println("  " + u);
        }
    }
}

// PROGRAMA PRINCIPAL 
public class biblioteca_oo {
    public static void main(String[] args) {
        Biblioteca biblioteca = new Biblioteca("Biblioteca Central");
        new Menu(biblioteca).executar();
    }
}