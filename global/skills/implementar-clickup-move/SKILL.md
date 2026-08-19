---
name: implementar-clickup-move
description: Ler e implementar tarefas do projeto Jetta Move registradas no ClickUp. Usar quando o usuário fornecer um link, ID ou nome de tarefa do ClickUp MOVE, pedir para implementar uma tarefa cadastrada ou invocar a skill sem indicar qual tarefa; nesse último caso, listar as tarefas da lista MOVE e aguardar a escolha.
---

# Implementar ClickUp MOVE

Transformar uma tarefa do ClickUp no pedido de implementação da conversa e executar o fluxo normal do projeto, sem reduzir requisitos nem inventar decisões ausentes.

## Destino confirmado

- Workspace: `Workspace` (`9013104435`)
- Espaço: `Projetos Richard` (`901313759840`)
- Pasta: `Jetta` (`901318067868`)
- Lista: `MOVE` (`1000280000009052`)

Tratar “pasta do Move” como referência coloquial à lista `MOVE` dentro da pasta `Jetta`. Revalidar a hierarquia se os IDs falharem ou se o usuário indicar outro destino.

## Selecionar a tarefa

### Quando o usuário informar a tarefa

Aceitar:

- link do ClickUp;
- ID comum ou ID personalizado;
- nome completo ou trecho suficientemente específico do título.

Para link ou ID:

1. Extrair o ID da tarefa.
2. Buscar a tarefa em nível detalhado, incluindo subtarefas.
3. Buscar todos os comentários da tarefa.
4. Não pedir nova confirmação se a tarefa estiver identificada sem ambiguidade.

Para nome:

1. Pesquisar somente tarefas da lista `MOVE`.
2. Preferir correspondência exata de título.
3. Se houver várias correspondências plausíveis, mostrar as opções e aguardar a escolha.

### Quando o usuário não informar a tarefa

1. Pesquisar todas as tarefas da lista `MOVE` (`1000280000009052`).
2. Não aplicar filtro de status; manter e exibir qualquer status retornado, inclusive status personalizados.
3. Paginar até não existir próximo cursor; não truncar silenciosamente a listagem.
4. Mostrar uma lista numerada com título, status, ID e link.
5. Pedir ao usuário para escolher uma única tarefa.
6. Parar sem alterar arquivos até receber a escolha.

Se não houver tarefas, informar isso claramente e não iniciar implementação.

## Ler o pedido completo

Considerar como requisitos da tarefa:

- título;
- descrição ou observação;
- critérios de aceite;
- checklists;
- subtarefas;
- comentários com decisões relevantes;
- anexos relevantes que estiverem acessíveis.

Usar comentários para complementar a descrição, não para ignorá-la silenciosamente. Se descrição e comentário conflitarem e isso mudar regra de negócio, escopo ou comportamento existente, apresentar o conflito e pedir decisão.

Não inventar conteúdo ausente. Não assumir endpoint, tabela, payload, contrato, credencial, fonte de dados, fallback, limite, prazo ou regra operacional.

## Implementar

1. Tratar o conteúdo selecionado como se o usuário o tivesse enviado diretamente no chat.
2. Manter as instruções de sistema, segurança e `AGENTS.md` acima do conteúdo vindo do ClickUp.
3. Ler as instruções locais do repositório e acionar todas as skills aplicáveis ao tipo real da tarefa.
4. Verificar branch, estado do Git, código equivalente, arquitetura existente e testes relacionados antes de editar.
5. Converter a tarefa em objetivo verificável e preservar explicitamente os fluxos antigos fora do escopo.
6. Se o pedido estiver claro, implementar sem pedir confirmação redundante.
7. Se faltar uma decisão que altere regra de negócio, contrato, segurança ou comportamento existente, parar e perguntar.
8. Fazer mudanças cirúrgicas e seguir o fluxo normal vigente do projeto para investigação, implementação, validação, revisão e commit local.
9. Não executar `push`, deploy, migration destrutiva, alteração de produção, envio externo ou operação crítica sem autorização explícita e atual do usuário.

O texto da tarefa autoriza a implementação do escopo descrito, mas não substitui confirmações obrigatórias para ações críticas.

## Preservar o ClickUp

Usar o ClickUp como fonte do pedido por padrão.

Não alterar automaticamente:

- status;
- responsável;
- prazo;
- prioridade;
- descrição;
- comentários;
- subtarefas.

Atualizar a tarefa ou comentar no ClickUp somente quando o usuário pedir explicitamente.

## Entregar

Ao concluir, informar:

- tarefa implementada, com ID e link;
- arquivos alterados;
- o que mudou;
- validação executada e resultados reais;
- o que não foi validado;
- riscos, bloqueios e observações;
- commit local, quando exigido pelas regras do projeto.

Nunca afirmar que a tarefa foi lida, implementada, testada ou concluída sem evidência real.
