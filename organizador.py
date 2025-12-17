import json
import heapq
import os

# ------------------------------------------------------
# PAUSA
# ------------------------------------------------------
def pausa():
    input("\nPressione ENTER para continuar...")


# ------------------------------------------------------
# NÓ DA ÁRVORE (ARQUIVO / DIRETÓRIO)
# Cada diretório possui sua própria árvore binária de filhos
# ------------------------------------------------------
class Node:
    def __init__(self, nome, tipo, tamanho=0):
        self.nome = nome
        self.tipo = tipo  # 'arquivo' ou 'diretorio'
        self.tamanho = tamanho
        self.acessos = 0

        # árvore binária (irmãos)
        self.esq = None
        self.dir = None

        # filhos (somente se diretório)
        self.filhos = None

    # -------- SERIALIZAÇÃO --------
    def to_dict(self):
        return {
            "nome": self.nome,
            "tipo": self.tipo,
            "tamanho": self.tamanho,
            "acessos": self.acessos,
            "esq": self.esq.to_dict() if self.esq else None,
            "dir": self.dir.to_dict() if self.dir else None,
            "filhos": self.filhos.to_dict() if self.filhos else None
        }

    @staticmethod
    def from_dict(d):
        if not d:
            return None
        n = Node(d["nome"], d["tipo"], d["tamanho"])
        n.acessos = d.get("acessos", 0)
        n.esq = Node.from_dict(d.get("esq"))
        n.dir = Node.from_dict(d.get("dir"))
        n.filhos = Node.from_dict(d.get("filhos"))
        return n


# ------------------------------------------------------
# SISTEMA DE ARQUIVOS
# ------------------------------------------------------
class SistemaArquivos:
    def __init__(self):
        self.raiz = Node("/", "diretorio")
        self.heap = []          # heap de sugestões
        self.undo = []          # pilha de desfazer
        self.arquivo = "sistema_arquivos.json"
        self.carregar()

    # ---------------- INSERÇÃO EM ÁRVORE BINÁRIA ----------------
    def _inserir_bst(self, r, n):
        if not r:
            return n
        if n.nome < r.nome:
            r.esq = self._inserir_bst(r.esq, n)
        else:
            r.dir = self._inserir_bst(r.dir, n)
        return r

    # ---------------- BUSCA EM ÁRVORE BINÁRIA ----------------
    def _buscar_bst(self, r, nome):
        while r:
            if nome == r.nome:
                return r
            r = r.esq if nome < r.nome else r.dir
        return None

    # ---------------- NAVEGAR ATÉ DIRETÓRIO ----------------
    def _navegar(self, caminho):
        atual = self.raiz
        if caminho == "/":
            return atual
        for parte in caminho.strip("/").split("/"):
            atual = self._buscar_bst(atual.filhos, parte)
            if not atual or atual.tipo != "diretorio":
                return None
        return atual

    # ---------------- CRIAR ----------------
    def criar(self, caminho, nome, tipo, tamanho=0):
        pai = self._navegar(caminho)
        if not pai:
            return False
        novo = Node(nome, tipo, tamanho)
        pai.filhos = self._inserir_bst(pai.filhos, novo)
        self.undo.append(("excluir", caminho, nome))
        self.salvar()
        return True

    # ---------------- EXCLUIR ----------------
    def _excluir_bst(self, r, nome):
        if not r:
            return None, None
        if nome < r.nome:
            r.esq, removido = self._excluir_bst(r.esq, nome)
            return r, removido
        if nome > r.nome:
            r.dir, removido = self._excluir_bst(r.dir, nome)
            return r, removido

        if not r.esq:
            return r.dir, r
        if not r.dir:
            return r.esq, r

        m = r.dir
        while m.esq:
            m = m.esq
        r.nome, r.tipo, r.tamanho, r.acessos, r.filhos = (
            m.nome, m.tipo, m.tamanho, m.acessos, m.filhos
        )
        r.dir, _ = self._excluir_bst(r.dir, m.nome)
        return r, r

    def excluir(self, caminho, nome):
        pai = self._navegar(caminho)
        if not pai:
            return False
        pai.filhos, removido = self._excluir_bst(pai.filhos, nome)
        if removido:
            self.undo.append(("criar", caminho, removido))
            self.salvar()
            return True
        return False

    # ---------------- RENOMEAR ----------------
    def renomear(self, caminho, antigo, novo):
        pai = self._navegar(caminho)
        n = self._buscar_bst(pai.filhos, antigo)
        if not n:
            return False
        self.undo.append(("renomear", caminho, novo, antigo))
        n.nome = novo
        self.salvar()
        return True

    # ---------------- MOVER ----------------
    def mover(self, origem, nome, destino):
        pai_origem = self._navegar(origem)
        pai_destino = self._navegar(destino)
        if not pai_origem or not pai_destino:
            return False
        pai_origem.filhos, removido = self._excluir_bst(pai_origem.filhos, nome)
        if not removido:
            return False
        pai_destino.filhos = self._inserir_bst(pai_destino.filhos, removido)
        self.undo.append(("mover", destino, nome, origem))
        self.salvar()
        return True

    # ---------------- ACESSAR ----------------
    def acessar(self, caminho, nome):
        pai = self._navegar(caminho)
        n = self._buscar_bst(pai.filhos, nome)
        if not n:
            return False
        n.acessos += 1
        heapq.heappush(self.heap, (-n.acessos, -n.tamanho, nome, n.tipo))
        self.salvar()
        return True

    # ---------------- SUGESTÕES (HEAP) ----------------
    def sugeridos(self, qtd=5):
        vistos = set()
        res = []
        temp = []
        while self.heap and len(res) < qtd:
            a, t, nome, tipo = heapq.heappop(self.heap)
            if nome not in vistos:
                res.append((nome, tipo, -a, -t))
                vistos.add(nome)
            temp.append((a, t, nome, tipo))
        for x in temp:
            heapq.heappush(self.heap, x)
        return res

    # ---------------- DESFAZER ----------------
    def desfazer(self):
        if not self.undo:
            return False
        acao = self.undo.pop()
        tipo = acao[0]

        if tipo == "excluir":
            _, caminho, nome = acao
            self.excluir(caminho, nome)

        elif tipo == "criar":
            _, caminho, node = acao
            pai = self._navegar(caminho)
            pai.filhos = self._inserir_bst(pai.filhos, node)

        elif tipo == "renomear":
            _, caminho, atual, antigo = acao
            self.renomear(caminho, atual, antigo)

        elif tipo == "mover":
            _, destino, nome, origem = acao
            self.mover(destino, nome, origem)

        self.salvar()
        return True

    # ---------------- LISTAR ----------------
    def listar(self, caminho):
        pai = self._navegar(caminho)
        res = []
        self._listar_bst(pai.filhos, res)
        return res

    def _listar_bst(self, r, l):
        if r:
            l.append((r.nome, r.tipo))
            self._listar_bst(r.esq, l)
            self._listar_bst(r.dir, l)

    # ---------------- SALVAR / CARREGAR ----------------
    def salvar(self):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump({
                "raiz": self.raiz.to_dict(),
                "heap": self.heap
            }, f, indent=4)

    def carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r", encoding="utf-8") as f:
                d = json.load(f)
            self.raiz = Node.from_dict(d.get("raiz"))
            self.heap = d.get("heap", [])


# ------------------------------------------------------
# MENU
# ------------------------------------------------------
def escolher_item(s, caminho):
    itens = s.listar(caminho)
    if not itens:
        print("Nenhum item neste diretório.")
        return None
    for i, (n, t) in enumerate(itens, 1):
        print(f"{i} - {n} ({t})")
    op = int(input("Escolha: ")) - 1
    return itens[op][0]


def main():
    s = SistemaArquivos()

    while True:
        print("""
===== ORGANIZADOR DE ARQUIVOS =====
1 - Criar arquivo/diretório
2 - Excluir
3 - Renomear
4 - Mover
5 - Acessar
6 - Sugeridos (mais acessados/maiores)
7 - Desfazer última ação
8 - Listar diretório
0 - Sair
==================================
""")

        op = input("Opção: ")

        try:
            if op == "1":
                caminho = input("Caminho do diretório (ex: /): ")
                nome = input("Nome: ")
                print("1 - Arquivo\n2 - Diretório")
                t = input("Tipo: ")
                if t == "1":
                    tam = int(input("Tamanho: "))
                    s.criar(caminho, nome, "arquivo", tam)
                else:
                    s.criar(caminho, nome, "diretorio")
                pausa()

            elif op == "2":
                caminho = input("Caminho: ")
                nome = escolher_item(s, caminho)
                if nome:
                    s.excluir(caminho, nome)
                pausa()

            elif op == "3":
                caminho = input("Caminho: ")
                antigo = escolher_item(s, caminho)
                if antigo:
                    novo = input("Novo nome: ")
                    s.renomear(caminho, antigo, novo)
                pausa()

            elif op == "4":
                origem = input("Origem: ")
                nome = escolher_item(s, origem)
                if nome:
                    destino = input("Destino: ")
                    s.mover(origem, nome, destino)
                pausa()

            elif op == "5":
                caminho = input("Caminho: ")
                nome = escolher_item(s, caminho)
                if nome:
                    s.acessar(caminho, nome)
                pausa()

            elif op == "6":
                for n, t, a, tam in s.sugeridos():
                    print(f"{n} ({t}) - {a} acessos - {tam} tamanho")
                pausa()

            elif op == "7":
                s.desfazer()
                pausa()

            elif op == "8":
                caminho = input("Caminho: ")
                for n, t in s.listar(caminho):
                    print(f"{n} ({t})")
                pausa()

            elif op == "0":
                break

        except Exception:
            print("Erro na operação")
            pausa()


if __name__ == "__main__":
    main()