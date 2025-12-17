# 📁 Organizador de Arquivos e Documentos

## 👥 Criadores do Projeto

- **Victor Gabryel da Silva**
  - Implementação da árvore binária de busca  
  - Operações de inserção, busca, listagem e exclusão de arquivos e diretórios  
  - Modelagem da estrutura hierárquica do sistema de arquivos  
  - Apoio na lógica geral do sistema  

- **Emanuel Bento da Silva**
  - Implementação do heap (fila de prioridade) para controle de acessos  
  - Desenvolvimento do ranking de arquivos e diretórios mais acessados  
  - Persistência de dados em arquivo JSON (salvar e carregar)  
  - Tratamento de erros, validações de entrada e organização do menu  

---

## 🎯 Objetivo do Projeto

Este projeto tem como objetivo desenvolver um **organizador de arquivos e diretórios em modo texto**, aplicando de forma prática as **Estruturas de Dados estudadas na disciplina**.  

O sistema simula funcionalidades básicas de um sistema de arquivos, como criação, acesso, exclusão e organização hierárquica de arquivos e diretórios, além do controle de acessos.

---

## 🧩 Problema Resolvido

Gerenciar arquivos e diretórios de forma organizada é um problema real presente em sistemas operacionais.  

Este projeto resolve esse problema simulando um sistema de arquivos que permite:
- Criar arquivos e diretórios  
- Organizar os itens de forma hierárquica  
- Acessar arquivos e diretórios  
- Excluir itens  
- Listar todos os itens cadastrados  
- Identificar os arquivos e diretórios mais acessados  

---

## 💡 Justificativa da Escolha do Tema

O tema **Organizador de Arquivos e Documentos** foi escolhido por representar um problema real e permitir a aplicação direta de estruturas de dados fundamentais, como **árvores binárias** e **heaps**, que são naturalmente utilizadas em sistemas de organização e priorização.

Além disso, o tema está alinhado com as sugestões propostas no enunciado do Projeto Final da disciplina.

---

## 🧠 Estruturas de Dados Utilizadas

### 🌳 Árvore Binária de Busca

- Implementada por meio da classe `Node`  
- Cada nó representa um arquivo ou diretório  
- A inserção é feita de forma ordenada pelo nome  
- Utilizada para:
  - Inserção de itens  
  - Busca de arquivos e diretórios  
  - Exclusão de itens  
  - Listagem de todos os elementos do sistema  

A árvore binária foi escolhida por permitir uma organização eficiente dos dados e por ser uma estrutura estudada ao longo da disciplina.

---

### 📊 Heap (Fila de Prioridade)

- Implementada com a biblioteca `heapq`  
- Utilizada para armazenar os arquivos e diretórios mais acessados  
- Cada acesso incrementa um contador e o item é inserido no heap  
- Permite listar rapidamente os itens mais acessados  

O heap foi escolhido por sua eficiência na recuperação de elementos prioritários.

---

### ➕ Estruturas Auxiliares

- **Dicionário (`dict`)**: utilizado para salvar a árvore e o heap no arquivo JSON  
- **Conjunto (`set`)**: utilizado para evitar duplicações ao listar os itens mais acessados  

---

## 💻 Interface do Sistema

O sistema possui uma **interface em modo texto (console)**, com um menu interativo que permite ao usuário escolher as operações disponíveis.

### 📋 Menu Principal
- Criar item (arquivo ou diretório)  
- Excluir item  
- Acessar item  
- Listar itens mais acessados  
- Listar todos os itens  
- Sair do sistema  

---

## 💾 Persistência de Dados

Os dados do sistema são salvos automaticamente no arquivo:

```txt
dados.json