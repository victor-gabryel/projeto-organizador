import json
import heapq
import os

# ------------------------------------------------------
# PAUSA
# ------------------------------------------------------
def pausa():
    input("\nPressione ENTER para continuar...")


# ------------------------------------------------------
# NÓ DA ÁRVORE
# ------------------------------------------------------
class Node:
    def __init__(self, nome, tipo, tamanho=0):
        self.nome = nome
        self.tipo = tipo
        self.tamanho = tamanho
        self.acessos = 0

        self.esq = None
        self.dir = None
        self.filhos = None

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
        n = Node(d["nome"], d["tipo"], d.get("tamanho", 0))
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
        self.arquivo = "sistema_arquivos.json"
        self.undo = []
        self.heap = []

        if os.path.exists(self.arquivo):
            self.carregar()
        else:
            self.raiz = Node("/", "diretorio")

    # ---------------- BST ----------------
    def _inserir_bst(self, r, n):
        if not r:
            return n
        if n.nome < r.nome:
            r.esq = self._inserir_bst(r.esq, n)
        else:
            r.dir = self._inserir_bst(r.dir, n)
        return r

    def _buscar_bst(self, r, nome):
        while r:
            if nome == r.nome:
                return r
            r = r.esq if nome < r.nome else r.dir
        return None

    def _excluir_bst(self, r, nome):
        if not r:
            return None, None

        if nome < r.nome:
            r.esq, rem = self._excluir_bst(r.esq, nome)
            return r, rem

        if nome > r.nome:
            r.dir, rem = self._excluir_bst(r.dir, nome)
            return r, rem

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

    # ---------------- NAVEGAÇÃO ----------------
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
        if not pai or self._buscar_bst(pai.filhos, nome):
            return False

        node = Node(nome, tipo, tamanho)
        pai.filhos = self._inserir_bst(pai.filhos, node)
        self.undo.append(("criar", caminho, nome))
        self.salvar()
        return True

    # ---------------- EXCLUIR ----------------
    def excluir(self, caminho, nome):
        pai = self._navegar(caminho)
        if not pai:
            return False

        pai.filhos, node = self._excluir_bst(pai.filhos, nome)
        if not node:
            return False

        self.undo.append(("excluir", caminho, node))
        self.salvar()
        return True

    # ---------------- RENOMEAR ----------------
    def renomear(self, caminho, antigo, novo):
        # bloqueia renomear raiz
        if caminho == "/" and antigo == "/":
            return False

        pai = self._navegar(caminho)
        if not pai or self._buscar_bst(pai.filhos, novo):
            return False

        pai.filhos, node = self._excluir_bst(pai.filhos, antigo)
        if not node:
            return False

        node.nome = novo
        pai.filhos = self._inserir_bst(pai.filhos, node)
        self.undo.append(("renomear", caminho, novo, antigo))
        self.salvar()
        return True

    # ---------------- MOVER ----------------
    def mover(self, origem, nome, destino):
        po = self._navegar(origem)
        pd = self._navegar(destino)
        if not po or not pd:
            return False

        po.filhos, node = self._excluir_bst(po.filhos, nome)
        if not node:
            return False

        pd.filhos = self._inserir_bst(pd.filhos, node)
        self.undo.append(("mover", destino, nome, origem))
        self.salvar()
        return True

    # ---------------- ACESSAR ----------------
    def acessar(self, caminho, nome):
        pai = self._navegar(caminho)
        if not pai:
            return False

        node = self._buscar_bst(pai.filhos, nome)
        if not node:
            return False

        node.acessos += 1
        heapq.heappush(self.heap, (-node.acessos, -node.tamanho, node.nome, node.tipo))
        self.salvar()
        return True

    # ---------------- SUGESTÕES ----------------
    def sugeridos(self, qtd=5):
        vistos, res, temp = set(), [], []

        while self.heap and len(res) < qtd:
            a, t, n, tp = heapq.heappop(self.heap)
            if n not in vistos:
                res.append((n, tp, -a, -t))
                vistos.add(n)
            temp.append((a, t, n, tp))

        for x in temp:
            heapq.heappush(self.heap, x)

        return res

    # ---------------- DESFAZER ----------------
    def desfazer(self):
        if not self.undo:
            return False

        acao = self.undo.pop()
        tipo = acao[0]

        if tipo == "criar":
            _, caminho, nome = acao
            self.excluir(caminho, nome)

        elif tipo == "excluir":
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
        if not pai:
            return []

        res = []
        self._listar_rec(pai.filhos, caminho.rstrip("/"), res)
        return res

    def _listar_rec(self, node, caminho, res):
        if not node:
            return
        self._listar_rec(node.esq, caminho, res)

        atual = f"{caminho}/{node.nome}".replace("//", "/")
        res.append((atual, node.tipo))

        if node.tipo == "diretorio":
            self._listar_rec(node.filhos, atual, res)

        self._listar_rec(node.dir, caminho, res)

    # ---------------- SALVAR / CARREGAR ----------------
    def salvar(self):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(
                {"raiz": self.raiz.to_dict(), "heap": self.heap},
                f,
                indent=4,
                ensure_ascii=False
            )

    def carregar(self):
        with open(self.arquivo, "r", encoding="utf-8") as f:
            d = json.load(f)
        self.raiz = Node.from_dict(d["raiz"])
        self.heap = d.get("heap", [])


# ------------------------------------------------------
# MENU
# ------------------------------------------------------
def escolher_item(s, caminho):
    itens = s.listar(caminho)
    if not itens:
        print("Nenhum item.")
        return None

    for i, (n, t) in enumerate(itens, 1):
        print(f"{i} - {n} ({t})")

    try:
        return itens[int(input("Escolha: ")) - 1][0].split("/")[-1]
    except:
        return None


def main():
    s = SistemaArquivos()

    while True:
        print("""
===== ORGANIZADOR DE ARQUIVOS =====
1 - Criar
2 - Excluir
3 - Renomear
4 - Mover
5 - Acessar
6 - Sugeridos
7 - Desfazer
8 - Listar
0 - Sair
==================================
""")

        op = input("Opção: ")

        if op == "0":
            break

        try:
            if op == "1":
                c = input("Caminho: ")
                n = input("Nome: ")
                t = input("1-Arquivo | 2-Diretório: ")
                tam = int(input("Tamanho: ")) if t == "1" else 0
                print("OK" if s.criar(c, n, "arquivo" if t == "1" else "diretorio", tam) else "Erro")

            elif op == "2":
                c = input("Caminho: ")
                n = escolher_item(s, c)
                print("OK" if n and s.excluir(c, n) else "Erro")

            elif op == "3":
                c = input("Caminho: ")
                n = escolher_item(s, c)
                novo = input("Novo nome: ")
                print("OK" if n and s.renomear(c, n, novo) else "Erro")

            elif op == "4":
                o = input("Origem: ")
                n = escolher_item(s, o)
                d = input("Destino: ")
                print("OK" if n and s.mover(o, n, d) else "Erro")

            elif op == "5":
                c = input("Caminho: ")
                n = escolher_item(s, c)
                print("OK" if n and s.acessar(c, n) else "Erro")

            elif op == "6":
                for n, t, a, tam in s.sugeridos():
                    print(f"{n} ({t}) - {a} acessos - {tam}")

            elif op == "7":
                print("OK" if s.desfazer() else "Nada a desfazer")

            elif op == "8":
                c = input("Caminho: ")
                for n, t in s.listar(c):
                    print(f"{n} ({t})")

        except Exception as e:
            print("Erro crítico:", e)

        pausa()


if __name__ == "__main__":
    main()