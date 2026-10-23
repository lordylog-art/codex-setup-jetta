---
name: luna-orchestrator
description: Orquestrar a fila aprovada de uma spec do ERP Jetta com Luna somente leitura e tasks executoras zeradas no projeto-worktree permanente da feature.
---

# Luna Orchestrator

Coordene a implementação de uma spec publicada por `to-spec` e dos tickets aprovados por `to-tickets`. O coordenador usa `gpt-5.6-luna`, administra fila/tasks e audita evidências; implementação, testes, revisão e commits pertencem às tasks que invocam `implement`.

Se spec ou tickets vierem de um workspace Obsidian explícito/herdado, use o [Spec Workspace Adapter](../spec-workspace/SKILL.md): passe somente o Index, spec e tickets necessários, preserve o workspace nas tasks, e salve relatórios Markdown do fluxo em `Validation/` ou `Research/`. Sem workspace, mantenha os destinos originais.

## Entrada e baseline

Receba a issue da spec e o projeto local exato da worktree permanente. Antes da fila:

1. Confirme que o diretório atual é a pasta principal do projeto e consta em `git worktree list --porcelain`.
2. Obtenha o checkout principal da primeira entrada e a branch padrão de `origin/HEAD`, ou da base explícita do bootstrap se ela não existir.
3. Recuse checkout principal, branch padrão/`main`/`master`, `HEAD` destacado, projeto diferente ou worktree sujo; informe e encerre sem executor.
4. Registre `HEAD` integrado inicial e status limpo.

O coordenador é somente leitura para arquivos, Git e issues e só altera estado de tasks no Codex: não edita produto, testa, usa `implement`, revisa ou commita.

## Fila e fronteira

Inclua apenas issues cujo `Parent` referencia explicitamente a spec; cada ticket é uma fase. Requisitos e aceite vêm exclusivamente da issue atual, comentários e dependências explícitas — nunca de `.specs/**`, Obsidian, outras features, conversa ou skills. `Blocked by` forma o grafo; a fronteira contém tickets pendentes com bloqueadores já commitados e auditados. Fechar issues ou comentar exige autorização explícita.

Para cada ticket livre:

1. Mapeie internamente cada requisito/validação ao trecho de origem.
2. Inspecione apenas o código necessário para dar ownership exclusivo por arquivo, módulo e superfície. Paralelize somente ownerships comprovadamente disjuntos; dúvida ou sobreposição exige serialização.
3. Leia `C:\Users\caila\.codex\references\agent-routing-policy.md`; antes de criar a task, informe modelo, esforço, papel, ownership e motivo.
4. Reserve fila de commit do lote: escrita pode ser paralela, staging/commit tem um titular por vez.

Não abra pesquisa prévia. Entregue issue, ownership e baseline ao executor principal; ele usa `orchestrate` para especialistas subsidiários quando houver trabalho independente útil.

## Executores zerados

Confirme com `list_projects` o `projectId` cuja pasta principal coincide com a worktree. Para cada ticket, use `create_thread` nesse projeto, ambiente `{ type: "local" }`, rota escolhida e título `Implementar · #<ticket> · <título>`. A task nasce sem histórico.

O primeiro prompt deve invocar literalmente `[$implement](C:\Users\caila\.codex\skills\implement\SKILL.md)`, ser autocontido e conter:

- issue/URL, corpo e comentários relevantes, bloqueadores explícitos e critérios rastreáveis;
- ownership, worktree compartilhada e commit-base;
- autorização para implementar, testar, revisar e fazer commit local seletivo;
- proibição de mudar `.specs/**`, trabalho alheio ou superfície sem ownership;
- validações e formato objetivo de evidência;
- em lote paralelo, parada antes de staging/commit até receber o slot.

Inclua o contrato `luna-orchestrator → executor principal do ticket → especialistas subsidiários`:

- a task criada usa `implement` e `orchestrate`, integra o ticket e executa seu núcleo, mesmo aparecendo internamente como `/root`;
- `orchestrate` delega só resultados auxiliares delimitados ou slices disjuntos; pesquisa/mapeamento faltante vai para Luna somente leitura no menor esforço canônico e retorna ao executor;
- nenhum especialista recebe o ticket completo; o executor não repassa ownership mutável nem promove a própria rota com descendente mais caro;
- rota insuficiente interrompe novas mutações e devolve evidência ao coordenador para novo roteamento.

Todas as fases usam `create_thread`. `fork_thread` herda contexto e ambiente `worktree` cria outro diretório; ambos violam a fronteira.

## Acompanhar e integrar

Use `wait_threads` com cursores e esperas limitadas, sem polling contínuo. Luna não manipula a worktree enquanto executores escrevem.

Em lote paralelo, conceda cada slot por `send_message_to_thread`; exija status/staging seletivo, commit restrito ao ownership e hash antes do próximo. Executor serial pode commitar no fluxo normal de `implement`.

Audite em leitura:

- evidência rastreável por critério e testes/revisão exigidos por `implement`;
- commit local existente, seletivo e descendente da referência integrada esperada;
- ausência de arquivos do ticket fora do commit, mudanças em `.specs/**` ou efeitos externos sem autorização.

Após lote paralelo, crie task nova, zerada, local e somente leitura para validação integrada. Defeito volta ao executor responsável; correção que cruza ownerships exige integrador novo com `implement`, ownership explícito, revalidação e commit seletivo. Só então registre hashes, marque tickets concluídos internamente e recalcule a fronteira. Nunca reutilize executor entre issues.

## Falhas

- Reative o mesmo executor somente com hipótese nova e contexto útil; se contaminado/esgotado, crie substituto zerado com issue, ownership, base, evidências e falha.
- Falha bloqueia dependentes; ramos independentes seguros continuam.
- Sobreposição inesperada interrompe novas escritas, preserva diffs e exige integrador novo; ninguém apaga trabalho alheio.
- Falta de acesso, requisito ou decisão preserva o estado e gera uma pergunta objetiva.
- Mudança de direção interrompe tasks afetadas e recalcula o grafo.

## Conclusão

Finalize apenas com todos os tickets tendo commit seletivo, evidência por critério, revisão de `implement` e validação integrada dos lotes. O ticket E2E final usa task própria com `implement` e `jetta-local-runtime` quando o aceite exigir ERP local.

Confirme worktree limpa, branch da feature, cadeia de commits e nenhuma mudança em `.specs/**`. Entregue tickets, hashes, testes, revisões, E2E e lacunas; preserve a worktree. Push, merge, deploy, publicação, produção, fechamento de issues e remoção da worktree exigem autorização explícita.
