---
name: start-luna-orchestration
description: "Explicitly prepare a permanent Jetta spec worktree and open a fresh Luna coordinator."
disable-model-invocation: true
---

# Start Luna Orchestration

Use somente por invocação explícita após `to-tickets`. A skill prepara/valida a worktree permanente e abre o coordenador; não implementa tickets.

Quando os tickets estiverem numa nota de um workspace Obsidian, passe o caminho desse ticket e o `Index.md` ao coordenador para herdar o workspace pelo [Spec Workspace Adapter](../spec-workspace/SKILL.md). Não copie Markdown do fluxo para `.specs/**` ou outro destino do repositório. Sem essa origem, preserve o fluxo atual.

## Entrada

Receba a issue da spec; só a infira da conversa quando houver exatamente uma recém-publicada. Leia seu título e derive slug curto e estável. Use:

- projeto `Jetta Move · <nome curto da feature>`;
- branch `codex/<slug>`;
- task `Coordenação Luna · #<spec>`;
- base indicada na invocação ou o `HEAD` limpo da branch padrão.

## Projeto-worktree

1. Em `list_projects`, encontre o Jetta Move base e o projeto local com o nome exato.
2. Resolva a branch padrão por `origin/HEAD`; sem ela, exija base explícita. Confirme base local e checkout principal limpo, sem alterá-lo.
3. Se o projeto não existir, use somente ferramenta nativa cuja descrição declare criar e cadastrar uma **worktree permanente como projeto**.
4. Sem essa ferramenta, encerre após um checkpoint: `Crie uma worktree permanente no projeto Jetta Move com o nome "Jetta Move · <nome curto>" a partir de "<base>" e execute $start-luna-orchestration <spec> novamente.` Não substitua por fork, worktree descartável, diretório Git manual sem cadastro ou checkout principal.
5. Na reinvocação, valide mesmo repositório, presença em `git worktree list --porcelain`, posição diferente da primeira (checkout principal), limpeza e commit-base esperado.
6. Se estiver em `HEAD` destacado e `codex/<slug>` não existir, crie a branch local ali. Se existir ligada à mesma worktree, valide-a. Recuse branch padrão/`main`/`master`, branch diferente, colisão em outro worktree ou base divergente, sem corrigir silenciosamente.

Se existir a seção `Jetta Move — Implementações`, mova o projeto. Se a ferramenta de seção estiver disponível e ela faltar, crie-a e mova o projeto. Isso não substitui guardas Git.

## Coordenador

Reconforme o `projectId` e use `create_thread` com target de projeto e ambiente `{ type: "local" }`, modelo `gpt-5.6-luna`, esforço proporcional à fila e título `Coordenação Luna · #<spec>`.

O prompt autocontido deve invocar `[$luna-orchestrator](<C:\Projetos\Jeta Move\.agents\skills\luna-orchestrator\SKILL.md>)`, informar spec, projeto, caminho, branch e commit-base e ordenar avanço automático até conclusão ou bloqueio real. Reitere que a fila contém somente issues cujo `Parent` referencia a spec e que cada executor será uma task local zerada no mesmo projeto-worktree.

Apresente o vínculo criado e preserve a worktree. Esta skill nunca faz push, merge, deploy ou alteração de issues.
