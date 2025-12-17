# 📁 Organizador de Arquivos e Documentos

## 👥 Criadores do Projeto

* **Victor Gabryel da Silva**

  * Implementação da **árvore binária de busca (BST)**
  * Operações de **inserção, busca, listagem ordenada e exclusão** de arquivos e diretórios
  * Modelagem da **estrutura hierárquica** do sistema de arquivos
  * Implementação da navegação por caminhos (`/`)
  * Apoio na lógica geral do sistema

* **Emanuel Bento da Silva**

  * Implementação do **heap (fila de prioridade)** para controle de acessos
  * Desenvolvimento do ranking de **arquivos e diretórios mais acessados**
  * Implementação da **persistência de dados em arquivo JSON**
  * Tratamento de erros, validações de entrada e organização do menu interativo

---

## 🎯 Objetivo do Projeto

Desenvolver um **organizador de arquivos e diretórios em modo texto**, aplicando de forma prática os conceitos de **Estruturas de Dados**, como árvores binárias, heaps e pilhas.

O sistema simula funcionalidades básicas de um sistema de arquivos real, permitindo a criação, organização, navegação e controle de acessos a arquivos e diretórios.

---

## 🧩 Problema Resolvido

O projeto resolve o problema de **organização e gerenciamento de arquivos** ao permitir:

* Criar arquivos e diretórios
* Organizar itens de forma hierárquica
* Renomear arquivos e diretórios
* Mover itens entre diretórios
* Acessar arquivos e diretórios
* Excluir itens
* Listar arquivos e diretórios de forma **recursiva e ordenada**
* Identificar os itens mais acessados
* Desfazer a última ação realizada

---

## 💡 Justificativa da Escolha do Tema

O tema **Organizador de Arquivos e Documentos** foi escolhido por representar um problema real presente em sistemas operacionais e permitir a aplicação direta dos principais conceitos estudados na disciplina de **Estrutura de Dados**.

Além disso, o projeto integra múltiplas estruturas de dados em um único sistema funcional, conforme proposto no **Projeto Final da disciplina**.

---

## 🧠 Estruturas de Dados Utilizadas

### 🌳 Árvore Binária de Busca (BST)

* Implementada pela classe `Node`
* Cada nó representa um **arquivo** ou **diretório**
* Organização automática em **ordem alfabética**
* Cada diretório possui sua própria árvore binária de filhos

Utilizada para:

* Inserção de arquivos e diretórios
* Busca eficiente de itens
* Exclusão de nós
* Listagem ordenada (percurso *in-order*)

---

### 📊 Heap (Fila de Prioridade)

* Implementado utilizando a biblioteca `heapq`
* Responsável pelo controle dos **arquivos e diretórios mais acessados**
* Critérios de prioridade:

  * Maior número de acessos
  * Maior tamanho do arquivo (em caso de empate)

Permite sugerir rapidamente os itens mais relevantes ao usuário.

---

### ↩️ Pilha (Stack)

* Implementada com uma lista em Python
* Armazena o histórico de ações realizadas no sistema
* Permite a funcionalidade **Desfazer (Undo)**

Segue o princípio **LIFO (Last In, First Out)**.

---

## 💻 Interface do Sistema

O sistema possui uma **interface em modo texto (console)**, baseada em um menu interativo que facilita a navegação do usuário.

### 📋 Menu Principal

* Criar arquivo ou diretório
* Excluir item
* Renomear item
* Mover item entre diretórios
* Acessar item
* Listar itens sugeridos (mais acessados)
* Desfazer última ação
* Listar arquivos e diretórios (recursivo)
* Sair do sistema

---

## 💾 Persistência de Dados

Os dados do sistema são salvos automaticamente no arquivo:

```txt
sistema_arquivos.json
```

Isso garante que as informações não sejam perdidas ao encerrar o programa.

---

## ▶️ Como Executar o Projeto

1. Certifique-se de ter o **Python 3** instalado
2. Salve o código-fonte em um arquivo chamado `main.py`
3. Execute o programa no terminal com o comando:

```bash
python main.py
```

---

## 📌 Observações Finais

Este projeto demonstra, de forma prática, a aplicação integrada de **árvores binárias, heaps e pilhas**, reforçando conceitos fundamentais da disciplina de **Estrutura de Dados**.

Trata-se de um sistema didático, funcional e alinhado aos objetivos acadêmicos do curso.