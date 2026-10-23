---
name: grill-to-front
description: "Plan with grill-with-docs and impeccable shape; prepare to-spec/to-tickets context without implementation."
---

# Grill to Front

Coordene `grill-with-docs` e `impeccable shape` no mesmo chat, sem subagentes. Feche decisões; não implemente.

## Pré-requisitos

1. Confirme que as skills instaladas `grill-with-docs` e `impeccable` existem.
2. Carregue o `SKILL.md` real de cada uma antes de executar sua etapa.
3. Se uma dependência não existir, informe o nome exato ausente e pare. Não substitua silenciosamente por outra skill.

## Contexto

Leia pedido, decisões anteriores e documentos relevantes da funcionalidade. Inclua `PRODUCT.md`, `DESIGN.md` e registros em `.impeccable/surfaces/`, quando existirem. Inspecione o código necessário para entender tela e padrões.

Separe decisões confirmadas, propostas de auditoria e pendências. Não pergunte algo respondido por documentos ou código.

## Formato das perguntas

Conduza a entrevista em rodadas na resposta normal do chat; não use o sistema nativo de perguntas do Codex. Modele as decisões como uma árvore e, em cada rodada, pergunte toda a fronteira já desbloqueada. Questões dependentes de respostas ainda abertas ficam para rodada posterior.

Classifique cada decisão antes de perguntar:

- 🧭 **PRODUTO**: objetivo, usuários, escopo, regras, permissões, exceções e resultado esperado;
- 🎨 **FRONTEND**: hierarquia visual, layout, componentes, interações, conteúdo, responsividade, acessibilidade e estados da interface.

Se uma pergunta misturar as duas categorias, divida-a em duas e faça primeiro a de produto. Uma decisão sobre o que o sistema faz ou quem pode fazer algo continua sendo de produto, mesmo quando aparece na interface.

Agrupe perguntas por categoria, com cabeçalho e numeração próprios. Não misture produto e frontend na mesma pergunta. Inclua uma recomendação e aguarde as respostas antes de recalcular a fronteira. Use exatamente estes formatos:

```md
## 🧭 PRODUTO

❓ **P1** - **<título>**: <pergunta, contexto e opções relevantes>

➡️ **Recomendação:** <resposta recomendada>

---

❓ **P2** - **<título>**: <pergunta, contexto e opções relevantes>

➡️ **Recomendação:** <resposta recomendada>
```

Após concluir produto, use:

```md
## 🎨 FRONTEND

❓ **F1** - **<título>**: <pergunta, contexto e opções relevantes>

➡️ **Recomendação:** <resposta recomendada>

---

❓ **F2** - **<título>**: <pergunta, contexto e opções relevantes>

➡️ **Recomendação:** <resposta recomendada>
```

Investigue fatos disponíveis em documentos, código e ferramentas. Leve ao usuário somente decisões. A etapa termina quando a fronteira estiver vazia e o usuário confirmar o entendimento compartilhado.

## Etapa funcional

Carregue e siga `grill-with-docs`, incluindo referências exigidas pela própria skill. Feche objetivo, usuários, escopo, regras, permissões, exceções e resultado esperado. Reserve questões puramente visuais para etapa seguinte.

Aproveite respostas existentes. Aguarde o usuário entre rodadas. Quando decisões funcionais estiverem resolvidas, avance para frontend no mesmo chat; não peça que usuário execute outro comando.

## Etapa frontend

Carregue `impeccable` e siga comando `shape`, levando decisões funcionais como contexto. Pergunte somente lacunas relevantes sobre estrutura, componentes, interações, conteúdo, responsividade, acessibilidade e estados de carregamento, vazio, erro e sucesso.

Preserve design system e padrões existentes. Não reabra decisões anteriores sem conflito concreto. Não amplie escopo nem escreva código. Se avaliação visual exigir referência ou protótipo, sinalize pendência; não adivinhe.

## Consolidação

Apresente resumo único e curto com:

- objetivo, escopo e decisões funcionais;
- decisões de interface e padrões preservados;
- critérios de aceite observáveis, incluindo frontend;
- documentos de referência;
- propostas e pendências, separadas das decisões confirmadas.

Peça aprovação. Incorpore correções do usuário e reapresente o resumo atualizado. Após aprovação, pare. O resumo e a conversa serão entrada para `to-spec`.

Não execute `to-spec` ou `to-tickets`. Não gere tickets, altere código, faça commits ou declare aprovação sem confirmação.
