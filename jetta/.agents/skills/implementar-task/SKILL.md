---
name: implementar-task
description: Implementar tarefas do ClickUp no projeto, vinculando o contexto do chat a uma task, decompondo-a em subtasks executáveis, acompanhando status e validando cada etapa. Usar quando o usuário pedir para implementar uma task, issue ou demanda registrada no ClickUp.
---

# Implementar Task

Executar o trabalho somente a partir de uma task identificada no ClickUp. A task é a fonte de requisitos; o chat complementa o contexto, mas não substitui o vínculo obrigatório.

## 1. Vincular a task antes de agir

1. Ler o contexto completo da conversa e procurar link, ID, nome ou referência inequívoca a uma task.
2. Se houver uma única correspondência clara, buscar a task detalhada, subtasks e todos os comentários.
3. Se não houver referência clara, pesquisar no ClickUp tarefas plausíveis do destino configurado pelo projeto, sem alterar nada. Mostrar uma lista numerada com título, status, ID e link e perguntar qual task deve ser implementada. Parar até a escolha.
4. Se houver mais de uma correspondência plausível, mostrar as opções e pedir uma única escolha.
5. Não inferir que uma task concluída, fechada ou arquivada deve ser reaberta; pedir orientação se a implementação depender disso.

Ao ler a task, considerar título, descrição, critérios de aceite, checklist, subtasks, comentários e anexos acessíveis. Se houver conflito que mude escopo, regra, contrato ou comportamento existente, parar e perguntar.

## 2. Preparar a execução

1. Tratar a task selecionada como objetivo verificável, preservando os requisitos e o comportamento antigo fora do escopo.
2. Ler `AGENTS.md`, instruções locais e skills aplicáveis antes de alterar código.
3. Inspecionar arquitetura equivalente, usos compartilhados e testes relacionados.
4. Produzir internamente um plano curto, com dependências explícitas e critérios de conclusão.
5. Decompor o trabalho em subtasks pequenas, testáveis e ordenadas. Cada subtask deve ter objetivo concreto, área provável, dependências, teste/evidência e risco/bloqueio conhecido.

Não criar subtasks artificiais para cada comando. Agrupar etapas coesas e manter cada unidade implementável por uma rodada de trabalho. Se a task já tiver subtasks úteis, reutilizá-las e complementar apenas o necessário.

## 3. Roteamento por complexidade

Escolher o nível disponível no ambiente, sem presumir que um modelo específico está habilitado:

- **Luna**: leitura, descoberta, busca de código, ajustes pequenos e testes focados.
- **Terra**: implementação comum com múltiplos arquivos, integração local ou mudança com dependências moderadas.
- **Sol**: arquitetura ambígua, regra de negócio sensível, integração crítica, investigação profunda, falhas difíceis ou revisão de risco elevado.

Para trabalho grande, separar análise/plano da execução e usar ciclos curtos de implementação e validação. Usar agentes paralelos somente quando as áreas forem independentes e não compartilharem os mesmos arquivos; consolidar os resultados antes de editar.

## 4. Status da task e das subtasks

Atualizar o ClickUp apenas depois de identificar a task e somente com os status que existirem na lista. Não inventar status nem substituir um status personalizado por outro parecido.

Fluxo padrão, se esses estados existirem:

`To Do` → `Analisando` → `Em andamento` → `Concluído`

Regras:

- Ao iniciar a análise, mover a task principal para `Analisando`.
- Antes de implementar uma subtask, marcar a subtask como `Em andamento` (ou o equivalente ativo existente).
- Ao concluir e validar uma subtask, marcar como `Concluído`.
- Se a subtask falhar, permanecer bloqueada/em andamento e registrar o erro; nunca marcar como concluída por aproximação.
- Só marcar a task principal como `Concluído` quando todos os critérios de aceite e subtasks obrigatórias estiverem concluídos e validados.
- Se faltar requisito, acesso, teste ou decisão, manter a task aberta e registrar o bloqueio.

Se a API do ClickUp não expuser os status da lista, não chutar. Preservar o status atual e informar que a atualização ficou bloqueada até os nomes válidos serem confirmados.

## 5. Criar e executar subtasks

Criar subtasks no ClickUp somente quando isso for necessário para acompanhar o trabalho e a ferramenta permitir a criação segura. Usar a task principal como `parent`, manter os títulos orientados a resultado e registrar descrição curta com objetivo, critério de aceite e dependências.

Executar em ordem topológica: investigação e contrato; implementação de menor risco; integração e tratamento de erros; testes e validação; revisão de regressões e fechamento.

Não executar push, deploy, migration destrutiva, restart, alteração de produção, envio externo ou outra ação crítica só porque consta na task; obedecer às confirmações exigidas pelo projeto.

## 6. Validação e entrega

Após cada subtask, fazer a validação proporcional ao risco e registrar o resultado real. Não esconder falhas com fallback silencioso, mock enfraquecido, teste pulado ou status concluído.

Ao finalizar, informar task implementada, ID e link; subtasks criadas/concluídas e status final; arquivos alterados; resumo do que mudou; testes, lint, build e validações manuais realmente executados; o que não foi validado e por quê; bloqueios, riscos e follow-ups; e commit local, quando exigido pelas regras do projeto.

Não alterar automaticamente descrição, prioridade, responsável, prazo ou comentários além do necessário para o acompanhamento definido acima. Nunca afirmar implementação, teste ou conclusão sem evidência.

## Ferramentas ClickUp

Preferir as ferramentas ClickUp disponíveis para `get_task` com subtasks, `get_task_comments`, `search`, `create_task` com `parent`, e `update_task` para status. Paginar resultados quando a ferramenta oferecer cursor. Confirmar cada mutação pelo retorno da ferramenta antes de continuar.

Para o destino padrão e regras específicas do Jeta Move, consultar a skill existente `implementar-clickup-move` quando ela estiver disponível; esta skill define o processo geral e não deve duplicar IDs ou inventar outro destino.
