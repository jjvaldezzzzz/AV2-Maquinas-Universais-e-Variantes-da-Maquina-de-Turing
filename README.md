# AV2 - Máquinas Universais e Variantes da Máquina de Turing

## 📌 Visão Geral do Projeto

Este repositório contém as implementações referentes à avaliação AV2. Conforme os requisitos para equipes de até 4 integrantes, foram selecionados **dois modelos computacionais distintos**, cada um resolvendo um problema específico de complexidade intermediária/alta.

Os modelos foram implementados em **Python**, atuando como interpretadores estritos das definições formais (matrizes de transição, manipulação de fita e pilha).

### Modelos Escolhidos

1. **Autômato de Pilha (PDA)** - Opção 9
2. **Máquina de Turing com Múltiplas Fitas (3 Fitas)** - Opção 3

---

## ⚙️ Máquina 1: Autômato de Pilha (PDA)

### Problema Resolvido
**Validador Sintático de Expressões Algébricas**

### Justificativa
O problema exige garantir o balanceamento correto de parênteses aninhados e a validade sintática de operadores e operandos. Autômatos finitos não possuem memória para lidar com o aninhamento arbitrário, tornando o PDA (com sua memória LIFO) o modelo formal adequado para esta Linguagem Livre de Contexto.

### Formalização Básica
- **Estados:** 8 estados - `q0` (inicial), `q_var`, `q_num`, `q_op`, `q_open`, `q_close`, `q_accept` (final) e `q_reject`
- **Alfabeto de entrada:** Variáveis, Números, Operadores (`+`, `-`, `*`, `/`) e Parênteses
- **Alfabeto da pilha:** `$` (fundo de pilha), `X` (marcador de abertura)

### Rastreamento de Execução

**Caso de Sucesso:** Expressão `(a+b)*c`
```
Execute: python pda_validador.py
```

**Caso de Falha 1:** Erro Sintático `a+*b`
```
Execute: python pda_validador.py
```

**Caso de Falha 2:** Desbalanceamento `((a+b)`
```
Execute: python pda_validador.py
```

---

## 🛠️ Máquina 2: Máquina de Turing Multifita (3 Fitas)

### Problema Resolvido
**Formatador e Gerador de Padrões:** $w \rightarrow w\#w\#w^R$

### Justificativa
Dada uma palavra de entrada $w$ (ex: `abc`), a máquina deve processá-la e gerar a saída com cópias e o reverso da string (ex: `abc#abc#cba`). Em uma MT de fita única, este problema exigiria complexidade quadrática ($O(n^2)$) com dezenas de transições de "vai e vem". Utilizando 3 fitas, usamos a Fita 2 como buffer contínuo (Fila) e a Fita 3 como inversor (Pilha), alcançando a solução em tempo linear ($O(n)$) e demonstrando o poder de paralelismo do modelo multifita.

### Formalização Básica
- O modelo mapeia a função de transição lendo e escrevendo em 3 posições simultâneas: $\delta(q, a, b, c) = (q', a', b', c', D_1, D_2, D_3)$
- Transições cobrem cópia paralela, rebobinamento independente de cabeças e concatenação reversa

### Rastreamento de Execução

**Entrada de Teste:** `abc`  
**Saída Esperada:** `abc#abc#cba`

```
Execute: python mt_multifita.py
```

---

## 🚀 Como Executar

Não há dependências externas complexas, apenas uma instalação padrão do Python 3.x.

1. **Clone este repositório:**
```bash
git clone [URL_DO_SEU_REPOSITORIO]
```

2. **Para testar o Autômato de Pilha:**
```bash
python pda_validador.py
```

3. **Para testar a Máquina de Turing Multifita:**
```bash
python mt_multifita.py
```

---

## 🤖 Declaração de Uso de IA

Conforme exigido na lauda da atividade, declaramos o uso de Inteligência Artificial como apoio ao desenvolvimento:

- **Ferramenta Utilizada:** Gemini (Google)
- **Data de Uso:** Junho de 2026
- **Finalidade:** Discussão para seleção de problemas com complexidade adequada que fugissem dos exemplos de sala de aula, auxílio na estruturação da lógica de transições em dicionários Python e revisão na formatação deste README
- **O que foi aproveitado/modificado:** A lógica de rastreamento no terminal (prints passo a passo) foi gerada com auxílio da IA. A equipe revisou as funções de transição ($\delta$) geradas, validando o mapeamento matemático dos estados, e garante a compreensão integral do código para a arguição do professor.

---

## 📚 Referências

1. DIVERIO, Tiarajú Asmuz; MENEZES, Paulo Blauth. *Teoria da Computação: Máquinas Universais e Computabilidade*. 3. ed. Porto Alegre: Bookman, 2011.
2. MENEZES, Paulo Blauth. *Linguagens Formais e Autômatos*. 6. ed. Porto Alegre: Bookman, 2011.
3. SOUZA, Daniel Leal. *Slides da disciplina Teoria da Computabilidade* (CESUPA, 2026).