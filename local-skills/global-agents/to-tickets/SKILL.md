---
name: to-tickets
description: "Criar tickets diretos com entregas completas, dependências reais e verificação proporcional ao pedido."
---

# To-Tickets — entrada global

1. Resolver projeto e instruções aplicáveis; ler `.agents/skills/to-tickets/SKILL.md` local quando existir. Aplicar a instrução atual do usuário e o [contrato proporcional](../smart-orchestrator/references/planning-contract.md), sem acrescentar gates por conta própria.
2. Criar o menor conjunto de tickets que entregue o pedido, aproveitando a base existente. Cada ticket contém resultado, escopo, critérios observáveis, dependências técnicas por etapa e verificação focal. Criar arquivos diretamente quando solicitado; perguntar apenas por ambiguidade material. Preservar o adaptador Obsidian quando aplicável.
3. Usar V2/controller somente quando explicitamente solicitado, não por quantidade de tickets. Em fila existente, reconciliar processo com a orientação atual e preservar provas e requisitos de produto.
4. Entregar a fila e os caminhos canônicos. Execução de produto e publicação/alteração externa dependem das respectivas autorizações.

Sem skill local, usar o tracker existente ou arquivos `.scratch/<feature>/issues/<NN>-<slug>.md`, sem instalar ferramentas nem criar um sistema paralelo. Mudança pequena autorizada pode ser executada diretamente com verificação focal.
