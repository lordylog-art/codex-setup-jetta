---
name: clickup-move
description: Criar e organizar pastas, listas e tarefas do projeto Jetta Move no ClickUp a partir de pedidos em linguagem natural. Usar quando o usuário pedir para registrar, abrir, criar ou estruturar uma demanda no ClickUp da operação Move, especialmente na lista MOVE da pasta Jetta.
---

# ClickUp MOVE

Transformar pedidos falados ou escritos em itens claros no ClickUp, preservando o que o usuário informou e executando a criação quando o destino estiver confirmado.

## Destino padrão confirmado

- Workspace: `Workspace` (`9013104435`)
- Espaço: `Projetos Richard` (`901313759840`)
- Pasta: `Jetta` (`901318067868`)
- Lista: `MOVE` (`1000280000009052`)

Usar a lista `MOVE` como destino padrão para tarefas da operação Move. Revalidar a hierarquia com as ferramentas do ClickUp se algum ID falhar ou se o usuário indicar outro destino.

## Fluxo

1. Identificar se o pedido é para criar uma tarefa, pasta ou lista.
2. Extrair apenas requisitos realmente informados pelo usuário.
3. Quando o pedido for uma tarefa da operação Move, usar diretamente a lista `MOVE`, salvo indicação contrária.
4. Criar um título curto, específico e orientado à ação.
5. Estruturar a descrição em Markdown com somente as seções úteis:
   - `Objetivo`
   - `Contexto`
   - `Escopo` ou `Fluxo esperado`
   - `Critérios de aceite`
   - `Pendências de definição`
   - `Fora de escopo`, quando necessário
6. Executar a criação pela ferramenta do ClickUp.
7. Confirmar o resultado com nome, destino e link do item criado.

Não pedir ao usuário para escolher o título quando for possível derivá-lo com segurança do pedido.

## Tarefas

Para criar uma tarefa:

- Resolver ou confirmar a lista antes da mutação.
- Usar o ID `1000280000009052` para a lista `MOVE`.
- Preservar nomes, textos de botões, mensagens, estados e regras citados pelo usuário.
- Registrar ambiguidades relevantes em `Pendências de definição` quando elas não impedirem a criação.
- Perguntar antes somente quando a decisão ausente puder mudar materialmente a regra de negócio ou o destino.
- Omitir responsável, prazo, prioridade, status, tags e campos personalizados quando não forem informados.

Não inventar endpoints, payloads, fontes de dados, integrações, contratos, responsáveis, prazos ou comportamento de erro.

## Pastas e listas

Criar pasta ou lista somente quando o usuário pedir isso explicitamente.

- Antes de criar uma pasta, confirmar o espaço de destino.
- Antes de criar uma lista, confirmar se ela deve ficar dentro de uma pasta ou diretamente no espaço.
- Verificar se já existe item equivalente para evitar duplicação.
- Não interpretar “criar uma tarefa dentro da pasta Jetta e lista MOVE” como autorização para criar uma nova pasta ou lista.

## Pedidos sobre chatbots

Ao registrar demandas de chatbot ou agente da Connect Channels:

- Descrever perfil, objetivo, fluxo, mensagens, botões, transferência e critérios de aceite somente com base no pedido.
- Registrar como pendência qualquer agente de destino, fonte de dados, contrato ou integração ainda não definido.
- Indicar que o chatbot deve permanecer em rascunho até autorização explícita para publicação.
- Não publicar, disparar conversas nem executar ações externas como consequência da criação da tarefa.

## Confirmação final

Após sucesso, responder de forma curta:

- tarefa, pasta ou lista criada;
- hierarquia de destino;
- link direto retornado pelo ClickUp;
- pendências relevantes.

Se a ferramenta falhar, informar o erro real e tentar novamente apenas quando a falha aparentar ser temporária. Nunca afirmar que o item foi criado sem confirmação da API.
